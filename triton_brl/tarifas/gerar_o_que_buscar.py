# -*- coding: utf-8 -*-
"""O que buscar para completar a base tarifária: uma busca por cartão, pronta no Google.

A lista de coleta antiga partia da URL que a base tinha para cada prestador, e essa URL
muitas vezes é uma página-índice da agência ou nem é do prestador certo. Aqui o ponto de
partida é a cidade: cada cartão diz por que ela está na lista (dado ruim, sem documento,
documento antigo), o que já veio e não serviu, e abre a busca pronta no Google.

Um cartão por cidade quando o prestador atende um município só; um cartão por prestador
quando uma resolução cobre vários (companhias estaduais). Ordem: primeiro o **lote** (os
municípios sem documento algum), depois o documento que falta para corrigir um dado
ruim, por fim os municípios de prestador a confirmar. Documento antigo não entra: desde
05/10/2026 o programa reajusta a tabela a partir da vigência
(triton/core/vigencia_tarifaria.py), e o autor decidiu manter as tabelas mais recentes
que conseguiu.

Uso:
    python tarifas/gerar_o_que_buscar.py

Saída: tarifas/o_que_buscar.html, autocontida (abre direto do disco). É regerada também
por gerar_lista_de_coleta.py, isto é, a cada registro e a cada transcrição aplicada.
"""

from __future__ import annotations

import html
import json
import os
import re
import sys
from collections import defaultdict
from datetime import date
from urllib.parse import quote_plus

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
for _p in (AQUI, os.path.join(RAIZ, "manual")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import procedencia as P  # noqa: E402
import registro_de_fontes as R  # noqa: E402
import tabela_de_faixas as T  # noqa: E402

SAIDA = os.path.join(AQUI, "o_que_buscar.html")
PENDENTE = ("ruim", "sem_documento", "a_confirmar")
GRUPO = {"sem_documento": "lote", "ruim": "corrigir", "a_confirmar": "confirmar"}
ORDEM_GRUPO = {"lote": 0, "corrigir": 1, "confirmar": 2}
#: Nomes de prestador que não ajudam numa busca.
#: «Dado ruim» que não se resolve com documento: a forma de cobrança é que o banco não
#: representa. Não é busca, é programa.
LIMITACAO = re.compile(r"não representa|forma direta", re.I)
GENERICOS = re.compile(r"prestador municipal|prestação local|servi[çc]o local|validar|confirmar", re.I)


def _google(termos: str) -> str:
    return "https://www.google.com/search?q=" + quote_plus(termos)


def _nome_limpo(prestador: str) -> str:
    """«SAAE / prestação municipal de Manacapuru – confirmar» → «SAAE»."""
    nome = re.split(r"\s+[–/-]\s+|\s*/\s*", prestador or "")[0].strip()
    return "" if not nome or GENERICOS.search(prestador) and len(nome) < 6 else nome


def dados() -> dict:
    cidades = T.carregar()
    reg = R.carregar()
    ano = date.today().year
    consultados = defaultdict(list)
    for i in reg["itens"]:
        if i["situacao"] == "consultado" and str(i.get("uso", "")).startswith("consultado:"):
            consultados[i["prestador"]].append(i["uso"].split(":", 1)[1].strip())
    # Tudo o que já veio, por prestador e por município citado (auditar_cobertura.py, leitura
    # do documento inteiro): o cartão mostra, para não se buscar de novo o que já foi mandado.
    cobertura, usados = {}, {}
    caminho_cob = os.path.join(AQUI, "transcricoes", "cobertura.json")
    if os.path.exists(caminho_cob):
        _cob = json.load(open(caminho_cob, encoding="utf-8"))
        cobertura = _cob.get("pendentes_com_documento", {})
        usados = {d["id"]: d["transcritos"] for d in _cob.get("documentos", [])}
    itens = {i["id"]: i for i in reg["itens"]}

    def recebidos(prestador, lista):
        ids = {i["id"] for i in reg["itens"] if i["situacao"] != "descartado" and P._mesmo(i["prestador"], prestador)}
        for d in lista:
            ids |= set(cobertura.get(f"{d['uf']} - {d['municipio']}", {}).get("documentos", []))
        out = []
        for k in sorted(ids):
            i = itens[k]
            uso = str(i.get("uso", ""))
            if i["situacao"] == "transcrito":
                para = [m.split(" - ", 1)[1] for m in usados.get(k, [])]
                txt = ("já usado para " + ", ".join(para[:6]) + (f" e mais {len(para) - 6}" if len(para) > 6 else "")
                       + "; não traz a tabela dos municípios deste cartão") if para else "já usado"
            elif uso.startswith("consultado:"):
                txt = "não bastou: " + uso.split(":", 1)[1].strip()
            else:
                txt = i["situacao"]
            out.append({"item": k, "arquivo": i["arquivo"], "recebido": i.get("recebido_em", ""), "txt": txt})
        return out

    por_prestador = defaultdict(list)
    for d in cidades.values():
        por_prestador[d.get("prestador_saneamento") or "—"].append(d)

    cartoes, nao_e_busca = [], []
    for prestador, lista in por_prestador.items():
        pend = [(d, P.classe(d)) for d in lista]
        pend = [(d, c) for d, c in pend if c in PENDENTE]
        limitacao = [d for d, c in pend if c == "ruim" and LIMITACAO.search(str(d.get("motivo_dado_ruim", "")))]
        if limitacao:
            nao_e_busca.append({"titulo": prestador, "municipios": [d["municipio"] for d in limitacao],
                                "motivo": limitacao[0]["motivo_dado_ruim"]})
            pend = [(d, c) for d, c in pend if d not in limitacao]
        if not pend:
            continue
        nome = _nome_limpo(prestador)
        porque = []
        for d, c in sorted(pend, key=lambda x: x[0]["municipio"]):
            if c == "ruim":
                motivo = d.get("motivo_dado_ruim") or str(d.get("confianca_grau", "")).split("—", 1)[-1].strip()
                txt = f"dado ruim: {motivo}"
            elif c == "a_confirmar":
                txt = "prestador a confirmar: quem atende o município, e com que tabela"
            else:
                txt = "sem documento oficial guardado" + (
                    f"; a base diz «{d.get('vigencia_saneamento')}»" if d.get("vigencia_saneamento") else "")
            igual = next((p for p in porque if p["txt"] == txt), None)
            if igual:
                igual["m"] += ", " + d["municipio"]
            else:
                porque.append({"m": d["municipio"], "uf": d["uf"], "cl": c, "txt": txt})
        grupo = min((GRUPO[c] for _d, c in pend), key=ORDEM_GRUPO.get)
        so_renovar = False
        if len(lista) == 1:
            d = lista[0]
            titulo = f"{d['municipio']} ({d['uf']})"
            buscas = [("Pesquisar no Google",
                       _google(f"tabela tarifária água esgoto {d['municipio']} {d['uf']} {ano}"
                               + (" reajuste" if so_renovar else "")))]
            if nome:
                cidade = "" if d["municipio"].lower() in nome.lower() else f" {d['municipio']}"
                buscas.append((f"Buscar «{nome}»", _google(f"{nome}{cidade} tarifas água esgoto {ano}")))
            sub = prestador
        else:
            titulo = prestador
            ufs = sorted({d["uf"] for d in lista})
            buscas = [("Pesquisar no Google",
                       _google(f"{nome or prestador} tabela tarifária {ano} resolução" + (" reajuste" if so_renovar else "")))]
            buscas.append(("Buscar a lista de municípios",
                           _google(f"{nome or prestador} resolução tarifária {ano} municípios atendidos {' '.join(ufs)}")))
            sub = f"{len(pend)} de {len(lista)} municípios pendentes · {', '.join(ufs)}"
        # O que já veio cita o documento que falta («Decreto nº 105, de 01/09/2026»): busca direta.
        for j in consultados.get(prestador, []):
            m = re.search(r"(Decreto|Resolução|Deliberação|Lei)( Municipal)?( n[º°o.]*)? ?[\d.]+(/\d{2,4})?(, de \d{2}/\d{2}/\d{4})?", j)
            if m:
                lugar = lista[0]["municipio"] if len(lista) == 1 else (nome or prestador)
                buscas.append((f"Buscar o {m.group(1).lower()} citado", _google(f"{m.group(0)} {lugar} tarifas água")))
                break
        cartoes.append({
            "id": prestador,
            "titulo": titulo,
            "sub": sub,
            "ufs": sorted({d["uf"] for d in lista}),
            "n": len(pend),
            "grupo": grupo,
            "porque": porque,
            "ja_veio": recebidos(prestador, [d for d, _c in pend]),
            "buscas": [{"rotulo": r, "url": u} for r, u in buscas],
            # No grupo «corrigir» o link da base é justamente o suspeito (já apontou para outro prestador).
            "link_base": "" if grupo == "corrigir" else next((d.get("fonte_url") for d in lista if d.get("fonte_url")), ""),
            "varios": len(lista) > 1,
        })
    cartoes.sort(key=lambda c: (ORDEM_GRUPO[c["grupo"]], -c["n"], c["titulo"].lower()))
    antigos = sum(1 for d in cidades.values() if P.classe(d) == "a_renovar")
    return {"gerado_em": date.today().isoformat(), "ano": ano, "cartoes": cartoes, "nao_e_busca": nao_e_busca,
            "antigos": antigos}


MODELO = r"""<!doctype html>
<html lang="pt-BR">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>O que buscar</title>
<style>
:root {
  --bg: #f3f6f5; --surface: #fff; --fg: #14211e; --muted: #56655f; --line: #d3ddd9;
  --accent: #0b6e64; --accent-ink: #fff; --bad: #a8432f; --bad-bg: #f8e6e1;
  --warn: #8a5a00; --warn-bg: #f8edd2; --old: #3d5a80; --old-bg: #e3ebf6; --done-bg: #eef3f1;
  --body: "IBM Plex Sans", system-ui, -apple-system, "Segoe UI", sans-serif;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg: #0f1614; --surface: #17211e; --fg: #e3ebe8; --muted: #9db0a9; --line: #2c3a36;
  --accent: #4cc2b2; --accent-ink: #062723; --bad: #f0957f; --bad-bg: #3a201a;
  --warn: #e9bb5e; --warn-bg: #352a12; --old: #9fb8d8; --old-bg: #1c2633; --done-bg: #131b19; color-scheme: dark; } }
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--fg); font: 15px/1.5 var(--body); }
.wrap { max-width: 980px; margin: 0 auto; padding: 24px 16px 64px; }
h1 { font-size: 26px; margin: 0 0 4px; }
.lead { color: var(--muted); margin: 0 0 16px; max-width: 70ch; }
.placar { display: flex; flex-wrap: wrap; gap: 10px; margin: 0 0 16px; }
.placar div { background: var(--surface); border: 1px solid var(--line); border-radius: 10px; padding: 10px 14px; }
.placar b { display: block; font-size: 22px; }
.placar span { color: var(--muted); font-size: 13px; }
.filtros { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; margin-bottom: 8px; position: sticky; top: 0;
  background: var(--bg); padding: 8px 0; z-index: 2; }
.filtros input[type=search] { flex: 1 1 240px; }
input, select, button { font: inherit; color: inherit; }
input[type=search], select { padding: 7px 10px; border: 1px solid var(--line); border-radius: 8px; background: var(--surface); }
h2 { font-size: 18px; margin: 28px 0 4px; }
h2 small { color: var(--muted); font-weight: normal; font-size: 14px; }
.nota { color: var(--muted); margin: 0 0 10px; font-size: 14px; }
ol { list-style: none; padding: 0; margin: 0; display: grid; gap: 10px; }
.cartao { background: var(--surface); border: 1px solid var(--line); border-left: 5px solid var(--line); border-radius: 10px; padding: 12px 14px; }
.cartao.corrigir { border-left-color: var(--bad); } .cartao.lote { border-left-color: var(--warn); } .cartao.confirmar { border-left-color: var(--old); }
.cartao.aberto .titulo::after { content: " · aberto"; color: var(--muted); font-weight: normal; font-size: 13px; }
.proxima { margin: 6px 0 12px; }
button.principal { padding: 8px 14px; border-radius: 8px; border: 1px solid var(--accent); background: var(--accent); color: var(--accent-ink); cursor: pointer; }
.cartao.salvo { background: var(--done-bg); opacity: .75; }
.topo { display: flex; flex-wrap: wrap; gap: 8px 14px; align-items: baseline; justify-content: space-between; }
.titulo { font-weight: 600; font-size: 16px; }
.sub { color: var(--muted); font-size: 13px; }
.acoes { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin-top: 8px; }
a.botao { display: inline-block; padding: 6px 12px; border-radius: 8px; border: 1px solid var(--line); text-decoration: none; color: var(--fg); }
a.botao.principal { background: var(--accent); color: var(--accent-ink); border-color: var(--accent); }
label.salvei { display: inline-flex; gap: 6px; align-items: center; margin-left: auto; cursor: pointer; }
ul.porque { margin: 8px 0 0; padding-left: 18px; font-size: 14px; }
ul.porque li.ruim { color: var(--bad); }
.ja { margin-top: 6px; font-size: 13px; background: var(--warn-bg); color: var(--warn); border-radius: 6px; padding: 6px 8px; }
.base { font-size: 12px; color: var(--muted); }
.base a { color: inherit; }
.vazio { color: var(--muted); padding: 8px 0; }
footer { margin-top: 32px; color: var(--muted); font-size: 13px; }
code { font-size: 13px; }
</style>
<div class="wrap">
  <h1>O que buscar</h1>
  <p class="lead">Cada cartão é uma busca. Abra o Google pelo botão, encontre a resolução, o decreto ou a
    página de tarifas vigente, salve o PDF (ou a página completa) em <code>tarifas/entrada/</code>, com qualquer
    nome, e marque «Já salvei». O resto o processamento faz.</p>
  <div class="placar" id="placar"></div>
  <div class="filtros">
    <input type="search" id="q" placeholder="Cidade ou prestador" aria-label="Buscar cidade ou prestador">
    <select id="uf" aria-label="Estado"><option value="">Todos os estados</option></select>
    <label><input type="checkbox" id="esconder"> Esconder os que já salvei</label>
  </div>
  <section><h2>1. Lote: municípios sem documento <small id="c-lote"></small></h2>
    <p class="nota">A tarifa destes municípios não tem documento oficial guardado. Vá de cartão em cartão: o botão
      abaixo abre a próxima busca ainda não aberta nem salva. Para companhias de vários municípios, vale um documento
      que liste os municípios ou que se declare a tabela única da companhia.</p>
    <p class="proxima"><button type="button" class="principal" id="proxima">Abrir a próxima busca do lote</button></p>
    <ol id="l-lote"></ol></section>
  <section><h2>2. O documento que falta para corrigir <small id="c-corrigir"></small></h2>
    <p class="nota">Um documento já recebido mostra que a tarifa da base está errada, mas não trouxe tudo: falta a
      tabela inteira, a lei que dá a fórmula ou a tabela de expoentes.</p>
    <ol id="l-corrigir"></ol></section>
  <section><h2>3. Prestador a confirmar <small id="c-confirmar"></small></h2>
    <p class="nota">Não se sabe com certeza quem atende o município. Comece pela prefeitura: a página de saneamento
      ou o contrato de concessão dizem o prestador, e daí se busca a tabela.</p>
    <ol id="l-confirmar"></ol></section>
  <section><h2>Não depende de busca</h2>
    <p class="nota">O documento destes já está guardado; a forma de cobrança é que o programa ainda não representa
      (ainda não suportado). Ficam marcados como dado ruim até o programa ser ajustado.</p>
    <ul id="l-nao" class="porque"></ul></section>
  <p class="nota" id="antigos"></p>
  <footer>Gerada em {{GERADO_EM}} por <code>tarifas/gerar_o_que_buscar.py</code> a partir do banco tarifário e de
    <code>tarifas/fontes/registro.json</code>. «Já salvei» fica só neste navegador; o cartão sai da lista quando o
    documento é transcrito.</footer>
</div>
<script>
(function () {
  var D = /*DADOS*/null, C = D.cartoes, CHAVE = "o-que-buscar-salvos", salvos = {};
  try { salvos = JSON.parse(localStorage.getItem(CHAVE) || "{}") || {}; } catch (e) {}
  function guardar() { try { localStorage.setItem(CHAVE, JSON.stringify(salvos)); } catch (e) {} }
  function el(t, a, f) { var n = document.createElement(t); for (var k in a || {}) { if (k === "text") n.textContent = a[k]; else n.setAttribute(k, a[k]); }
    (f || []).forEach(function (x) { if (x != null) n.appendChild(typeof x === "string" ? document.createTextNode(x) : x); }); return n; }
  function semAcento(t) { return t.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase(); }
  var ufs = {}; C.forEach(function (c) { c.ufs.forEach(function (u) { ufs[u] = 1; }); });
  Object.keys(ufs).sort().forEach(function (u) { document.getElementById("uf").appendChild(el("option", { value: u, text: u })); });
  var itens = C.map(function (c) {
    var li = el("li", { class: "cartao " + c.grupo + (salvos[c.id] ? " salvo" : "") });
    var cb = el("input", { type: "checkbox" }); cb.checked = !!salvos[c.id];
    cb.addEventListener("change", function () {
      if (cb.checked) salvos[c.id] = new Date().toISOString().slice(0, 10); else delete salvos[c.id];
      guardar(); li.classList.toggle("salvo", cb.checked); filtrar();
    });
    var acoes = el("div", { class: "acoes" });
    c.buscas.forEach(function (b, i) { acoes.appendChild(el("a", { class: "botao" + (i ? "" : " principal"), href: b.url, target: "_blank", rel: "noopener", text: b.rotulo })); });
    acoes.appendChild(el("label", { class: "salvei" }, [cb, "Já salvei"]));
    var ul = el("ul", { class: "porque" });
    c.porque.slice(0, 8).forEach(function (p) { ul.appendChild(el("li", { class: p.cl, text: (c.varios ? p.m + ": " : "") + p.txt })); });
    if (c.porque.length > 8) ul.appendChild(el("li", { text: "e mais " + (c.porque.length - 8) + " municípios na mesma situação" }));
    li.appendChild(el("div", { class: "topo" }, [el("div", null, [el("div", { class: "titulo", text: c.titulo }), el("div", { class: "sub", text: c.sub })])]));
    li.appendChild(ul);
    if (c.ja_veio.length) {
      var ja = el("div", { class: "ja" }, [el("strong", { text: "Você já mandou:" })]);
      c.ja_veio.forEach(function (j) {
        var linha = el("div", null, ["item " + j.item + " «" + j.arquivo + "»" + (j.recebido ? " (" + j.recebido + ")" : "") + " — "]);
        j.txt.split(/(https?:\/\/\S+)/).forEach(function (pedaco) {
          if (/^https?:\/\//.test(pedaco)) {
            var u = pedaco.replace(/[),.;]+$/, "");
            linha.appendChild(el("a", { href: u, target: "_blank", rel: "noopener", text: "abrir o documento citado" }));
          } else if (pedaco) linha.appendChild(document.createTextNode(pedaco));
        });
        ja.appendChild(linha);
      });
      li.appendChild(ja);
    }
    li.appendChild(acoes);
    if (c.link_base) li.appendChild(el("div", { class: "base" }, ["Link que estava na base (pode ser página-índice): ",
      el("a", { href: c.link_base, target: "_blank", rel: "noopener", text: c.link_base.replace(/^https?:\/\//, "").slice(0, 70) })]));
    li._c = c; li._t = semAcento(c.titulo + " " + c.sub + " " + c.porque.map(function (p) { return p.m; }).join(" "));
    document.getElementById("l-" + c.grupo).appendChild(li);
    return li;
  });
  var q = document.getElementById("q"), uf = document.getElementById("uf"), esc = document.getElementById("esconder");
  try { esc.checked = localStorage.getItem(CHAVE + "-esconder") === "1"; } catch (e) {}
  function filtrar() {
    var t = semAcento(q.value).trim(), u = uf.value, n = { lote: 0, corrigir: 0, confirmar: 0 };
    itens.forEach(function (li) {
      var c = li._c, ok = (!t || li._t.indexOf(t) >= 0) && (!u || c.ufs.indexOf(u) >= 0) && !(esc.checked && salvos[c.id]);
      li.hidden = !ok; if (ok) n[c.grupo]++;
    });
    ["lote", "corrigir", "confirmar"].forEach(function (g) {
      document.getElementById("c-" + g).textContent = n[g] + (n[g] === 1 ? " busca" : " buscas");
      var l = document.getElementById("l-" + g), v = l.querySelector(".vazio");
      if (!n[g] && !v) l.appendChild(el("li", { class: "vazio", text: "Nada aqui com esses filtros." }));
      if (n[g] && v) v.remove();
    });
    var feitos = C.filter(function (c) { return salvos[c.id]; }).length;
    var p = document.getElementById("placar"); p.textContent = "";
    [[C.filter(function (c) { return c.grupo === "lote"; }).length, "buscas no lote"], [C.filter(function (c) { return c.grupo === "corrigir"; }).length, "para corrigir"],
     [C.reduce(function (s, c) { return s + c.n; }, 0), "municípios pendentes"], [feitos, "já salvas por você"]]
      .forEach(function (x) { p.appendChild(el("div", null, [el("b", { text: String(x[0]) }), el("span", { text: x[1] })])); });
  }
  var ABERTOS = CHAVE + "-abertos", abertos = {};
  try { abertos = JSON.parse(localStorage.getItem(ABERTOS) || "{}") || {}; } catch (e) {}
  function marcarAberto(li) { abertos[li._c.id] = 1; li.classList.add("aberto");
    try { localStorage.setItem(ABERTOS, JSON.stringify(abertos)); } catch (e) {} }
  itens.forEach(function (li) {
    if (abertos[li._c.id]) li.classList.add("aberto");
    li.querySelectorAll("a.botao").forEach(function (a) { a.addEventListener("click", function () { marcarAberto(li); }); });
  });
  document.getElementById("proxima").addEventListener("click", function () {
    var li = itens.find(function (x) { return x._c.grupo === "lote" && !salvos[x._c.id] && !abertos[x._c.id]; });
    if (!li) { alert("Todas as buscas do lote já foram abertas ou salvas."); return; }
    window.open(li._c.buscas[0].url, "_blank", "noopener"); marcarAberto(li);
    li.scrollIntoView({ behavior: "smooth", block: "center" });
  });
  if (D.antigos) document.getElementById("antigos").textContent = D.antigos + " municípios têm documento com vigência de mais de 12 meses. "
    + "Ficam como estão: o programa reajusta a tabela a partir da vigência dela, e não é preciso buscar o reajuste.";
  (D.nao_e_busca || []).forEach(function (n) {
    document.getElementById("l-nao").appendChild(el("li", null, [el("strong", { text: n.titulo + " (" + n.municipios.join(", ") + "): " }), n.motivo]));
  });
  [q, uf].forEach(function (x) { x.addEventListener(x.tagName === "INPUT" ? "input" : "change", filtrar); });
  esc.addEventListener("change", function () { try { localStorage.setItem(CHAVE + "-esconder", esc.checked ? "1" : "0"); } catch (e) {} filtrar(); });
  filtrar();
})();
</script>
"""


def gerar(saida: str = SAIDA) -> dict:
    conteudo = dados()
    carga = json.dumps(conteudo, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    texto = MODELO.replace("/*DADOS*/null", carga).replace("{{GERADO_EM}}", html.escape(conteudo["gerado_em"]))
    with open(saida, "w", encoding="utf-8", newline="") as f:
        f.write(texto)
    return conteudo


if __name__ == "__main__":
    c = gerar()["cartoes"]
    print(f"o que buscar: {len(c)} buscas ({sum(1 for x in c if x['grupo'] == 'corrigir')} para corrigir) -> "
          f"{os.path.relpath(SAIDA, RAIZ)}")
