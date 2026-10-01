"""Exportar tudo: uma planilha com tudo o que o estudo considerou.

A planilha de dados (`simulation_excel_exporter.py`) mostra resultados escolhidos
para leitura. Esta aqui existe para **auditoria**: o projetista precisa conferir,
item por item, o que entrou em cada conta — premissas, tarifa, tratamento, ciclo de
vida, economia e o arranjo 3D — sem depender de que alguém tenha lembrado de
colocar o campo numa tela.

Por isso as abas de auditoria não são curadas: percorrem **todos** os campos dos
objetos que o programa usou (a configuração do projeto e os resultados da
simulação, da análise econômica e da ambiental), com o valor exatamente como está
na memória. Um campo novo no programa aparece aqui sem que ninguém precise se
lembrar dele. As seis abas da planilha de dados vêm junto, para que o arquivo seja
o único a guardar.
"""

from __future__ import annotations

import ast
import dataclasses
import datetime as _dt
import inspect
import json
import math
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

from netuno.core.simulation_excel_exporter import export_simulation_to_excel

#: Sequências com mais itens que isto viram aba própria em vez de célula.
_SEQUENCIA_LONGA = 12
_LIMITE_DE_LINHAS = 1_048_000
_VERDE = "087F6B"


# ── leitura genérica dos objetos ────────────────────────────────────────────

def _campos(obj: Any) -> List[Tuple[str, Any]]:
    """Pares (nome, valor) de um dataclass, dict ou objeto comum."""
    if obj is None:
        return []
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        return [(f.name, getattr(obj, f.name)) for f in dataclasses.fields(obj)]
    if isinstance(obj, dict):
        return [(str(k), v) for k, v in obj.items()]
    if hasattr(obj, "__dict__"):
        return [(k, v) for k, v in vars(obj).items() if not k.startswith("_")]
    return [("valor", obj)]


def _escalar(valor: Any) -> bool:
    return valor is None or isinstance(valor, (bool, int, float, str, _dt.date))


def _texto_da_celula(valor: Any) -> Any:
    """Valor que o Excel aceita, sem perder informação."""
    if valor is None:
        return ""
    if isinstance(valor, bool):
        return "sim" if valor else "não"
    if isinstance(valor, float):
        return valor if math.isfinite(valor) else str(valor)
    if isinstance(valor, (int, str)):
        return valor
    if isinstance(valor, _dt.datetime):
        return valor.isoformat(sep=" ", timespec="seconds")
    if isinstance(valor, _dt.date):
        return valor.isoformat()
    try:
        import numpy as np  # noqa: WPS433 — opcional, só para converter

        if isinstance(valor, np.generic):
            return _texto_da_celula(valor.item())
        if isinstance(valor, np.ndarray):
            valor = valor.tolist()
    except ImportError:  # pragma: no cover
        pass
    try:
        return json.dumps(valor, ensure_ascii=False, default=str)
    except (TypeError, ValueError):
        return str(valor)


def _sequencia(valor: Any) -> Optional[list]:
    """A lista por trás do valor, se ele for uma sequência (lista, tupla, array, série)."""
    if isinstance(valor, (list, tuple)):
        return list(valor)
    try:
        import numpy as np

        if isinstance(valor, np.ndarray):
            return valor.tolist()
    except ImportError:  # pragma: no cover
        pass
    if hasattr(valor, "tolist") and hasattr(valor, "__len__") and not isinstance(valor, (str, bytes, dict)):
        try:
            return list(valor.tolist())
        except Exception:
            return None
    return None


def descricoes_da_configuracao() -> Dict[str, str]:
    """Comentário de cada campo de ``NetunoConfig``, lido do próprio código.

    No executável congelado o código-fonte pode não estar disponível; nesse caso a
    coluna de descrição sai vazia e o resto da planilha não muda.
    """
    try:
        from netuno.core import parser as modulo

        fonte = inspect.getsource(modulo)
    except (OSError, TypeError):
        return {}
    linhas = fonte.splitlines()
    saida: Dict[str, str] = {}
    for no in ast.walk(ast.parse(fonte)):
        if isinstance(no, ast.ClassDef) and no.name == "NetunoConfig":
            for item in no.body:
                if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                    achado = re.search(r"#\s*(.+)$", linhas[item.lineno - 1])
                    if achado:
                        saida[item.target.id] = achado.group(1).strip()
    return saida


# ── escrita ─────────────────────────────────────────────────────────────────

def _nome_de_aba(wb, desejado: str) -> str:
    base = re.sub(r"[\[\]\*\?/\\:]", "_", desejado)[:31]
    nome, i = base, 2
    while nome in wb.sheetnames:
        sufixo = f"_{i}"
        nome = base[: 31 - len(sufixo)] + sufixo
        i += 1
    return nome


def _cabecalho(ws, colunas: Iterable[str]) -> None:
    ws.append(list(colunas))
    for celula in ws[ws.max_row]:
        celula.font = Font(bold=True, color="FFFFFF")
        celula.fill = PatternFill(start_color=_VERDE, end_color=_VERDE, fill_type="solid")
        celula.alignment = Alignment(vertical="center", wrap_text=True)
    if ws.max_row == 1:
        ws.freeze_panes = "A2"  # só o primeiro cabeçalho; referência, sem criar célula


def _larguras(ws, maximo: int = 70) -> None:
    for coluna in ws.columns:
        largura = max((len(str(c.value)) for c in coluna[:400] if c.value is not None), default=8)
        ws.column_dimensions[get_column_letter(coluna[0].column)].width = min(maximo, max(10, largura + 2))


def _aba_de_tabela(wb, titulo: str, linhas: list) -> Optional[str]:
    """Uma lista de registros (dataclasses, dicts ou valores) como tabela."""
    if not linhas:
        return None
    ws = wb.create_sheet(_nome_de_aba(wb, titulo))
    registros = [dict(_campos(l)) if not _escalar(l) and _sequencia(l) is None else {"valor": l} for l in linhas]
    if all(_sequencia(l) is not None for l in linhas):
        registros = [{f"c{i + 1}": v for i, v in enumerate(_sequencia(l))} for l in linhas]
    colunas: List[str] = []
    for r in registros:
        for k in r:
            if k not in colunas:
                colunas.append(k)
    _cabecalho(ws, ["#"] + colunas)
    for i, r in enumerate(registros[:_LIMITE_DE_LINHAS], start=1):
        ws.append([i] + [_texto_da_celula(r.get(c)) for c in colunas])
    _larguras(ws)
    return ws.title


def _aba_de_campos(wb, titulo: str, objeto: Any, descricoes: Optional[Dict[str, str]] = None,
                   origem: str = "") -> List[str]:
    """Todos os campos de um objeto, um por linha; sequências longas viram abas."""
    campos = _campos(objeto)
    if not campos:
        return []
    ws = wb.create_sheet(_nome_de_aba(wb, titulo))
    colunas = ["Campo", "Valor", "Tipo"] + (["Descrição (do código)"] if descricoes is not None else [])
    _cabecalho(ws, colunas)
    criadas = [ws.title]
    for nome, valor in campos:
        seq = _sequencia(valor)
        tipo = type(valor).__name__
        registros = seq is not None and any(not _escalar(x) for x in seq)
        if seq is not None and seq and (len(seq) > _SEQUENCIA_LONGA or registros):
            aba = _aba_de_tabela(wb, f"{titulo[:14]}·{nome}", seq)
            celula = f"{len(seq)} itens → aba «{aba}»" if aba else "vazio"
            if aba:
                criadas.append(aba)
        elif not _escalar(valor) and seq is None and (dataclasses.is_dataclass(valor) or isinstance(valor, dict)):
            celula = _texto_da_celula(dict(_campos(valor)))
        else:
            celula = _texto_da_celula(valor)
        linha = [nome, celula, tipo]
        if descricoes is not None:
            linha.append(descricoes.get(nome, ""))
        ws.append(linha)
    if origem:
        ws.append([])
        ws.append([f"Origem: {origem}"])
    _larguras(ws)
    return criadas


def _aba_da_tarifa(wb, config: Any) -> Optional[str]:
    """A tarifa como o motor a lê: cada quádrupla com o significado do código."""
    faixas = list(getattr(config, "water_tariffs", None) or [])
    if not faixas:
        return None
    from netuno.core.economic import calculate_water_bill
    from netuno.core.tariff_regimes import ler_estrutura, resumo_do_regime, validar_estrutura
    from netuno.core.tariffs_structure import DESCRICAO_DO_CODIGO

    ws = wb.create_sheet(_nome_de_aba(wb, "Auditoria_Tarifa"))
    _cabecalho(ws, ["Mínimo (m³)", "Máximo (m³)", "Valor", "Código", "Significado do código"])
    for f in faixas:
        codigo = int(f[3])
        ws.append([float(f[0]), float(f[1]), float(f[2]), codigo, DESCRICAO_DO_CODIGO.get(codigo, "desconhecido")])
    est = ler_estrutura(faixas)
    registro = {"faixas": faixas}
    ws.append([])
    ws.append(["Regime", est.regime])
    ws.append(["Leitura do regime", resumo_do_regime(registro)])
    modo = int(getattr(config, "sewage_mode", 1))
    ws.append(["Esgoto", {0: "valor fixo (R$)", 1: "percentual da água (%)", 2: "preço por m³ consumido (R$/m³)"}.get(modo, str(modo)),
               float(getattr(config, "sewage_rate", 0.0))])
    ws.append(["Tributos sobre a água", float(getattr(config, "water_tax_fixed", 0.0)),
               f"{float(getattr(config, 'water_tax_var', 0.0))}%"])
    achados = validar_estrutura(registro)
    ws.append(["Achados da validação", "; ".join(f"[{a.gravidade}] {a.mensagem}" for a in achados) or "nenhum"])
    ws.append([])
    _cabecalho(ws, ["Consumo (m³/mês)", "Água (R$)", "Água e esgoto (R$)", "Preço médio (R$/m³)"])
    for m3 in (0, 5, 10, 15, 20, 25, 30, 40, 50):
        agua = calculate_water_bill(m3 * 1000.0, faixas, sewage_mode=1, sewage_rate=0.0)
        total = calculate_water_bill(m3 * 1000.0, faixas, sewage_mode=modo,
                                     sewage_rate=float(getattr(config, "sewage_rate", 0.0)))
        ws.append([m3, round(agua, 2), round(total, 2), round(total / m3, 2) if m3 else ""])
    _larguras(ws)
    return ws.title


def _aba_do_arranjo(wb, dados: Dict[str, Any]) -> List[str]:
    criadas = []
    componentes = dados.get("bim_components") or []
    if componentes:
        ws = wb.create_sheet(_nome_de_aba(wb, "Auditoria_Componentes"))
        _cabecalho(ws, ["ID", "Tipo", "Nível", "x (mm)", "y (mm)", "z (mm)", "Rotação (°)", "Parâmetros"])
        for c in componentes:
            p = c.get("position_mm") or {}
            ws.append([c.get("instance_id"), c.get("type_id"), c.get("level"), p.get("x"), p.get("y"), p.get("z"),
                       c.get("rotation_deg"), _texto_da_celula(c.get("parameters") or {})])
        _larguras(ws)
        criadas.append(ws.title)
    trechos = dados.get("pipe_runs") or []
    if trechos:
        ws = wb.create_sheet(_nome_de_aba(wb, "Auditoria_Trechos"))
        _cabecalho(ws, ["Trecho", "Sistema", "DN (mm)", "Início", "Rota", "Fim", "Nível"])
        for r in trechos:
            ws.append([r.get("run_id"), r.get("system"), r.get("dn_mm"), _texto_da_celula(r.get("start")),
                       _texto_da_celula(r.get("route")), _texto_da_celula(r.get("end")), r.get("level")])
        try:
            from netuno.core.bim_exporter import build_bim_manifest
            from netuno.core.pipe_network import lengths_by_dn

            manifesto = build_bim_manifest(dados)
            ws.append([])
            _cabecalho(ws, ["Quantitativo por DN", "Comprimento (m)"])
            for dn, metros in lengths_by_dn(manifesto["pipe_runs"]).items():
                ws.append([f"DN {dn:g}", round(metros, 2)])
        except Exception as erro:  # o quantitativo é um extra: o arranjo pode estar incompleto
            ws.append([f"Quantitativo indisponível: {erro}"])
        _larguras(ws)
        criadas.append(ws.title)
    return criadas


def _aba_do_quantitativo(wb, config: Any, dados: Dict[str, Any], ambiental: Any) -> Optional[str]:
    """Cada item do arranjo, com preço, massa, carbono e destino, e a conferência."""
    from netuno.core.quantitativo_do_arranjo import (
        arranjo_do_projeto, conferir_cobertura, divergencias_com_o_projeto, levantar, mao_de_obra_do_projeto,
    )

    try:
        q = levantar(arranjo_do_projeto(config, dados), dados,
                     subsistema_de_descarte=bool(getattr(config, "first_flush_system_enabled", False)),
                     etap=bool(getattr(config, "etap_enabled", True)))
    except Exception as erro:
        ws = wb.create_sheet(_nome_de_aba(wb, "Auditoria_Quantitativo"))
        ws.append([f"Quantitativo indisponível: o arranjo não fecha ({erro})"])
        return ws.title
    ws = wb.create_sheet(_nome_de_aba(wb, "Auditoria_Quantitativo"))
    _cabecalho(ws, ["Item", "Tipo", "Quantidade", "Unidade", "DN (mm)", "Custo (R$)", "Massa (kg)",
                    "Carbono incorporado (kg CO2e)", "No CAPEX", "Na ACV", "Origem de preço, massa e fator"])
    for i in q.itens:
        ws.append([i.item, i.tipo, i.quantidade, i.unidade, i.dn_mm, i.custo_brl, i.massa_kg,
                   round(i.co2e_kg, 3), i.no_capex, i.na_acv, i.origem])
    ws.append([])
    _cabecalho(ws, ["Conferência", "Do quantitativo", "No projeto", "Confere"])
    no_projeto_tub = float(getattr(config, "cost_piping", 0.0) or 0.0) if config is not None else 0.0
    no_projeto_acc = float(getattr(config, "cost_accessories", 0.0) or 0.0) if config is not None else 0.0
    do_arranjo = bool(getattr(config, "capex_do_arranjo", False)) if config is not None else False
    linhas = [
        ("CAPEX: tubulação e conexões (R$)", q.custo_de_tubulacao, no_projeto_tub),
        ("CAPEX: acessórios (R$)", q.custo_de_acessorios, no_projeto_acc),
    ]
    tubos_projeto = sum(float(l) for _, l in (getattr(config, "pipes_list", None) or [])) if config is not None else 0.0
    linhas.append(("ACV: tubulação (m)", round(sum(q.tubos_m_por_dn.values()), 3), round(tubos_projeto, 3)))
    if ambiental is not None:
        itens = getattr(ambiental, "inventory_items", None) or []
        no_inventario = sum(float(getattr(it, "embodied_co2_kg", 0.0)) for it in itens
                            if str(getattr(it, "category", "")).startswith("Arranjo 3D"))
        linhas.append(("ACV: conexões, peças e cabos (kg CO2e)", round(q.co2e_de_acessorios + q.co2e_de_conexoes, 2),
                       round(no_inventario, 2)))
    for nome, do_q, do_proj in linhas:
        ws.append([nome, do_q, do_proj, "sim" if abs(float(do_q) - float(do_proj)) < 0.5 else "NÃO"])
    ws.append(["Fonte do CAPEX de tubulação e acessórios",
               "arranjo 3D" if do_arranjo else "valores digitados pelo projetista", "", ""])
    if config is not None:
        automatica = bool(getattr(config, "mao_de_obra_automatica", False))
        regra = mao_de_obra_do_projeto(config)
        ws.append(["Mão de obra (R$): fração dos materiais do projeto", regra,
                   float(getattr(config, "cost_labor", 0.0) or 0.0),
                   ("sim" if abs(regra - float(config.cost_labor)) < 0.5 else "NÃO") if automatica
                   else "valor digitado pelo projetista"])
    faltam = conferir_cobertura(q)
    ws.append(["Itens do arranjo sem destino no CAPEX ou na ACV", len(faltam), "; ".join(faltam) or "nenhum",
               "sim" if not faltam else "NÃO"])
    divergencias = divergencias_com_o_projeto(config, q)
    ws.append(["Arranjo coerente com o abastecimento e as motobombas do projeto", len(divergencias),
               "; ".join(divergencias) or "sim", "sim" if not divergencias else "NÃO"])
    _larguras(ws)
    return ws.title


def exportar_tudo(
    caminho: str,
    config: Any = None,
    project_data: Optional[Dict[str, Any]] = None,
    single_result: Any = None,
    sweep_result: Any = None,
    economic_result: Any = None,
    environmental_result: Any = None,
    mcdm_result: Any = None,
    horizon_years: int = 20,
) -> str:
    """Grava a planilha de auditoria completa e devolve o caminho."""
    dados = dict(project_data or {})
    export_simulation_to_excel(
        project_data=dados, file_path=caminho, single_result=single_result, sweep_result=sweep_result,
        economic_result=economic_result, environmental_result=environmental_result, mcdm_result=mcdm_result,
        selected_sheets={k: True for k in ("resumo", "balanco", "varredura", "fluxo", "acv", "mcdm")},
        horizon_years=horizon_years, daily_mode="all",
    )
    wb = openpyxl.load_workbook(caminho)
    if "Sem_Dados" in wb.sheetnames:
        del wb["Sem_Dados"]

    indice: List[Tuple[str, str]] = [(n, "planilha de dados (seleção de leitura)") for n in wb.sheetnames]
    blocos = [
        ("Auditoria_Premissas", config, descricoes_da_configuracao(),
         "todos os campos da configuração do projeto (NetunoConfig), como estão na memória"),
        ("Auditoria_Projeto", {k: v for k, v in dados.items() if k not in ("bim_components", "pipe_runs")}, None,
         "dados reunidos para relatórios e exportações"),
        ("Auditoria_Simulacao", single_result, None, "resultado da simulação do volume adotado"),
        ("Auditoria_Varredura", sweep_result, None, "resultado da varredura de volumes"),
        ("Auditoria_Economia", economic_result, None, "resultado da análise econômica"),
        ("Auditoria_Ambiental", environmental_result, None, "resultado da ACV, com a ETAP e o cloro da etapa de qualidade"),
        ("Auditoria_Multicriterio", mcdm_result, None, "resultado da decisão multicritério"),
    ]
    for titulo, objeto, descricoes, origem in blocos:
        for aba in _aba_de_campos(wb, titulo, objeto, descricoes, origem):
            indice.append((aba, origem if aba == titulo else f"sequência de «{titulo}»"))
    if config is not None:
        # A ETAP que a etapa de qualidade dimensiona: estágios, doses, CAPEX e o
        # carbono que a ACV soma. Dimensionada de novo aqui, com o mesmo volume.
        try:
            from netuno.core.etap_integration import dimensionar_etap_do_projeto

            volume = getattr(environmental_result, "annual_pluvial_m3", None) if environmental_result else None
            etap = dimensionar_etap_do_projeto(config, annual_pluvial_m3=volume, sim_result=single_result)
            for aba in _aba_de_campos(wb, "Auditoria_ETAP", etap, None,
                                      "linha de tratamento da etapa de qualidade, como entra no custo e no carbono"):
                indice.append((aba, "ETAP: estágios, doses, custo e carbono"))
        except Exception as erro:
            indice.append(("—", f"ETAP não dimensionada: {erro}"))
    quantitativo = _aba_do_quantitativo(wb, config, dados, environmental_result)
    if quantitativo:
        indice.append((quantitativo, "quantitativo do arranjo 3D: cada item, onde entra no CAPEX e na ACV, "
                                     "e a conferência de que nada ficou de fora"))
    tarifa = _aba_da_tarifa(wb, config) if config is not None else None
    if tarifa:
        indice.append((tarifa, "estrutura tarifária aplicada, regime, esgoto e conta por consumo"))
    for aba in _aba_do_arranjo(wb, dados):
        indice.append((aba, "arranjo 3D: peças, trechos e quantitativo por diâmetro"))

    leia = wb.create_sheet("0_Leia_me", 0)
    try:
        from netuno import __version__ as versao
    except ImportError:  # pragma: no cover
        versao = "—"
    leia.append(["Netuno — exportação completa para auditoria"])
    leia["A1"].font = Font(bold=True, size=14, color=_VERDE)
    leia.append([f"Projeto: {dados.get('project_name', '—')}"])
    leia.append([f"Versão do programa: {versao}"])
    leia.append([f"Gerado em: {_dt.datetime.now().isoformat(sep=' ', timespec='seconds')}"])
    leia.append(["As abas «Auditoria_*» trazem todos os campos dos objetos que o programa usou, "
                 "sem seleção; as numeradas são a planilha de dados de sempre."])
    leia.append([])
    _cabecalho(leia, ["Aba", "O que contém"])
    for aba, texto in indice:
        leia.append([aba, texto])
    _larguras(leia, maximo=110)
    wb.save(caminho)
    return str(Path(caminho))
