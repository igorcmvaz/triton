# -*- coding: utf-8 -*-
"""Consolida os ``resultados.csv`` de várias execuções de ``triton estudo`` numa só tabela (``triton estudo consolidar``).

Procura ``resultados.csv`` em uma ou mais pastas (inclusive de lotes: uma subpasta por estudo) e agrupa as linhas por
tipologia (coluna ``grupo``), caso e métrica, com mínimo, média, mediana e máximo. Escreve ``consolidado.csv`` e
``consolidado.md``. Só entram valores de casos com ``status`` igual a ``ok``; a unidade faz parte da chave do grupo, para
nunca misturar moedas ou idiomas diferentes.

Dois caminhos de leitura dão o MESMO resultado, byte a byte:

* ``duckdb`` (extra opcional ``analise``, via :mod:`triton.core._opcional`): lê todos os arquivos de uma vez e agrupa por SQL;
* alternativa em biblioteca padrão (``csv``), sem o pacote.

Os dois só leem e agrupam. Os números são lidos como texto e as estatísticas saem do mesmo código nos dois caminhos
(:func:`triton.core.estudo.estatisticas`, com a mesma limpeza de ``estudo run``: 10 algarismos significativos), a ordem
das linhas é a ordem estável por tipologia, caso e métrica, e o arquivo não leva data nem caminho da máquina.
"""

from __future__ import annotations

import csv
import io
import math
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

from triton.core import _opcional
from triton.core import estudo as E

NOME_DE_ENTRADA = "resultados.csv"
COLUNAS_OBRIGATORIAS = ("estudo_id", "caso_id", "caso", "grupo", "metrica", "rotulo", "valor", "unidade", "status")
MOTORES = ("auto", "duckdb", "csv")
CABECALHO_CSV = ["tipologia", "caso_id", "caso", "metrica", "rotulo", "unidade", "estudos", "registros", "n",
                 "minimo", "media", "mediana", "maximo"]
_ESTATISTICAS = ("minimo", "media", "mediana", "maximo")

#: (tipologia, caso_id, métrica, unidade) -> dados brutos do grupo
Chave = Tuple[str, str, str, str]
Grupos = Dict[Chave, Dict[str, Any]]


def descobrir_resultados(pastas: Sequence[Path]) -> List[Path]:
    """Os ``resultados.csv`` das pastas (e subpastas), sem repetição, em ordem estável."""
    achados: Dict[Path, str] = {}
    for pasta in pastas:
        pasta = Path(pasta)
        if not pasta.is_dir():
            raise FileNotFoundError(E._m("Pasta não encontrada: {0}", pasta.name))
        arquivos = sorted((p for p in pasta.rglob(NOME_DE_ENTRADA) if p.is_file()),
                          key=lambda p: p.relative_to(pasta).as_posix())
        if not arquivos:
            raise ValueError(E._m("nenhum resultados.csv em {0} (é a pasta de saída de «triton estudo run»?)", pasta.name))
        for p in arquivos:
            achados.setdefault(p.resolve(), p.relative_to(pasta).as_posix())
    return list(achados)


def _conferir_cabecalho(arquivo: Path) -> None:
    with open(arquivo, encoding="utf-8-sig", newline="") as f:
        cabecalho = next(csv.reader(f), [])
    faltam = [c for c in COLUNAS_OBRIGATORIAS if c not in cabecalho]
    if faltam:
        raise ValueError(E._m("{0}: faltam as colunas {1} (não é o resultados.csv de «triton estudo run»?)",
                              arquivo.parent.name, ", ".join(faltam)))


def _agrupar_csv(arquivos: Sequence[Path]) -> Grupos:
    """Leitura e agrupamento só com a biblioteca padrão."""
    grupos: Dict[Chave, Dict[str, Any]] = {}
    for arquivo in arquivos:
        with open(arquivo, encoding="utf-8-sig", newline="") as f:
            for linha in csv.DictReader(f):
                chave = (linha["grupo"], linha["caso_id"], linha["metrica"], linha["unidade"])
                g = grupos.setdefault(chave, {"casos": [], "rotulos": [], "estudos": set(), "registros": 0, "valores": []})
                g["casos"].append(linha["caso"])
                g["rotulos"].append(linha["rotulo"])
                if linha["estudo_id"]:
                    g["estudos"].add(linha["estudo_id"])
                g["registros"] += 1
                if linha["status"] == "ok" and linha["valor"] != "":
                    g["valores"].append(linha["valor"])
    return {k: {**g, "estudos": len(g["estudos"])} for k, g in grupos.items()}


_SQL = """
SELECT COALESCE(grupo, ''), COALESCE(caso_id, ''), COALESCE(metrica, ''), COALESCE(unidade, ''),
       min(caso), min(rotulo), count(DISTINCT estudo_id), count(*),
       list(valor) FILTER (WHERE status = 'ok' AND valor IS NOT NULL)
FROM read_csv(?, header = true, delim = ',', quote = '"', escape = '"', all_varchar = true, union_by_name = true)
GROUP BY 1, 2, 3, 4
"""


def _agrupar_duckdb(arquivos: Sequence[Path], duckdb: Any) -> Grupos:
    """Leitura e agrupamento por SQL no duckdb (os valores continuam texto; a conta fica fora, igual nos dois caminhos)."""
    con = duckdb.connect(":memory:")
    try:
        linhas = con.execute(_SQL, [[str(a) for a in arquivos]]).fetchall()
    finally:
        con.close()
    return {(g, c, m, u): {"casos": [caso or ""], "rotulos": [rotulo or ""], "estudos": int(estudos),
                           "registros": int(registros), "valores": list(valores or [])}
            for g, c, m, u, caso, rotulo, estudos, registros, valores in linhas}


def agrupar(arquivos: Sequence[Path], motor: str = "auto") -> Tuple[Grupos, str]:
    """Os grupos brutos e o nome do caminho usado (``duckdb`` ou ``csv``). ``motor="duckdb"`` exige o extra ``analise``."""
    if motor not in MOTORES:
        raise ValueError(E._m("motor desconhecido: {0}. Use {1}.", motor, ", ".join(MOTORES)))
    for a in arquivos:
        _conferir_cabecalho(a)
    if motor != "csv" and (motor == "duckdb" or _opcional.disponivel("duckdb")):
        try:
            duckdb = _opcional.importar("duckdb", "analise", E._m("consolidar resultados por SQL"))
        except _opcional.PacoteOpcionalAusente as erro:
            raise ValueError(str(erro)) from erro
        return _agrupar_duckdb(arquivos, duckdb), "duckdb"
    return _agrupar_csv(arquivos), "csv"


def _primeiro(textos: Sequence[str]) -> str:
    """O menor texto não vazio (ordem de pontos de código, igual à do duckdb em UTF-8); vazio se não houver."""
    return min((t for t in textos if t), default="")


def linhas_do_consolidado(grupos: Grupos) -> List[Dict[str, Any]]:
    """Uma linha por grupo, ordenada por tipologia, caso, métrica e unidade, com as estatísticas já limpas."""
    saida: List[Dict[str, Any]] = []
    for chave in sorted(grupos):
        g = grupos[chave]
        valores = []
        for bruto in g["valores"]:
            try:
                v = float(bruto)
            except ValueError:
                continue
            if math.isfinite(v):
                valores.append(v)
        valores.sort()
        est = E.estatisticas(valores)
        tip, caso_id, metrica, unidade = chave
        saida.append({"tipologia": tip, "caso_id": caso_id, "caso": _primeiro(g["casos"]), "metrica": metrica,
                      "rotulo": _primeiro(g["rotulos"]), "unidade": unidade, "estudos": g["estudos"],
                      "registros": g["registros"], "n": est["n"], **{k: E._num_limpo(est[k]) for k in _ESTATISTICAS}})
    return saida


def consolidado_csv(linhas: Sequence[Dict[str, Any]]) -> str:
    """O CSV: ponto decimal e ``repr`` do número limpo, como o ``resultados.csv`` de ``estudo run``."""
    buf = io.StringIO(newline="")
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(CABECALHO_CSV)
    for L in linhas:
        w.writerow([("" if L[c] is None else repr(L[c])) if c in _ESTATISTICAS else L[c] for c in CABECALHO_CSV])
    return buf.getvalue()


def consolidado_md(linhas: Sequence[Dict[str, Any]], n_arquivos: int, idioma: str) -> str:
    """A tabela em Markdown, com os números no formato do idioma e as casas decimais padrão de cada métrica."""
    cab = [E._txt("tipologia", idioma), E._txt("caso", idioma), E._txt("metrica", idioma), E._txt("n", idioma),
           E._txt("minimo", idioma), E._txt("media", idioma), E._txt("mediana", idioma), E._txt("maximo", idioma)]
    partes = [f"**{E._txt('consolidado', idioma)}** — {E._txt('consolidado_faixa', idioma)}", "",
              E._txt("consolidado_fontes", idioma, n_arquivos, len(linhas)), "",
              "| " + " | ".join(E._md_escape(c) for c in cab) + " |", "| :--- | :--- | :--- | ---: | ---: | ---: | ---: | ---: |"]
    for L in linhas:
        casas = E.METRICAS[L["metrica"]]["casas"] if L["metrica"] in E.METRICAS else 2
        f = lambda v: "—" if v is None else (E.formatar_numero(v, casas, idioma, True) or "—")
        metrica = L["rotulo"] or L["metrica"]
        if L["unidade"]:
            metrica += f" ({L['unidade']})"
        celulas = [L["tipologia"], L["caso"] or L["caso_id"], metrica, str(L["n"]),
                   f(L["minimo"]), f(L["media"]), f(L["mediana"]), f(L["maximo"])]
        partes.append("| " + " | ".join(E._md_escape(c) for c in celulas) + " |")
    return "\n".join(partes) + "\n"


def consolidar(pastas: Sequence[Path], saida: Path, idioma: Optional[str] = None, motor: str = "auto"
               ) -> Tuple[List[str], int, int, str]:
    """Consolida e grava ``consolidado.csv`` e ``consolidado.md``. Devolve (arquivos, nº de resultados.csv, nº de grupos, motor)."""
    lingua = E.resolver_idioma(idioma)
    arquivos = descobrir_resultados(pastas)
    grupos, usado = agrupar(arquivos, motor)
    linhas = linhas_do_consolidado(grupos)
    saida = Path(saida)
    E._escrever(saida / "consolidado.csv", consolidado_csv(linhas))
    E._escrever(saida / "consolidado.md", consolidado_md(linhas, len(arquivos), lingua))
    return ["consolidado.csv", "consolidado.md"], len(arquivos), len(linhas), usado
