# -*- coding: utf-8 -*-
"""Caminhos dos scripts de dados da edição IBE: relativos ao repositório e configuráveis por variável de ambiente.

Variáveis (todas opcionais):

    TRITON_IBE_FONTES        pasta com a E-OBS (rr_ens_mean_0.1deg_reg_v33.0e.nc) e a subpasta caop/ (CAOP 2025, .gpkg)
                             padrão: <triton_ibe>/data/portugal/fontes  (fora do Git, ~3 GB)
    TRITON_IBE_BRUTOS        dados brutos de validação (ECA&D, GHCN-D, Iberia01, Open-Meteo, CPC)
                             padrão: <triton_ibe>/scripts/dados/dados_brutos  (fora do Git)
    TRITON_IBE_AUTOMATICOS   respostas JSON da coleta automática   padrão: scripts/dados/dados_automaticos
    TRITON_IBE_RESULTADOS    saídas de verificação (CSV, relatórios)  padrão: scripts/dados/resultados
    TRITON_IBE_BASE          o banco de chuva por concelho            padrão: <triton_ibe>/data/portugal_eobs.db
    TRITON_IBE_PROTOTIPO     pasta dos bancos de protótipo (ibe_prototipo.db, ibe_correcao.db)
                             padrão: scripts/dados/prototipo  (fora do Git, ~95 MB)
"""
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(AQUI))          # triton_ibe/


def _caminho(variavel, padrao):
    return os.path.abspath(os.environ.get(variavel) or padrao)


FONTES = _caminho("TRITON_IBE_FONTES", os.path.join(REPO, "data", "portugal", "fontes"))
EOBS_NC = os.path.join(FONTES, "rr_ens_mean_0.1deg_reg_v33.0e.nc")
CAOP_DIR = os.path.join(FONTES, "caop")
CAOP_CONTINENTE = os.path.join(CAOP_DIR, "Continente_CAOP2025.gpkg")
BRUTOS = _caminho("TRITON_IBE_BRUTOS", os.path.join(AQUI, "dados_brutos"))
AUTOMATICOS = _caminho("TRITON_IBE_AUTOMATICOS", os.path.join(AQUI, "dados_automaticos"))
RESULTADOS = _caminho("TRITON_IBE_RESULTADOS", os.path.join(AQUI, "resultados"))
PROTOTIPO = _caminho("TRITON_IBE_PROTOTIPO", os.path.join(AQUI, "prototipo"))
BASE = _caminho("TRITON_IBE_BASE", os.path.join(REPO, "data", "portugal_eobs.db"))
IBERIA01_NC = os.path.join(BRUTOS, "iberia01", "Iberia01_v1.0_DD_010reg_aa3d_pr.nc")

for _p in (RESULTADOS, PROTOTIPO):
    os.makedirs(_p, exist_ok=True)
