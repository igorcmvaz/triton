# -*- coding: utf-8 -*-
"""Licença da E-OBS na edição IBE/PRT: o aviso do primeiro arranque, a escolha de uso e o rodapé do laudo.

A chuva da edição vem da E-OBS (ECA&D/Copernicus), de uso estritamente não comercial em pesquisa e
educação. A licença não trata da redistribuição de produtos derivados (``LICENCAS_DOS_DADOS.md``);
o aviso diz ao utilizador o que a licença pede, e o laudo repete a restrição e a citação. Nada aqui é
parecer jurídico: o texto precisa de revisão da UFSC antes da primeira distribuição (D5).

O que NÃO acontece por defeito: o programa não bloqueia a E-OBS. O bloqueio (E-OBS desligada, com o
caminho ``custom_file`` da série própria) existe, mas fica atrás de ``BLOQUEAR_E_OBS_EM_USO_COMERCIAL``.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

# decisão do usuário pendente (D1)
#: Bloquear a E-OBS quando o utilizador declara uso comercial? False (padrão): só avisa, regista a declaração no laudo e segue. True: a E-OBS fica indisponível
#: e o programa pede a série própria (``climate_source_mode = "custom_file"``).
BLOQUEAR_E_OBS_EM_USO_COMERCIAL = False

USO_PESQUISA = "pesquisa"
USO_COMERCIAL = "comercial"
USOS = (USO_PESQUISA, USO_COMERCIAL)

#: As duas respostas do aviso, tal como aparecem nos botões.
RESPOSTAS = {
    USO_PESQUISA: "Uso de pesquisa ou educação",
    USO_COMERCIAL: "Uso comercial",
}

TITULO_DO_AVISO = "Dados de chuva: licença da E-OBS"

TEXTO_DO_AVISO = (
    "Os dados de chuva desta edição vêm da E-OBS, de uso estritamente não comercial em pesquisa e educação. "
    "A E-OBS é um produto do projeto ECA&D e do serviço Copernicus (versão {versao}). "
    "Se o seu projeto é profissional ou pago, carregue a sua própria série de chuva ou obtenha autorização "
    "dos titulares dos dados. O programa não verifica o uso; a responsabilidade é de quem o declara. "
    "Este aviso não é parecer jurídico. Escolha o uso que se aplica a este computador."
)

#: O que o ecrã diz depois de «Uso comercial», conforme a constante.
TEXTO_COMERCIAL_BLOQUEADO = (
    "A base E-OBS foi desligada neste computador. Carregue a série diária de chuva do seu projeto "
    "(ficheiro próprio) ou obtenha autorização dos titulares dos dados."
)
TEXTO_COMERCIAL_SO_AVISA = (
    "A E-OBS só pode ser usada em pesquisa e educação não comerciais. O programa mantém a base disponível, "
    "mas a sua declaração de uso comercial fica registada nos laudos. Para uso comercial, carregue a sua "
    "própria série de chuva ou obtenha autorização dos titulares dos dados."
)

CITACAO = ("Cornes, R. C., van der Schrier, G., van den Besselaar, E. J. M., Jones, P. D. (2018). An Ensemble Version "
           "of the E-OBS Temperature and Precipitation Data Sets. J. Geophys. Res. Atmos., 123(17), 9391-9409. "
           "doi:10.1029/2017JD028200")
RECONHECIMENTO = ("We acknowledge the E-OBS dataset from the EU-FP6 project UERRA (https://www.uerra.eu) and the "
                  "Copernicus Climate Change Service, and the data providers in the ECA&D project (https://www.ecad.eu)")

_CHAVE = "licenca_eobs/uso"
_memoria: Dict[str, str] = {}


class LicencaEObsBloqueada(RuntimeError):
    """A E-OBS está desligada neste computador (uso comercial declarado e bloqueio ligado)."""


# ── Escolha de uso, lembrada na configuração do utilizador ──────────────────────────────────

def _armazem():
    """A configuração do utilizador (QSettings da edição); None sem PySide6."""
    try:
        from PySide6.QtCore import QSettings
        # o mesmo par organização/aplicação das preferências da edição (triton/ui/translation.py)
        return QSettings("UFSC", "Triton-PRT")
    except Exception:
        return None


def ler_escolha(armazem: Optional[Any] = None) -> Optional[str]:
    """O uso que o utilizador declarou neste computador: 'pesquisa', 'comercial' ou None (nunca escolheu)."""
    arm = armazem if armazem is not None else _armazem()
    valor = _memoria.get(_CHAVE) if arm is None else arm.value(_CHAVE, "")
    valor = str(valor or "")
    return valor if valor in USOS else None


def gravar_escolha(uso: str, armazem: Optional[Any] = None) -> None:
    if uso not in USOS:
        raise ValueError(f"Uso inválido: {uso!r}; use um de {USOS}.")
    arm = armazem if armazem is not None else _armazem()
    if arm is None:
        _memoria[_CHAVE] = uso
        return
    arm.setValue(_CHAVE, uso)
    arm.sync()


def precisa_perguntar(armazem: Optional[Any] = None) -> bool:
    """Só a edição com a base E-OBS pergunta, e só uma vez por instalação (até haver escolha gravada)."""
    from triton.core.edition import usa_dados_de_portugal
    return usa_dados_de_portugal() and ler_escolha(armazem) is None


def e_obs_bloqueada(armazem: Optional[Any] = None) -> bool:
    """A E-OBS está desligada? Só com a constante ligada e a declaração de uso comercial."""
    return bool(BLOQUEAR_E_OBS_EM_USO_COMERCIAL) and ler_escolha(armazem) == USO_COMERCIAL


def texto_do_aviso() -> str:
    from triton.core import base_climatica_portugal as _pt
    versao = "v33.0e"
    try:
        if _pt.disponivel():
            versao = _pt.pacote().get("versao_eobs") or versao
    except Exception:
        pass
    return TEXTO_DO_AVISO.format(versao=versao)


def texto_depois_da_escolha(uso: str) -> str:
    """O que o utilizador lê depois de responder; vazio para o uso de pesquisa ou educação."""
    if uso != USO_COMERCIAL:
        return ""
    return TEXTO_COMERCIAL_BLOQUEADO if BLOQUEAR_E_OBS_EM_USO_COMERCIAL else TEXTO_COMERCIAL_SO_AVISA


# ── Rodapé do laudo ──────────────────────────────────────────────────────────────────────────

def rodape_do_laudo(auditoria: Optional[Dict[str, Any]] = None, ingles: bool = False) -> str:
    """As linhas de texto que fecham todo laudo da edição IBE/PRT; vazio nas outras edições.

    ``auditoria`` é o ``audit_context`` do laudo: ``chuva_serie_propria`` (a série não é da E-OBS),
    ``climate_city_name`` (o concelho) e ``chuva_procedencia`` (a procedência gravada no projeto).
    Devolve HTML simples, já escapado, uma linha por ``<br/>``.
    """
    from html import escape
    from triton.core.edition import usa_dados_de_portugal
    if not usa_dados_de_portugal():
        return ""
    from triton.core import qualidade_chuva as _q
    aud = auditoria or {}
    proc = aud.get("chuva_procedencia") or {}
    linhas = []
    if aud.get("chuva_serie_propria"):
        linhas.append("Rainfall: series supplied by the user." if ingles else "Chuva: série fornecida pelo utilizador.")
    else:
        pid = proc.get("pacote_id") or ""
        sha = str(proc.get("sha256_pacote") or "")[:8]
        try:
            atual = _pacote_atual()
        except Exception:
            atual = {}
        pid = pid or atual.get("pacote_id", "")
        sha = sha or str(atual.get("sha256_pacote", ""))[:8]
        versao = proc.get("versao_eobs") or atual.get("versao_eobs") or "v33.0e"
        pacote = (f" Pacote {pid}, SHA-256 {sha}." if pid else "")
        pacote_en = (f" Package {pid}, SHA-256 {sha}." if pid else "")
        if ingles:
            linhas.append(f"Rainfall: E-OBS {versao} (Cornes et al., 2018); use restricted to non-commercial research and "
                          f"education.{pacote_en}")
        else:
            linhas.append(f"Chuva: E-OBS {versao} (Cornes et al., 2018); uso restrito a pesquisa e educação não comerciais."
                          f"{pacote}")
        linhas.append(RECONHECIMENTO)
        if proc.get("mudou") and proc.get("aviso"):
            linhas.append(("Warning: the rainfall package changed since the project was saved. " if ingles else "Aviso: ")
                          + proc["aviso"])
        elif proc and not proc.get("registrado", True):
            linhas.append(proc.get("nota") or "")
        if ler_escolha() == USO_COMERCIAL:
            linhas.append("Declared use on this computer: commercial (the E-OBS licence does not allow it)."
                          if ingles else
                          "Uso declarado neste computador: comercial (a licença da E-OBS não o permite).")
        cidade = str(aud.get("climate_city_name") or "")
        if cidade:
            t = _q.texto_da_qualidade(cidade, "en" if ingles else "pt")
            if t:
                linhas.append(t)
    linhas.append(_q.linha_de_cobertura("en" if ingles else "pt"))
    return "<br/>".join(escape(l) for l in linhas if l)


def _pacote_atual() -> Dict[str, str]:
    from triton.core import base_climatica_portugal as _pt
    return _pt.pacote() if _pt.disponivel() else {}
