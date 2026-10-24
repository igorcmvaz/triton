# -*- coding: utf-8 -*-
"""De onde vem o tarifário de cada concelho, e quanto confiar nele (Triton IBE, parte portuguesa).

Ferramenta de desenvolvimento (fica fora do Git, como ``tarifas_portugal/*.py``). É o equivalente
de ``triton_brl/tarifas/procedencia.py``, mas com o esquema do consenso do debate IBE: TRÊS estados,
por concelho e POR SERVIÇO (água, saneamento, resíduos), em vez de muitas classes.

* **verde, verificado**: documento oficial arquivado (URL e SHA-256); ``confirmado_em`` há menos de 12
  meses; transcrição conferida com as contas impressas (que o teste reproduz); verificação
  INDEPENDENTE registada em ``verificado_por`` (fatura real ±0,05 € ou segunda leitura por outra pessoa;
  um modelo de IA nunca conta); e nenhuma pendência com efeito acima de 1 % na conta de 10 m³;
* **amarelo, a validar**: há documento arquivado ou transcrito, mas falta algum desses requisitos;
* **cinza, sem dado**: sem documento, entidade a identificar, ou dado ruim.

A regra de cada serviço vive em ``triton/core/tarifarios_portugal.py`` (``avaliar_servico``), a mesma
que o programa usa nos concelhos transcritos; aqui só se reúnem os dados: ``entidades.json`` (entidade →
serviço → concelhos → documentos), ``fontes/FONTES.tsv`` (registo mínimo de cada ficheiro: caminho, url,
sha256, data_coleta, entidade, concelhos, tipo, vigencia, confirmado_em, verificado_por, redistribuivel)
e ``portugal_tarifarios.json`` (o que está transcrito, com ``procedencia``). O estado do concelho é verde
se os três serviços forem verdes, cinza se forem todos cinza, amarelo nos restantes casos.

Particularidades portuguesas: a água, o saneamento e os resíduos urbanos são muitas vezes de entidades
diferentes (EPAL e Câmara de Lisboa; Águas do Porto e EMAP), por isso cada serviço tem a sua entidade e o
seu documento; o saneamento cobra-se por escalões; o IVA vem de cada documento; a TRH é parcela própria; a
tarifa fixa depende do calibre. Só se avalia o utilizador doméstico.

Uso (na pasta ``triton_prt``):
    python tarifas_portugal/procedencia_pt.py        # regera CONFIANCA_POR_CONCELHO.csv e .md
"""

from __future__ import annotations

import csv
import json
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import date

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)

from triton.core import tarifarios_portugal as TP  # noqa: E402  (a regra do verde é uma só)

ENTIDADES = os.path.join(AQUI, "entidades.json")
FONTES = os.path.join(AQUI, "fontes", "FONTES.tsv")
TARIFARIOS = os.path.join(RAIZ, "triton", "data", "portugal_tarifarios.json")
CSV = os.path.join(AQUI, "CONFIANCA_POR_CONCELHO.csv")
MD = os.path.join(AQUI, "CONFIANCA_POR_CONCELHO.md")
NL = chr(10)
SERVICOS = TP.SERVICOS
ROTULO = TP.ROTULO_DO_SERVICO
MESES_DE_VIGENCIA = 12
ICONE = {"verde": "🟢", "amarelo": "🟡", "cinza": "⚪"}
ROTULO_ESTADO = {"verde": "verde, verificado", "amarelo": "amarelo, a validar", "cinza": "cinza, sem dado"}
CRITERIO = {
    "verde": ("Documento oficial arquivado com URL e SHA-256; `confirmado_em` há menos de 12 meses; transcrição "
              "conferida com as contas impressas; verificação independente registada em `verificado_por` (fatura "
              "real com tolerância de ±0,05 €, ou segunda leitura por uma pessoa diferente do transcritor; um "
              "modelo de IA nunca conta); e nenhuma pendência com efeito acima de 1 % na conta de 10 m³."),
    "amarelo": ("Há documento oficial arquivado ou transcrito, mas falta algum dos requisitos do verde: transcrição, "
                "conferência, reconfirmação nos últimos 12 meses, verificação independente, ou há pendência com "
                "efeito acima de 1 %."),
    "cinza": ("Sem documento oficial arquivado, entidade gestora por identificar, ou dado ruim. O programa não "
              "traz tarifário e a ficha da ERSAR indica onde o procurar."),
}


# --------------------------------------------------------------------------------------------
# leitura
# --------------------------------------------------------------------------------------------
def url_de(origem: str) -> str:
    m = re.search(r"https?://\S+", origem)
    return m.group(0) if m else ""


def ler_json(caminho: str) -> dict:
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


def ler_fontes() -> dict:
    """FONTES.tsv: caminho → registo mínimo (11 colunas, sem cabeçalho; as 4 primeiras são as de sempre)."""
    cols = ["caminho", "origem", "sha256", "data_coleta", "entidade", "concelhos", "tipo", "vigencia",
            "confirmado_em", "verificado_por", "redistribuivel"]
    out = {}
    with open(FONTES, encoding="utf-8") as f:
        for linha in f:
            c = linha.rstrip(NL).rstrip(chr(13)).split(chr(9))
            if not c[0]:
                continue
            c += [""] * (len(cols) - len(c))
            r = dict(zip(cols, c))
            r["url"] = url_de(r["origem"])
            out[r["caminho"]] = r
    return out


def _meses(desde: date, hoje: date) -> int:
    return (hoje.year - desde.year) * 12 + hoje.month - desde.month


def rotulo_vigencia(iso: str, precisao: str) -> str:
    if not iso:
        return "—"
    d = date.fromisoformat(iso)
    if precisao == "dia":
        return d.strftime("%d/%m/%Y")
    if precisao == "mes":
        return d.strftime("%m/%Y")
    if precisao == "publicacao":
        return "publicado em " + d.strftime("%d/%m/%Y")
    return f"{d.year} (data exata não impressa)"


def _chave(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()


def _entidades_do(ent: dict, concelho: str, servico: str, fichas: dict) -> list:
    """Entidades do concelho no serviço: as da ficha ERSAR primeiro, depois as que só o documento revela."""
    nomes = [f["entidade"] for f in fichas.get(servico, [])]
    for nome, e in ent["entidades"].items():
        if concelho in e["servicos"].get(servico, {}).get("concelhos", []) and nome not in nomes:
            nomes.append(nome)
    return nomes


def _documentos_do(ent: dict, concelho: str, servico: str) -> list:
    """(id, documento, nomeia_o_concelho) dos documentos oficiais que cobrem o concelho no serviço."""
    out = []
    for did, d in ent["documentos"].items():
        if d["tipo"] != "oficial" or servico not in d["servicos"]:
            continue
        if concelho in d.get("concelhos", []):
            out.append((did, d, True))
        elif d.get("entidade_toda"):
            serve = ent["entidades"].get(d["entidade"], {}).get("servicos", {}).get(servico, {}).get("concelhos", [])
            if concelho in serve:
                out.append((did, d, len(serve) == 1))
    return out


# --------------------------------------------------------------------------------------------
# avaliação
# --------------------------------------------------------------------------------------------
def avaliar(hoje: date | None = None) -> list:
    """Uma linha por concelho, em ordem alfabética (sem acentos)."""
    hoje = hoje or date.today()
    ent = ler_json(ENTIDADES)
    fontes = ler_fontes()
    tar = {k: v for k, v in ler_json(TARIFARIOS).items() if not k.startswith("_")}
    linhas = []
    for nome, meta in ent["concelhos"].items():
        fichas = meta.get("fichas_ersar", {})
        transcrito = tar.get(nome)
        proc = (transcrito or {}).get("procedencia") or {}
        por_servico, entidades_de, urls_doc = {}, {}, []
        vigs = []
        for s in SERVICOS:
            entidades = _entidades_do(ent, nome, s, fichas)
            entidades_de[s] = entidades
            docs = _documentos_do(ent, nome, s)
            extras = []
            if meta.get("dado_ruim"):
                por_servico[s] = ("cinza", ["dado ruim: " + meta["dado_ruim"]])
            elif not docs:
                por_servico[s] = ("cinza", [f"entidade {' / '.join(entidades)}: sem documento arquivado" if entidades
                                            else "entidade a identificar"])
            else:
                registos = []
                for did, d, nomeia in docs:
                    for caminho in d["ficheiros"]:
                        r = fontes.get(caminho, {})
                        registos.append({"url": r.get("url", ""), "sha256": r.get("sha256", ""),
                                         "confirmado_em": r.get("confirmado_em", ""),
                                         "verificado_por": r.get("verificado_por", "")})
                    u = fontes.get(d["ficheiros"][0], {}).get("url", "")
                    if u and u not in urls_doc:
                        urls_doc.append(u)
                    vigs.append((d["vigencia_inicio"], d["vigencia_precisao"]))
                    ers = [f["entidade"] for f in fichas.get(s, [])]
                    if not nomeia:
                        extras.append(f"o documento da {d['entidade']} não nomeia concelhos: confirmar que vale em {nome}")
                    if ers and d["entidade"] not in ers:
                        extras.append(f"a ERSAR indica {' / '.join(ers)}, e o documento é de {d['entidade']}")
                transcr = proc.get("servicos", {}).get(s) == "transcrito"
                pend = [p for p in proc.get("pendencias", []) if s in p.get("servicos", SERVICOS)]
                estado_s, motivos = TP.avaliar_servico(registos, transcr, bool(proc.get("conferido")), pend, hoje)
                por_servico[s] = (estado_s, motivos + extras)
        if proc.get("vigencia_inicio"):
            vigs.append((proc["vigencia_inicio"], "dia"))
        vig = min(vigs) if vigs else ("", "")
        vencida = bool(vig[0]) and _meses(date.fromisoformat(vig[0]), hoje) > MESES_DE_VIGENCIA
        if vencida:
            for s in SERVICOS:
                if por_servico[s][0] != "cinza":
                    por_servico[s][1].append(f"vigência {rotulo_vigencia(*vig)}, com mais de 12 meses: procurar o tarifário atual")
        estado = TP.estado_do_concelho(por_servico)

        # «o que falta»: o que é comum aos serviços com documento diz-se uma vez
        vivos = [s for s in SERVICOS if por_servico[s][0] != "cinza"]
        comuns = []
        if len(vivos) > 1:
            comuns = [m for m in por_servico[vivos[0]][1] if all(m in por_servico[s][1] for s in vivos[1:])]
        falta = []
        if comuns:
            falta.append("em todos os serviços com documento: " + "; ".join(comuns))
        for s in SERVICOS:
            est, mot = por_servico[s]
            resto = [m for m in mot if m not in comuns]
            if est != "verde" and resto:
                falta.append(f"{ROTULO[s]}: " + "; ".join(resto))
        if not falta:
            falta.append("nada em aberto")

        rots = {s: (" / ".join(entidades_de[s]) if entidades_de[s] else "a identificar") for s in SERVICOS}
        entidade = rots["agua"] if len(set(rots.values())) == 1 else "; ".join(f"{ROTULO[s]}: {rots[s]}" for s in SERVICOS)
        urls_ficha = []
        for s in SERVICOS:
            for f in fichas.get(s, [])[:1]:
                if f["url"] not in urls_ficha:
                    urls_ficha.append(f["url"])
        linhas.append({
            "concelho": nome, "distrito": meta["distrito"], "entidade": entidade, "estado": estado,
            "estados": {s: por_servico[s][0] for s in SERVICOS}, "motivos": {s: por_servico[s][1] for s in SERVICOS},
            "vigencia": rotulo_vigencia(*vig) if vig[0] else "—", "o_que_falta": " | ".join(falta),
            "url_documento": " | ".join(urls_doc), "url_ficha_ersar": " | ".join(urls_ficha),
            "transcrito": bool(transcrito),
        })
    linhas.sort(key=lambda l: _chave(l["concelho"]))
    return linhas


# --------------------------------------------------------------------------------------------
# saídas
# --------------------------------------------------------------------------------------------
COLUNAS = ["concelho", "distrito", "entidade", "estado", "estado_agua", "estado_saneamento", "estado_residuos",
           "vigencia", "o_que_falta", "url_documento", "url_ficha_ersar", "gerado_em"]


def escrever_csv(linhas: list, hoje: date) -> None:
    with open(CSV, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";", lineterminator=NL)
        w.writerow(COLUNAS)
        for l in linhas:
            w.writerow([l["concelho"], l["distrito"], l["entidade"], l["estado"], l["estados"]["agua"],
                        l["estados"]["saneamento"], l["estados"]["residuos"], l["vigencia"], l["o_que_falta"],
                        l["url_documento"], l["url_ficha_ersar"], hoje.isoformat()])


def contagens(linhas: list) -> dict:
    """{'concelho': Counter, 'agua': Counter, 'saneamento': Counter, 'residuos': Counter}."""
    out = {"concelho": Counter(l["estado"] for l in linhas)}
    for s in SERVICOS:
        out[s] = Counter(l["estados"][s] for l in linhas)
    return out


def resumo_por_distrito(linhas: list) -> list:
    por = defaultdict(Counter)
    for l in linhas:
        por[l["distrito"]][l["estado"]] += 1
    return sorted(por.items(), key=lambda kv: _chave(kv[0]))


def tabela_dos_estados() -> list:
    L = ["| Estado | Critério |", "| :--- | :--- |"]
    for k in ROTULO_ESTADO:
        L.append(f"| {ICONE[k]} {ROTULO_ESTADO[k]} | {CRITERIO[k]} |")
    return L


def tabela_das_contagens(c: dict) -> list:
    L = ["| Estado | Concelhos | Água | Saneamento | Resíduos |", "| :--- | ---: | ---: | ---: | ---: |"]
    for k in ROTULO_ESTADO:
        L.append(f"| {ICONE[k]} {ROTULO_ESTADO[k]} | {c['concelho'][k]} | {c['agua'][k]} | {c['saneamento'][k]} | {c['residuos'][k]} |")
    n = sum(c["concelho"].values())
    L.append(f"| **total** | **{n}** | **{n}** | **{n}** | **{n}** |")
    return L


def tabela_por_distrito(linhas: list) -> list:
    L = ["| Distrito | 🟢 verde | 🟡 amarelo | ⚪ cinza | Total |", "| :--- | ---: | ---: | ---: | ---: |"]
    for dist, cc in resumo_por_distrito(linhas):
        L.append(f"| {dist} | {cc['verde']} | {cc['amarelo']} | {cc['cinza']} | {sum(cc.values())} |")
    return L


def escrever_md(linhas: list, hoje: date) -> None:
    c = contagens(linhas)
    L = ["# Confiança dos valores tarifários por concelho (Triton IBE, Portugal)", "",
         f"Gerado em {hoje.isoformat()} por `tarifas_portugal/procedencia_pt.py`. Não edite à mão.", "",
         f"{len(linhas)} concelhos: 278 de Portugal continental, mais Funchal e Ponta Delgada. Só o utilizador "
         "doméstico. Três estados, por concelho e por serviço (água, saneamento, resíduos). O estado do concelho é verde se "
         "os três serviços forem verdes, cinza se forem todos cinza, e amarelo nos restantes casos. Formato aberto: "
         "`CONFIANCA_POR_CONCELHO.csv`.", "",
         "## Estados e critérios", ""] + tabela_dos_estados() + [""]
    L += ["## Contagem", ""] + tabela_das_contagens(c) + [""]
    L += ["## Por distrito", ""] + tabela_por_distrito(linhas) + [""]
    L += ["## Por concelho", "",
          "| Concelho | Entidade | Estado | Água | Saneamento | Resíduos | Vigência | O que falta | Documento |",
          "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |"]
    for l in linhas:
        url = (l["url_documento"] or l["url_ficha_ersar"]).split(" | ")[0]
        rot = "documento" if l["url_documento"] else ("ficha ERSAR" if url else "—")
        lig = f"[{rot}]({url})" if url else "—"
        e = l["estados"]
        L.append(f"| {l['concelho']} | {l['entidade']} | {ICONE[l['estado']]} {l['estado']} | {ICONE[e['agua']]} | "
                 f"{ICONE[e['saneamento']]} | {ICONE[e['residuos']]} | {l['vigencia']} | "
                 f"{l['o_que_falta'].replace(' | ', '; ')} | {lig} |")
    with open(MD, "w", encoding="utf-8", newline="") as f:
        f.write(NL.join(L) + NL)


# --------------------------------------------------------------------------------------------
# texto do manual (apêndice D), em português europeu
# --------------------------------------------------------------------------------------------
def texto_manual(linhas: list | None = None, hoje: date | None = None) -> list:
    """Linhas Markdown da secção «Confiança dos valores tarifários por concelho» do apêndice D."""
    hoje = hoje or date.today()
    linhas = linhas or avaliar(hoje)
    c = contagens(linhas)
    n = len(linhas)
    transcritos = [l for l in linhas if l["transcrito"]]
    L = [
        "## Confiança dos valores tarifários por concelho",
        "",
        f"Nem todos os tarifários valem o mesmo. O Triton IBE traz transcritos {len(transcritos)} dos {n} concelhos que "
        "cobre (278 de Portugal continental, mais Funchal e Ponta Delgada), e para os restantes o utilizador introduz o "
        "tarifário do projeto. Para cada concelho, e para cada um dos três serviços (água, saneamento e resíduos "
        "urbanos), o programa de manutenção atribui um de três estados, com o motivo escrito.",
        "",
        "Em Portugal a água, o saneamento de águas residuais e os resíduos urbanos são muitas vezes de entidades "
        "diferentes (em Lisboa, a EPAL fornece a água e a Câmara trata do saneamento e dos resíduos; no Porto, a Águas e "
        "Energia do Porto trata da água e do saneamento, e a EMAP dos resíduos). Por isso o estado é dado por serviço, "
        "cada um com a sua entidade e o seu documento. O saneamento cobra-se por escalões sobre uma fração do volume de "
        "água, o IVA vem de cada documento, a taxa de recursos hídricos (TRH) é uma parcela própria e a tarifa fixa "
        "depende do calibre do contador. Só se avalia o utilizador doméstico.",
        "",
        "### A escala e os critérios",
        "",
        "<!-- tabela: Estados de confiança dos valores tarifários e respetivos critérios -->",
    ] + tabela_dos_estados() + [
        "",
        "O estado do concelho é verde quando os três serviços são verdes, cinza quando são todos cinza, e amarelo nos "
        "restantes casos. **Não há verde sem verificação independente**: a transcrição feita por quem leu o documento prova "
        "a aritmética, não a leitura. Uma **pendência** é uma hipótese que o documento não resolve (o IVA aplicado, um "
        "valor que não vem impresso, a leitura de uma tabela); cada uma traz o efeito estimado na conta de 10 m³ e, acima "
        "de 1 %, impede o verde.",
        "",
        f"### Situação em {hoje.strftime('%d/%m/%Y')}",
        "",
        "<!-- tabela: Concelhos e serviços por estado de confiança dos valores tarifários -->",
    ] + tabela_das_contagens(c) + [
        "",
        "Por distrito (e região autónoma), com o estado do concelho:",
        "",
        "<!-- tabela: Concelhos por distrito e estado de confiança dos valores tarifários -->",
    ] + tabela_por_distrito(linhas) + [
        "",
        "A tabela concelho a concelho (entidade gestora de cada serviço, estado de cada serviço, vigência, o que falta e a "
        "ligação ao documento ou à ficha tarifária da ERSAR) acompanha o programa em "
        "`tarifas_portugal/CONFIANCA_POR_CONCELHO.csv`, em formato aberto.",
        "",
        "Os concelhos transcritos:",
        "",
        "<!-- tabela: Concelhos com tarifário transcrito e o estado de cada serviço -->",
        "| Concelho | Água | Saneamento | Resíduos | O que falta |",
        "| :--- | :--- | :--- | :--- | :--- |",
    ]
    for l in transcritos:
        e = l["estados"]
        L.append(f"| {l['concelho']} | {ICONE[e['agua']]} | {ICONE[e['saneamento']]} | {ICONE[e['residuos']]} | "
                 f"{l['o_que_falta'].replace(' | ', '; ')} |")
    L += [
        "",
        "### Como ler o estado",
        "",
        "1. Procure o concelho do projeto. A entidade gestora de cada serviço vem da ficha tarifária da ERSAR (e, no "
        "Funchal e em Ponta Delgada, do próprio documento); quando nenhuma fonte a indica, a tabela diz «a identificar».",
        "2. Leia o estado de cada serviço, não só o do concelho: um concelho amarelo pode ter a água documentada e os "
        "resíduos sem dado.",
        "3. Leia «o que falta». É a lista do que o utilizador deve verificar antes de apoiar uma conclusão económica.",
        "4. Confira a vigência. Os tarifários portugueses mudam em regra todos os anos, em janeiro ou nos primeiros "
        "meses, e um tarifário com mais de 12 meses pode já ter sido substituído.",
        "",
        "### O que fazer em concelhos amarelos e cinzentos",
        "",
        "- **Cinza.** Obtenha o tarifário em vigor da entidade gestora de cada serviço (a ficha da ERSAR indica a entidade "
        "e o ano), introduza os escalões, as tarifas fixas, o IVA e a regra do saneamento na janela de tarifário "
        "(etapa 5) e confira a fatura que o programa calcula com uma fatura real do edifício.",
        "- **Amarelo.** O valor tem documento oficial por trás, mas não foi verificado de modo independente. Confira "
        "a conta com uma fatura real e, se o programa lhe der um valor diferente por mais de 0,05 €, use o da fatura.",
        "- **Em qualquer estado diferente de verde.** Declare no estudo a entidade gestora, a data de vigência e o estado "
        "de confiança, e acompanhe o resultado económico de uma análise de sensibilidade à tarifa.",
        "",
    ]
    return L


def main() -> None:
    hoje = date.today()
    linhas = avaliar(hoje)
    escrever_csv(linhas, hoje)
    escrever_md(linhas, hoje)
    c = contagens(linhas)
    print(f"{len(linhas)} concelhos: " + ", ".join(f"{k} {c['concelho'][k]}" for k in ROTULO_ESTADO))
    for s in SERVICOS:
        print(f"  {ROTULO[s]}: " + ", ".join(f"{k} {c[s][k]}" for k in ROTULO_ESTADO))
    print("escrito: " + os.path.relpath(CSV, RAIZ) + " e " + os.path.relpath(MD, RAIZ))


if __name__ == "__main__":
    main()
