"""
Detector de alteração nos links tarifários oficiais, sem acesso à rede.

`netuno/core/tariff_updater/change_detector.py` estava com 24% de cobertura porque
toda a sua lógica interessante fica atrás de uma requisição HTTP. Aqui a sessão é
substituída por um dublê, o que permite exercitar as transições de estado — primeira
assinatura, conteúdo inalterado, conteúdo alterado, erro HTTP, URL inválida — de forma
determinística e sem depender da disponibilidade dos sites das concessionárias.

O registro é sempre isolado em diretório temporário: estes testes nunca escrevem em
`data/tarifas/change_tracking_registry.json`.
"""

import json

import pytest

from netuno.core.tariff_updater.change_detector import TariffChangeDetector

URL = "https://exemplo.gov.br/tarifas/resolucao.pdf"


class RespostaFalsa:
    """Substituto mínimo de `requests.Response` para o caminho usado pelo detector."""

    def __init__(self, conteudo: bytes = b"", status_code: int = 200, headers=None):
        self._conteudo = conteudo
        self.status_code = status_code
        self.headers = headers or {}

    def iter_content(self, chunk_size: int = 65536):
        for inicio in range(0, len(self._conteudo), chunk_size):
            yield self._conteudo[inicio:inicio + chunk_size]


class SessaoFalsa:
    """Sessão que devolve respostas programadas e registra as chamadas feitas."""

    def __init__(self, *respostas):
        self._respostas = list(respostas)
        self.headers = {}
        self.urls_consultadas = []

    def get(self, url, **kwargs):
        self.urls_consultadas.append(url)
        if not self._respostas:
            raise AssertionError("a sessão recebeu mais chamadas do que respostas programadas")
        resposta = self._respostas.pop(0)
        if isinstance(resposta, Exception):
            raise resposta
        return resposta

    def update(self, *args, **kwargs):  # compatível com session.headers.update
        pass


@pytest.fixture
def detector(tmp_path):
    """Detector com registro isolado, sem tocar nos dados do repositório."""
    return TariffChangeDetector(root_dir=tmp_path)


# ---------------------------------------------------------------------------------
# Assinatura de conteúdo
# ---------------------------------------------------------------------------------

def test_hash_e_estavel_e_sensivel():
    """A assinatura identifica o conteúdo: igual para o mesmo, distinta para diferente."""
    assert (TariffChangeDetector.compute_sha256(b"tarifa 2026")
            == TariffChangeDetector.compute_sha256(b"tarifa 2026"))
    assert (TariffChangeDetector.compute_sha256(b"tarifa 2026")
            != TariffChangeDetector.compute_sha256(b"tarifa 2027"))
    assert len(TariffChangeDetector.compute_sha256(b"")) == 64


# ---------------------------------------------------------------------------------
# Persistência do registro
# ---------------------------------------------------------------------------------

def test_registro_ausente_produz_estrutura_inicial(detector):
    """Sem arquivo prévio, o detector parte de um registro vazio e válido."""
    registro = detector.load_registry()
    assert registro["monitored_urls"] == {}
    assert "version" in registro


def test_registro_sobrevive_a_ida_e_volta(detector):
    """O que é salvo é relido — o histórico de assinaturas não pode se perder."""
    detector._registry["monitored_urls"][URL] = {"content_sha256": "abc123"}
    detector.save_registry()

    assert detector.registry_path.exists()
    relido = json.loads(detector.registry_path.read_text(encoding="utf-8"))
    assert relido["monitored_urls"][URL]["content_sha256"] == "abc123"


def test_registro_corrompido_nao_derruba_o_detector(tmp_path):
    """Um JSON inválido em disco degrada para registro vazio, sem exceção.

    O detector é usado em rotina de atualização em lote; abortar por causa de um
    arquivo corrompido interromperia a verificação de todas as demais cidades.
    """
    caminho = tmp_path / "data" / "tarifas" / "change_tracking_registry.json"
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text("{ isto não é json válido", encoding="utf-8")

    detector = TariffChangeDetector(root_dir=tmp_path)
    assert detector.load_registry()["monitored_urls"] == {}


# ---------------------------------------------------------------------------------
# Transições de estado
# ---------------------------------------------------------------------------------

def test_url_invalida_e_sinalizada_sem_requisicao(detector):
    """URL ausente ou malformada exige ação manual e não gera tráfego."""
    detector.session = SessaoFalsa()  # nenhuma resposta programada
    for invalida in ("", "ftp://arquivo", "nao-e-url"):
        resultado = detector.check_url(invalida, "CASAN", "SC")
        assert resultado["status"] == "INVALID_URL"
        assert resultado["requires_manual_action"] is True
    assert detector.session.urls_consultadas == [], "houve requisição para URL inválida"


def test_primeira_verificacao_registra_a_assinatura_inicial(detector):
    """Na primeira vez a URL é apenas registrada, sem alarme de mudança."""
    detector.session = SessaoFalsa(RespostaFalsa(b"conteudo tarifario original"))
    resultado = detector.check_url(URL, "CASAN", "SC")

    assert resultado["status"] == "INITIALIZED"
    assert resultado["requires_manual_action"] is False
    assert resultado["content_sha256"] == TariffChangeDetector.compute_sha256(
        b"conteudo tarifario original"
    )
    assert resultado["content_length"] == len(b"conteudo tarifario original")


def test_conteudo_identico_nao_dispara_alarme(detector):
    """Mesma assinatura em duas verificações significa documento inalterado."""
    conteudo = b"resolucao tarifaria 2026"
    detector.session = SessaoFalsa(RespostaFalsa(conteudo), RespostaFalsa(conteudo))

    primeira = detector.check_url(URL, "CASAN", "SC")
    segunda = detector.check_url(URL, "CASAN", "SC")

    assert primeira["status"] == "INITIALIZED"
    assert segunda["status"] == "UNCHANGED"
    assert segunda["requires_manual_action"] is False
    assert segunda["content_sha256"] == primeira["content_sha256"]


def test_conteudo_alterado_exige_acao_manual(detector):
    """Assinatura diferente indica que a concessionária publicou nova tarifa.

    Esta é a razão de existir do módulo: sem a sinalização, o catálogo de 652
    municípios envelheceria silenciosamente.
    """
    detector.session = SessaoFalsa(
        RespostaFalsa(b"resolucao tarifaria 2026"),
        RespostaFalsa(b"resolucao tarifaria 2027 - valores reajustados"),
    )

    antes = detector.check_url(URL, "CASAN", "SC")
    depois = detector.check_url(URL, "CASAN", "SC")

    assert depois["status"] == "PAGE_CHANGED_MANUAL_REVIEW_REQUIRED"
    assert depois["requires_manual_action"] is True
    assert depois["content_sha256"] != antes["content_sha256"], (
        "a nova assinatura não substituiu a anterior no resultado"
    )
    assert depois["change_history"], "a alteração não foi registrada no histórico"


def test_erro_http_e_sinalizado_para_acao_manual(detector):
    """Link quebrado no site da concessionária precisa chegar ao operador."""
    detector.session = SessaoFalsa(RespostaFalsa(b"", status_code=404))
    resultado = detector.check_url(URL, "CASAN", "SC")

    assert resultado["status"] == "HTTP_ERROR"
    assert resultado["http_status"] == 404
    assert resultado["requires_manual_action"] is True


def test_cabecalhos_de_validacao_sao_preservados(detector):
    """ETag e Last-Modified são guardados para diagnóstico da origem."""
    detector.session = SessaoFalsa(RespostaFalsa(
        b"documento",
        headers={"ETag": '"abc-123"', "Last-Modified": "Mon, 01 Sep 2026 10:00:00 GMT"},
    ))
    resultado = detector.check_url(URL, "CASAN", "SC")

    assert resultado["etag"] == '"abc-123"'
    assert resultado["last_modified_header"] == "Mon, 01 Sep 2026 10:00:00 GMT"


def test_documento_gigante_e_truncado_no_limite(detector):
    """O hash usa no máximo 2 MB, para que um arquivo enorme não trave a rotina."""
    detector.session = SessaoFalsa(RespostaFalsa(b"x" * (3 * 1024 * 1024)))
    resultado = detector.check_url(URL, "CASAN", "SC")

    assert resultado["content_length"] <= 2 * 1024 * 1024 + 64 * 1024, (
        f"leu {resultado['content_length']} bytes, acima do limite previsto"
    )
    assert resultado["status"] == "INITIALIZED"
