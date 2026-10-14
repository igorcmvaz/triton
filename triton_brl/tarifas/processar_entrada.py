# -*- coding: utf-8 -*-
"""Registra os arquivos recebidos na pasta tarifas/entrada/ no registro de fontes.

Varre a pasta tarifas/entrada/ (e subpastas por prestador), identifica o prestador
e o arquivo, calcula a impressão digital SHA-256 e registra em tarifas/fontes/registro.json,
move o material original para tarifas/fontes/<prestador>/ (só apaga da entrada depois de
conferir a cópia pela impressão digital). Arquivo já registrado também sai da entrada; o que
não se identifica vai para tarifas/entrada/_a_identificar/. A entrada fica só com o pendente.

Ao final, regera automaticamente REGISTRO.md e lista_de_coleta.html.

Uso:
    python tarifas/processar_entrada.py
"""

from __future__ import annotations

import os
import re
import shutil
import sys
import unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
ENTRADA = os.path.join(AQUI, "entrada")

for p in (AQUI, os.path.join(RAIZ, "manual")):
    if p not in sys.path:
        sys.path.insert(0, p)

import gerar_lista_de_coleta  # noqa: E402
import registro_de_fontes as R  # noqa: E402
import tabela_de_faixas as T  # noqa: E402

# Metadados conhecidos ordenados por especificidade (chave, (prestador, conteudo, vigencia))
REGRAS = [
    # Recebidos em 05/10/2026
    ("resolucao_arsap", ("CSA Equatorial", "Resolução ARSAP nº 009/2026 (Diário Oficial do Amapá de 30/07/2026), reajuste da CSA Equatorial", "30/07/2026")),
    ("so_carlos", ("SAAE São Carlos", "Resolução ARES-PCJ nº 646/2025 - Revisão tarifária SAAE São Carlos (digitalizada)", "2025")),
    ("tarifria_itu", ("Companhia Ituana de Saneamento (CIS)", "Resolução ARES-PCJ nº 693/2026 - Revisão tarifária de Itu", "02/04/2026")),
    ("tarifa_novembro_2023", ("COSANPA", "Tabela tarifária COSANPA aplicada a partir de 28/11/2023 (Resolução Normativa ARBEL nº 002/2022)", "28/11/2023")),
    # Recebidos em 04/10/2026
    ("daev_valinhos", ("DAE Valinhos", "Resolução ARES-PCJ nº 483/2023 - Revisão tarifária DAEV Valinhos", "27/02/2023")),
    ("bo_bm_1510", ("SAAE Barra Mansa", "Boletim Oficial de Barra Mansa nº 1510 (06/03/2026), com a tabela tarifária do SAAE", "06/03/2026")),
    ("dae_bauru", ("DAE Bauru", "Página oficial de tarifas do DAE Bauru", "2026")),
    ("diario_07082025", ("DAESC Coruripe", "Diário Oficial de Coruripe de 07/08/2025: portaria de tarifas e preços do DAESC", "07/08/2025")),
    ("cosama", ("COSAMA", "Página oficial de Estrutura Tarifária da COSAMA (Amazonas)", "2026")),
    ("gs_inima_samar", ("GS Inima SAMAR", "Página oficial de Legislação e Tarifas - GS Inima SAMAR (Araçatuba)", "2026")),
    ("ourinhos", ("Ourinhos Saneamento", "Página oficial de Legislação e Tarifas - Ourinhos Saneamento", "2026")),
    ("res_285_2024", ("SAAE Passos", "Resolução ARISB-MG nº 285/2024 - Revisão tarifária SAAE Passos", "26/04/2024")),
    ("resolucao_383", ("CODAU Uberaba", "Resolução ARISB-MG nº 383/2026 - Revisão tarifária CODAU Uberaba", "19/02/2026")),
    ("dae_americana", ("DAE Americana", "Página oficial de Serviços/Tarifas do DAE Americana", "2026")),
    ("vigente_a_partir_de_1_de_marco_de_2026", ("Companhia Águas de Joinville", "Tabela tarifária de água e esgoto da Companhia Águas de Joinville vigente a partir de 01/03/2026, todas as categorias", "01/03/2026")),
    ("tabela_valores_2026", ("DAEB Bagé", "Tabela de tarifas de água e esgoto do DAEB Bagé para 2026 (Resolução AGESAN CSR nº 040/2025), todas as categorias", "2026")),
    ("dmae", ("DMAE Poços de Caldas", "Página oficial Tarifa - Tabela de Preço do DMAE Poços de Caldas", "2026")),
    ("tarifas_2026_parcela1", ("COMUSA Novo Hamburgo", "Tabela das tarifas de água e esgoto de Novo Hamburgo 2026 (1ª parcela)", "2026")),
    ("oficio_361_2026aris", ("EMASA Balneário Camboriú", "Deliberação ARIS nº 015/2026 - Reajuste tarifário EMASA Balneário Camboriú", "2026")),
    ("publicado_27336", ("COHASB / Prefeitura de Humaitá – prestação local", "Diário Oficial dos Municípios do Amazonas nº 1258 (30/12/2014): Lei Municipal de Humaitá nº 669/2014, tarifas da COHASB", "29/12/2014")),
    ("lei_5_693", ("SAAE Cacoal", "Lei Municipal de Cacoal nº 5.693/2025, tarifas do SAAE", "2025")),
    ("realinhamento_tarifas", ("DAEP Penápolis", "Resolução nº 01/2026 de realinhamento de tarifas do DAEP Penápolis (Diário Oficial de 12/03/2026)", "12/03/2026")),
    ("resolucao_332", ("CESAMA Juiz de Fora", "Resolução ARISB-MG nº 332/2025 - Revisão tarifária CESAMA Juiz de Fora (digitalizada)", "31/03/2025")),
    ("samae_sbs", ("SAMAE São Bento do Sul", "Tabela tarifária do SAMAE São Bento do Sul (SAMAE SBS)", "")),
    ("estrutura_tarifaria_bloco_c", ("Verde Alagoas", "Estrutura tarifária do Bloco C – Verde Ambiental Alagoas (ARSAL)", "")),
    ("prolagos", ("Prolagos", "Material tarifário oficial de Prolagos", "2026")),
    ("aguaspiaui", ("Águas do Piauí", "Página oficial de Legislação e Tarifas - Águas do Piauí", "2026")),
    ("aguasdorio", ("Águas do Rio", "Página oficial de Legislação e Tarifas - Águas do Rio", "2026")),
    # «legislacao_e_tarifas» não identifica ninguém: é o nome da página de todas as
    # concessionárias da Aegea (Águas de Sorriso, de Teresina, do Rio…). A Águas do Rio
    # é reconhecida por «aguasdorio» e pelo nome do prestador.
    ("cachoeiro", ("BRK Ambiental Cachoeiro", "Estrutura Tarifária BRK Ambiental Cachoeiro 2024/2025, todas as categorias", "2024")),
    ("sumar", ("BRK Ambiental Sumaré", "Resolução ARES-PCJ nº 672/2025 - Reajuste Tarifário BRK Ambiental Sumaré", "11/12/2025")),
    ("limeira", ("BRK Ambiental Limeira", "Resolução ARES-PCJ nº 705/2026 - Reajuste Tarifário BRK Ambiental Limeira", "29/05/2026")),
    ("15120915", ("BRK Ambiental Uruguaiana", "Tabela de Tarifas BRK Uruguaiana 2025 (Reajuste 14,58%), todas as categorias", "30/08/2025")),
    ("bloco_a", ("BRK Alagoas", "Estrutura Tarifária Bloco A - BRK Alagoas (Resolução ARSAL nº 237/2025), todas as categorias", "05/11/2025")),
    ("resolucao_reajuste_tarifariopdf", ("BRK Tocantins", "Resolução ATR nº 13/2025 - Reajuste Tarifário BRK Tocantins", "05/11/2025")),
    ("csa", ("CSA Equatorial", "Resolução ARSAP nº 008/2025 - Reajuste Tarifário Anual CSA Equatorial (Amapá)", "30/07/2025")),
    ("anexo_vii", ("COSANPA", "Anexo VII - Concessão Regionalizada Blocos A, B, C e D (Pará / Cosanpa)", "13/12/2024")),
    ("022455", ("Águas do Sertão", "Tabela tarifária Águas do Sertão 2026 (Alagoas)", "06/02/2026")),
    ("nfvjp", ("Iguá Sergipe", "Estrutura Tarifária Iguá Sergipe 2025/2026 (Portaria AGRESE nº 56/2025), todas as categorias", "01/09/2025")),
    ("arpb", ("CAGEPA", "Resolução ARPB nº 004/2025 - Homologação do Reajuste Tarifário CAGEPA (Paraíba)", "16/06/2025")),
    ("natal", ("CAERN", "Resolução CAERN RS.CA.P.G.02.0002.03 - Reajuste Tarifário Natal e Interior RN", "10/06/2025")),
    ("082_2025", ("CAERD", "Resolução AGERO nº 82/2025 - Reajuste Tarifário CAERD (Rondônia)", "2025")),
    ("tabela_de_tarifas_de_agua_tem_novo_valor", ("CAEMA", "Notícia e Tabela oficial de novas tarifas da CAEMA (Maranhão)", "2025")),
    ("01_06_2026_a_31_05_2027", ("CAESB", "Tabela de tarifas da CAESB (DF) de 01/06/2026 a 31/05/2027 (Resolução ADASA nº 70/2026)", "01/06/2026")),
    ("tarifas_2026_institucional", ("EMBASA", "Página oficial de Tarifas 2026 - EMBASA (Bahia)", "2026")),
    ("estruturatarifaria_2025_corrigida", ("SANEACRE", "Estrutura Tarifária do SANEACRE 2025 (Resolução nº 104/AGEAC, de 14/04/2025)", "14/04/2025")),
    ("estrutura_tarifaria_jan_2026_vigente", ("Rio+ Saneamento", "Estrutura tarifária vigente (AGENERSA, incidência a partir de 22/01/2026), área de Barra do Piraí, Itaperuna, Macaé e outros", "22/01/2026")),
    ("tarifas_categoria_comercial", ("ARES-PCJ", "Tarifas Categoria Comercial dos municípios regulados pela ARES-PCJ (posição 01/09/2026)", "01/09/2026")),
    ("tarifas_categoria_industrial", ("ARES-PCJ", "Tarifas Categoria Industrial dos municípios regulados pela ARES-PCJ (posição 01/09/2026)", "01/09/2026")),
    ("tarifas_categoria_residencial_social", ("ARES-PCJ", "Tarifas Categoria Residencial Social dos municípios regulados pela ARES-PCJ (posição 01/09/2026)", "01/09/2026")),
    ("tarifas_categoria_residencial", ("ARES-PCJ", "Tarifas Categoria Residencial dos municípios regulados pela ARES-PCJ (posição 01/09/2026)", "01/09/2026")),
    ("estrutura_tarifaria_2026", ("CASAL", "Estrutura Tarifária CASAL 2026 (Resolução ARSAL nº 233/2025), todas as categorias", "08/12/2025")),
    ("casan", ("CASAN", "Página oficial de tarifas CASAN (Resolução ARESC 389/2026), todas as categorias", "01/04/2026")),
    ("sanepar", ("SANEPAR", "Página oficial de tarifas Sanepar (Curitiba e Demais localidades), todas as categorias", "2026")),
    ("sabesp", ("SABESP", "Nota Técnica 1º Reajuste Tarifário SABESP URAE-1 Sudeste - Tarifa de Aplicação", "01/01/2026")),
    ("cesan", ("CESAN", "Resolução ARSP nº 107/2026 (2ª RTO CESAN), novas estruturas tarifárias de água e esgoto", "01/09/2026")),
    ("sanesul", ("SANESUL", "Estrutura Tarifária 2026 SANESUL (Áreas 1, 2 e 3 MS), água e esgoto, todas as categorias", "2026")),
    ("saneago", ("SANEAGO", "Resolução Normativa Conjunta AGR/AR nº 01/2026, reajuste tarifário Saneago", "2026")),
    ("agr_ar", ("SANEAGO", "Resolução Normativa Conjunta AGR/AR nº 01/2026, reajuste tarifário Saneago", "2026")),
    ("copasa", ("COPASA", "Tabela Tarifária AMASBE 2026/2027 para COPASA (Montes Claros - MG), todas as faixas e categorias", "22/01/2026")),
    ("amasbe", ("COPASA", "Tabela Tarifária AMASBE 2026/2027 para COPASA (Montes Claros - MG), todas as faixas e categorias", "22/01/2026")),
    ("caer", ("CAER", "Material tarifário oficial de CAER", "")),
    ("cagece", ("CAGECE", "Material tarifário oficial de CAGECE", "")),
    ("compesa", ("COMPESA", "Material tarifário oficial de COMPESA", "")),
]


def _normalizar(texto: str) -> str:
    sem = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "_", sem.lower()).strip("_")


def _identificar_prestador(caminho_rel: str) -> tuple[str, str, str]:
    """Retorna (prestador, conteudo, vigencia) a partir do nome ou subpasta."""
    norm = _normalizar(caminho_rel)
    # A subpasta com o nome de um prestador da base (a pasta que a lista de coleta sugere)
    # vence as regras por nome de arquivo: «dmae_porto_alegre/DMAE_...» é de Porto Alegre.
    partes = caminho_rel.replace("\\", "/").split("/")
    if len(partes) > 1:
        pasta = partes[0]
        for p in sorted({d.get("prestador_saneamento") for d in T.carregar().values()
                         if d.get("prestador_saneamento")}):
            if R._pasta(p) == pasta:
                return p, f"Material tarifário oficial de {p}", ""
    # O mais específico primeiro: o nome completo de um prestador da base, do mais longo
    # para o mais curto; depois o município no nome do arquivo («dmae_porto_alegre_...»
    # é de Porto Alegre, não do primeiro «DMAE»); só então as regras por fragmento de
    # nome, que são genéricas («estrutura_tarifaria_2026», «dmae»).
    cidades = T.carregar()
    todos = sorted({d.get("prestador_saneamento") for d in cidades.values() if d.get("prestador_saneamento")},
                   key=lambda p: -len(_normalizar(p)))
    for p in todos:
        if _normalizar(p) in norm:
            return p, f"Material tarifário oficial de {p}", ""

    for nome, p in sorted(_prestador_de_cada_municipio_normalizado(cidades).items(), key=lambda kv: -len(kv[0])):
        if len(nome) >= 5 and re.search(r"(?:^|_)" + re.escape(nome) + r"(?:_|$)", norm):
            return p, f"Material tarifário oficial de {p}", ""

    for chave, (prestador, conteudo, vigencia) in REGRAS:
        if chave in norm:
            return prestador, conteudo, vigencia

    return "", "", ""


def _prestador_de_cada_municipio_normalizado(cidades: dict) -> dict:
    """{município normalizado: prestador da base} de todos os municípios."""
    return {_normalizar(d["municipio"]): d["prestador_saneamento"] for d in cidades.values()
            if d.get("prestador_saneamento")}


def _prestador_por_municipio(cidades: dict) -> dict:
    """{município normalizado: prestador} só para prestador de um município só."""
    contagem: dict = {}
    for d in cidades.values():
        contagem[d.get("prestador_saneamento")] = contagem.get(d.get("prestador_saneamento"), 0) + 1
    return {_normalizar(d["municipio"]): d["prestador_saneamento"] for d in cidades.values()
            if d.get("prestador_saneamento") and contagem[d["prestador_saneamento"]] == 1}


def _texto(caminho: str) -> str:
    try:
        if caminho.lower().endswith(".pdf"):
            import fitz
            return "\n".join(p.get_text() for p in fitz.open(caminho))
        if caminho.lower().endswith((".html", ".htm")):
            from bs4 import BeautifulSoup
            with open(caminho, encoding="utf-8", errors="replace") as f:
                return BeautifulSoup(f.read(), "html.parser").get_text(" ")
    except Exception:  # noqa: BLE001 - arquivo ilegível só deixa de ser identificado
        return ""
    return ""


def _sem_acento(texto: str) -> str:
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn")


def _prestador_de_cada_municipio(cidades: dict) -> dict:
    """{nome do município sem acento: prestador} de todos os municípios da base."""
    return {_sem_acento(d["municipio"]): d["prestador_saneamento"] for d in cidades.values()
            if d.get("prestador_saneamento")}


def _citacoes(nome: str, texto: str) -> int:
    """Quantas vezes o município aparece como nome próprio («Natal», «NATAL»).

    A palavra comum em minúscula não conta: «registro do cavalete» não é o município
    de Registro, e «natal» não é Natal.
    """
    formas = {nome, nome.upper()}
    return sum(len(re.findall(r"(?<![\w])" + re.escape(f) + r"(?![\w])", texto)) for f in formas)


#: «Castilho/SP», «Castilho - SP»: município com UF, para avisar quando está fora da base.
_CIDADE_UF = re.compile(r"([A-ZÀ-Ú][\wÀ-ú' ]{2,40}?)\s*[/-]\s*(AC|AL|AM|AP|BA|CE|DF|ES|GO|MA|MG|MS|MT|PA|PB|PE|"
                        r"PI|PR|RJ|RN|RO|RR|RS|SC|SE|SP|TO)\b")


def municipios_fora_da_base(texto: str, cidades: dict) -> list:
    """Municípios citados com a UF («Castilho/SP») que não estão entre os 652."""
    base = {(_normalizar(d["municipio"]), d["uf"]) for d in cidades.values()}
    fora = []
    for m in _CIDADE_UF.finditer(texto):
        nome = m.group(1).strip().split("  ")[-1]
        if nome.isupper() and " " not in nome:
            continue  # sigla («AGESAN/RS»), não município
        par = (_normalizar(nome), m.group(2))
        if par not in base and f"{nome}/{m.group(2)}" not in fora:
            fora.append(f"{nome}/{m.group(2)}")
    return fora


def _identificar_pelo_conteudo(caminho: str) -> tuple[str, str, str]:
    """O prestador do município da base mais citado no texto, se nenhum outro o disputa.

    Serve para páginas salvas com nome genérico («TARIFAS VIGENTES.html») e para
    resoluções de agência que só nomeiam o município («no âmbito do Município do
    Natal»). Vale para qualquer município da base: o prestador é o que a base dá a
    ele. O registro diz que a identificação veio do conteúdo, para ser conferida.
    """
    texto = _sem_acento(_texto(caminho))
    if not texto.strip():
        return "", "", ""
    achados = {}
    # Do nome mais longo para o mais curto: «Barra do Garças» não conta como «Barra».
    for nome, p in sorted(_prestador_de_cada_municipio(T.carregar()).items(), key=lambda kv: -len(kv[0])):
        if len(nome) < 5:
            continue
        n = _citacoes(nome, texto)
        if n:
            for f in (nome, nome.upper()):
                texto = re.sub(r"(?<![\w])" + re.escape(f) + r"(?![\w])", " ", texto)
            achados[p] = achados.get(p, 0) + n
    if not achados:
        return "", "", ""
    ordem = sorted(achados.items(), key=lambda kv: -kv[1])
    if len(ordem) > 1 and ordem[1][1] * 2 > ordem[0][1]:
        return "", "", ""  # ambíguo: dois municípios disputam o texto
    p = ordem[0][0]
    return p, f"Material tarifário de {p} (prestador identificado pelo conteúdo do arquivo; conferir)", ""


A_IDENTIFICAR = os.path.join(ENTRADA, "_a_identificar")


def _tirar_da_entrada(caminho: str, item: dict) -> None:
    """Apaga da entrada o arquivo já guardado em fontes/, depois de conferir a impressão digital."""
    guardado = os.path.join(RAIZ, item.get("guardado_em") or "")
    if not item.get("guardado_em") or not os.path.isfile(guardado):
        return  # não guardado (material de terceiros): fica onde está
    if R.impressao(guardado) != item["sha256"]:
        return
    os.remove(caminho)
    anexa = os.path.splitext(caminho)[0] + "_files"
    destino_anexa = os.path.join(os.path.dirname(guardado), os.path.basename(anexa))
    if os.path.isdir(anexa) and os.path.isdir(destino_anexa):
        shutil.rmtree(anexa)


def _urls_anotadas() -> dict:
    """{nome do arquivo: URL} dos `fontes.txt` da entrada (uma linha por arquivo)."""
    urls = {}
    for raiz, _dirs, arquivos in os.walk(ENTRADA):
        if "fontes.txt" in arquivos:
            with open(os.path.join(raiz, "fontes.txt"), encoding="utf-8") as f:
                for linha in f:
                    m = re.match(r"\s*(.+?)\s+(https?://\S+)\s*$", linha)
                    if m:
                        urls[m.group(1)] = m.group(2)
    return urls


def processar() -> int:
    """Registra o que é novo, move para tarifas/fontes/ e deixa na entrada só o pendente."""
    reg = R.carregar()
    R.ADIAR_PAGINAS = True   # as páginas saem uma vez, no fim (gerar_lista_de_coleta abaixo)
    registrados = removidos = 0
    pendentes = []
    urls = _urls_anotadas()

    for raiz, dirs, arquivos in os.walk(ENTRADA):
        # Ignora as pastas de suporte (_files); a de não identificados é tentada de novo
        dirs[:] = [d for d in dirs if not d.endswith("_files")]
        for arq in sorted(arquivos):
            if arq in ("LEIAME.md", "fontes.txt") or arq.startswith("."):
                continue
            caminho = os.path.join(raiz, arq)
            caminho_rel = os.path.relpath(caminho, ENTRADA)

            anterior = R.ja_recebido(reg, R.impressao(caminho))
            if anterior:
                _tirar_da_entrada(caminho, anterior)
                removidos += 1
                continue

            prestador, conteudo, vigencia = _identificar_prestador(caminho_rel)
            if not prestador:
                prestador, conteudo, vigencia = _identificar_pelo_conteudo(caminho)
            if not prestador:
                if os.path.dirname(caminho) != A_IDENTIFICAR:
                    os.makedirs(A_IDENTIFICAR, exist_ok=True)
                    shutil.move(caminho, os.path.join(A_IDENTIFICAR, arq))
                    anexa = os.path.splitext(caminho)[0] + "_files"
                    if os.path.isdir(anexa):
                        shutil.move(anexa, os.path.join(A_IDENTIFICAR, os.path.basename(anexa)))
                fora = municipios_fora_da_base(_texto(os.path.join(A_IDENTIFICAR, arq)), T.carregar())
                pendentes.append((arq, fora))
                continue

            item = R.registrar(caminho, prestador=prestador, conteudo=conteudo,
                               vigencia=vigencia, guardar=True)
            reg = R.carregar()
            if arq in urls:
                for i in reg["itens"]:
                    if i["id"] == item["id"]:
                        i["url"] = urls[arq]
                R.gravar(reg)
            _tirar_da_entrada(caminho, item)
            registrados += 1
            print(f"Registrado: item {item['id']} — {item['arquivo']} ({prestador})")

    # Pastas que o processamento esvaziou saem da entrada.
    for raiz, _dirs, _arqs in sorted(os.walk(ENTRADA, topdown=False), key=lambda x: -len(x[0])):
        if raiz != ENTRADA and not os.listdir(raiz):
            os.rmdir(raiz)

    # As URLs anotadas já foram para o registro: o fontes.txt sai da entrada.
    for raiz, _dirs, arquivos in os.walk(ENTRADA):
        if "fontes.txt" in arquivos and "_a_identificar" not in raiz:
            os.remove(os.path.join(raiz, "fontes.txt"))

    R.ADIAR_PAGINAS = False
    R.gerar(reg)
    import procedencia
    procedencia.gerar_fila()

    if registrados:
        print(f"\n{registrados} novo(s) arquivo(s) registrado(s) e movido(s) para tarifas/fontes/.")
    else:
        print("Nenhum arquivo novo em tarifas/entrada/.")
    if removidos:
        print(f"{removidos} arquivo(s) já registrados saíram da entrada (a cópia em fontes/ confere).")
    for arq, fora in pendentes:
        aviso = (f" — cita município fora da base: {', '.join(fora[:3])}" if fora else "")
        print(f"Sem prestador identificado, em entrada/_a_identificar/: {arq}{aviso}")
    print(f"Total no registro de fontes: {len(reg['itens'])} item(ns). Próximo passo: transcrever "
          "(ver tarifas/transcricoes/FILA.md).")
    return registrados


if __name__ == "__main__":
    processar()
