"""Consolida, documenta e pontua a confiança das tarifas usadas pelo estudo.

Fontes: base detalhada do projeto, dados abertos ANEEL vigentes e URLs oficiais
de prestadores/agências já registradas na base. O script não transforma tarifa
ANEEL sem tributos em tarifa final: ambas são mantidas com escopo explícito.
"""

from __future__ import annotations

import csv
import datetime as dt
import json
import math
import re
import unicodedata
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "estudo_5_tipologias_residenciais" / "Tarifas_Brasil_652_Cidades_COMPLETO_2026-08-19.csv"
ANEEL = ROOT / "tmp" / "aneel_tarifas_homologadas_2026.csv"
GEO = ROOT / "tarifas" / "validated_cidades_50k.json"
OUT_DIR = ROOT / "tarifas"
DETAILED_OUT = OUT_DIR / "tarifas_detalhadas_auditadas.csv"
SUMMARY_OUT = OUT_DIR / "catalogo_tarifas_auditado_652.csv"
AUDIT_DATE = dt.date(2026, 8, 24)
ANEEL_DATA_URL = (
    "https://dadosabertos.aneel.gov.br/dataset/5a583f3e-1646-4f67-bf0f-69db4203e89e/"
    "resource/fcf2906c-7c32-4b9b-a637-054e7a5234f4/download/"
    "tarifas-homologadas-distribuidoras-energia-eletrica.csv"
)
ANEEL_METHOD_URL = "https://www.gov.br/aneel/pt-br/centrais-de-conteudos/relatorios-e-indicadores/tarifas-e-informacoes-economico-financeiras"
SINISA_URL = "https://www.gov.br/cidades/pt-br/acesso-a-informacao/acoes-e-programas/saneamento/sinisa/resultados-sinisa"
ANA_SOCIAL_TARIFF_URL = "https://www.gov.br/ana/pt-br/assuntos/saneamento-basico/tarifa-social-de-agua-e-esgoto/lista-positiva/lista-positiva-1"


ANEEL_ALIASES = {
    "Amazonas Energia": "Âmbar Amazonas",
    "CEEE Equatorial": "CEEE-D",
    "CEMIG Distribuição": "CEMIG-D",
    "COCEL": "COCEL",
    "COPEL Distribuição": "COPEL-DIS",
    "CPFL Paulista": "CPFL-PAULISTA",
    "CPFL Piratininga": "CPFL-PIRATINING",
    "CPFL Piratininga – Oeste": "CPFL-PIRATINING",
    "CPFL Santa Cruz": "CPFL Santa Cruz",
    "CPFL Santa Cruz – Jaguari": "CPFL Santa Cruz",
    "CPFL Santa Cruz – Leste Paulista": "CPFL Santa Cruz",
    "CPFL Santa Cruz – Mococa": "CPFL Santa Cruz",
    "CPFL Santa Cruz – Sul Paulista": "CPFL Santa Cruz",
    "Cooperaliança": "COOPERALIANÇA",
    "DCELT": "DCELT",
    "DEMEI": "DEMEI",
    "DMED Poços de Caldas": "DMED",
    "EDP Espírito Santo": "EDP ES",
    "EDP São Paulo": "EDP SP",
    "ELFSM – Empresa Luz e Força Santa Maria": "ELFSM",
    "ENEL Distribuição São Paulo": "ELETROPAULO",
    "Enel Distribuição São Paulo – Sul": "ELETROPAULO",
    "Eletrocar": "ELETROCAR",
    "Enel Ceará": "ENEL CE",
    "Enel Distribuição Rio": "ENEL RJ",
    "Energisa Acre (EAC)": "EAC",
    "Energisa Mato Grosso": "EMT",
    "Energisa Mato Grosso do Sul": "EMS",
    # A antiga EMG passou a integrar a Energisa Minas Rio (EMR).
    "Energisa Minas Gerais (EMG)": "EMR",
    "Energisa Minas Rio": "EMR",
    "Energisa Paraíba": "EPB",
    "Energisa Rondônia": "ERO",
    "Energisa Sergipe": "ESE",
    "Energisa Sul-Sudeste – Leste": "ESS",
    "Energisa Sul-Sudeste – Norte": "ESS",
    "Energisa Sul-Sudeste – Oeste": "ESS",
    "Energisa Sul-Sudeste – Sul": "ESS",
    "Energisa Tocantins": "ETO",
    "Equatorial Alagoas": "EQUATORIAL AL",
    "Equatorial Amapá": "CEA",
    "Equatorial Goiás": "EQUATORIAL GO",
    "Equatorial Maranhão": "EQUATORIAL MA",
    "Equatorial Pará": "EQUATORIAL PA",
    "Equatorial Piauí": "EQUATORIAL PI",
    "CELESC Distribuição": "CELESC",
    "Sulgipe": "SULGIPE",
    "Light Serviços de Eletricidade": "LIGHT SESA",
    "Light Serviços de Eletricidade – Vale do Paraíba": "LIGHT SESA",
    "Neoenergia Brasília": "Neoenergia Brasília",
    "Neoenergia Coelba": "COELBA",
    "Neoenergia Cosern": "COSERN",
    "Neoenergia Elektro": "ELEKTRO",
    "Neoenergia Elektro – Leste": "ELEKTRO",
    "Neoenergia Elektro – Oeste": "ELEKTRO",
    "Neoenergia Elektro – Sul": "ELEKTRO",
    "Neoenergia Pernambuco (Celpe)": "Neoenergia PE",
    "RGE Sul (CPFL)": "RGE",
    "Roraima Energia": "ÂMBAR ENERGIA RR",
}


# Evidências primárias revistas manualmente em 24/08/2026. O campo
# ``reconciliado`` só é verdadeiro quando os números usados no modelo foram
# conferidos contra a tabela/ato indicado; encontrar uma página oficial, por si
# só, não autoriza elevar a confiança do valor.
SANITATION_EVIDENCE = {
    "CAESB": {
        "url": "https://s3.caesb.df.gov.br/www/prod/site1/Tabela-01-06-2026-a-31-05-2027.pdf",
        "tipo": "tabela tarifária oficial 2026/2027", "reconciliado": True,
    },
    "CASAN": {
        "url": "https://www.casan.com.br/menu-conteudo/index/url/tarifas",
        "tipo": "tabela tarifária oficial vigente", "reconciliado": True,
    },
    "CAGECE": {
        "url": "https://www.cagece.com.br/produtos-e-servicos/precos-e-prazos/estrutura-tarifaria/",
        "tipo": "tabela tarifária oficial vigente desde 05/11/2025",
        "reconciliado": True,
    },
    "SANEAGO": {
        "url": "https://www.saneago.com.br/2026/arquivos/Res_Normativa_Conjunta_AGR_AR_01_2026.pdf",
        "tipo": "Resolução Conjunta nº 1/2026 e estrutura tarifária vigente desde 01/04/2026",
        "reconciliado": True,
    },
    "COMPESA": {
        "url": "https://www.arpe.pe.gov.br/images/COORDENADORIAS/TARIFAS/SANEAMENTO/Estrutura-Tarifria-Compesa-2025---Resoluo-ARPE-n-289-2025.pdf",
        "tipo": "estrutura tarifária homologada pela Resolução ARPE nº 289/2025",
        "reconciliado": True,
    },
    "EMBASA": {
        "url": "https://www.embasa.ba.gov.br/w/tarifas-2026",
        "tipo": "tabela tarifária oficial 2026, Resolução AGERSA nº 001/2026, vigente desde 20/07/2026",
        "reconciliado": True,
    },
    "SANESUL": {
        "url": "https://www.sanesul.ms.gov.br/evolucao-tarifaria",
        "tipo": "repositório oficial de estruturas tarifárias 2026", "reconciliado": None,
    },
    "CORSAN": {
        "url": "https://www.corsan.com.br/sistematarifario/",
        "tipo": "repositório oficial 2026 com cinco tabelas por município/agência reguladora",
        "reconciliado": True,
    },
    "DESO": {
        "url": "https://transparencia.deso-se.com.br/Categorias/index/11",
        "tipo": "repositório oficial de estruturas tarifárias", "reconciliado": True,
    },
    "Iguá Sergipe": {
        "url": "https://agrese.se.gov.br/wp-content/uploads/2025/07/RESOLUCAO-78-2025-Reajuste-Tarifario-dos-Servicos-executados-pela-Igua-Sergipe-para-2025-2026.pdf",
        "tipo": "Resolução AGRESE nº 78/2025, tarifa da Iguá Sergipe vigente desde 01/08/2025",
        "reconciliado": True,
    },
    "CAERN": {
        "url": "https://agencia.caern.com.br/assets/documentos/novos/",
        "tipo": "repositório oficial das tabelas 2025 de Natal, Mossoró e interior",
        "reconciliado": True,
    },
    "CAERD": {
        "url": "https://rondonia.ro.gov.br/wp-content/uploads/2025/06/Resolucao_n._082_2025.pdf",
        "tipo": "Resolução AGERO nº 82/2025 e estrutura tarifária oficial da CAERD",
        "reconciliado": True,
    },
    "SAAE Cacoal": {
        "url": "https://sapl.cacoal.ro.leg.br/media/sapl/public/normajuridica/2025/3515/publicado_dioc-_lei_5.693_-_25.pdf",
        "tipo": "Lei Municipal nº 5.693/2025 e tabela tarifária oficial vigente",
        "reconciliado": True,
    },
    "SAAE Vilhena": {
        "url": "https://vilhena.ro.gov.br/secretarias-saae/",
        "tipo": "página municipal específica do SAAE, com operação de água e esgoto e atividades publicadas em 2026; tabela numérica pendente",
        "reconciliado": False,
    },
    "BRK Tocantins": {
        "url": "https://central.to.gov.br/download/452504",
        "tipo": "Resolução ATR nº 13/2025 e estrutura tarifária oficial vigente desde 05/12/2025",
        "reconciliado": True,
    },
    "CAEMA": {
        "url": "https://www.caema.ma.gov.br/images/2023/12/diario_ex20231205.pdf",
        "url_esgoto": "https://www.tjma.jus.br/financas/downacordo.php?acordo=0060%2F2021&anodoc=2021&nome=Publica%EF%BF%BD%EF%BF%BDo+6%EF%BF%BD+Aditivo&nrTermo=pu_6&tpAcordo=C",
        "tipo": "Resolução MOB/MA nº 10/2023 e ata oficial publicada em 19/01/2026",
        "reconciliado": True,
    },
    "Águas do Rio": {
        "url": "https://aguasdorio.com.br/legislacao-e-tarifas/",
        "tipo": "tabelas tarifárias oficiais das Regiões 1 e 4 vigentes desde dezembro de 2025",
        "reconciliado": True,
    },
    "CAGEPA": {
        "url": "https://auniao.pb.gov.br/servicos/doe/2025-1/maio/diario-oficial-31-05-2025-portal.pdf",
        "tipo": "Resolução ARPB nº 004/2025 e tabela tarifária oficial vigente desde 30/06/2025",
        "reconciliado": True,
    },
    "COSANPA": {
        "url": "https://www.cosanpa.pa.gov.br/wp-content/uploads/2018/05/Tarifa_Novembro_2023.pdf",
        "tipo": "tabela tarifária oficial aplicada desde 28/11/2023",
        "reconciliado": True,
    },
    "SABESP": {
        "url": "https://www.arsesp.sp.gov.br/Paginas/Tarifas.aspx",
        "tipo": "atos tarifários do regulador estadual", "reconciliado": None,
    },
    "Sanepar": {
        "url": "https://www.sanepar.com.br/tarifas",
        "tipo": "tabela tarifária oficial vigente", "reconciliado": None,
    },
    "Águas de Manaus": {
        "url": "https://www.aguasdemanaus.com.br/legislacao-e-tarifas/",
        "tipo": "estrutura tarifária oficial vigente após reajuste de fevereiro de 2026", "reconciliado": True,
    },
    "Águas do Piauí": {
        "url": "https://www.aguasdopiaui.com.br/legislacao-e-tarifas/",
        "tipo": "estrutura tarifária oficial vigente desde 01/03/2026",
        "reconciliado": True,
    },
    "Águas de Teresina": {
        "url": "https://www.aguasdeteresina.com.br/legislacao-e-tarifas/",
        "tipo": "estrutura tarifária oficial e Resolução ARSETE nº 82/2026, vigente desde 28/06/2026",
        "reconciliado": True,
    },
    "SANEACRE": {
        "url": "https://saneacre.ac.gov.br/saneacre-atualiza-estrutura-tarifaria-para-promover-equidade-e-sustentabilidade-financeira/",
        "tipo": "estrutura tarifária oficial 2025, Resolução AGEAC nº 104/2025, vigente desde julho de 2025",
        "reconciliado": True,
    },
    "CASAL": {
        "url": "https://www.casal.al.gov.br/app/uploads/2026/01/ESTRUTURA-TARiFARIA-2026.pdf",
        "tipo": "estrutura tarifária oficial 2026, Resolução ARSAL nº 233/2025, vigente desde 08/12/2025",
        "reconciliado": True,
    },
    "BRK Alagoas": {
        "url": "https://arsal.al.gov.br/transporte-intermunicipal/complementar/tarifas-complementar?catid=373&id=1316&m=0&task=download.send",
        "tipo": "estrutura tarifária oficial do Bloco A, Resoluções ARSAL nº 230 e 237/2025",
        "reconciliado": True,
    },
    "Águas do Sertão": {
        "url": "https://aguasdosertao.com/img/galerialistagensarquivos/listagem-arquivo-022455000000-06022026.pdf",
        "tipo": "estrutura tarifária oficial do Bloco B, Resolução ARSAL nº 252/2026",
        "reconciliado": True,
    },
    "Verde Alagoas": {
        "url": "https://www.verdealagoas.com.br/wp/wp-content/uploads/2026/02/RAMPA-TARIFARIA-2026.pdf",
        "tipo": "rampa tarifária oficial 2026, Resolução ARSAL nº 251/2026",
        "reconciliado": True,
    },
    "SAAE Coruripe": {
        "url": "https://coruripe.al.gov.br/",
        "tipo": "prestador municipal identificado; ato tarifário numérico pendente",
        "reconciliado": False,
    },
    "Prolagos": {
        "url": "https://www.prolagos.com.br/legislacao-e-tarifas/",
        "tipo": "estrutura tarifária oficial vigente desde dezembro de 2025",
        "reconciliado": True,
    },
    "Águas de Juturnaíba": {
        "url": "https://www.rj.gov.br/agenersa/sites/default/files/arquivos_paginas_basicas/DELIBERACAO4980.pdf",
        "tipo": "Deliberação AGENERSA nº 4.980/2025 e tabela tarifária vigente desde 01/12/2025",
        "reconciliado": True,
    },
    "SANEAR Colatina": {
        "url": "https://arsp.es.gov.br/Media/arsi/Legisla%C3%A7%C3%A3o/Resolu%C3%A7%C3%B5es%20Saneamento%20B%C3%A1sico/ARSP/%20Resolu%C3%A7%C3%A3oARSP094_2025.pdf",
        "tipo": "Resolução ARSP nº 094/2025 e tabela tarifária vigente de 01/12/2025 a 30/11/2026",
        "reconciliado": True,
    },
    "Águas Guariroba": {
        "url": "https://www.aguasguariroba.com.br/legislacao-e-tarifas/",
        "tipo": "estrutura tarifária oficial e Portaria nº 37/2025, vigente desde 03/01/2026",
        "reconciliado": True,
    },
    "Companhia Águas de Joinville": {
        "url": "https://www.aguasdejoinville.com.br/wp-content/uploads/2024/02/Tabela-Tarifaria-de-Agua-e-Esgoto-Vigente-a-partir-de-1-de-marco-de-2026.pdf",
        "tipo": "tabela tarifária oficial de água e esgoto vigente desde 01/03/2026",
        "reconciliado": True,
    },
    "DAE Bauru": {
        "url": "https://www.daebauru.sp.gov.br/conta_agua.php?item=CA1",
        "tipo": "tabela residencial oficial da Resolução nº 02/2026, vigente desde 02/03/2026",
        "reconciliado": True,
    },
    "COMUSA Novo Hamburgo": {
        "url": "https://www.comusa.rs.gov.br/_common/dados/arquivos/files/Tarifas_2026-Parcela1_Tarifas.pdf",
        "tipo": "Resolução CSR nº 046/2025 e tabela tarifária oficial vigente desde 01/03/2026",
        "reconciliado": True,
    },
    "DMAE Poços de Caldas": {
        "url": "https://dmaepc.mg.gov.br/taxas-tabela-de-preco/",
        "tipo": "tabela oficial vigente e Resolução ARISB-MG nº 394/2026, aplicada desde 01/06/2026",
        "reconciliado": True,
    },
    "RIC Ambiental": {
        "url": "https://www.marilia.sp.gov.br/portal/diario-oficial/ver/4292",
        "tipo": "Resolução AMAE nº 04/2026 e ato municipal que homologam reajuste linear de 6,72%",
        "reconciliado": True,
    },
    "GS Inima SAMAR": {
        "url": "https://www.samar.eco.br/legislacao-e-tarifas/",
        "tipo": "tabela oficial 2026 e Resolução AGRF-DAEA nº 001/2026, vigente desde 01/03/2026",
        "reconciliado": True,
    },
    "DAE Americana": {
        "url": "https://daeamericana.sp.gov.br/servicos/",
        "tipo": "Resolução ARES-PCJ nº 626/2025 e tabela oficial indicada como vigente pelo DAE",
        "reconciliado": True,
    },
    "DAAE Araraquara": {
        "url": "https://www.arespcj.com.br/public/media/arquivos/1759774558-resoluo_n_656_2025_-_reviso_tarifria_-_araraquara.pdf",
        "tipo": "Resolução ARES-PCJ nº 656/2025 e tabela tarifária vigente desde novembro de 2025",
        "reconciliado": True,
    },
    "SAEMA Araras": {
        "url": "https://www.arespcj.com.br/public/media/arquivos/1762372659-resoluo_n_662_2025_-_reajuste_tarifrio_-_araras.pdf",
        "tipo": "Resolução ARES-PCJ nº 662/2025 e tabela tarifária vigente desde dezembro de 2025",
        "reconciliado": True,
    },
    "BRK Ambiental Sumaré": {
        "url": "https://www.arespcj.com.br/public/media/arquivos/1765993558-resoluo_n_672_2025_-_reajuste_tarifrio_-_sumar.pdf",
        "tipo": "Resolução ARES-PCJ nº 672/2025 e tabela tarifária vigente desde fevereiro de 2026",
        "reconciliado": True,
    },
    "SANEBAVI Vinhedo": {
        "url": "https://www.arespcj.com.br/public/media/arquivos/1782828007-resoluo_n_710_2026_-_reviso_tarifria_-_vinhedo.pdf",
        "tipo": "Resolução ARES-PCJ nº 710/2026 e tabela tarifária vigente desde agosto de 2026",
        "reconciliado": True,
    },
    "SAAE São Carlos": {
        "url": "https://www.arespcj.com.br/public/media/arquivos/1760448426-resoluo_n_646_2025_-_reviso_tarifria_-_saae_so_carlos_assi.pdf",
        "tipo": "Resolução ARES-PCJ nº 646/2025 e tabela tarifária vigente desde setembro de 2025",
        "reconciliado": True,
    },
    "SAEC Catanduva": {
        "url": "https://www.arespcj.com.br/public/media/arquivos/1772798851-resolucao_n_677_2025_-_reviso_tarifaria_-_saec_catanduva.pdf",
        "tipo": "Resolução ARES-PCJ nº 677/2025 e tabela tarifária vigente desde janeiro de 2026",
        "reconciliado": True,
    },
    "SAEV Ambiental": {
        "url": "https://www.saev.com.br/arquivos/decreto_saev_2026_12115041.pdf",
        "tipo": "Decreto Municipal nº 19.729/2025 e tabela tarifária oficial do exercício de 2026",
        "reconciliado": True,
    },
    "DAEP Penápolis": {
        "url": "https://www.daep.com.br/publicos/resolucao_01_2026_(realinhamento_tarifas)_15055405.pdf",
        "url_base": "https://www.daep.com.br/publicos/resolucao_05_2024_(aprova_tarifas)_12051036.pdf",
        "tipo": "Resolução DAEP nº 5/2024, reajuste de 5% em 2025 e Decreto Municipal nº 8.504/2026 (8%), vigente desde 01/03/2026",
        "reconciliado": True,
    },
    "Ourinhos Saneamento": {
        "url": "https://www.ourinhossaneamento.com.br/legislacao-e-tarifas/",
        "tipo": "tabela tarifária oficial vigente desde novembro de 2025, com reajuste contratual de 10,18%",
        "reconciliado": True,
    },
    "SAEG": {
        "url": "https://www.arsesp.sp.gov.br/LegislacaoArquivos/Delibera%C3%A7%C3%A3o-1773.pdf",
        "url_nota_tecnica": "https://www.arsesp.sp.gov.br/Documentosgerais/NT%20Reajuste%202026%20-%20SAEG%20Guaratinguet%C3%A1.pdf",
        "tipo": "Deliberação ARSESP nº 1.773/2026 e tabela residencial oficial vigente desde 15/03/2026",
        "reconciliado": True,
    },
    "DAEB Bagé": {
        "url": "https://www.daeb.com.br/uploads/pagina/arquivos/Tabela-valores-2026.pdf",
        "url_ato": "https://daeb.com.br/uploads/pagina/arquivos/RESOLUCAOCSRNBA402025.pdf",
        "tipo": "tabela oficial do exercício de 2026 e Resolução AGESAN-RS CSR nº 40/2025",
        "reconciliado": True,
    },
    "SAAE Atibaia": {
        "url": "https://www.arespcj.com.br/public/media/arquivos/1763579706-resoluo_n_663_2025_-_reviso_tarifria_-_atibaia.pdf",
        "tipo": "Resolução ARES-PCJ nº 663/2025 e tabela tarifária vigente desde dezembro de 2025",
        "reconciliado": True,
    },
    "CSA Equatorial": {
        "url": "https://matrix.amapa.gov.br/storage/submenus/41/files/114624-RESOLUCAO%20N%C2%BA%20008-2025%2C%20DE%2030%20DE%20JULHO%20DE%202025%20-%20Reajuste%20Tarifa_rio%20de%202025%20CSA.pdf",
        "tipo": "Resolução ARSAP nº 008/2025 e estrutura tarifária vigente de 30/08/2025 a 29/08/2026",
        "reconciliado": True,
    },
    "DAE Valinhos": {
        "url": "https://www.arespcj.com.br/public/media/arquivos/1678301025-resolucao_n_483_2023_-_revisao_tarifaria_-_daev_valinhos.pdf",
        "tipo": "Resolução ARES-PCJ nº 483/2023, último ato tarifário listado pelo regulador para Valinhos",
        "reconciliado": True,
    },
    "Saneaqua": {
        "url": "https://www.arsesp.sp.gov.br/Documentosgerais/Nota%20T%C3%A9cnica%20-%20Reajuste%202026%20Saneaqua%20Mairinque.pdf",
        "url_esgoto": "https://www.saneaqua.com.br/estrutura-tarifaria",
        "tipo": "Nota Técnica ARSESP do reajuste 2026 e estrutura oficial da concessionária, vigente desde 01/05/2026",
        "reconciliado": True,
    },
    "DMAE Porto Alegre": {
        "url": "https://prefeitura.poa.br/sites/default/files/usu_doc/sites/dmae/23.639-Decreto_Preco_Basico_01-03-2026pdf.pdf",
        "url_metodo": "https://prefeitura.poa.br/dmae/entenda-conta",
        "tipo": "Decreto Municipal nº 23.639/2026 e página oficial da fórmula progressiva do DMAE",
        "reconciliado": True,
    },
    "SEMAE São Leopoldo": {
        "url": "https://semae.rs.gov.br/wp-content/uploads/2026/01/TABELA-2026.pdf",
        "tipo": "tabela tarifária oficial 2026, reajuste de 4,68% homologado pela Resolução CSR nº 45/2025",
        "reconciliado": True,
    },
    "SAMAE Caxias do Sul": {
        "url": "https://www.samaecaxias.com.br/Upload/Paginas/Pagina/9591e130-dedc-4336-bf74-122229e030e6.pdf",
        "url_pagina": "https://www.samaecaxias.com.br/Pagina/Index/20202",
        "tipo": "Tabela de Valores 2026 e Resolução AGESAN-RS CSR nº 3/2026, vigentes desde 01/07/2026",
        "reconciliado": True,
    },
    "SANEP Pelotas": {
        "url": "https://www2.sanep.com.br/sau_sanep/arquivos/f4f6d42e4fcc644bf6cb328f058260f0.pdf",
        "url_ato": "https://agesan-rs.com.br/wp-content/uploads/RESOLUCAO_CSR_NBA_9_2026_assinado.pdf",
        "tipo": "matriz tarifária oficial 2026/07 e Resolução AGESAN-RS CSR nº 9/2026",
        "reconciliado": True,
    },
    "Águas de Barra do Garças": {
        "url": "https://www.aegeamt.com.br/legislacao-e-tarifas/aguas-de-barra-do-garcas/",
        "tipo": "estrutura tarifária oficial da concessionária e histórico dos atos, vigente desde janeiro de 2026",
        "reconciliado": True,
    },
    "Águas de Sinop": {
        "url": "https://www.aegeamt.com.br/legislacao-e-tarifas/aguas-de-sinop/",
        "tipo": "estrutura tarifária oficial da concessionária após os reajustes/revisões de março e junho de 2026",
        "reconciliado": True,
    },
    "Águas de Primavera": {
        "url": "https://www.aegeamt.com.br/legislacao-e-tarifas/aguas-de-primavera/",
        "tipo": "estrutura tarifária oficial da concessionária e atos de reajuste/revisão de janeiro de 2026",
        "reconciliado": True,
    },
    "Águas de Sorriso": {
        "url": "https://www.aegeamt.com.br/legislacao-e-tarifas/aguas-de-sorriso/",
        "tipo": "estrutura tarifária oficial vigente e reajuste AGER-Sorriso de novembro de 2025",
        "reconciliado": True,
    },
    "SAAE Nova Mutum": {
        "url": "https://www.saaenm.com.br/pagina/tarifas-vigentes",
        "url_ato": "https://cdn.saaenm.com.br/assets/files/publicacao-d_2509051544.pdf",
        "tipo": "Decreto Municipal nº 17/2025 e página oficial de tarifas vigentes do SAAE",
        "reconciliado": True,
    },
    "SAMAE Blumenau / BRK Ambiental Blumenau": {
        "url": "https://samae.com.br/tabela-tarifaria",
        "url_esgoto": "https://www.brkambiental.com.br/storage/rebranding/blumenau/carta-de-servicos-blu-oficial-2026.pdf",
        "tipo": "tabelas oficiais de água do SAMAE e esgoto da BRK, vigentes em 2026",
        "reconciliado": True,
    },
    "SEMASA Itajaí": {
        "url": "https://suporte.semasaitajai.com.br/informacoes/tarifas",
        "url_ato": "https://www.semasaitajai.com.br/noticias/8366",
        "tipo": "tabela oficial e Decreto nº 13.761/2025, vigentes desde outubro de 2025",
        "reconciliado": True,
    },
    "SAMAE Jaraguá do Sul": {
        "url": "https://www.samaejs.com.br/central-do-usuario/tabela-de-tarifas-agua-e-esgoto/",
        "tipo": "tabela oficial de água e esgoto do exercício de 2026",
        "reconciliado": True,
    },
    "EMASA Balneário Camboriú": {
        "url": "https://emasa.com.br/emasa/conteudo/oficio_361_2026aris.pdf",
        "url_pagina": "https://emasa.com.br/emasa/consultas/tabela-tarifaria",
        "tipo": "Deliberação ARIS nº 15/2026 e estrutura tarifária vigente desde 04/05/2026",
        "reconciliado": True,
    },
    "SEMASA Lages": {
        "url": "https://www.semasalages.com.br/arquivos_legislacao/1769100952861.pdf",
        "url_pagina": "https://www.semasalages.com.br/tarifas",
        "tipo": "tabela tarifária oficial do exercício de 2026 e anexo municipal de serviços",
        "reconciliado": True,
    },
    "Tubarão Saneamento": {
        "url": "https://tubaraosaneamento.com.br/uploads/Tabela_tarif%C3%A1ria_e_servi%C3%A7os_complementares.pdf",
        "url_ato": "https://tubarao.sc.gov.br/prefeitura-sanciona-reajuste-anual-da-tarifa-de-agua/",
        "tipo": "matriz tarifária 2026/2027 e Decreto Municipal nº 9.159/2026",
        "reconciliado": True,
    },
    "SAMAE São Bento do Sul": {
        "url": "https://www.samaesbs.sc.gov.br/reajuste-tarifario-anual-a-partir-de-agosto2026",
        "tipo": "Portaria SAMAE/SBS nº 353/2026 e anexos tarifários, vigentes desde 01/08/2026",
        "reconciliado": True,
    },
    "SAMAE Brusque": {
        "url": "https://samaebru.com.br/tarifas-2026",
        "url_esgoto": "https://www.brusque.sc.gov.br/cidadao/noticia/operacao-assistida-ambiental-samae-e-ambiental-brusque-realizam-primeira-reuniao-de-alinhamento",
        "tipo": "Decreto tarifário municipal de 2026 e tabela oficial de água; esgoto ainda sem cobrança corrente na operação assistida",
        "reconciliado": True,
    },
    "SAMAE Gaspar": {
        "url": "https://www.samaegaspar.com.br/servicos/agua/tarifas",
        "url_ato": "https://www.samaegaspar.com.br/noticias/noticias/samae-tera-nova-tabela-de-tarifas-e-servicos-a-partir-de-1-de-julho-recomendada-pelo-agir",
        "tipo": "tabela oficial residencial e Decisão AGIR nº 332/2026, vigentes desde 01/07/2026",
        "reconciliado": True,
    },
    "BRK Ambiental Limeira": {
        "url": "https://www.arespcj.com.br/public/media/arquivos/1780515925-resoluo_n_705_2026_-_reajuste_tarifrio_-_limeira_rtf.pdf",
        "tipo": "Resolução ARES-PCJ nº 705/2026 e tabela residencial vigente nas contas emitidas desde julho de 2026",
        "reconciliado": True,
    },
    "SAMAE Mogi Guaçu": {
        "url": "https://www.arespcj.com.br/public/media/arquivos/1770038955-resoluo_n_686_2026_-_reajuste_tarifrio_-_mogi_guau.pdf",
        "tipo": "Resolução ARES-PCJ nº 686/2026 e tabela residencial de água e esgoto",
        "reconciliado": True,
    },
    "SAAE Itapira": {
        "url": "https://www.arespcj.com.br/public/media/arquivos/1778508605-resoluo_n_698_2026_-_reajuste_tarifrio_-_itapira.pdf",
        "tipo": "Resolução ARES-PCJ nº 698/2026 e tabela residencial vigente desde junho de 2026",
        "reconciliado": True,
    },
    "Companhia Ituana de Saneamento (CIS)": {
        "url": "https://www.arespcj.com.br/public/media/arquivos/1777896808-resoluo_n_693_2026_-_reviso_tarifria_-_itu.pdf",
        "tipo": "Resolução ARES-PCJ nº 693/2026 e tabela residencial vigente desde maio de 2026",
        "reconciliado": True,
    },
    "SAAE Mogi Mirim": {
        "url": "https://www.arespcj.com.br/public/media/arquivos/1780491027-resoluo_n_706_2026_-_reajuste_tarifrio_-_mogi_mirim.pdf",
        "tipo": "Resolução ARES-PCJ nº 706/2026, incluindo tarifa de esgoto e TCTE, vigente desde julho de 2026",
        "reconciliado": True,
    },
    "SAAEB Barretos": {
        "url": "https://www.arespcj.com.br/public/media/arquivos/1754333350-resoluo_n_643_2025_-_reviso_tarifria_-_barretos.pdf",
        "tipo": "Resolução ARES-PCJ nº 643/2025 e tabela residencial vigente desde setembro de 2025; Resolução nº 718/2026 ainda em noventena na data de corte",
        "reconciliado": True,
    },
    "SAERP Ribeirão Preto": {
        "url": "https://www.arespcj.com.br/public/media/arquivos/1778174854-resoluo_n_690_2026_-_reviso_tarifria_-_ribeiro_preto_retificada.pdf",
        "tipo": "Resolução ARES-PCJ nº 690/2026 retificada; água, coleta/afastamento e tratamento de esgoto vigentes desde maio de 2026",
        "reconciliado": True,
    },
    "DAAE Rio Claro": {
        "url": "https://www.arespcj.com.br/public/media/arquivos/1768419516-resoluo_n_681_2026_-_reviso_tarifria_-_rio_claro.pdf",
        "tipo": "Resolução ARES-PCJ nº 681/2026 e tabela residencial vigente desde fevereiro de 2026",
        "reconciliado": True,
    },
    "SeMAE Rio Preto": {
        "url": "https://www.arespcj.com.br/public/media/arquivos/1784893910-resoluo_n_715_2026_-_reajuste_tarifrio_-_so_jos_do_rio_preto.pdf",
        "tipo": "Resolução ARES-PCJ nº 715/2026 e tabela residencial vigente após o prazo legal de 30 dias, em agosto de 2026",
        "reconciliado": True,
    },
    "SANASA Campinas": {
        "url": "https://www.arespcj.com.br/public/media/arquivos/1767039489-resoluo_n_679_2025_-_reajuste_tarifrio_-_campinas.pdf",
        "tipo": "Resolução ARES-PCJ nº 679/2025; água, coleta/afastamento e tratamento de esgoto vigentes desde fevereiro de 2026",
        "reconciliado": True,
    },
    "SAAE Salto": {
        "url": "https://www.arespcj.com.br/public/media/arquivos/1759866527-resoluo_n_658_2025_-_reviso_tarifria_-_salto.pdf",
        "tipo": "Resolução ARES-PCJ nº 658/2025; água, coleta/afastamento e tratamento de esgoto vigentes desde novembro de 2025",
        "reconciliado": True,
    },
    "SAECIL Leme": {
        "url": "https://www.arespcj.com.br/public/media/arquivos/1768225265-resoluo_n_680_2025_-_reajuste_tarifrio_-_leme_c.pdf",
        "tipo": "Resolução ARES-PCJ nº 680/2025 e tabela residencial vigente em 2026, com alternativa de esgoto tratado",
        "reconciliado": True,
    },
    "SAE Louveira": {
        "url": "https://www.arespcj.com.br/public/media/arquivos/1770039048-resoluo_n_687_2026_-_reviso_tarifria_-_louveira.pdf",
        "tipo": "Resolução ARES-PCJ nº 687/2026 e tabela residencial de água e esgoto",
        "reconciliado": True,
    },
    "SAEMAS Sertãozinho": {
        "url": "https://www.arespcj.com.br/public/media/arquivos/1767038705-resoluo_n_678_2025_-_reajuste_tarifrio_-_sertozinho.pdf",
        "tipo": "Resolução ARES-PCJ nº 678/2025 e tabela residencial vigente em 2026",
        "reconciliado": True,
    },
    "SAEP Pirassununga": {
        "url": "https://www.arespcj.com.br/public/media/arquivos/1777897172-resoluo_n_695_2026_-_reajuste_tarifrio_-_pirassununga.pdf",
        "tipo": "Resolução ARES-PCJ nº 695/2026; cobrança direta por faixa ainda não integralmente representada no esquema",
        "reconciliado": False,
    },
    "SAERP São José do Rio Pardo": {
        "url": "https://www.arespcj.com.br/public/media/arquivos/1777896921-resoluo_n_694_2026_-_reajuste_tarifrio_-_so_jos_do_rio_pardo.pdf",
        "tipo": "Resolução ARES-PCJ nº 694/2026; cobrança direta e parcelas a deduzir ainda não integralmente representadas no esquema",
        "reconciliado": False,
    },
}

# Segunda rodada de qualificação dos registros C (24/08/2026). Estes
# documentos confirmam, em fonte primária, a estrutura/ato tarifário aplicável
# ou oferecem o repositório regulatório específico. ``reconciliado=False`` é
# deliberado: a fonte é suficiente para grau B, mas os valores legados ainda
# não foram conciliados linha a linha. Quando o ato é antigo ou a vigência não
# está expressa, o campo fica sem afirmação de reconciliação/atualidade.
_arisb_resolutions = "https://www.arisb.com.br/resolucoes-de-fiscalizacao-e-regulacao-"
_ares_tariffs = "https://www.arespcj.com.br/conteudo/comparativos-de-tarifas"

SANITATION_EVIDENCE.update({
    # Evidência institucional recente para prestadores cujos valores legados
    # ainda não puderam ser conciliados com uma tabela tarifária completa.
    # A classificação B registra exatamente essa limitação; não equivale a
    # afirmar que o valor numérico foi confirmado.
    "CAESC – Companhia de Água, Esgoto e Saneamento de Coari": {
        "url": "https://www.diariomunicipal.com.br/aam/materia/9E9DDE34/0f54bf1c6047f7a2abd30cceb39c97400f54bf1c6047f7a2abd30cceb39c9740",
        "tipo": "ato oficial CAESC nº 001/2026 que confirma o prestador municipal atual; tabela tarifária numérica pendente",
        "reconciliado": False,
    },
    "SAAE Itacoatiara": {
        "url": "https://saaeitacoatiara.com.br/portal-da-transparencia/",
        "tipo": "portal oficial específico do SAAE com registros institucionais de 2025 e 2026; tabela tarifária numérica pendente",
        "reconciliado": False,
    },
    "Prestador municipal/local – Manicoré": {
        "url": "https://www.mpam.mp.br/images-j5/SCOMS/PROCESSOS%20DISPENSAS/2024.027455.pdf",
        "tipo": "processo oficial do MPAM atualizado em 2025, com contratação direta e fatura do SISÁGUA/Município de Manicoré; estrutura tarifária completa pendente",
        "reconciliado": False,
    },
    "Prestador municipal/local – São Gabriel da Cachoeira": {
        "url": "https://www.diariomunicipal.com.br/aam/materia/D5AE6883/4ed394dbffa6fa13b44b2a4bd0c60fd74ed394dbffa6fa13b44b2a4bd0c60fd7",
        "tipo": "lei municipal de diretrizes de 2025 para 2026 que atribui ao município ações de captação, tratamento e distribuição de água; tarifa numérica pendente",
        "reconciliado": False,
    },
    "Prestador municipal/local – Tefé": {
        "url": "https://tefe.am.gov.br/wp-content/uploads/2025/09/transparencia-pmt-informacoes-financeira-despesas-realizadas-2019-2020-orcada-2021-e-estimadas-2022-2025-anexo-06-base-estrategica-2019-2025-23-01-2022.pdf",
        "tipo": "anexo orçamentário oficial municipal publicado em 2025 com programa específico de abastecimento de água; prestador e estrutura tarifária numérica ainda requerem confirmação",
        "reconciliado": False,
    },
    "Prefeitura de Birigui – Diretoria de Água e Esgoto": {
        "url": "https://www.birigui.sp.gov.br/birigui/controle/arquivo/pe_10-2026_-_edital_e_anexos.pdf",
        "tipo": "edital municipal de 2026 que confirma a operação direta pelas diretorias de água e esgoto; tabela tarifária numérica pendente",
        "reconciliado": False,
    },
    # Minas Gerais: repositório oficial atualizado com resoluções tarifárias
    # individualizadas por prestador/município.
    "SAAE Itabira": {"url": _arisb_resolutions, "tipo": "repositório oficial ARISB-MG de resoluções tarifárias, atualizado em 2026", "reconciliado": False},
    "SAAE Itabirito": {"url": "https://www.arisb.com.br/imgeditor/file/RES_406_2026_ARISB_MG_Reajuste_Itabirito_assinada.pdf", "tipo": "Resolução ARISB-MG nº 406/2026, conciliada nas 12 faixas residenciais, tarifa básica operacional e esgoto a 60%", "reconciliado": True},
    "SAAE Sete Lagoas": {"url": "https://www.saaesetelagoas.com.br/documentos-e-anexos/415-tabela-de-tarifas-03-03-2026/file", "tipo": "Tabela oficial do Decreto nº 7.702/2026; mínimo residencial de 6 m³ conciliado e esgoto a 80%", "reconciliado": True},
    "SAAE Manhuaçu": {"url": _arisb_resolutions, "tipo": "repositório oficial ARISB-MG de resoluções tarifárias, atualizado em 2026", "reconciliado": False},
    "DEMSUR": {"url": _arisb_resolutions, "tipo": "repositório oficial ARISB-MG de resoluções tarifárias, atualizado em 2026", "reconciliado": False},
    "Águas de Pará de Minas": {"url": _arisb_resolutions, "tipo": "repositório oficial ARISB-MG de resoluções tarifárias, atualizado em 2026", "reconciliado": False},
    "SAAE Passos": {"url": _arisb_resolutions, "tipo": "Resolução ARISB-MG nº 401/2026 e repositório oficial de tarifas", "reconciliado": False},
    "DAEPA": {"url": _arisb_resolutions, "tipo": "repositório oficial ARISB-MG de resoluções tarifárias, atualizado em 2026", "reconciliado": False},
    "DMAES Ponte Nova": {"url": _arisb_resolutions, "tipo": "repositório oficial ARISB-MG de resoluções tarifárias, atualizado em 2026", "reconciliado": False},
    "SAAE Três Pontas": {"url": _arisb_resolutions, "tipo": "repositório oficial ARISB-MG de resoluções tarifárias, atualizado em 2026", "reconciliado": False},
    "CODAU Uberaba": {"url": "https://www.arisb.com.br/imgeditor/file/Resolu%C3%A7%C3%A3o%20383%20-%20Rev1.pdf", "tipo": "Resolução ARISB-MG nº 383/2026, conciliada nas sete faixas residenciais e esgoto a 95%", "reconciliado": True},
    "DAMAE São João del-Rei": {"url": "https://www.arismig.mg.gov.br/legislacoes/detalhes/310", "tipo": "Resolução ARISMIG nº 031/2026 de reajuste de água e esgoto do DAMAE", "reconciliado": False},
    "DMAE Uberlândia": {"url": "https://dmae.uberlandia.mg.gov.br/", "tipo": "portal oficial do DMAE com legislação e estrutura tarifária consultadas em 2026", "reconciliado": False},

    # São Paulo: o comparativo oficial da ARES-PCJ remete à resolução
    # específica de cada prestador e disponibiliza tabelas residenciais.
    "Águas de Andradina": {"url": _ares_tariffs, "tipo": "repositório oficial ARES-PCJ de tabelas e resoluções tarifárias, consultado em 2026", "reconciliado": False},
    "SAAE Cruzeiro": {"url": _ares_tariffs, "tipo": "repositório oficial ARES-PCJ de tabelas e resoluções tarifárias, consultado em 2026", "reconciliado": False},
    "SAAE Jacareí": {"url": _ares_tariffs, "tipo": "repositório oficial ARES-PCJ de tabelas e resoluções tarifárias, consultado em 2026", "reconciliado": False},
    "Águas de Jahu": {"url": _ares_tariffs, "tipo": "repositório oficial ARES-PCJ de tabelas e resoluções tarifárias, consultado em 2026", "reconciliado": False},
    "SAAE Lençóis Paulista": {"url": _ares_tariffs, "tipo": "repositório oficial ARES-PCJ de tabelas e resoluções tarifárias, consultado em 2026", "reconciliado": False},
    "Sanessol": {"url": _ares_tariffs, "tipo": "repositório oficial ARES-PCJ de tabelas e resoluções tarifárias, consultado em 2026", "reconciliado": False},
    "BRK Ambiental Porto Ferreira": {"url": _ares_tariffs, "tipo": "repositório oficial ARES-PCJ de tabelas e resoluções tarifárias, consultado em 2026", "reconciliado": False},
    "SAESA": {"url": _ares_tariffs, "tipo": "repositório oficial ARES-PCJ de tabelas e resoluções tarifárias, consultado em 2026", "reconciliado": False},
    "SAAET": {"url": _ares_tariffs, "tipo": "repositório oficial ARES-PCJ de tabelas e resoluções tarifárias, consultado em 2026", "reconciliado": False},
    "SAAE Ibitinga": {"url": "https://www.saaeibitinga.sp.gov.br/portal/leis_decretos", "tipo": "repositório oficial de legislação tarifária do SAAE", "reconciliado": None},

    # Demais atos/tabelas oficiais específicos localizados nesta rodada.
    "BRK Ambiental Cachoeiro": {"url": "https://www.brkambiental.com.br/storage/cachoeiro/01-estrutura-tarifaria-cachoeiro-2024.pdf", "tipo": "estrutura tarifária oficial de Cachoeiro vigente desde 01/02/2024", "reconciliado": False},
    "SAAE Linhares": {"url": "https://arsp.es.gov.br/saneamento/tarifas/SAAELinhares", "tipo": "repositório oficial ARSP da tarifa vigente do SAAE Linhares, consultado em 2026", "reconciliado": False},
    "CAER": {"url": "https://agencia.caer.com.br/gsan/exibirConsultarEstruturaTarifariaPortalCaerAction.do", "tipo": "estrutura tarifária oficial da CAER e regra de esgoto a 80%", "reconciliado": None},
    "SAAE Parintins": {"url": "https://diariomunicipalaam.org.br/visualizar-publicacao/20210201", "tipo": "Decreto Municipal nº 040/2021 com reajuste e tarifas do SAAE Parintins", "reconciliado": None},
    "São Gabriel Saneamento S.A.": {"url": "https://www.sgssa.com.br/comunicacao/", "tipo": "repositório oficial de comunicações de correção tarifária de 2025 e 2026", "reconciliado": False},
    "SANEAR Rondonópolis": {"url": "https://sanearmt.com.br/simulador/", "tipo": "simulador tarifário oficial do SANEAR, consultado em 2026", "reconciliado": None},
    "DAE/VG": {"url": "https://template-site.daevg.com.br/institucional/legislacao", "tipo": "repositório oficial de legislação tarifária de água e esgoto", "reconciliado": None},
    "SAAE Lucas do Rio Verde": {"url": "https://saae.lucasdorioverde.mt.gov.br/site/tarifas", "tipo": "Decreto nº 7.349/2025 e tabela oficial completa de água e esgoto para 2026, conciliada nas seis faixas residenciais", "reconciliado": True},
    "Águas Cuiabá (Iguá)": {"url": "https://igua.com.br/storage/e3/69/85/historico-das-tarifa-urkqd.pdf", "tipo": "comunicado oficial vigente desde 20/03/2025, conciliado em cinco faixas residenciais com esgoto a 90%", "reconciliado": True},
    "Águas Alta Floresta / Norte Saneamento": {"url": "https://www.aguasaltafloresta.com.br/c%C3%B3pia-comunicados", "tipo": "comunicados oficiais de recomposição e manutenção da estrutura tarifária em 2026", "reconciliado": False},
    "Águas do Pantanal (autarquia municipal)": {"url": "https://www.aguasdopantanal.eco.br/Informacoes-ao-consumidor/Tabela-tarifaria/", "tipo": "tabela oficial 2026 conciliada em cinco faixas residenciais; tratamento de esgoto equivalente a 50% da água", "reconciliado": True},
    "SAMAE Tangará da Serra": {"url": "https://tangaradaserra.mt.gov.br/wp-content/uploads/2023/04/171-atualiza-valores-da-tarifa-de-consumo-de-agua-samae-2023-e-anexo.pdf", "tipo": "Decreto Municipal nº 171/2023 e anexo tarifário do SAMAE", "reconciliado": False},
    "Águas da Imperatriz": {"url": "https://www.rj.gov.br/agenersa/sites/default/files/arquivos_paginas_basicas/DELIBERACAO_AGENERSA_NA___4995_1.pdf", "tipo": "Deliberação AGENERSA nº 4.995/2026, conciliada nas cinco faixas domiciliares de água e esgoto", "reconciliado": True},
    "Águas das Agulhas Negras": {"url": "https://sanearesenderj.com.br/contrato-concessao/", "tipo": "repositório oficial do contrato, aditivos e regras tarifárias da concessão, consultado em 2026", "reconciliado": False},
    "SAAE Angra dos Reis": {"url": "https://angra.rj.gov.br/legislacao/1157", "tipo": "Decreto Municipal nº 12.128/2021, cobrança tarifária de esgoto do SAAE", "reconciliado": None},
    "SAAE Três Rios": {"url": "https://tresrios.rj.gov.br/wp-content/uploads/2025/06/TAC-01-2025.pdf", "tipo": "TAC oficial de 2025 que confirma a estrutura tarifária publicada pelo SAAETRI", "reconciliado": False},
    "CEDAE/serviço local – validar área": {"url": "https://www.cedae.com.br/SERVI%C3%87OS/Contas-e-Tarifas/Estrutura-Tarif%C3%A1ria", "tipo": "estrutura tarifária oficial CEDAE de janeiro de 2026; cobertura municipal ainda requer validação", "reconciliado": False},
    "Águas Pontes e Lacerda / Norte Saneamento": {"url": "https://5bffdcd3-acd1-40b3-a6ad-b27e6176bd71.filesusr.com/ugd/4b7c39_6e231a86fe124123986c8a503ce2aa26.pdf", "tipo": "comunicado oficial e estrutura tarifária 2026 conciliada nas cinco faixas residenciais de água e esgoto", "reconciliado": True},
    "SAAEB Ambiental": {"url": "https://saaebambiental.sp.gov.br/decretos/", "tipo": "repositório oficial de decretos e reajustes tarifários de 2025 e 2026", "reconciliado": False},
    "SAAE Maués": {"url": "https://www.diariomunicipal.com.br/aam/materia/001B8A87/03AL8dmw9H-MICgdeyagG54on4RegOlNvuqVcHACYKTfX8arx_vHxEQf8r_qOOa", "tipo": "regulamento municipal de 2019 com tabela completa de tarifas do SAAE Maués", "reconciliado": None},
    "COHASB / Prefeitura de Humaitá – prestação local": {"url": "https://www-storage.voxtecnologia.com.br/?f=251&i=publicado_27336_2014-12-29_585ddfcef92d6a007feb8db90d1cd821.pdf&m=sigpub.publicacao", "tipo": "ato municipal com tabela de tarifa de água da COHASB", "reconciliado": None},
    "Prestador municipal/local – Iranduba": {"url": "https://www.mpam.mp.br/images-j5/SCOMS/PROCESSOS%20DISPENSAS/SEI_2024.029620.pdf", "tipo": "Decreto Municipal nº 328/2024 e anexos de tarifa de água e serviços do SAAE", "reconciliado": False},
    "SAAE / prestação municipal de Manacapuru – confirmar": {"url": "https://www.mpam.mp.br/images-j5/SCOMS/PROCESSOS%20DISPENSAS/SEI_2025.011455.pdf", "tipo": "fatura oficial do SAAE Manacapuru de janeiro de 2025 anexada a processo do MPAM; estrutura completa pendente", "reconciliado": None},
    "COSAMA": {"url": "https://cosama.am.gov.br/perguntas-frequentes/", "tipo": "página oficial que documenta tarifa mínima, seis faixas e cálculo em cascata da COSAMA", "reconciliado": None},
    "Serviço local – Barra do Piraí": {"url": "https://sapl.barradopirai.rj.leg.br/media/sapl/public/normajuridica/1989/4088/lei_no_352_-_aprova_normas_de_cobranca_de_tarifa_de_agua_e_esgoto.pdf", "tipo": "Lei Municipal nº 352/1989 e anexo de cobrança da tarifa de água e esgoto", "reconciliado": None},
    "DAESC Coruripe": {"url": "https://diario.coruripe.al.gov.br/diarios/1093/download", "tipo": "Portaria DAESC de 2025 e tabela oficial de serviços de água e esgoto; tarifa-base ainda não reconciliada", "reconciliado": False},
    "SAAE Barra Mansa": {"url": "https://portaltransparencia.barramansa.rj.gov.br/download/noticia-oficial-edicao-n1510-de-06-de-marco-de-2026/", "tipo": "Boletim Oficial Municipal nº 1.510/2026 com Resolução SAAE nº 002/2026 de reajuste tarifário", "reconciliado": False},
})


TEXT_REPAIRS = {
    "m�": "m³", "R$/m�": "R$/m³", "Resolu��o": "Resolução", "resolu��o": "resolução",
    "n�": "nº", "�gua": "água", "Água": "Água", "Bras�lia": "Brasília",
    "Goi�nia": "Goiânia", "S�o": "São", "Bel�m": "Belém", "Cuiab�": "Cuiabá",
    "Macei�": "Maceió", "Macap�": "Macapá", "Vit�ria": "Vitória",
    "Jo�o": "João", "Lu�s": "Luís", "Par�": "Pará", "Goi�s": "Goiás",
    "Maranh�o": "Maranhão", "Piau�": "Piauí", "Rond�nia": "Rondônia",
    "Para�ba": "Paraíba", "Esp�rito": "Espírito", "Distribui��o": "Distribuição",
    "El�trica": "Elétrica", "el�trica": "elétrica", "padr�o": "padrão",
    "Al�quota": "Alíquota", "al�quota": "alíquota", "faixa progressiva por m�": "faixa progressiva por m³",
}


def repair_text(value: str) -> str:
    s = value or ""
    for bad, good in TEXT_REPAIRS.items():
        s = s.replace(bad, good)
    return s


def key_text(value: str) -> str:
    s = repair_text(value).replace("�", "")
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]", "", s)


def num(value):
    if value in (None, "", "nan"):
        return None
    try:
        return float(str(value).replace(".", ".").replace(",", "."))
    except ValueError:
        return None


def grade(score: float) -> str:
    if score >= 85:
        return "A — alta"
    if score >= 70:
        return "B — boa"
    if score >= 50:
        return "C — moderada"
    return "D — baixa"


def load_aneel_current():
    candidates = defaultdict(list)
    with ANEEL.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f, delimiter=";"):
            try:
                start = dt.date.fromisoformat(row["DatInicioVigencia"])
                end = dt.date.fromisoformat(row["DatFimVigencia"])
            except (ValueError, TypeError):
                continue
            selected = (
                start <= AUDIT_DATE
                and row["DscBaseTarifaria"] == "Tarifa de Aplicação"
                and row["DscSubGrupo"] == "B1"
                and row["DscModalidadeTarifaria"] == "Convencional"
                and row["DscClasse"] == "Residencial"
                and row["DscSubClasse"] == "Residencial"
                and row["DscDetalhe"] == "Não se aplica"
                and row["DscUnidadeTerciaria"] == "MWh"
            )
            if not selected:
                continue
            tusd = num(row["VlrTUSD"])
            te = num(row["VlrTE"])
            if tusd is None or te is None:
                continue
            candidates[row["SigAgente"]].append({
                "energia_aneel_sem_tributos_r_kwh": (tusd + te) / 1000.0,
                "energia_aneel_inicio_vigencia": start.isoformat(),
                "energia_aneel_fim_vigencia": end.isoformat(),
                "energia_aneel_ato": row["DscREH"],
                "energia_aneel_status_vigencia": "VIGENTE" if start <= AUDIT_DATE <= end else "EXPIRADA",
                "_end": end,
            })
    current = {}
    for agent, records in candidates.items():
        valid = [r for r in records if r["energia_aneel_status_vigencia"] == "VIGENTE"]
        chosen = max(valid or records, key=lambda r: r["_end"])
        if chosen["energia_aneel_status_vigencia"] == "EXPIRADA":
            days = (AUDIT_DATE - chosen["_end"]).days
            chosen["energia_aneel_status_vigencia"] = f"EXPIRADA_HA_{days}_DIAS_REFERENCIA_MAIS_RECENTE"
        chosen.pop("_end", None)
        current[agent] = chosen
    return current


def load_rows():
    with SOURCE.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    # Campos necessários para reproduzir estruturas que usam tarifa por bloco
    # acompanhada de parcela a deduzir (em vez de simples soma progressiva).
    for row in rows:
        row["parcela_deduzir_agua_r"] = ""
        row["parcela_deduzir_esgoto_r"] = ""
        row["tarifa_tratamento_esgoto_r_m3"] = ""
        row["tarifa_tratamento_esgoto_fixa_r"] = ""
        row["tarifa_esgoto_coleta_afastamento_r_m3"] = ""
        row["tarifa_esgoto_coleta_afastamento_fixa_r"] = ""
        row["condicao_aplicacao_tarifa"] = ""
    # Corrigir operadores municipais antes de expandir a estrutura CAERD.
    # Cacoal e Vilhena mantêm SAAEs próprios e não usam a tabela estadual.
    for row in rows:
        if row.get("municipio") == "Cacoal" and row.get("saneamento_prestador") == "CAERD":
            row["saneamento_prestador"] = "SAAE Cacoal"
            row["fonte_saneamento"] = SANITATION_EVIDENCE["SAAE Cacoal"]["url"]
            row["status_saneamento"] = "OPERADOR_ATUAL_VERIFICADO_VALOR_NAO_RECONCILIADO"
        elif row.get("municipio") == "Vilhena" and row.get("saneamento_prestador") == "CAERD":
            row["saneamento_prestador"] = "SAAE Vilhena"
            row["fonte_saneamento"] = SANITATION_EVIDENCE["SAAE Vilhena"]["url"]
            row["status_saneamento"] = "OPERADOR_ATUAL_VERIFICADO_VALOR_NAO_RECONCILIADO"
        elif row.get("municipio") == "Nova Mutum":
            row["saneamento_prestador"] = "SAAE Nova Mutum"
            row["agencia_reguladora"] = "AGER-MT / Município de Nova Mutum"
        elif row.get("municipio") == "Blumenau":
            row["saneamento_prestador"] = "SAMAE Blumenau / BRK Ambiental Blumenau"
        elif row.get("municipio") == "Birigui":
            # A documentação municipal de 2025/2026 identifica diretorias
            # próprias de produção/abastecimento de água e tratamento de
            # esgoto; não há evidência atual para o rótulo legado
            # "Águas de Birigui".
            row["saneamento_prestador"] = "Prefeitura de Birigui – Diretoria de Água e Esgoto"
            row["agencia_reguladora"] = "Regulação municipal"
            row["fonte_saneamento"] = SANITATION_EVIDENCE[row["saneamento_prestador"]]["url"]
            row["status_saneamento"] = "OPERADOR_ATUAL_VERIFICADO_VALOR_NAO_RECONCILIADO"
        elif row.get("uf") == "PI" and row.get("saneamento_prestador") == "AGESPISA":
            row["saneamento_prestador"] = "Águas do Piauí"
            row["agencia_reguladora"] = "AGRESPI / MRAE-PI"
        elif row.get("uf") == "AL":
            al_operator = {
                "Arapiraca": "CASAL",
                "Coruripe": "SAAE Coruripe",
                "Delmiro Gouveia": "Águas do Sertão",
                "Maceió": "BRK Alagoas",
                "Marechal Deodoro": "BRK Alagoas",
                "Palmeira dos Índios": "Águas do Sertão",
                "Penedo": "Águas do Sertão",
                "Rio Largo": "BRK Alagoas",
                "São Miguel dos Campos": "Águas do Sertão",
                "União dos Palmares": "Verde Alagoas",
            }.get(row.get("municipio"))
            if al_operator:
                row["saneamento_prestador"] = al_operator
                row["agencia_reguladora"] = "ARSAL" if al_operator != "SAAE Coruripe" else "Regulação municipal"
        elif row.get("municipio") == "Araruama":
            row["saneamento_prestador"] = "Águas de Juturnaíba"
            row["agencia_reguladora"] = "AGENERSA"
    # Algumas tabelas oficiais são mais granulares do que a base legada.
    # Expandir as linhas antes da conciliação preserva a estrutura publicada.
    expanded_rows = []
    for row in rows:
        if row.get("saneamento_prestador") == "EMBASA" and key_text(row.get("faixa_consumo_m3", "")) in {"21a30m3", "21a30m"}:
            for band in ("21 a 25 m³", "26 a 30 m³"):
                clone = dict(row)
                clone["faixa_consumo_m3"] = band
                expanded_rows.append(clone)
        elif row.get("saneamento_prestador") == "CAERN":
            caern_expansion = {
                "11a20m3": ("11 a 15 m³", "16 a 20 m³"),
                "21a50m3": ("21 a 30 m³", "31 a 50 m³"),
                ">50m3": ("51 a 100 m³", ">100 m³"),
            }
            source_band = key_text(row.get("faixa_consumo_m3", ""))
            if source_band in caern_expansion:
                for band in caern_expansion[source_band]:
                    clone = dict(row)
                    clone["faixa_consumo_m3"] = band
                    expanded_rows.append(clone)
            else:
                expanded_rows.append(row)
        elif row.get("saneamento_prestador") == "CAERD":
            caerd_expansion = {
                "11a20m3": ("11 a 15 m³", "16 a 20 m³"),
                "21a50m3": ("21 a 25 m³", "26 a 30 m³", "31 a 50 m³"),
                ">50m3": ("51 a 75 m³", "76 a 150 m³", ">150 m³"),
            }
            source_band = key_text(row.get("faixa_consumo_m3", ""))
            if source_band in caerd_expansion:
                for band in caerd_expansion[source_band]:
                    clone = dict(row)
                    clone["faixa_consumo_m3"] = band
                    expanded_rows.append(clone)
            else:
                expanded_rows.append(row)
        elif row.get("saneamento_prestador") == "BRK Tocantins":
            brk_to_expansion = {
                "0a10m3": ("0 a 5 m³", "6 a 10 m³"),
                "21a30m3": ("21 a 25 m³", "26 a 30 m³"),
                ">30m3": ("31 a 35 m³", "36 a 40 m³", "41 a 50 m³", ">50 m³"),
            }
            source_band = key_text(row.get("faixa_consumo_m3", ""))
            if source_band in brk_to_expansion:
                for band in brk_to_expansion[source_band]:
                    clone = dict(row)
                    clone["faixa_consumo_m3"] = band
                    expanded_rows.append(clone)
            else:
                expanded_rows.append(row)
        elif row.get("saneamento_prestador") == "DAAE Araraquara":
            araraquara_expansion = {
                "11a20m3": ("11 a 20 m³",),
                "21a50m3": ("21 a 30 m³", "31 a 40 m³", "41 a 50 m³"),
                "50m3": ("51 a 100 m³", "101 a 200 m³", ">201 m³"),
            }
            source_band = key_text(row.get("faixa_consumo_m3", ""))
            if source_band in araraquara_expansion:
                for band in araraquara_expansion[source_band]:
                    clone = dict(row)
                    clone["faixa_consumo_m3"] = band
                    expanded_rows.append(clone)
            else:
                expanded_rows.append(row)
        elif row.get("saneamento_prestador") == "SAEMA Araras":
            araras_expansion = {
                "21a50m3": ("21 a 30 m³", "31 a 50 m³"),
                "50m3": ("51 a 100 m³", "101 a 500 m³", "501 a 5.000 m³", ">5.000 m³"),
            }
            source_band = key_text(row.get("faixa_consumo_m3", ""))
            if source_band in araras_expansion:
                for band in araras_expansion[source_band]:
                    clone = dict(row)
                    clone["faixa_consumo_m3"] = band
                    expanded_rows.append(clone)
            else:
                expanded_rows.append(row)
        elif row.get("saneamento_prestador") == "BRK Ambiental Sumaré":
            sumare_expansion = {
                "21a50m3": ("21 a 30 m³", "31 a 50 m³"),
                "50m3": (">50 m³",),
            }
            source_band = key_text(row.get("faixa_consumo_m3", ""))
            if source_band in sumare_expansion:
                for band in sumare_expansion[source_band]:
                    clone = dict(row)
                    clone["faixa_consumo_m3"] = band
                    expanded_rows.append(clone)
            else:
                expanded_rows.append(row)
        elif row.get("saneamento_prestador") == "SANEBAVI Vinhedo":
            vinhedo_expansion = {
                "11a20m3": ("11 a 15 m³", "16 a 20 m³"),
                "21a50m3": ("21 a 35 m³", "36 a 50 m³"),
                "50m3": ("51 a 75 m³", ">75 m³"),
            }
            source_band = key_text(row.get("faixa_consumo_m3", ""))
            if source_band in vinhedo_expansion:
                for band in vinhedo_expansion[source_band]:
                    clone = dict(row)
                    clone["faixa_consumo_m3"] = band
                    expanded_rows.append(clone)
            else:
                expanded_rows.append(row)
        elif row.get("saneamento_prestador") == "SAAE São Carlos":
            sao_carlos_expansion = {
                "21a50m3": ("21 a 30 m³", "31 a 40 m³", "41 a 50 m³"),
                "50m3": ("51 a 60 m³", ">60 m³"),
            }
            source_band = key_text(row.get("faixa_consumo_m3", ""))
            if source_band in sao_carlos_expansion:
                for band in sao_carlos_expansion[source_band]:
                    clone = dict(row)
                    clone["faixa_consumo_m3"] = band
                    expanded_rows.append(clone)
            else:
                expanded_rows.append(row)
        elif row.get("saneamento_prestador") == "SAEC Catanduva":
            catanduva_expansion = {
                "0a10m3": ("0 a 7 m³ (mínimo I)", "8 a 15 m³ (mínimo II)", "0 a 10 m³ (>15)"),
                "11a20m3": ("11 a 20 m³ (>15)",),
                "21a50m3": ("21 a 25 m³ (>15)", "26 a 30 m³ (>15)", "31 a 40 m³ (>15)", "41 a 50 m³ (>15)"),
                "50m3": ("51 a 100 m³ (>15)", ">100 m³ (>15)"),
            }
            source_band = key_text(row.get("faixa_consumo_m3", ""))
            if source_band in catanduva_expansion:
                for band in catanduva_expansion[source_band]:
                    clone = dict(row)
                    clone["faixa_consumo_m3"] = band
                    expanded_rows.append(clone)
            else:
                expanded_rows.append(row)
        elif row.get("saneamento_prestador") == "SAEV Ambiental":
            saev_expansion = {
                "21a50m3": ("21 a 30 m³", "31 a 50 m³"),
                "50m3": (">50 m³",),
            }
            source_band = key_text(row.get("faixa_consumo_m3", ""))
            if source_band in saev_expansion:
                for band in saev_expansion[source_band]:
                    clone = dict(row)
                    clone["faixa_consumo_m3"] = band
                    expanded_rows.append(clone)
            else:
                expanded_rows.append(row)
        elif row.get("saneamento_prestador") == "DAEP Penápolis":
            source_band = key_text(row.get("faixa_consumo_m3", ""))
            daep_expansion = {
                "0a10m3": ("1 a 20 m³",),
                "21a50m3": ("21 a 30 m³", "31 a 40 m³", "41 a 50 m³"),
                "50m3": ("51 a 75 m³", "76 a 100 m³", ">100 m³"),
            }
            if source_band == "11a20m3":
                continue
            if source_band in daep_expansion:
                for band in daep_expansion[source_band]:
                    clone = dict(row)
                    clone["faixa_consumo_m3"] = band
                    expanded_rows.append(clone)
            else:
                expanded_rows.append(row)
        elif row.get("saneamento_prestador") == "Ourinhos Saneamento":
            ourinhos_expansion = {
                "21a50m3": ("21 a 30 m³", "31 a 50 m³"),
                "50m3": (">50 m³",),
            }
            source_band = key_text(row.get("faixa_consumo_m3", ""))
            if source_band in ourinhos_expansion:
                for band in ourinhos_expansion[source_band]:
                    clone = dict(row)
                    clone["faixa_consumo_m3"] = band
                    expanded_rows.append(clone)
            else:
                expanded_rows.append(row)
        elif row.get("saneamento_prestador") == "CSA Equatorial":
            if key_text(row.get("faixa_consumo_m3", "")) == "30m3":
                for band in ("31 a 50 m³", ">50 m³"):
                    clone = dict(row)
                    clone["faixa_consumo_m3"] = band
                    expanded_rows.append(clone)
            else:
                expanded_rows.append(row)
        elif row.get("saneamento_prestador") == "DAE Valinhos":
            valinhos_expansion = {
                "11a20m3": ("10,001 a 17 m³", "17,001 a 25 m³"),
                "21a50m3": ("25,001 a 35 m³", "35,001 a 50 m³"),
                "50m3": (">50 m³",),
            }
            source_band = key_text(row.get("faixa_consumo_m3", ""))
            if source_band in valinhos_expansion:
                for band in valinhos_expansion[source_band]:
                    clone = dict(row)
                    clone["faixa_consumo_m3"] = band
                    expanded_rows.append(clone)
            else:
                expanded_rows.append(row)
        elif row.get("saneamento_prestador") == "Águas do Piauí":
            aguas_pi_expansion = {
                "11a20m3": ("11 a 15 m³", "16 a 20 m³"),
                ">20m3": ("21 a 25 m³", "26 a 35 m³", ">35 m³"),
            }
            source_band = key_text(row.get("faixa_consumo_m3", ""))
            if source_band in aguas_pi_expansion:
                for band in aguas_pi_expansion[source_band]:
                    clone = dict(row)
                    clone["faixa_consumo_m3"] = band
                    expanded_rows.append(clone)
            else:
                expanded_rows.append(row)
        elif row.get("saneamento_prestador") == "SANEACRE":
            saneacre_expansion = {
                "0a10m3": ("0 a 15 m³",),
                "11a20m3": ("16 a 20 m³",),
                "20m3": (
                    "21 a 25 m³", "26 a 30 m³", "31 a 35 m³",
                    "36 a 40 m³", "41 a 45 m³", "46 a 50 m³", ">50 m³",
                ),
            }
            source_band = key_text(row.get("faixa_consumo_m3", ""))
            if source_band in saneacre_expansion:
                for band in saneacre_expansion[source_band]:
                    clone = dict(row)
                    clone["faixa_consumo_m3"] = band
                    expanded_rows.append(clone)
            else:
                expanded_rows.append(row)
        elif row.get("saneamento_prestador") == "SAAE Cacoal":
            cacoal_expansion = {
                "0a10m3": ("0 a 10 m³",),
                "11a20m3": ("11 a 15 m³", "16 a 20 m³"),
                "21a50m3": ("21 a 25 m³", "26 a 30 m³", "31 a 50 m³"),
                "50m3": (">50 m³",),
            }
            source_band = key_text(row.get("faixa_consumo_m3", ""))
            if source_band in cacoal_expansion:
                for band in cacoal_expansion[source_band]:
                    clone = dict(row)
                    clone["faixa_consumo_m3"] = band
                    expanded_rows.append(clone)
            else:
                expanded_rows.append(row)
        elif row.get("uf") == "AL" and row.get("saneamento_prestador") != "SAAE Coruripe":
            al_expansion = {
                "0a10m3": ("0 a 10 m³",),
                "11a20m3": ("11 a 15 m³", "16 a 20 m³"),
                "21a50m3": ("21 a 30 m³", "31 a 40 m³", "41 a 50 m³"),
                "50m3": ("51 a 90 m³", "91 a 150 m³", ">150 m³"),
            }
            source_band = key_text(row.get("faixa_consumo_m3", ""))
            if source_band in al_expansion:
                for band in al_expansion[source_band]:
                    clone = dict(row)
                    clone["faixa_consumo_m3"] = band
                    expanded_rows.append(clone)
            else:
                expanded_rows.append(row)
        elif row.get("saneamento_prestador") == "Águas de Manaus" and key_text(row.get("faixa_consumo_m3", "")) == "40m3":
            for band in ("41 a 60 m³", ">60 m³"):
                clone = dict(row)
                clone["faixa_consumo_m3"] = band
                expanded_rows.append(clone)
        elif row.get("saneamento_prestador") == "Águas Guariroba":
            guariroba_expansion = {
                "21a30m3": ("21 a 25 m³", "26 a 30 m³"),
                ">30m3": ("31 a 50 m³", ">50 m³"),
            }
            source_band = key_text(row.get("faixa_consumo_m3", ""))
            if source_band in guariroba_expansion:
                for band in guariroba_expansion[source_band]:
                    clone = dict(row)
                    clone["faixa_consumo_m3"] = band
                    expanded_rows.append(clone)
            else:
                expanded_rows.append(row)
        elif key_text(row.get("saneamento_prestador", "")) == "aguasdebarradogarcasaegea":
            barra_expansion = {
                "0a10m3": ("0 a 10 m³",),
                "11a20m3": ("11 a 20 m³",),
                "21a30m3": ("21 a 30 m³",),
                "30m3": ("31 a 40 m³", ">40 m³"),
            }
            source_band = key_text(row.get("faixa_consumo_m3", ""))
            if source_band in barra_expansion:
                for band in barra_expansion[source_band]:
                    clone = dict(row)
                    clone["faixa_consumo_m3"] = band
                    expanded_rows.append(clone)
            else:
                expanded_rows.append(row)
        elif key_text(row.get("saneamento_prestador", "")) == "aguasdeprimaveraaegea":
            primavera_expansion = {
                "0a10m3": ("0 a 10 m³",), "11a20m3": ("11 a 20 m³",),
                "21a30m3": ("21 a 30 m³",), "30m3": ("31 a 40 m³", ">40 m³"),
            }
            source_band = key_text(row.get("faixa_consumo_m3", ""))
            if source_band in primavera_expansion:
                for band in primavera_expansion[source_band]:
                    clone = dict(row)
                    clone["faixa_consumo_m3"] = band
                    expanded_rows.append(clone)
            else:
                expanded_rows.append(row)
        elif key_text(row.get("saneamento_prestador", "")) == "aguasdesorrisoaegea":
            sorriso_expansion = {
                "0a10m3": ("0 a 10 m³",), "11a20m3": ("11 a 20 m³",),
                "21a30m3": ("21 a 30 m³",), "30m3": ("31 a 40 m³", ">40 m³"),
            }
            source_band = key_text(row.get("faixa_consumo_m3", ""))
            if source_band in sorriso_expansion:
                for band in sorriso_expansion[source_band]:
                    clone = dict(row)
                    clone["faixa_consumo_m3"] = band
                    expanded_rows.append(clone)
            else:
                expanded_rows.append(row)
        elif row.get("saneamento_prestador") == "SAAE Nova Mutum":
            nova_mutum_expansion = {
                "0a10m3": ("0 a 10 m³",), "11a20m3": ("11 a 20 m³",),
                "21a30m3": ("21 a 30 m³",),
                "30m3": ("31 a 40 m³", "41 a 50 m³", ">50 m³"),
            }
            source_band = key_text(row.get("faixa_consumo_m3", ""))
            if source_band in nova_mutum_expansion:
                for band in nova_mutum_expansion[source_band]:
                    clone = dict(row)
                    clone["faixa_consumo_m3"] = band
                    expanded_rows.append(clone)
            else:
                expanded_rows.append(row)
        elif row.get("saneamento_prestador") in {
            "SAAEB Barretos", "SAERP Ribeirão Preto", "DAAE Rio Claro",
            "SeMAE Rio Preto", "SANASA Campinas", "SAAE Salto",
        } and row.get("categoria") == "Residencial normal":
            # Salto tinha duas linhas-resumo na base original (mínimo e referência
            # de 25 m³). A tabela oficial completa deve ser expandida apenas uma vez.
            if row.get("saneamento_prestador") == "SAAE Salto" and key_text(row.get("faixa_consumo_m3", "")) != "010m3":
                continue
            ares_city_bands = {
                "SAAEB Barretos": ("0 a 10 m³", "11 a 15 m³", "16 a 20 m³", "21 a 25 m³", "26 a 30 m³", "31 a 35 m³", "36 a 40 m³", "41 a 50 m³", "51 a 100 m³", ">100 m³"),
                "SAERP Ribeirão Preto": ("0 a 10 m³", "11 a 15 m³", "16 a 20 m³", "21 a 25 m³", "26 a 30 m³", "31 a 40 m³", "41 a 50 m³", "51 a 80 m³", "81 a 100 m³", ">100 m³"),
                "DAAE Rio Claro": ("0 a 10 m³", "11 a 20 m³", "21 a 50 m³", "51 a 100 m³", ">100 m³"),
                "SeMAE Rio Preto": ("0 a 10 m³", "11 a 20 m³", "21 a 30 m³", "31 a 40 m³", "41 a 50 m³", "51 a 100 m³", ">100 m³"),
                "SANASA Campinas": ("0 a 10 m³", "11 a 15 m³", "16 a 20 m³", "21 a 25 m³", "26 a 30 m³", "31 a 50 m³", ">50 m³"),
                "SAAE Salto": ("0 a 10 m³", "11 a 15 m³", "16 a 20 m³", "21 a 25 m³", "26 a 30 m³", "31 a 35 m³", "36 a 40 m³", "41 a 60 m³", "61 a 80 m³", ">80 m³"),
            }
            for band in ares_city_bands[row["saneamento_prestador"]]:
                clone = dict(row)
                clone["faixa_consumo_m3"] = band
                expanded_rows.append(clone)
        elif row.get("municipio") in {"Leme", "Louveira", "Sertãozinho"} and row.get("categoria") == "Residencial normal":
            municipal_ares = {
                "Leme": ("SAECIL Leme", ("0 a 10 m³", "11 a 20 m³", "21 a 30 m³", "31 a 40 m³", "41 a 50 m³", "51 a 100 m³", ">100 m³")),
                "Louveira": ("SAE Louveira", ("0 a 10 m³", "11 a 20 m³", "21 a 30 m³", "31 a 40 m³", "41 a 50 m³", "51 a 70 m³", ">70 m³")),
                "Sertãozinho": ("SAEMAS Sertãozinho", ("0 a 15 m³", "16 a 20 m³", "21 a 25 m³", "26 a 30 m³", "31 a 35 m³", "36 a 40 m³", "41 a 50 m³", "51 a 60 m³", "61 a 70 m³", "71 a 80 m³", "81 a 90 m³", "91 a 100 m³", ">100 m³")),
            }
            provider, bands = municipal_ares[row["municipio"]]
            for band in bands:
                clone = dict(row)
                clone["saneamento_prestador"] = provider
                clone["faixa_consumo_m3"] = band
                expanded_rows.append(clone)
        elif row.get("saneamento_prestador") == "BRK Ambiental Limeira" and row.get("categoria") == "Residencial normal":
            # A base original continha apenas o consumo mínimo. A Resolução
            # ARES-PCJ nº 705/2026 publica seis faixas em cascata.
            for band in ("0 a 10 m³", "11 a 15 m³", "16 a 30 m³", "31 a 60 m³", "61 a 100 m³", ">100 m³"):
                clone = dict(row)
                clone["faixa_consumo_m3"] = band
                expanded_rows.append(clone)
        elif row.get("saneamento_prestador") == "SAMAE Mogi Guaçu" and row.get("categoria") == "Residencial normal":
            for band in ("0 a 10 m³", "11 a 15 m³", "16 a 20 m³", "21 a 30 m³", "31 a 40 m³", "41 a 50 m³", ">50 m³"):
                clone = dict(row)
                clone["faixa_consumo_m3"] = band
                expanded_rows.append(clone)
        elif row.get("saneamento_prestador") == "SAAE Itapira" and row.get("categoria") == "Residencial normal":
            for band in ("0 a 15 m³", "16 a 20 m³", "21 a 30 m³", "31 a 35 m³", "36 a 40 m³", "41 a 50 m³", ">50 m³"):
                clone = dict(row)
                clone["faixa_consumo_m3"] = band
                expanded_rows.append(clone)
        elif row.get("saneamento_prestador") == "Companhia Ituana de Saneamento (CIS)" and row.get("categoria") == "Residencial normal":
            for band in ("0 a 10 m³", "11 a 20 m³", "21 a 30 m³", "31 a 50 m³", ">50 m³"):
                clone = dict(row)
                clone["faixa_consumo_m3"] = band
                expanded_rows.append(clone)
        elif row.get("saneamento_prestador") == "SAAE Mogi Mirim" and row.get("categoria") == "Residencial normal":
            for band in ("0 a 10 m³", "11 a 15 m³", "16 a 20 m³", "21 a 30 m³", "31 a 40 m³", "41 a 50 m³", "51 a 75 m³", "76 a 100 m³", ">100 m³"):
                clone = dict(row)
                clone["faixa_consumo_m3"] = band
                expanded_rows.append(clone)
        elif row.get("saneamento_prestador") in {
            "SAAE Lucas do Rio Verde", "Águas Pontes e Lacerda / Norte Saneamento",
            "Águas do Pantanal (autarquia municipal)", "Águas da Imperatriz", "Águas Cuiabá (Iguá)",
            "SAAE Itabirito", "CODAU Uberaba",
        } and row.get("categoria") == "Residencial normal":
            official_expansion = {
                "SAAE Lucas do Rio Verde": {
                    "0a10m3": ("0 a 10 m³",), "11a20m3": ("11 a 20 m³",),
                    "21a30m3": ("21 a 25 m³", "26 a 35 m³"),
                    "30m3": ("36 a 50 m³", ">50 m³"),
                },
                "Águas Pontes e Lacerda / Norte Saneamento": {
                    "0a10m3": ("0 a 10 m³",), "11a20m3": ("11 a 20 m³",),
                    "21a30m3": ("21 a 30 m³",), "30m3": ("31 a 40 m³", ">40 m³"),
                },
                "Águas do Pantanal (autarquia municipal)": {
                    "0a10m3": ("0 a 10 m³",), "11a20m3": ("11 a 20 m³",),
                    "21a30m3": ("21 a 30 m³",), "30m3": ("31 a 40 m³", ">40 m³"),
                },
                "Águas da Imperatriz": {
                    "0a10m3": ("0 a 15 m³",), "11a20m3": ("16 a 30 m³",),
                    "21a50m3": ("31 a 45 m³", "46 a 60 m³"), "50m3": (">60 m³",),
                },
                "Águas Cuiabá (Iguá)": {
                    "0a10m3": ("0 a 10 m³",), "11a20m3": ("10,1 a 20 m³",),
                    "21a30m3": ("20,1 a 30 m³",), "30m3": ("30,1 a 50 m³", ">50 m³"),
                },
                "SAAE Itabirito": {
                    "0a10m3": ("0 a 5 m³", "6 a 10 m³"),
                    "11a20m3": ("11 a 15 m³", "16 a 20 m³"),
                    "21a30m3": ("21 a 25 m³", "26 a 30 m³"),
                    "30m3": ("31 a 40 m³", "41 a 50 m³", "51 a 75 m³", "76 a 100 m³", "101 a 200 m³", ">200 m³"),
                },
                "CODAU Uberaba": {
                    "0a10m3": ("0 a 10 m³",), "11a20m3": ("11 a 20 m³",),
                    "21a30m3": ("21 a 30 m³",),
                    "30m3": ("31 a 50 m³", "51 a 100 m³", "101 a 200 m³", ">200 m³"),
                },
            }
            source_band = key_text(row.get("faixa_consumo_m3", ""))
            for band in official_expansion[row["saneamento_prestador"]].get(source_band, ()):
                clone = dict(row)
                clone["faixa_consumo_m3"] = band
                expanded_rows.append(clone)
        else:
            expanded_rows.append(row)
    rows = expanded_rows
    geo_names = list(json.loads(GEO.read_text(encoding="utf-8")).keys())
    by_key = defaultdict(list)
    for name in geo_names:
        by_key[key_text(name)].append(name)
    ares_city_configs = {
        "SAAE Itabirito": {
            "precision": 4,
            "pct": "60", "vigencia": "Vigente desde agosto de 2026", "status": "OFICIAL_ATUAL_RECONCILIADO",
            "rates": {
                "0a5m3": (1.6601, 22.7266, 0.99606, 13.6360), "6a10m3": (1.9517, None, 1.17102, None),
                "11a15m3": (3.8360, None, 2.30160, None), "16a20m3": (5.6441, None, 3.38646, None),
                "21a25m3": (6.1947, None, 3.71682, None), "26a30m3": (6.8280, None, 4.09680, None),
                "31a40m3": (7.4886, None, 4.49316, None), "41a50m3": (8.2872, None, 4.97232, None),
                "51a75m3": (9.0855, None, 5.45130, None), "76a100m3": (9.9942, None, 5.99652, None),
                "101a200m3": (10.9851, None, 6.59106, None), "200m3": (12.0865, None, 7.25190, None),
            },
            "note": "Doze faixas residenciais conciliadas com o Anexo I da Resolução ARISB-MG nº 406/2026; tarifa básica operacional residencial de água e esgoto preservada e esgoto equivalente a 60% da água.",
        },
        "CODAU Uberaba": {
            "precision": 4,
            "pct": "95", "vigencia": "Vigente desde março de 2026", "status": "OFICIAL_ATUAL_RECONCILIADO",
            "rates": {
                "0a10m3": (3.9110, None, 3.71545, None), "11a20m3": (5.1966, None, 4.93677, None),
                "21a30m3": (5.7411, None, 5.45405, None), "31a50m3": (6.1268, None, 5.82046, None),
                "51a100m3": (6.8758, None, 6.53201, None), "101a200m3": (7.0346, None, 6.68287, None),
                "200m3": (7.2843, None, 6.92009, None),
            },
            "note": "Sete faixas residenciais conciliadas com o Anexo I da Resolução ARISB-MG nº 383/2026; esgoto calculado a 95% da tarifa de água, conforme o ato.",
        },
        "SAAEB Barretos": {
            "pct": "50", "vigencia": "Vigente desde setembro de 2025; tabela sucessora ainda não aplicável na data de corte",
            "status": "OFICIAL_ATUAL_RECONCILIADO_COM_CORTE_TEMPORAL",
            "rates": {
                "0a10m3": (None, 28.90, None, 14.45), "11a15m3": (5.99, None, 3.00, None),
                "16a20m3": (6.71, None, 3.35, None), "21a25m3": (7.58, None, 3.79, None),
                "26a30m3": (8.64, None, 4.32, None), "31a35m3": (9.94, None, 4.97, None),
                "36a40m3": (11.54, None, 5.77, None), "41a50m3": (13.50, None, 6.75, None),
                "51a100m3": (15.91, None, 7.96, None), "100m3": (17.18, None, 8.59, None),
            },
            "note": "Dez faixas residenciais conciliadas com a Resolução ARES-PCJ nº 643/2025; esgoto equivale a 50% da água. A Resolução nº 718, de 30/07/2026, não foi antecipada porque dependia do prazo mínimo de 30 dias após publicação.",
        },
        "SAERP Ribeirão Preto": {
            "pct": "127.5", "vigencia": "Vigente desde maio de 2026",
            "status": "OFICIAL_ATUAL_RECONCILIADO_COM_TRATAMENTO",
            "rates": {
                "0a10m3": (None, 14.06, None, 17.92), "11a15m3": (2.48, None, 3.16, None),
                "16a20m3": (3.93, None, 5.03, None), "21a25m3": (5.39, None, 6.86, None),
                "26a30m3": (7.18, None, 9.12, None), "31a40m3": (9.33, None, 11.88, None),
                "41a50m3": (12.57, None, 16.02, None), "51a80m3": (15.77, None, 20.11, None),
                "81a100m3": (19.02, None, 24.22, None), "100m3": (21.87, None, 27.90, None),
            },
            "note": "Dez faixas residenciais conciliadas com a Resolução ARES-PCJ nº 690/2026 retificada. A coluna de esgoto agrega coleta/afastamento e tratamento, mantendo os valores publicados sem inferência por percentual.",
        },
        "DAAE Rio Claro": {
            "pct": "100", "vigencia": "Vigente desde fevereiro de 2026", "status": "OFICIAL_ATUAL_RECONCILIADO",
            "rates": {
                "0a10m3": (None, 35.36, None, 35.36), "11a20m3": (7.19, None, 7.19, None),
                "21a50m3": (10.77, None, 10.77, None), "51a100m3": (15.55, None, 15.55, None),
                "100m3": (17.91, None, 17.91, None),
            },
            "note": "Cinco faixas residenciais de água e esgoto conciliadas com a Resolução ARES-PCJ nº 681/2026; os dois serviços têm valores idênticos.",
        },
        "SeMAE Rio Preto": {
            "pct": "100", "vigencia": "Vigente em agosto de 2026, após o prazo legal mínimo", "status": "OFICIAL_ATUAL_RECONCILIADO",
            "rates": {
                "0a10m3": (None, 26.63, None, 26.63), "11a20m3": (3.84, None, 3.84, None),
                "21a30m3": (5.25, None, 5.25, None), "31a40m3": (6.99, None, 6.99, None),
                "41a50m3": (8.64, None, 8.64, None), "51a100m3": (13.14, None, 13.14, None),
                "100m3": (14.59, None, 14.59, None),
            },
            "note": "Sete faixas residenciais padrão conciliadas com a Resolução ARES-PCJ nº 715/2026; água e esgoto têm valores idênticos e cobrança em cascata.",
        },
        "SANASA Campinas": {
            "pct": "123", "vigencia": "Vigente desde fevereiro de 2026", "status": "OFICIAL_ATUAL_RECONCILIADO_COM_TRATAMENTO",
            "rates": {
                "0a10m3": (None, 53.65, None, 65.99), "11a15m3": (9.96, None, 12.25, None),
                "16a20m3": (10.18, None, 12.52, None), "21a25m3": (10.43, None, 12.82, None),
                "26a30m3": (12.82, None, 15.77, None), "31a50m3": (13.65, None, 16.79, None),
                "50m3": (20.94, None, 25.75, None),
            },
            "note": "Sete faixas residenciais padrão conciliadas com a Resolução ARES-PCJ nº 679/2025. A coluna de esgoto agrega coleta/afastamento e tratamento; a cobrança por tarifa e parcela a deduzir é representada de forma progressiva equivalente.",
        },
        "SAAE Salto": {
            "pct": "100", "vigencia": "Vigente desde novembro de 2025", "status": "OFICIAL_ATUAL_RECONCILIADO_COM_TRATAMENTO",
            "rates": {
                "0a10m3": (None, 32.22, None, 31.70), "11a15m3": (3.60, None, 3.49, None),
                "16a20m3": (3.92, None, 3.91, None), "21a25m3": (4.31, None, 4.35, None),
                "26a30m3": (4.77, None, 4.90, None), "31a35m3": (5.27, None, 5.75, None),
                "36a40m3": (6.34, None, 6.82, None), "41a60m3": (8.07, None, 8.14, None),
                "61a80m3": (10.21, None, 10.38, None), "80m3": (13.58, None, 13.99, None),
            },
            "note": "Dez faixas residenciais conciliadas com a Resolução ARES-PCJ nº 658/2025. A coluna de esgoto agrega coleta/afastamento e tratamento publicados separadamente, preservando os valores exatos por faixa.",
        },
        "SAECIL Leme": {
            "pct": "85", "vigencia": "Tabela da Resolução ARES-PCJ nº 680/2025 vigente em 2026", "status": "OFICIAL_ATUAL_RECONCILIADO_ESGOTO_TRATADO",
            "rates": {
                "0a10m3": (None, 35.33, None, 30.04), "11a20m3": (4.03, None, 3.44, None),
                "21a30m3": (5.15, None, 4.39, None), "31a40m3": (6.62, None, 5.63, None),
                "41a50m3": (6.90, None, 5.87, None), "51a100m3": (9.23, None, 7.84, None),
                "100m3": (10.87, None, 9.24, None),
            },
            "note": "Sete faixas residenciais conciliadas com a Resolução ARES-PCJ nº 680/2025. O cenário-base usa a coluna de coleta, afastamento e tratamento (85% da água), e não soma essa alternativa à tarifa de coleta simples.",
        },
        "SAE Louveira": {
            "pct": "85", "vigencia": "Resolução ARES-PCJ nº 687/2026", "status": "OFICIAL_ATUAL_RECONCILIADO",
            "rates": {
                "0a10m3": (None, 27.93, None, 23.74), "11a20m3": (3.78, None, 3.21, None),
                "21a30m3": (4.68, None, 3.98, None), "31a40m3": (6.43, None, 5.47, None),
                "41a50m3": (7.25, None, 6.16, None), "51a70m3": (10.21, None, 8.68, None),
                "70m3": (15.08, None, 12.82, None),
            },
            "note": "Sete faixas residenciais de água e esgoto conciliadas com a Resolução ARES-PCJ nº 687/2026; esgoto corresponde a 85% da água e ambos são cobrados em cascata.",
        },
        "SAEMAS Sertãozinho": {
            "pct": "80", "vigencia": "Tabela da Resolução ARES-PCJ nº 678/2025 vigente em 2026", "status": "OFICIAL_ATUAL_RECONCILIADO",
            "rates": {
                "0a15m3": (None, 25.31, None, 20.25), "16a20m3": (2.05, None, 1.64, None),
                "21a25m3": (4.81, None, 3.85, None), "26a30m3": (5.39, None, 4.31, None),
                "31a35m3": (5.83, None, 4.66, None), "36a40m3": (5.93, None, 4.74, None),
                "41a50m3": (6.46, None, 5.17, None), "51a60m3": (7.02, None, 5.62, None),
                "61a70m3": (7.67, None, 6.14, None), "71a80m3": (9.92, None, 7.94, None),
                "81a90m3": (12.03, None, 9.62, None), "91a100m3": (12.81, None, 10.25, None),
                "100m3": (13.20, None, 10.56, None),
            },
            "note": "Treze faixas residenciais conciliadas com a Resolução ARES-PCJ nº 678/2025; esgoto equivale a 80% da água e a cobrança é escalonada.",
        },
    }
    final_reconciliations = {
        "SAAE Lucas do Rio Verde": {
            "pct": "80", "vigencia": "Tabela oficial de 2026",
            "rates": {
                "0a10m3": (2.43, 1.944), "11a20m3": (3.12, 2.496),
                "21a25m3": (4.15, 3.32), "26a35m3": (5.96, 4.768),
                "36a50m3": (7.03, 5.624), "50m3": (8.20, 6.56),
            },
            "note": "Seis faixas residenciais e esgoto a 80% conciliados com a tabela oficial de 2026 e o Decreto nº 7.349/2025.",
        },
        "Águas Pontes e Lacerda / Norte Saneamento": {
            "pct": "90", "vigencia": "Estrutura tarifária 2026; aplicação publicada para março de 2026",
            "rates": {
                "0a10m3": (3.03, 2.72), "11a20m3": (4.55, 4.09),
                "21a30m3": (7.57, 6.81), "31a40m3": (9.99, 8.99),
                "40m3": (16.04, 14.44),
            },
            "note": "Cinco faixas residenciais conciliadas com o comunicado tarifário de 2026; preservados os valores nominais publicados para água e esgoto.",
        },
        "Águas do Pantanal (autarquia municipal)": {
            "pct": "50", "vigencia": "Tabela oficial consultada em 24/08/2026",
            "rates": {
                "0a10m3": (3.270, 1.635), "11a20m3": (5.716, 2.858),
                "21a30m3": (8.869, 4.4345), "31a40m3": (11.374, 5.687),
                "40m3": (15.882, 7.941),
            },
            "note": "Cinco faixas residenciais conciliadas com a tabela oficial; tratamento de esgoto representado como 50% da tarifa de água, conforme regra publicada.",
        },
        "Águas da Imperatriz": {
            "pct": "90", "vigencia": "Vigente desde 06/01/2026",
            "rates": {
                "0a15m3": (5.2836, 4.7551), "16a30m3": (11.6238, 10.4614),
                "31a45m3": (15.8506, 14.2655), "46a60m3": (31.7012, 28.5310),
                "60m3": (42.2682, 38.0414),
            },
            "note": "Cinco faixas domiciliares conciliadas com a Deliberação AGENERSA nº 4.995/2026; mantida a conta mínima regulatória de 15 m³ na observação.",
        },
        "Águas Cuiabá (Iguá)": {
            "pct": "90", "vigencia": "Vigente desde 20/03/2025",
            "rates": {
                "0a10m3": (4.92, 4.428), "101a20m3": (6.01, 5.409),
                "201a30m3": (10.06, 9.054), "301a50m3": (12.31, 11.079),
                "50m3": (16.29, 14.661),
            },
            "note": "Cinco faixas residenciais e esgoto a 90% conciliados com o comunicado oficial vigente desde 20/03/2025; consumo mínimo de 10 m³.",
        },
    }
    for row in rows:
        row.update({k: repair_text(v) for k, v in row.items()})
        if row.get("municipio") == "Pirassununga":
            row["saneamento_prestador"] = "SAEP Pirassununga"
        elif row.get("municipio") == "São José do Rio Pardo":
            row["saneamento_prestador"] = "SAERP São José do Rio Pardo"
        ares_config = ares_city_configs.get(row.get("saneamento_prestador"))
        if ares_config and row.get("categoria") == "Residencial normal":
            values = ares_config["rates"].get(key_text(row.get("faixa_consumo_m3", "")))
            if values:
                water, water_fixed, sewer, sewer_fixed = values
                precision = ares_config.get("precision", 2)
                row["tarifa_agua_r_m3"] = "" if water is None else f"{water:.{precision}f}"
                row["tarifa_agua_fixa_minima_r"] = "" if water_fixed is None else f"{water_fixed:.{precision}f}"
                row["tarifa_esgoto_r_m3"] = "" if sewer is None else f"{sewer:.{precision}f}"
                row["tarifa_esgoto_fixa_minima_r"] = "" if sewer_fixed is None else f"{sewer_fixed:.{precision}f}"
                row["esgoto_pct_sobre_agua"] = ares_config["pct"]
                row["vigencia_saneamento"] = ares_config["vigencia"]
                row["fonte_saneamento"] = SANITATION_EVIDENCE[row["saneamento_prestador"]]["url"]
                row["status_saneamento"] = ares_config["status"]
                row["observacao"] = ares_config["note"]
        final_config = final_reconciliations.get(row.get("saneamento_prestador"))
        if final_config and row.get("categoria") == "Residencial normal":
            values = final_config["rates"].get(key_text(row.get("faixa_consumo_m3", "")))
            if values:
                water, sewer = values
                row["tarifa_agua_r_m3"] = f"{water:.4f}"
                row["tarifa_agua_fixa_minima_r"] = ""
                row["tarifa_esgoto_r_m3"] = f"{sewer:.4f}"
                row["tarifa_esgoto_fixa_minima_r"] = ""
                row["esgoto_pct_sobre_agua"] = final_config["pct"]
                row["vigencia_saneamento"] = final_config["vigencia"]
                row["fonte_saneamento"] = SANITATION_EVIDENCE[row["saneamento_prestador"]]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["observacao"] = final_config["note"]
        if row.get("saneamento_prestador") == "SAAE Sete Lagoas" and row.get("categoria") == "Residencial normal":
            # A tabela oficial apresenta o valor básico operacional residencial
            # até 6 m³ e, em seguida, os pontos da matriz de excedentes.
            row["faixa_consumo_m3"] = "0 a 6 m³"
            row["tarifa_agua_r_m3"] = ""
            row["tarifa_agua_fixa_minima_r"] = "30.9599"
            row["tarifa_esgoto_r_m3"] = ""
            row["tarifa_esgoto_fixa_minima_r"] = "24.7679"
            row["esgoto_pct_sobre_agua"] = "80"
            row["vigencia_saneamento"] = "Vigente desde 03/03/2026"
            row["fonte_saneamento"] = SANITATION_EVIDENCE["SAAE Sete Lagoas"]["url"]
            row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO_FAIXA_MINIMA"
            row["observacao"] = (
                "Mínimo residencial de 6 m³ conciliado com a tabela oficial do Decreto nº 7.702/2026; "
                "esgoto corresponde a 80% da água. A matriz oficial de excedentes possui pontos de corte "
                "não convertidos em faixas contínuas para evitar interpretação indevida."
            )
        if row.get("saneamento_prestador") == "SAMAE Blumenau / BRK Ambiental Blumenau" and row.get("categoria") == "Residencial normal":
            blumenau_rates = {
                "010": (None, 47.43, None, 52.63),
                "1130": (8.63, None, 9.635, None),
                "30": (11.00, None, 12.279, None),
            }
            band_key = key_text(row.get("faixa_consumo_m3", ""))
            if band_key in blumenau_rates:
                water, water_fixed, sewer, sewer_fixed = blumenau_rates[band_key]
                row["tarifa_agua_r_m3"] = "" if water is None else f"{water:.2f}"
                row["tarifa_agua_fixa_minima_r"] = "" if water_fixed is None else f"{water_fixed:.2f}"
                row["tarifa_esgoto_r_m3"] = "" if sewer is None else f"{sewer:.3f}"
                row["tarifa_esgoto_fixa_minima_r"] = "" if sewer_fixed is None else f"{sewer_fixed:.2f}"
                row["esgoto_pct_sobre_agua"] = ""
                row["vigencia_saneamento"] = "Água desde 01/01/2026; esgoto desde 01/04/2026"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["SAMAE Blumenau / BRK Ambiental Blumenau"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["condicao_aplicacao_tarifa"] = (
                    "Água faturada pelo SAMAE e esgoto pela BRK, com estruturas próprias. Esgoto parcial para redes somente de afastamento: 50%."
                )
                row["observacao"] = (
                    "As três faixas de água foram conciliadas com a tabela SAMAE 2026 e as três faixas de esgoto com a "
                    "Carta de Serviços BRK/Decisão AGIR nº 325/2026; não foi presumida proporcionalidade entre as duas estruturas."
                )
        if key_text(row.get("saneamento_prestador", "")) == "semasaitajai" and row.get("categoria") == "Residencial normal":
            itajai_rates = {
                "010": (None, 41.70, None, 33.36),
                "1125": (7.48, None, 5.984, None),
                "25": (10.38, None, 8.304, None),
            }
            band_key = key_text(row.get("faixa_consumo_m3", ""))
            if band_key in itajai_rates:
                water, water_fixed, sewer, sewer_fixed = itajai_rates[band_key]
                row["tarifa_agua_r_m3"] = "" if water is None else f"{water:.2f}"
                row["tarifa_agua_fixa_minima_r"] = "" if water_fixed is None else f"{water_fixed:.2f}"
                row["tarifa_esgoto_r_m3"] = "" if sewer is None else f"{sewer:.3f}"
                row["tarifa_esgoto_fixa_minima_r"] = "" if sewer_fixed is None else f"{sewer_fixed:.2f}"
                row["esgoto_pct_sobre_agua"] = "80"
                row["vigencia_saneamento"] = "Vigente para faturas com vencimento desde 05/10/2025"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["SEMASA Itajaí"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["observacao"] = (
                    "Tarifa mínima, duas faixas excedentes e taxa de esgoto de 80% conciliadas com a tabela do SEMASA e "
                    "o Decreto nº 13.761/2025."
                )
        if key_text(row.get("saneamento_prestador", "")) == "samaejaraguadosul" and row.get("categoria") == "Residencial normal":
            jaragua_rates = {
                "05": 1.59, "610": 1.80, "1115": 8.05, "1620": 10.23,
                "2125": 11.37, "2630": 12.49, "30": 14.79,
            }
            band_key = key_text(row.get("faixa_consumo_m3", ""))
            if band_key in jaragua_rates:
                water = jaragua_rates[band_key]
                row["tarifa_agua_r_m3"] = f"{water:.2f}"
                row["tarifa_agua_fixa_minima_r"] = "30.16"
                row["tarifa_esgoto_r_m3"] = f"{0.8 * water:.3f}"
                row["tarifa_esgoto_fixa_minima_r"] = "24.13"
                row["tarifa_esgoto_coleta_afastamento_r_m3"] = f"{0.2 * water:.3f}"
                row["tarifa_esgoto_coleta_afastamento_fixa_r"] = "6.03"
                row["esgoto_pct_sobre_agua"] = "80"
                row["vigencia_saneamento"] = "Tabela tarifária do exercício de 2026"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["SAMAE Jaraguá do Sul"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["condicao_aplicacao_tarifa"] = "Esgoto convencional = 80% da água; sistema coletivo com fossa/filtro mantido pelo SAMAE = 20%."
                row["observacao"] = (
                    "TBO de água e esgoto e sete faixas residenciais conciliadas com a tabela oficial 2026; "
                    "registradas separadamente as modalidades de esgoto de 80% e 20%."
                )
        if key_text(row.get("saneamento_prestador", "")) == "emasabalneariocamboriu" and row.get("categoria") == "Residencial normal":
            emasa_rates = {"010": 0.6585, "1125": 4.6959, "25": 7.8312}
            band_key = key_text(row.get("faixa_consumo_m3", ""))
            if band_key in emasa_rates:
                water = emasa_rates[band_key]
                row["tarifa_agua_r_m3"] = f"{water:.4f}"
                row["tarifa_agua_fixa_minima_r"] = "44.95"
                row["tarifa_esgoto_r_m3"] = f"{water:.4f}"
                row["tarifa_esgoto_fixa_minima_r"] = ""
                row["esgoto_pct_sobre_agua"] = "80"
                row["vigencia_saneamento"] = "Vigente desde 04/05/2026"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["EMASA Balneário Camboriú"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["condicao_aplicacao_tarifa"] = (
                    "A tarifa unitária de esgoto é igual à de água, aplicada sobre volume de esgoto equivalente a 80% do volume faturado de água; "
                    "a TFDI residencial de R$ 44,95 é cobrada uma vez por unidade consumidora."
                )
                row["observacao"] = (
                    "TFDI e três faixas residenciais conciliadas com o Anexo I da Deliberação ARIS nº 15/2026. "
                    "Corrigida a modelagem para não duplicar a TFDI nem reduzir simultaneamente tarifa e volume do esgoto."
                )
        if key_text(row.get("saneamento_prestador", "")) == "semasalages" and row.get("categoria") == "Residencial normal":
            lages_rates = {
                "010": (None, 44.00, None, 35.20),
                "1125": (7.48, None, 5.98, None),
                "25": (10.20, None, 8.16, None),
            }
            band_key = key_text(row.get("faixa_consumo_m3", ""))
            if band_key in lages_rates:
                water, water_fixed, sewer, sewer_fixed = lages_rates[band_key]
                row["tarifa_agua_r_m3"] = "" if water is None else f"{water:.2f}"
                row["tarifa_agua_fixa_minima_r"] = "" if water_fixed is None else f"{water_fixed:.2f}"
                row["tarifa_esgoto_r_m3"] = "" if sewer is None else f"{sewer:.2f}"
                row["tarifa_esgoto_fixa_minima_r"] = "" if sewer_fixed is None else f"{sewer_fixed:.2f}"
                row["esgoto_pct_sobre_agua"] = "80"
                row["vigencia_saneamento"] = "Tabela tarifária do exercício de 2026"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["SEMASA Lages"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["observacao"] = (
                    "Tarifa mínima e duas faixas excedentes de água e esgoto conciliadas com o Anexo I municipal de 2026; "
                    "preservado o arredondamento oficial de R$ 5,98 para o esgoto da faixa intermediária."
                )
        if key_text(row.get("saneamento_prestador", "")) == "tubaraosaneamento" and row.get("categoria") == "Residencial normal":
            tubarao_rates = {
                "010": 5.25, "1120": 9.68, "2130": 11.11,
                "3150": 13.59, "50": 16.29,
            }
            band_key = key_text(row.get("faixa_consumo_m3", ""))
            if band_key in tubarao_rates:
                rate = tubarao_rates[band_key]
                row["tarifa_agua_r_m3"] = f"{rate:.2f}"
                row["tarifa_agua_fixa_minima_r"] = ""
                row["tarifa_esgoto_r_m3"] = f"{rate:.2f}"
                row["tarifa_esgoto_fixa_minima_r"] = ""
                row["esgoto_pct_sobre_agua"] = "100"
                row["vigencia_saneamento"] = "Vigente de 01/05/2026 a 30/04/2027"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["Tubarão Saneamento"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["observacao"] = (
                    "Cinco faixas residenciais de água e esgoto conciliadas com a matriz tarifária 2026/2027; "
                    "os valores de água e esgoto são publicados separadamente e são iguais em todas as faixas."
                )
        if key_text(row.get("saneamento_prestador", "")) == "samaebrusque" and row.get("categoria") == "Residencial normal":
            brusque_rates = {
                "010": (None, 42.38), "1115": (7.80, None),
                "1620": (10.01, None), "2125": (11.37, None),
                "2650": (12.54, None), "50": (13.18, None),
            }
            band_key = key_text(row.get("faixa_consumo_m3", ""))
            if band_key in brusque_rates:
                water, water_fixed = brusque_rates[band_key]
                row["tarifa_agua_r_m3"] = "" if water is None else f"{water:.2f}"
                row["tarifa_agua_fixa_minima_r"] = "" if water_fixed is None else f"{water_fixed:.2f}"
                # Em agosto de 2026 a concessão de esgoto ainda estava em operação
                # assistida/implantação. Não tratar a tarifa contratual futura como
                # cobrança corrente evita inflar artificialmente a economia simulada.
                row["tarifa_esgoto_r_m3"] = ""
                row["tarifa_esgoto_fixa_minima_r"] = ""
                row["esgoto_pct_sobre_agua"] = "0"
                row["vigencia_saneamento"] = "Tarifa de água vigente desde 17/05/2026; esgoto ainda não faturado no cenário atual"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["SAMAE Brusque"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO_SEM_COBRANCA_ESGOTO"
                row["observacao"] = (
                    "Seis faixas residenciais de água conciliadas com a tabela oficial de 2026. "
                    "A antiga parcela de esgoto de R$ 44,63 foi removida do cenário atual: a Prefeitura registra "
                    "a concessão em operação assistida e implantação, sem tarifa corrente publicada na tabela do SAMAE."
                )
        if key_text(row.get("saneamento_prestador", "")) == "samaegaspar" and row.get("categoria") == "Residencial normal":
            gaspar_rates = {
                "010": (None, 50.58), "1125": (7.81, None),
                "2640": (10.30, None), "4150": (12.49, None),
                "50": (14.31, None),
            }
            band_key = key_text(row.get("faixa_consumo_m3", ""))
            if band_key in gaspar_rates:
                water, water_fixed = gaspar_rates[band_key]
                row["tarifa_agua_r_m3"] = "" if water is None else f"{water:.2f}"
                row["tarifa_agua_fixa_minima_r"] = "" if water_fixed is None else f"{water_fixed:.2f}"
                # A tabela corrente do prestador caracteriza estes valores como
                # fatura mensal de água e não publica um multiplicador geral de
                # esgoto. A cobrança deve ser ativada apenas quando comprovada para
                # a unidade/trecho atendido, em vez de presumida para todo o município.
                row["tarifa_esgoto_r_m3"] = ""
                row["tarifa_esgoto_fixa_minima_r"] = ""
                row["esgoto_pct_sobre_agua"] = "0"
                row["vigencia_saneamento"] = "Tarifa de água vigente desde 01/07/2026; adicional de esgoto condicionado à unidade atendida"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["SAMAE Gaspar"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO_ESGOTO_CONDICIONAL"
                row["observacao"] = (
                    "Tarifa mínima e quatro faixas excedentes reconciliadas com a imagem oficial vigente do SAMAE. "
                    "A notícia oficial vincula a tabela à Decisão AGIR nº 332/2026 e ao reajuste de 4,669%. "
                    "Removido do cenário-base o espelhamento automático de 100% para esgoto, que não consta da tabela corrente."
                )
        if row.get("saneamento_prestador") == "BRK Ambiental Limeira" and row.get("categoria") == "Residencial normal":
            limeira_rates = {
                "0a10m3": (None, 37.10), "11a15m3": (5.11, None),
                "16a30m3": (10.14, None), "31a60m3": (13.18, None),
                "61a100m3": (16.48, None), "100m3": (20.60, None),
            }
            band_key = key_text(row.get("faixa_consumo_m3", ""))
            if band_key in limeira_rates:
                rate, fixed = limeira_rates[band_key]
                row["tarifa_agua_r_m3"] = "" if rate is None else f"{rate:.2f}"
                row["tarifa_agua_fixa_minima_r"] = "" if fixed is None else f"{fixed:.2f}"
                row["tarifa_esgoto_r_m3"] = "" if rate is None else f"{rate:.2f}"
                row["tarifa_esgoto_fixa_minima_r"] = "" if fixed is None else f"{fixed:.2f}"
                row["esgoto_pct_sobre_agua"] = "100"
                row["vigencia_saneamento"] = "Contas emitidas desde julho de 2026"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["BRK Ambiental Limeira"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["observacao"] = (
                    "Seis faixas residenciais de água e esgoto conciliadas com o Anexo I da Resolução ARES-PCJ nº 705/2026. "
                    "Ambos os serviços usam os mesmos valores e cobrança em cascata; o total mínimo é R$ 74,20."
                )
        if row.get("saneamento_prestador") == "SAMAE Mogi Guaçu" and row.get("categoria") == "Residencial normal":
            mogi_guacu_rates = {
                "0a10m3": (None, 18.91), "11a15m3": (2.29, None),
                "16a20m3": (2.82, None), "21a30m3": (7.52, None),
                "31a40m3": (7.58, None), "41a50m3": (9.34, None),
                "50m3": (10.74, None),
            }
            band_key = key_text(row.get("faixa_consumo_m3", ""))
            if band_key in mogi_guacu_rates:
                rate, fixed = mogi_guacu_rates[band_key]
                row["tarifa_agua_r_m3"] = "" if rate is None else f"{rate:.2f}"
                row["tarifa_agua_fixa_minima_r"] = "" if fixed is None else f"{fixed:.2f}"
                row["tarifa_esgoto_r_m3"] = "" if rate is None else f"{rate:.2f}"
                row["tarifa_esgoto_fixa_minima_r"] = "" if fixed is None else f"{fixed:.2f}"
                row["esgoto_pct_sobre_agua"] = "100"
                row["vigencia_saneamento"] = "Resolução ARES-PCJ nº 686/2026"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["SAMAE Mogi Guaçu"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["observacao"] = (
                    "Sete faixas residenciais de água e esgoto conciliadas com o Anexo I da Resolução ARES-PCJ nº 686/2026. "
                    "A representação progressiva é algebricamente equivalente à tarifa por faixa menos a parcela a deduzir publicada."
                )
        if row.get("saneamento_prestador") == "SAAE Itapira" and row.get("categoria") == "Residencial normal":
            itapira_rates = {
                "0a15m3": (None, 22.71), "16a20m3": (7.29, None),
                "21a30m3": (8.27, None), "31a35m3": (8.37, None),
                "36a40m3": (8.50, None), "41a50m3": (8.67, None),
                "50m3": (10.44, None),
            }
            band_key = key_text(row.get("faixa_consumo_m3", ""))
            if band_key in itapira_rates:
                rate, fixed = itapira_rates[band_key]
                row["tarifa_agua_r_m3"] = "" if rate is None else f"{rate:.2f}"
                row["tarifa_agua_fixa_minima_r"] = "" if fixed is None else f"{fixed:.2f}"
                row["tarifa_esgoto_r_m3"] = "" if rate is None else f"{rate:.2f}"
                row["tarifa_esgoto_fixa_minima_r"] = "" if fixed is None else f"{fixed:.2f}"
                row["esgoto_pct_sobre_agua"] = "100"
                row["vigencia_saneamento"] = "Vigente desde junho de 2026"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["SAAE Itapira"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["observacao"] = (
                    "Sete faixas residenciais conciliadas com o Anexo I da Resolução ARES-PCJ nº 698/2026; "
                    "a resolução confirma cobrança em cascata e esgoto equivalente a 100% da tarifa de água."
                )
        if row.get("saneamento_prestador") == "Companhia Ituana de Saneamento (CIS)" and row.get("categoria") == "Residencial normal":
            itu_rates = {
                "0a10m3": (None, 36.96), "11a20m3": (4.34, None),
                "21a30m3": (6.63, None), "31a50m3": (6.63, None),
                "50m3": (7.94, None),
            }
            band_key = key_text(row.get("faixa_consumo_m3", ""))
            if band_key in itu_rates:
                rate, fixed = itu_rates[band_key]
                row["tarifa_agua_r_m3"] = "" if rate is None else f"{rate:.2f}"
                row["tarifa_agua_fixa_minima_r"] = "" if fixed is None else f"{fixed:.2f}"
                row["tarifa_esgoto_r_m3"] = "" if rate is None else f"{rate:.2f}"
                row["tarifa_esgoto_fixa_minima_r"] = "" if fixed is None else f"{fixed:.2f}"
                row["esgoto_pct_sobre_agua"] = "100"
                row["vigencia_saneamento"] = "Vigente desde maio de 2026"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["Companhia Ituana de Saneamento (CIS)"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["observacao"] = (
                    "Cinco faixas residenciais conciliadas com a Resolução ARES-PCJ nº 693/2026; "
                    "a revisão equiparou o esgoto de 80% para 100% da água e confirmou cobrança em cascata."
                )
        if row.get("saneamento_prestador") == "SAAE Mogi Mirim" and row.get("categoria") == "Residencial normal":
            mogi_mirim_rates = {
                "0a10m3": (None, 20.25, None, 28.35),
                "11a15m3": (2.22, None, 3.11, None),
                "16a20m3": (9.09, None, 12.73, None),
                "21a30m3": (9.17, None, 12.84, None),
                "31a40m3": (9.56, None, 13.38, None),
                "41a50m3": (10.05, None, 14.07, None),
                "51a75m3": (10.66, None, 14.92, None),
                "76a100m3": (11.67, None, 16.34, None),
                "100m3": (12.75, None, 17.85, None),
            }
            band_key = key_text(row.get("faixa_consumo_m3", ""))
            if band_key in mogi_mirim_rates:
                water, water_fixed, sewer_effective, sewer_fixed = mogi_mirim_rates[band_key]
                row["tarifa_agua_r_m3"] = "" if water is None else f"{water:.2f}"
                row["tarifa_agua_fixa_minima_r"] = "" if water_fixed is None else f"{water_fixed:.2f}"
                row["tarifa_esgoto_r_m3"] = "" if sewer_effective is None else f"{sewer_effective:.2f}"
                row["tarifa_esgoto_fixa_minima_r"] = "" if sewer_fixed is None else f"{sewer_fixed:.2f}"
                row["esgoto_pct_sobre_agua"] = "140"
                row["vigencia_saneamento"] = "Vigente desde julho de 2026"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["SAAE Mogi Mirim"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO_COM_TCTE"
                row["observacao"] = (
                    "Nove faixas residenciais conciliadas com a Resolução ARES-PCJ nº 706/2026. "
                    "A coluna de esgoto do modelo agrega tarifa de esgoto (100% da água) e TCTE (40%), "
                    "preservando o total sanitário efetivamente evitável sem contar a água duas vezes."
                )
        if key_text(row.get("saneamento_prestador", "")) == "aguasdebarradogarcasaegea" and row.get("categoria") == "Residencial normal":
            barra_rates = {
                "0a10m3": (4.33, 3.46), "11a20m3": (6.50, 5.20),
                "21a30m3": (10.83, 8.66), "31a40m3": (14.29, 11.43),
                "40m3": (22.95, 18.36),
            }
            band_key = key_text(row.get("faixa_consumo_m3", ""))
            if band_key in barra_rates:
                water, sewer = barra_rates[band_key]
                row["tarifa_agua_r_m3"] = f"{water:.2f}"
                row["tarifa_agua_fixa_minima_r"] = ""
                row["tarifa_esgoto_r_m3"] = f"{sewer:.2f}"
                row["tarifa_esgoto_fixa_minima_r"] = ""
                row["esgoto_pct_sobre_agua"] = "80"
                row["vigencia_saneamento"] = "Vigente desde janeiro de 2026"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["Águas de Barra do Garças"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["observacao"] = (
                    "Cinco faixas residenciais de água e esgoto conciliadas com a seção 'Tarifas em vigor' da concessionária. "
                    "O histórico oficial identifica os reajustes e revisões de janeiro de 2026."
                )
        if key_text(row.get("saneamento_prestador", "")) == "aguasdesinopaegea" and row.get("categoria") == "Residencial normal":
            sinop_rates = {
                "0a10m3": 6.015, "11a20m3": 8.541,
                "21a30m3": 14.316, "30m3": 17.925,
            }
            band_key = key_text(row.get("faixa_consumo_m3", ""))
            if band_key in sinop_rates:
                rate = sinop_rates[band_key]
                row["tarifa_agua_r_m3"] = f"{rate:.3f}"
                row["tarifa_agua_fixa_minima_r"] = ""
                row["tarifa_esgoto_r_m3"] = f"{rate:.3f}"
                row["tarifa_esgoto_fixa_minima_r"] = ""
                row["esgoto_pct_sobre_agua"] = "100"
                row["vigencia_saneamento"] = "Estrutura vigente após as parcelas/reajustes de junho de 2026"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["Águas de Sinop"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["observacao"] = (
                    "Quatro faixas residenciais de água e esgoto conciliadas com a tabela 'Tarifas em vigor'. "
                    "A página oficial registra os reajustes de março e junho e a revisão de janeiro de 2026."
                )
        if key_text(row.get("saneamento_prestador", "")) == "aguasdeprimaveraaegea" and row.get("categoria") == "Residencial normal":
            primavera_rates = {
                "0a10m3": (5.76, 5.18), "11a20m3": (8.64, 7.78),
                "21a30m3": (14.40, 12.96), "31a40m3": (19.01, 17.11),
                "40m3": (26.90, 24.19),
            }
            band_key = key_text(row.get("faixa_consumo_m3", ""))
            if band_key in primavera_rates:
                water, sewer = primavera_rates[band_key]
                row["tarifa_agua_r_m3"] = f"{water:.2f}"
                row["tarifa_agua_fixa_minima_r"] = ""
                row["tarifa_esgoto_r_m3"] = f"{sewer:.2f}"
                row["tarifa_esgoto_fixa_minima_r"] = ""
                row["esgoto_pct_sobre_agua"] = "90"
                row["vigencia_saneamento"] = "Vigente desde janeiro de 2026"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["Águas de Primavera"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["observacao"] = (
                    "Cinco faixas residenciais de água e esgoto conciliadas com a tabela 'Tarifas em vigor'; "
                    "a página oficial registra reajuste e duas parcelas revisionais aplicadas em janeiro de 2026."
                )
        if key_text(row.get("saneamento_prestador", "")) == "aguasdesorrisoaegea" and row.get("categoria") == "Residencial normal":
            # Normaliza o nome para a mesma chave usada no catálogo de evidências;
            # o sufixo corporativo não representa outro prestador/tarifário.
            row["saneamento_prestador"] = "Águas de Sorriso"
            sorriso_rates = {
                "0a10m3": (3.062, 2.450), "11a20m3": (4.593, 3.674),
                "21a30m3": (7.655, 6.124), "31a40m3": (11.483, 9.186),
                "40m3": (18.035, 14.422),
            }
            band_key = key_text(row.get("faixa_consumo_m3", ""))
            if band_key in sorriso_rates:
                water, sewer = sorriso_rates[band_key]
                row["tarifa_agua_r_m3"] = f"{water:.3f}"
                row["tarifa_agua_fixa_minima_r"] = ""
                row["tarifa_esgoto_r_m3"] = f"{sewer:.3f}"
                row["tarifa_esgoto_fixa_minima_r"] = ""
                row["esgoto_pct_sobre_agua"] = "80"
                row["vigencia_saneamento"] = "Vigente desde novembro de 2025"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["Águas de Sorriso"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["observacao"] = (
                    "Cinco faixas residenciais de água e esgoto conciliadas com a primeira estrutura indicada como vigente "
                    "na página oficial; reajuste de 4,39% autorizado pela AGER-Sorriso em novembro de 2025."
                )
        if row.get("saneamento_prestador") == "SAAE Nova Mutum" and row.get("categoria") == "Residencial normal":
            nova_mutum_rates = {
                "0a10m3": (None, 24.82), "11a20m3": (5.22, None),
                "21a30m3": (7.54, None), "31a40m3": (9.28, None),
                "41a50m3": (11.59, None), "50m3": (13.92, None),
            }
            band_key = key_text(row.get("faixa_consumo_m3", ""))
            if band_key in nova_mutum_rates:
                water, fixed = nova_mutum_rates[band_key]
                row["tarifa_agua_r_m3"] = "" if water is None else f"{water:.2f}"
                row["tarifa_agua_fixa_minima_r"] = "" if fixed is None else f"{fixed:.2f}"
                row["tarifa_esgoto_r_m3"] = ""
                row["tarifa_esgoto_fixa_minima_r"] = ""
                row["esgoto_pct_sobre_agua"] = "0"
                row["vigencia_saneamento"] = "Vigente desde abril de 2025; mantida como vigente pelo SAAE em 24/08/2026"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["SAAE Nova Mutum"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["observacao"] = (
                    "Tarifa mínima e cinco faixas excedentes conciliadas com o Anexo I do Decreto nº 17/2025, "
                    "que a página do SAAE ainda identifica como tarifa vigente. A fatura oficial confirma E (%) = 0,0."
                )
        if row.get("saneamento_prestador") == "SAEMA Araras" and row.get("categoria") == "Residencial normal":
            araras_rates = {
                "0 a 10 m3": (None, 25.71, None, 20.57),
                "11 a 20 m3": (3.21, None, 2.57, None),
                "21 a 30 m3": (4.13, None, 3.30, None),
                "31 a 50 m3": (5.58, None, 4.46, None),
                "51 a 100 m3": (7.82, None, 6.26, None),
                "101 a 500 m3": (11.34, None, 9.07, None),
                "501 a 5.000 m3": (17.02, None, 13.62, None),
                ">5.000 m3": (26.39, None, 21.11, None),
            }
            band_key = unicodedata.normalize("NFKD", row.get("faixa_consumo_m3", "")).encode("ascii", "ignore").decode().strip()
            if band_key in araras_rates:
                water, water_fixed, sewer, sewer_fixed = araras_rates[band_key]
                row["tarifa_agua_r_m3"] = "" if water is None else f"{water:.2f}"
                row["tarifa_agua_fixa_minima_r"] = "" if water_fixed is None else f"{water_fixed:.2f}"
                row["tarifa_esgoto_r_m3"] = "" if sewer is None else f"{sewer:.2f}"
                row["tarifa_esgoto_fixa_minima_r"] = "" if sewer_fixed is None else f"{sewer_fixed:.2f}"
                row["esgoto_pct_sobre_agua"] = "80"
                row["vigencia_saneamento"] = "Vigente desde dezembro de 2025"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["SAEMA Araras"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["observacao"] = (
                    "Tarifa mínima e sete faixas incrementais residenciais conciliadas com a Resolução "
                    "ARES-PCJ nº 662/2025; esgoto equivale a 80% da água."
                )
        if row.get("saneamento_prestador") == "BRK Ambiental Sumaré" and row.get("categoria") == "Residencial normal":
            sumare_rates = {
                "0 a 10 m3": (None, 36.35, None, 29.08, None, 7.27),
                "11 a 20 m3": (3.64, None, 2.91, None, 0.73, None),
                "21 a 30 m3": (4.01, None, 3.21, None, 0.80, None),
                "31 a 50 m3": (5.64, None, 4.51, None, 1.13, None),
                ">50 m3": (7.57, None, 6.06, None, 1.51, None),
            }
            band_key = unicodedata.normalize("NFKD", row.get("faixa_consumo_m3", "")).encode("ascii", "ignore").decode().strip()
            if band_key in sumare_rates:
                water, water_fixed, sewer, sewer_fixed, treatment, treatment_fixed = sumare_rates[band_key]
                row["tarifa_agua_r_m3"] = "" if water is None else f"{water:.2f}"
                row["tarifa_agua_fixa_minima_r"] = "" if water_fixed is None else f"{water_fixed:.2f}"
                row["tarifa_esgoto_r_m3"] = "" if sewer is None else f"{sewer:.2f}"
                row["tarifa_esgoto_fixa_minima_r"] = "" if sewer_fixed is None else f"{sewer_fixed:.2f}"
                row["tarifa_tratamento_esgoto_r_m3"] = "" if treatment is None else f"{treatment:.2f}"
                row["tarifa_tratamento_esgoto_fixa_r"] = "" if treatment_fixed is None else f"{treatment_fixed:.2f}"
                row["esgoto_pct_sobre_agua"] = "80"
                row["vigencia_saneamento"] = "Vigente desde fevereiro de 2026"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["BRK Ambiental Sumaré"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["observacao"] = (
                    "Cinco faixas residenciais conciliadas com a Resolução ARES-PCJ nº 672/2025. "
                    "A coluna principal de esgoto representa coleta e afastamento (80% da água); o tratamento "
                    "regional, quando disponível, está registrado separadamente (20%)."
                )
        if row.get("saneamento_prestador") == "SANEBAVI Vinhedo" and row.get("categoria") == "Residencial normal":
            vinhedo_rates = {
                "0 a 10 m3": (None, 40.20, None, 32.16, None, 40.20),
                "11 a 15 m3": (4.56, None, 3.65, None, 4.56, None),
                "16 a 20 m3": (5.73, None, 4.58, None, 5.73, None),
                "21 a 35 m3": (8.00, None, 6.40, None, 8.00, None),
                "36 a 50 m3": (11.63, None, 9.30, None, 11.63, None),
                "51 a 75 m3": (16.92, None, 13.54, None, 16.92, None),
                ">75 m3": (22.82, None, 18.26, None, 22.82, None),
            }
            band_key = unicodedata.normalize("NFKD", row.get("faixa_consumo_m3", "")).encode("ascii", "ignore").decode().strip()
            if band_key in vinhedo_rates:
                water, water_fixed, collection, collection_fixed, full_sewer, full_sewer_fixed = vinhedo_rates[band_key]
                row["tarifa_agua_r_m3"] = "" if water is None else f"{water:.2f}"
                row["tarifa_agua_fixa_minima_r"] = "" if water_fixed is None else f"{water_fixed:.2f}"
                row["tarifa_esgoto_r_m3"] = "" if full_sewer is None else f"{full_sewer:.2f}"
                row["tarifa_esgoto_fixa_minima_r"] = "" if full_sewer_fixed is None else f"{full_sewer_fixed:.2f}"
                row["tarifa_esgoto_coleta_afastamento_r_m3"] = "" if collection is None else f"{collection:.2f}"
                row["tarifa_esgoto_coleta_afastamento_fixa_r"] = "" if collection_fixed is None else f"{collection_fixed:.2f}"
                if water is not None:
                    row["tarifa_tratamento_esgoto_r_m3"] = f"{full_sewer - collection:.2f}"
                elif water_fixed is not None:
                    row["tarifa_tratamento_esgoto_fixa_r"] = f"{full_sewer_fixed - collection_fixed:.2f}"
                row["esgoto_pct_sobre_agua"] = "100"
                row["vigencia_saneamento"] = "Vigente desde agosto de 2026"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["SANEBAVI Vinhedo"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["observacao"] = (
                    "Sete faixas residenciais conciliadas com a Resolução ARES-PCJ nº 710/2026. "
                    "A tarifa principal representa coleta, afastamento e tratamento (100% da água); "
                    "a modalidade sem tratamento (80%) também está registrada em campos próprios."
                )
        if row.get("saneamento_prestador") == "SAAE São Carlos" and row.get("categoria") == "Residencial normal":
            sao_carlos_rates = {
                "0 a 10 m3": 2.41, "11 a 20 m3": 6.05, "21 a 30 m3": 7.77,
                "31 a 40 m3": 9.81, "41 a 50 m3": 11.65, "51 a 60 m3": 12.78,
                ">60 m3": 14.16,
            }
            band_key = unicodedata.normalize("NFKD", row.get("faixa_consumo_m3", "")).encode("ascii", "ignore").decode().strip()
            if band_key in sao_carlos_rates:
                rate = sao_carlos_rates[band_key]
                row["tarifa_agua_r_m3"] = f"{rate:.2f}"
                row["tarifa_agua_fixa_minima_r"] = ""
                row["tarifa_esgoto_r_m3"] = f"{rate:.2f}"
                row["tarifa_esgoto_fixa_minima_r"] = ""
                row["esgoto_pct_sobre_agua"] = "100"
                row["vigencia_saneamento"] = "Vigente desde setembro de 2025"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["SAAE São Carlos"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["observacao"] = (
                    "Sete faixas residenciais de água e esgoto conciliadas visualmente com o Anexo I da "
                    "Resolução ARES-PCJ nº 646/2025; cobrança em cascata e esgoto a 100% da água."
                )
        if row.get("saneamento_prestador") == "SAEC Catanduva" and row.get("categoria") == "Residencial normal":
            catanduva_rates = {
                "0 a 7 m3 (minimo I)": (None, 18.57, "Consumo total de 0 a 7 m³"),
                "8 a 15 m3 (minimo II)": (None, 24.79, "Consumo total de 8 a 15 m³"),
                "0 a 10 m3 (>15)": (2.63, None, "Estrutura em cascata quando o consumo total excede 15 m³"),
                "11 a 20 m3 (>15)": (3.25, None, "Estrutura em cascata quando o consumo total excede 15 m³"),
                "21 a 25 m3 (>15)": (7.75, None, "Estrutura em cascata quando o consumo total excede 15 m³"),
                "26 a 30 m3 (>15)": (7.79, None, "Estrutura em cascata quando o consumo total excede 15 m³"),
                "31 a 40 m3 (>15)": (8.34, None, "Estrutura em cascata quando o consumo total excede 15 m³"),
                "41 a 50 m3 (>15)": (9.77, None, "Estrutura em cascata quando o consumo total excede 15 m³"),
                "51 a 100 m3 (>15)": (11.47, None, "Estrutura em cascata quando o consumo total excede 15 m³"),
                ">100 m3 (>15)": (13.46, None, "Estrutura em cascata quando o consumo total excede 15 m³"),
            }
            band_key = unicodedata.normalize("NFKD", row.get("faixa_consumo_m3", "")).encode("ascii", "ignore").decode().strip()
            if band_key in catanduva_rates:
                rate, fixed, condition = catanduva_rates[band_key]
                row["tarifa_agua_r_m3"] = "" if rate is None else f"{rate:.2f}"
                row["tarifa_agua_fixa_minima_r"] = "" if fixed is None else f"{fixed:.2f}"
                row["tarifa_esgoto_r_m3"] = "" if rate is None else f"{rate:.2f}"
                row["tarifa_esgoto_fixa_minima_r"] = "" if fixed is None else f"{fixed:.2f}"
                row["condicao_aplicacao_tarifa"] = condition
                row["esgoto_pct_sobre_agua"] = "100"
                row["vigencia_saneamento"] = "Vigente desde janeiro de 2026"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["SAEC Catanduva"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["observacao"] = (
                    "Dois mínimos condicionais e oito faixas para consumo acima de 15 m³ conciliados com a "
                    "Resolução ARES-PCJ nº 677/2025; esgoto equivale a 100% da água."
                )
        if row.get("saneamento_prestador") == "SAEV Ambiental" and row.get("categoria") == "Residencial normal":
            saev_rates = {
                "0 a 10 m3": (None, 28.22), "11 a 20 m3": (4.87, None),
                "21 a 30 m3": (8.31, None), "31 a 50 m3": (8.25, None),
                ">50 m3": (9.94, None),
            }
            band_key = unicodedata.normalize("NFKD", row.get("faixa_consumo_m3", "")).encode("ascii", "ignore").decode().strip()
            if band_key in saev_rates:
                rate, fixed = saev_rates[band_key]
                row["tarifa_agua_r_m3"] = "" if rate is None else f"{rate:.2f}"
                row["tarifa_agua_fixa_minima_r"] = "" if fixed is None else f"{fixed:.2f}"
                row["tarifa_esgoto_r_m3"] = "" if rate is None else f"{rate:.2f}"
                row["tarifa_esgoto_fixa_minima_r"] = "" if fixed is None else f"{fixed:.2f}"
                row["esgoto_pct_sobre_agua"] = "100"
                row["vigencia_saneamento"] = "Vigente no exercício de 2026"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["SAEV Ambiental"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["observacao"] = (
                    "Tarifa mínima e quatro faixas residenciais conciliadas visualmente com a Tabela C do "
                    "Decreto Municipal nº 19.729/2025. O art. 18 fixa esgoto residencial em 100% da água."
                )
        if row.get("saneamento_prestador") == "DAEP Penápolis" and row.get("categoria") == "Residencial normal":
            daep_rates = {
                "1 a 20 m3": (3.7580, 2.6305), "21 a 30 m3": (4.8854, 3.4198),
                "31 a 40 m3": (5.2612, 3.6828), "41 a 50 m3": (5.6370, 3.9459),
                "51 a 75 m3": (6.0127, 4.2090), "76 a 100 m3": (6.3885, 4.4719),
                ">100 m3": (6.7643, 4.7350),
            }
            band_key = unicodedata.normalize("NFKD", row.get("faixa_consumo_m3", "")).encode("ascii", "ignore").decode().strip()
            if band_key in daep_rates:
                water, sewer = daep_rates[band_key]
                row["tarifa_agua_r_m3"] = f"{water:.4f}"
                row["tarifa_esgoto_r_m3"] = f"{sewer:.4f}"
                row["tarifa_agua_fixa_minima_r"] = "7.3143" if band_key == "1 a 20 m3" else ""
                row["tarifa_esgoto_fixa_minima_r"] = "5.1257" if band_key == "1 a 20 m3" else ""
                row["esgoto_pct_sobre_agua"] = "70"
                row["vigencia_saneamento"] = "Vigente desde 01/03/2026"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["DAEP Penápolis"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO_POR_REAJUSTE"
                row["observacao"] = (
                    "TBO mensal e sete faixas residenciais derivados da tabela oficial da Resolução DAEP nº 5/2024, "
                    "com aplicação cumulativa dos reajustes oficiais de 5% (2025) e 8% (Decreto nº 8.504/2026)."
                )
        if row.get("saneamento_prestador") == "Ourinhos Saneamento" and row.get("categoria") == "Residencial normal":
            ourinhos_rates = {
                "0 a 10 m3": (3.11, 1.55), "11 a 20 m3": (6.17, 3.08),
                "21 a 30 m3": (7.77, 3.88), "31 a 50 m3": (10.04, 5.02),
                ">50 m3": (15.77, 7.88),
            }
            band_key = unicodedata.normalize("NFKD", row.get("faixa_consumo_m3", "")).encode("ascii", "ignore").decode().strip()
            if band_key in ourinhos_rates:
                water, sewer = ourinhos_rates[band_key]
                row["tarifa_agua_r_m3"] = f"{water:.2f}"
                row["tarifa_esgoto_r_m3"] = f"{sewer:.2f}"
                row["tarifa_agua_fixa_minima_r"] = ""
                row["tarifa_esgoto_fixa_minima_r"] = ""
                row["esgoto_pct_sobre_agua"] = "50"
                row["vigencia_saneamento"] = "Vigente desde novembro de 2025"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["Ourinhos Saneamento"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["observacao"] = (
                    "Cinco faixas residenciais de água e esgoto conciliadas com a tabela oficial vigente; "
                    "o esgoto corresponde a aproximadamente 50% da tarifa de água por faixa."
                )
        if row.get("saneamento_prestador") == "SAEG" and row.get("categoria") == "Residencial normal":
            saeg_rates = {
                "0 a 10 m3": (None, 30.063, None, 24.051),
                "11 a 20 m3": (4.121, None, 3.298, None),
                "21 a 50 m3": (6.912, None, 5.531, None),
                ">50 m3": (11.312, None, 9.050, None),
            }
            band_key = unicodedata.normalize("NFKD", row.get("faixa_consumo_m3", "")).encode("ascii", "ignore").decode().strip()
            if band_key in saeg_rates:
                water, water_fixed, sewer, sewer_fixed = saeg_rates[band_key]
                row["tarifa_agua_r_m3"] = "" if water is None else f"{water:.3f}"
                row["tarifa_agua_fixa_minima_r"] = "" if water_fixed is None else f"{water_fixed:.3f}"
                row["tarifa_esgoto_r_m3"] = "" if sewer is None else f"{sewer:.3f}"
                row["tarifa_esgoto_fixa_minima_r"] = "" if sewer_fixed is None else f"{sewer_fixed:.3f}"
                row["esgoto_pct_sobre_agua"] = "80"
                row["vigencia_saneamento"] = "Vigente desde 15/03/2026"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["SAEG"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["observacao"] = (
                    "Tarifa mínima residencial e três faixas incrementais conciliadas com o Anexo I da "
                    "Deliberação ARSESP nº 1.773/2026; o esgoto corresponde a 80% da tarifa de água."
                )
        if row.get("saneamento_prestador") == "SAAE Atibaia" and row.get("categoria") == "Residencial normal":
            atibaia_rates = {
                "0 a 10 m3": (None, 52.97, None, 52.97, None, 42.36),
                "11 a 20 m3": (7.97, None, 7.97, None, 6.39, None),
                "21 a 50 m3": (13.13, None, 13.13, None, 10.50, None),
                ">50 m3": (16.09, None, 16.09, None, 12.86, None),
            }
            band_key = unicodedata.normalize("NFKD", row.get("faixa_consumo_m3", "")).encode("ascii", "ignore").decode().strip()
            if band_key in atibaia_rates:
                water, water_fixed, full_sewer, full_fixed, collection, collection_fixed = atibaia_rates[band_key]
                row["tarifa_agua_r_m3"] = "" if water is None else f"{water:.2f}"
                row["tarifa_agua_fixa_minima_r"] = "" if water_fixed is None else f"{water_fixed:.2f}"
                row["tarifa_esgoto_r_m3"] = "" if full_sewer is None else f"{full_sewer:.2f}"
                row["tarifa_esgoto_fixa_minima_r"] = "" if full_fixed is None else f"{full_fixed:.2f}"
                row["tarifa_esgoto_coleta_afastamento_r_m3"] = "" if collection is None else f"{collection:.2f}"
                row["tarifa_esgoto_coleta_afastamento_fixa_r"] = "" if collection_fixed is None else f"{collection_fixed:.2f}"
                row["esgoto_pct_sobre_agua"] = "100"
                row["vigencia_saneamento"] = "Vigente desde dezembro de 2025"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["SAAE Atibaia"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["observacao"] = (
                    "Tarifa mínima e três faixas residenciais conciliadas com a Resolução ARES-PCJ nº 663/2025. "
                    "A tarifa principal inclui tratamento (100% da água); coleta e afastamento (80%) constam em campos próprios."
                )
        if row.get("saneamento_prestador") == "CSA Equatorial" and row.get("categoria") == "Residencial normal":
            csa_rates = {
                "0 a 10 m3": (None, 42.91), "11 a 20 m3": (4.49, None),
                "21 a 30 m3": (5.06, None), "31 a 50 m3": (6.58, None),
                ">50 m3": (9.31, None),
            }
            band_key = unicodedata.normalize("NFKD", row.get("faixa_consumo_m3", "")).encode("ascii", "ignore").decode().strip()
            if band_key in csa_rates:
                rate, fixed = csa_rates[band_key]
                row["tarifa_agua_r_m3"] = "" if rate is None else f"{rate:.2f}"
                row["tarifa_agua_fixa_minima_r"] = "" if fixed is None else f"{fixed:.2f}"
                row["tarifa_esgoto_r_m3"] = "" if rate is None else f"{rate:.2f}"
                row["tarifa_esgoto_fixa_minima_r"] = "" if fixed is None else f"{fixed:.2f}"
                row["esgoto_pct_sobre_agua"] = "100"
                row["vigencia_saneamento"] = "Vigente de 30/08/2025 a 29/08/2026"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["CSA Equatorial"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["observacao"] = (
                    "Tarifa mínima e quatro faixas residenciais conciliadas com o Anexo I da Resolução ARSAP nº 008/2025; "
                    "o esgoto corresponde a 100% da tarifa de água."
                )
        if row.get("saneamento_prestador") == "DAE Valinhos" and row.get("categoria") == "Residencial normal":
            valinhos_rates = {
                "0 a 10 m3": (None, 23.73), "10,001 a 17 m3": (4.40, None),
                "17,001 a 25 m3": (5.69, None), "25,001 a 35 m3": (7.77, None),
                "35,001 a 50 m3": (10.69, None), ">50 m3": (22.18, None),
            }
            band_key = unicodedata.normalize("NFKD", row.get("faixa_consumo_m3", "")).encode("ascii", "ignore").decode().strip()
            if band_key in valinhos_rates:
                rate, fixed = valinhos_rates[band_key]
                row["tarifa_agua_r_m3"] = "" if rate is None else f"{rate:.2f}"
                row["tarifa_agua_fixa_minima_r"] = "" if fixed is None else f"{fixed:.2f}"
                row["tarifa_esgoto_r_m3"] = "" if rate is None else f"{rate:.2f}"
                row["tarifa_esgoto_fixa_minima_r"] = "" if fixed is None else f"{fixed:.2f}"
                row["esgoto_pct_sobre_agua"] = "100"
                row["vigencia_saneamento"] = "Vigente desde abril de 2023; último ato listado pela ARES-PCJ"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["DAE Valinhos"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["observacao"] = (
                    "Tarifa mínima e cinco faixas residenciais conciliadas com a Resolução ARES-PCJ nº 483/2023; "
                    "a página municipal do regulador não lista ato tarifário posterior até a data da auditoria."
                )
        if row.get("saneamento_prestador") == "Saneaqua" and row.get("categoria") == "Residencial normal":
            saneaqua_rates = {
                "0 a 10 m3": 4.71, "11 a 20 m3": 6.50,
                "21 a 50 m3": 10.04, ">50 m3": 11.91,
            }
            band_key = unicodedata.normalize("NFKD", row.get("faixa_consumo_m3", "")).encode("ascii", "ignore").decode().strip()
            if band_key in saneaqua_rates:
                rate = saneaqua_rates[band_key]
                row["tarifa_agua_r_m3"] = f"{rate:.2f}"
                row["tarifa_esgoto_r_m3"] = f"{rate:.2f}"
                row["tarifa_agua_fixa_minima_r"] = ""
                row["tarifa_esgoto_fixa_minima_r"] = ""
                row["tarifa_esgoto_coleta_afastamento_r_m3"] = f"{0.8 * rate:.3f}"
                row["esgoto_pct_sobre_agua"] = "100"
                row["vigencia_saneamento"] = "Vigente desde 01/05/2026"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["Saneaqua"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["observacao"] = (
                    "Quatro faixas residenciais conciliadas com o Anexo I da Nota Técnica ARSESP 2026. "
                    "A estrutura da concessionária fixa esgoto em 100% da água quando tratado e 80% sem tratamento."
                )
        if row.get("saneamento_prestador") == "SEMAE São Leopoldo" and row.get("categoria") == "Residencial normal":
            semae_sl_rates = {
                "015": (5.1517, 4.1214, 61.29, 49.03),
                "1630": (11.4524, 4.5809, None, None),
                "30": (16.0298, 6.4120, None, None),
            }
            band_key = key_text(row.get("faixa_consumo_m3", ""))
            if band_key in semae_sl_rates:
                water, sewer, water_fixed, sewer_fixed = semae_sl_rates[band_key]
                row["tarifa_agua_r_m3"] = f"{water:.4f}"
                row["tarifa_esgoto_r_m3"] = f"{sewer:.4f}"
                row["tarifa_agua_fixa_minima_r"] = "" if water_fixed is None else f"{water_fixed:.2f}"
                row["tarifa_esgoto_fixa_minima_r"] = "" if sewer_fixed is None else f"{sewer_fixed:.2f}"
                row["esgoto_pct_sobre_agua"] = "80"
                row["vigencia_saneamento"] = "Tabela tarifária do exercício de 2026"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["SEMAE São Leopoldo"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["observacao"] = (
                    "Serviços básicos e três faixas residenciais de água e esgoto conciliados diretamente com a tabela oficial 2026. "
                    "Foram preservados os valores específicos publicados para a modalidade de esgoto 80%, sem inferência proporcional."
                )
        if row.get("saneamento_prestador") == "SAMAE Caxias do Sul" and row.get("categoria") == "Residencial normal":
            caxias_rates = {
                "05": (None, 38.30), "610": (8.77, None),
                "1115": (10.54, None), "1620": (16.56, None),
                "2130": (21.75, None), "3150": (22.66, None),
                "51100": (24.36, None), "100": (28.35, None),
            }
            band_key = key_text(row.get("faixa_consumo_m3", ""))
            if band_key in caxias_rates:
                water, water_fixed = caxias_rates[band_key]
                row["tarifa_agua_r_m3"] = "" if water is None else f"{water:.2f}"
                row["tarifa_agua_fixa_minima_r"] = "" if water_fixed is None else f"{water_fixed:.2f}"
                # O ato define primeiro o volume de escoamento como 80% do consumo
                # de água e depois aplica percentuais do preço básico (R$ 7,66/m³)
                # conforme a modalidade. Não se trata de 80% de cada faixa de água.
                row["tarifa_esgoto_r_m3"] = "6.1280"
                row["tarifa_esgoto_fixa_minima_r"] = "24.51" if band_key == "05" else ""
                row["tarifa_tratamento_esgoto_r_m3"] = "6.1280"
                row["tarifa_tratamento_esgoto_fixa_r"] = "24.51" if band_key == "05" else ""
                row["tarifa_esgoto_coleta_afastamento_r_m3"] = "3.0640"
                row["tarifa_esgoto_coleta_afastamento_fixa_r"] = "12.26" if band_key == "05" else ""
                row["esgoto_pct_sobre_agua"] = "80"
                row["vigencia_saneamento"] = "Vigente desde 01/07/2026"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["SAMAE Caxias do Sul"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["condicao_aplicacao_tarifa"] = (
                    "Volume faturável de esgoto = 80% do consumo de água. Sobre esse volume: tratamento = 80% do preço básico; "
                    "coleta/afastamento = 40%; transição = 60%. Preço básico de água = R$ 7,66/m³."
                )
                row["observacao"] = (
                    "Tarifa mínima e sete faixas excedentes de água conciliadas com a Tabela de Valores 2026. "
                    "O esgoto foi modelado em duas etapas exatamente como o ato: volume de escoamento de 80% e tarifa por modalidade."
                )
        if row.get("saneamento_prestador") == "SANEP Pelotas" and row.get("categoria") == "Residencial normal":
            pelotas_rates = {
                "010": (6.13, 1.84, 3.68, 4.90),
                "1120": (7.05, 2.11, 4.23, 5.64),
                "2130": (9.32, 2.80, 5.59, 7.46),
                "3150": (10.74, 3.22, 6.45, 8.59),
                "51100": (12.33, 3.70, 7.40, 9.86),
                "100": (14.18, 4.25, 8.51, 11.34),
            }
            band_key = key_text(row.get("faixa_consumo_m3", ""))
            if band_key in pelotas_rates:
                water, sewer30, sewer60, sewer80 = pelotas_rates[band_key]
                row["tarifa_agua_r_m3"] = f"{water:.2f}"
                row["tarifa_agua_fixa_minima_r"] = "28.96" if band_key == "010" else ""
                row["tarifa_esgoto_r_m3"] = f"{sewer80:.2f}"
                row["tarifa_esgoto_fixa_minima_r"] = ""
                row["tarifa_tratamento_esgoto_r_m3"] = f"{sewer80:.2f}"
                row["tarifa_tratamento_esgoto_fixa_r"] = ""
                row["tarifa_esgoto_coleta_afastamento_r_m3"] = f"{sewer60:.2f}"
                row["tarifa_esgoto_coleta_afastamento_fixa_r"] = ""
                row["esgoto_pct_sobre_agua"] = "80"
                row["vigencia_saneamento"] = "Vigente de 07/2026 a 06/2027"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["SANEP Pelotas"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["condicao_aplicacao_tarifa"] = (
                    f"Esgoto publicado por faixa: drenagem convencional/30% = R$ {sewer30:.2f}/m³; "
                    f"somente coletado/60% = R$ {sewer60:.2f}/m³; coletado e tratado/80% = R$ {sewer80:.2f}/m³."
                )
                row["observacao"] = (
                    "Serviço básico, seis faixas de água e os três níveis de esgoto foram conciliados diretamente com a matriz "
                    "tarifária oficial 2026/07; o serviço básico de R$ 28,96 foi mantido como componente de água, sem duplicação no esgoto."
                )
        # Araraquara aplica tarifa por faixa ao volume total e subtrai uma
        # parcela específica. Registrar ambos os componentes evita interpretar
        # equivocadamente a tabela como blocos incrementais.
        if row.get("saneamento_prestador") == "DAAE Araraquara" and row.get("categoria") == "Residencial normal":
            araraquara_rates = {
                "0 a 10 m3": (2.27, 0.00),
                "11 a 20 m3": (4.09, 18.18),
                "21 a 30 m3": (5.83, 52.97),
                "31 a 40 m3": (7.64, 107.36),
                "41 a 50 m3": (9.07, 164.86),
                "51 a 100 m3": (10.82, 251.83),
                "101 a 200 m3": (12.76, 448.47),
                ">201 m3": (15.21, 930.94),
            }
            band_key = unicodedata.normalize("NFKD", row.get("faixa_consumo_m3", "")).encode("ascii", "ignore").decode().strip()
            if band_key in araraquara_rates:
                rate, deduction = araraquara_rates[band_key]
                row["tarifa_agua_r_m3"] = f"{rate:.2f}"
                row["tarifa_esgoto_r_m3"] = f"{rate:.2f}"
                row["tarifa_agua_fixa_minima_r"] = "22.70" if band_key == "0 a 10 m3" else ""
                row["tarifa_esgoto_fixa_minima_r"] = "22.70" if band_key == "0 a 10 m3" else ""
                row["parcela_deduzir_agua_r"] = f"{deduction:.2f}"
                row["parcela_deduzir_esgoto_r"] = f"{deduction:.2f}"
                row["esgoto_pct_sobre_agua"] = "100"
                row["vigencia_saneamento"] = "Vigente desde novembro de 2025"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["DAAE Araraquara"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["observacao"] = (
                    "Oito faixas de água e esgoto conciliadas com a Resolução ARES-PCJ nº 656/2025; "
                    "fatura da faixa = volume × tarifa − parcela a deduzir, com consumo mínimo de 10 m³."
                )
        # A Iguá Sergipe assumiu a prestação ao usuário; a DESO permaneceu
        # como fornecedora de água tratada. A Resolução AGRESE nº 78/2025
        # homologou reajuste linear de 7,837% sobre a estrutura anterior.
        if row.get("saneamento_prestador") == "DESO" and row.get("categoria") == "Residencial normal":
            factor = 1.07837
            for field in (
                "tarifa_agua_r_m3", "tarifa_agua_fixa_minima_r",
                "tarifa_esgoto_r_m3", "tarifa_esgoto_fixa_minima_r",
            ):
                old_value = num(row.get(field))
                if old_value is not None:
                    row[field] = f"{old_value * factor:.2f}"
            row["saneamento_prestador"] = "Iguá Sergipe"
            row["agencia_reguladora"] = "AGRESE"
            row["vigencia_saneamento"] = "Vigente desde 01/08/2025"
            row["fonte_saneamento"] = SANITATION_EVIDENCE["Iguá Sergipe"]["url"]
            row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO_POR_REAJUSTE"
            row["observacao"] = (
                "Prestador varejista atualizado para Iguá Sergipe; valores da estrutura anterior "
                "reajustados em 7,837% conforme Resolução AGRESE nº 78/2025."
            )
        # A CAGECE publica diretamente as cinco faixas da categoria
        # Residencial Normal. A base legada continha valores anteriores à
        # revisão extraordinária vigente desde 05/11/2025; as tarifas abaixo
        # foram conciliadas faixa a faixa com a tabela oficial.
        if row.get("saneamento_prestador") == "CAGECE" and row.get("categoria") == "Residencial normal":
            cagece_water = {
                "0 a 10 m³": 6.77,
                "11 a 15 m³": 8.78,
                "16 a 20 m³": 9.49,
                "21 a 50 m³": 16.29,
                ">50 m³": 28.77,
            }
            band = row.get("faixa_consumo_m3")
            if band in cagece_water:
                row["tarifa_agua_r_m3"] = f"{cagece_water[band]:.2f}"
                row["tarifa_esgoto_r_m3"] = ""
                row["esgoto_pct_sobre_agua"] = "80"
                row["vigencia_saneamento"] = "Vigente desde 05/11/2025"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["CAGECE"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["observacao"] = (
                    "Faixa residencial normal conciliada com a tabela oficial CAGECE; "
                    "o volume faturado de esgoto corresponde a 80% do volume de água."
                )
        # Tabela EMBASA 2026, categoria Residencial/Normal/Veraneio. A tarifa
        # mínima cobre 6 m³; as demais linhas são valores incrementais por m³.
        if row.get("saneamento_prestador") == "EMBASA" and row.get("categoria") == "Residencial normal":
            embasa_water = {
                "0 a 6 m3": (None, 44.77),
                "7 a 10 m3": (1.77, None),
                "11 a 15 m3": (12.53, None),
                "16 a 20 m3": (13.41, None),
                "21 a 25 m3": (15.08, None),
                "26 a 30 m3": (16.82, None),
                "31 a 40 m3": (18.49, None),
                "41 a 50 m3": (20.28, None),
                ">50 m3": (24.40, None),
            }
            band_key = unicodedata.normalize("NFKD", row.get("faixa_consumo_m3", "")).encode("ascii", "ignore").decode().strip()
            if band_key in embasa_water:
                volumetric, fixed = embasa_water[band_key]
                row["tarifa_agua_r_m3"] = "" if volumetric is None else f"{volumetric:.2f}"
                row["tarifa_agua_fixa_minima_r"] = "" if fixed is None else f"{fixed:.2f}"
                row["tarifa_esgoto_r_m3"] = ""
                row["esgoto_pct_sobre_agua"] = "80"
                row["vigencia_saneamento"] = "Vigente desde 20/07/2026"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["EMBASA"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["observacao"] = (
                    "Categoria residencial normal conciliada faixa a faixa com a tabela EMBASA 2026; "
                    "esgoto convencional corresponde a 80% da conta de água."
                )
        # A CORSAN opera estruturas diferentes por município/agência. Os
        # quatro conjuntos presentes na amostra foram conciliados com os
        # anexos oficiais atualmente apontados no repositório da companhia.
        if row.get("saneamento_prestador") == "CORSAN":
            corsan_sources = {
                "Erechim": "https://corsan.com.br/wp-content/uploads/2025/11/Tabela-Tarifaria-Erechim_2026-x.pdf",
                "Santa Cruz do Sul": "https://corsan.com.br/wp-content/uploads/2025/11/Tabela-Tarifaria-Santa-Cruz-do-Sul_2026-x.pdf",
                "Canoas": "https://www.corsan.com.br/wp-content/uploads/2026/07/ANEXO-3-CANOAS-E-ESTEIO-TABELA-TARIFARIA_AGOSTO-2026.pdf",
                "Esteio": "https://www.corsan.com.br/wp-content/uploads/2026/07/ANEXO-3-CANOAS-E-ESTEIO-TABELA-TARIFARIA_AGOSTO-2026.pdf",
            }
            anexo4_keys = {key_text(n) for n in ("Campo Bom", "Sapucaia do Sul", "Tramandaí", "Parobé", "Sapiranga")}
            city_name = row.get("municipio", "")
            source_url = corsan_sources.get(city_name)
            city_source_key = key_text(city_name)
            if city_source_key in anexo4_keys or city_source_key.startswith(("tramanda", "parob")):
                source_url = "https://www.corsan.com.br/wp-content/uploads/2026/07/ANEXO-4-TABELA-TARIFARIA_AGOSTO-2026.pdf"
            elif source_url is None:
                source_url = "https://www.corsan.com.br/wp-content/uploads/2026/07/ANEXO-5-TABELA-TARIFARIA_AGOSTO-2026.pdf"
            row["fonte_saneamento"] = source_url
            row["vigencia_saneamento"] = (
                "Vigente desde 01/01/2026" if city_name in {"Erechim", "Santa Cruz do Sul"}
                else "Vigente desde 01/07/2026"
            )
            row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO_POR_MUNICIPIO"
            row["observacao"] = (
                "Preço-base, serviço básico e esgoto tratado (70%) conciliados com o anexo CORSAN "
                "específico do município. O faturamento de água usa PB×C^n acrescido do serviço básico."
            )
        # Resolução MOB/MA nº 10/2023: estrutura residencial vigente desde
        # 05/01/2024. Ata oficial publicada em 19/01/2026 registra que a
        # relação então vigente entre esgoto e água permanecia 1:1; a
        # passagem a 0,8:1 era proposta, não tarifa homologada.
        if row.get("saneamento_prestador") == "CAEMA" and row.get("categoria") == "Residencial normal":
            caema_water = {
                "0 a 10 m3": (None, 33.58),
                "11 a 20 m3": (6.80, None),
                "21 a 30 m3": (10.77, None),
                "31 a 50 m3": (13.68, None),
                ">50 m3": (21.48, None),
            }
            band_key = unicodedata.normalize("NFKD", row.get("faixa_consumo_m3", "")).encode("ascii", "ignore").decode().strip()
            if band_key in caema_water:
                volumetric, fixed = caema_water[band_key]
                row["tarifa_agua_r_m3"] = "" if volumetric is None else f"{volumetric:.2f}"
                row["tarifa_agua_fixa_minima_r"] = "" if fixed is None else f"{fixed:.2f}"
                row["tarifa_esgoto_r_m3"] = ""
                row["esgoto_pct_sobre_agua"] = "100"
                row["vigencia_saneamento"] = "Água vigente desde 05/01/2024; relação esgoto/água confirmada em 19/01/2026"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["CAEMA"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["observacao"] = (
                    "Água conciliada faixa a faixa com a Resolução MOB/MA nº 10/2023. "
                    "Ata oficial de janeiro de 2026 confirma relação esgoto/água de 1:1; "
                    "a redução a 0,8:1 constava apenas como proposta."
                )
        # A página oficial da concessionária mantém as tabelas vigentes das
        # Regiões 1 e 4 separadas. Para consumo residencial normal aplica-se
        # a Tarifa 2 da Área A; água e esgoto possuem o mesmo valor.
        if row.get("saneamento_prestador") == "Águas do Rio" and row.get("categoria") == "Residencial normal":
            region4_cities = {
                "Belford Roxo", "Duque de Caxias", "Japeri", "Mesquita",
                "Nilópolis", "Nova Iguaçu", "Queimados", "São João de Meriti",
            }
            region1_rates = {
                "0 a 15 m3": 7.436291, "16 a 30 m3": 16.359841,
                "31 a 45 m3": 22.308872, "46 a 60 m3": 44.617747,
                ">60 m3": 59.490329,
            }
            region4_rates = {
                "0 a 15 m3": 7.520046, "16 a 30 m3": 16.544101,
                "31 a 45 m3": 22.560137, "46 a 60 m3": 45.120276,
                ">60 m3": 60.160368,
            }
            band_key = unicodedata.normalize("NFKD", row.get("faixa_consumo_m3", "")).encode("ascii", "ignore").decode().strip()
            rates = region4_rates if row.get("municipio") in region4_cities else region1_rates
            if band_key in rates:
                value = rates[band_key]
                row["tarifa_agua_r_m3"] = f"{value:.6f}"
                row["tarifa_esgoto_r_m3"] = f"{value:.6f}"
                row["esgoto_pct_sobre_agua"] = "100"
                row["vigencia_saneamento"] = "Vigente desde dezembro de 2025"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["Águas do Rio"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO_POR_REGIAO"
                row["observacao"] = (
                    f"Tarifa 2 residencial normal da Área A, Região {'4' if rates is region4_rates else '1'}, "
                    "conciliada faixa a faixa; tarifa de esgoto igual à de água."
                )
        # Resolução ARPB nº 004/2025: tarifa residencial normal, com tarifa
        # mínima para 10 m³ e percentuais de esgoto distintos por faixa.
        if row.get("saneamento_prestador") == "CAGEPA" and row.get("categoria") == "Residencial normal":
            cagepa_rates = {
                "0 a 10 m3": (None, 54.82, None, 43.86, 80),
                "11 a 20 m3": (7.08, None, 5.66, None, 80),
                "21 a 30 m3": (9.32, None, 8.39, None, 90),
                ">30 m3": (12.67, None, 12.67, None, 100),
            }
            band_key = unicodedata.normalize("NFKD", row.get("faixa_consumo_m3", "")).encode("ascii", "ignore").decode().strip()
            if band_key in cagepa_rates:
                water, water_fixed, sewer, sewer_fixed, sewer_pct = cagepa_rates[band_key]
                row["tarifa_agua_r_m3"] = "" if water is None else f"{water:.2f}"
                row["tarifa_agua_fixa_minima_r"] = "" if water_fixed is None else f"{water_fixed:.2f}"
                row["tarifa_esgoto_r_m3"] = "" if sewer is None else f"{sewer:.2f}"
                row["tarifa_esgoto_fixa_minima_r"] = "" if sewer_fixed is None else f"{sewer_fixed:.2f}"
                row["esgoto_pct_sobre_agua"] = str(sewer_pct)
                row["vigencia_saneamento"] = "Vigente desde 30/06/2025"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["CAGEPA"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["observacao"] = (
                    "Estrutura residencial normal conciliada com a Tabela 1 da Resolução ARPB nº 004/2025; "
                    "percentual de esgoto específico da faixa."
                )
        # A CAERN publica tabelas próprias para Natal, Mossoró e os demais
        # municípios. O esgoto convencional equivale a 70% da tarifa de água.
        if row.get("saneamento_prestador") == "CAERN" and row.get("categoria") == "Residencial normal":
            interior_rates = {
                "0 a 10 m3": (None, 56.96), "11 a 15 m3": (6.34, None),
                "16 a 20 m3": (7.51, None), "21 a 30 m3": (8.45, None),
                "31 a 50 m3": (9.74, None), "51 a 100 m3": (12.61, None),
                ">100 m3": (14.33, None),
            }
            natal_rates = {
                "0 a 10 m3": (None, 51.40), "11 a 15 m3": (5.73, None),
                "16 a 20 m3": (6.77, None), "21 a 30 m3": (7.64, None),
                "31 a 50 m3": (8.79, None), "51 a 100 m3": (11.38, None),
                ">100 m3": (12.93, None),
            }
            band_key = unicodedata.normalize("NFKD", row.get("faixa_consumo_m3", "")).encode("ascii", "ignore").decode().strip()
            is_natal = row.get("municipio") == "Natal"
            rates = natal_rates if is_natal else interior_rates
            if band_key in rates:
                water, water_fixed = rates[band_key]
                row["tarifa_agua_r_m3"] = "" if water is None else f"{water:.2f}"
                row["tarifa_agua_fixa_minima_r"] = "" if water_fixed is None else f"{water_fixed:.2f}"
                row["tarifa_esgoto_r_m3"] = "" if water is None else f"{water * 0.70:.2f}"
                row["tarifa_esgoto_fixa_minima_r"] = "" if water_fixed is None else f"{water_fixed * 0.70:.2f}"
                row["esgoto_pct_sobre_agua"] = "70"
                row["vigencia_saneamento"] = "Vigente desde 01/07/2025" if is_natal else "Vigente desde 01/04/2025"
                if is_natal:
                    source_url = "https://agencia.caern.com.br/assets/documentos/novos/RS.CA.P.G.02.0002.03_REAJUSTE_TARIFARIO_NATAL.pdf"
                elif row.get("municipio") == "Mossoró":
                    source_url = "https://agencia.caern.com.br/assets/documentos/novos/Resolucao_RS.CA.P.G.02.0007.00_Mossoro_2025.pdf"
                else:
                    source_url = "https://agencia.caern.com.br/assets/documentos/novos/Resolucao_RS.CA.P.G.02.0003.03_Interior_2025.pdf"
                row["fonte_saneamento"] = source_url
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO_POR_REGULADOR"
                row["observacao"] = (
                    f"Tabela residencial 2025 de {'Natal' if is_natal else ('Mossoró' if row.get('municipio') == 'Mossoró' else 'interior')} "
                    "conciliada faixa a faixa; esgoto convencional = 70% da água."
                )
        # Estrutura residencial normal da CAERD homologada pela Resolução
        # AGERO nº 82/2025. Adota-se coleta e tratamento de esgoto (70%).
        if row.get("saneamento_prestador") == "CAERD" and row.get("categoria") == "Residencial normal":
            caerd_rates = {
                "0 a 10 m3": (None, 57.51), "11 a 15 m3": (6.52, None),
                "16 a 20 m3": (7.17, None), "21 a 25 m3": (8.61, None),
                "26 a 30 m3": (9.87, None), "31 a 50 m3": (11.82, None),
                "51 a 75 m3": (14.18, None), "76 a 150 m3": (14.18, None),
                ">150 m3": (14.18, None),
            }
            band_key = unicodedata.normalize("NFKD", row.get("faixa_consumo_m3", "")).encode("ascii", "ignore").decode().strip()
            if band_key in caerd_rates:
                water, water_fixed = caerd_rates[band_key]
                row["tarifa_agua_r_m3"] = "" if water is None else f"{water:.2f}"
                row["tarifa_agua_fixa_minima_r"] = "" if water_fixed is None else f"{water_fixed:.2f}"
                row["tarifa_esgoto_r_m3"] = "" if water is None else f"{water * 0.70:.2f}"
                row["tarifa_esgoto_fixa_minima_r"] = "" if water_fixed is None else f"{water_fixed * 0.70:.2f}"
                row["esgoto_pct_sobre_agua"] = "70"
                row["vigencia_saneamento"] = "Vigente em 2025/2026"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["CAERD"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["observacao"] = (
                    "Estrutura residencial normal conciliada faixa a faixa com a Resolução AGERO nº 82/2025; "
                    "esgoto com coleta e tratamento = 70% da água."
                )
        # Estrutura unificada dos municípios Saneatins/BRK no Tocantins,
        # homologada pela Resolução ATR nº 13/2025.
        if row.get("saneamento_prestador") == "BRK Tocantins" and row.get("categoria") == "Residencial normal":
            brk_to_rates = {
                "0 a 5 m3": 8.76, "6 a 10 m3": 3.05,
                "11 a 15 m3": 8.66, "16 a 20 m3": 11.07,
                "21 a 25 m3": 13.53, "26 a 30 m3": 15.67,
                "31 a 35 m3": 17.28, "36 a 40 m3": 21.34,
                "41 a 50 m3": 23.94, ">50 m3": 28.57,
            }
            band_key = unicodedata.normalize("NFKD", row.get("faixa_consumo_m3", "")).encode("ascii", "ignore").decode().strip()
            if band_key in brk_to_rates:
                water = brk_to_rates[band_key]
                row["tarifa_agua_r_m3"] = f"{water:.2f}"
                row["tarifa_agua_fixa_minima_r"] = ""
                row["tarifa_esgoto_r_m3"] = f"{water * 0.80:.2f}"
                row["tarifa_esgoto_fixa_minima_r"] = ""
                row["esgoto_pct_sobre_agua"] = "80"
                row["vigencia_saneamento"] = "Vigente desde 05/12/2025"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["BRK Tocantins"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["observacao"] = (
                    "Estrutura residencial normal unificada conciliada faixa a faixa com a Resolução ATR nº 13/2025; "
                    "esgoto = 80% da água."
                )
        # Estrutura estadual da Águas do Piauí publicada pela concessionária,
        # com vigência em 01/03/2026 e esgoto equivalente a 80% da água.
        if row.get("saneamento_prestador") == "Águas do Piauí" and row.get("categoria") == "Residencial normal":
            aguas_pi_rates = {
                "0 a 10 m3": 5.289, "11 a 15 m3": 9.815,
                "16 a 20 m3": 10.917, "21 a 25 m3": 11.800,
                "26 a 35 m3": 18.747, ">35 m3": 20.401,
            }
            band_key = unicodedata.normalize("NFKD", row.get("faixa_consumo_m3", "")).encode("ascii", "ignore").decode().strip()
            if band_key in aguas_pi_rates:
                water = aguas_pi_rates[band_key]
                row["tarifa_agua_r_m3"] = f"{water:.3f}"
                row["tarifa_agua_fixa_minima_r"] = ""
                row["tarifa_esgoto_r_m3"] = f"{water * 0.80:.3f}"
                row["tarifa_esgoto_fixa_minima_r"] = ""
                row["esgoto_pct_sobre_agua"] = "80"
                row["vigencia_saneamento"] = "Vigente desde 01/03/2026"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["Águas do Piauí"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["observacao"] = (
                    "Estrutura residencial normal conciliada faixa a faixa com a tabela oficial 2026; "
                    "esgoto = 80% da água."
                )
        if row.get("saneamento_prestador") == "Águas de Teresina" and row.get("categoria") == "Residencial normal":
            teresina_rates = {
                "0 a 10 m3": (None, 46.83),
                "11 a 25 m3": (8.72, None),
                ">25 m3": (15.06, None),
            }
            band_key = unicodedata.normalize("NFKD", row.get("faixa_consumo_m3", "")).encode("ascii", "ignore").decode().strip()
            if band_key in teresina_rates:
                water, water_fixed = teresina_rates[band_key]
                row["tarifa_agua_r_m3"] = "" if water is None else f"{water:.2f}"
                row["tarifa_agua_fixa_minima_r"] = "" if water_fixed is None else f"{water_fixed:.2f}"
                row["tarifa_esgoto_r_m3"] = "" if water is None else f"{water * 0.80:.2f}"
                row["tarifa_esgoto_fixa_minima_r"] = "" if water_fixed is None else f"{water_fixed * 0.80:.2f}"
                row["esgoto_pct_sobre_agua"] = "80"
                row["vigencia_saneamento"] = "Vigente desde 28/06/2026"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["Águas de Teresina"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["observacao"] = (
                    "Estrutura residencial não social conciliada com a tabela oficial 2026; esgoto = 80% da água."
                )
        # Estrutura tarifária residencial publicada pelo SANEACRE em 2025,
        # conforme Resolução AGEAC nº 104/2025. Água e esgoto são mantidos
        # com os valores nominais da tabela, evitando reconstruir os
        # arredondamentos oficiais a partir de um percentual.
        if row.get("saneamento_prestador") == "SANEACRE" and row.get("categoria") == "Residencial normal":
            saneacre_rates = {
                "0 a 15 m3": (None, 38.37, None, 30.69),
                "16 a 20 m3": (3.68, None, 2.94, None),
                "21 a 25 m3": (4.57, None, 3.66, None),
                "26 a 30 m3": (5.46, None, 4.37, None),
                "31 a 35 m3": (6.35, None, 5.08, None),
                "36 a 40 m3": (7.24, None, 5.79, None),
                "41 a 45 m3": (8.12, None, 6.50, None),
                "46 a 50 m3": (9.01, None, 7.21, None),
                ">50 m3": (9.90, None, 7.92, None),
            }
            band_key = unicodedata.normalize("NFKD", row.get("faixa_consumo_m3", "")).encode("ascii", "ignore").decode().strip()
            if band_key in saneacre_rates:
                water, water_fixed, sewer, sewer_fixed = saneacre_rates[band_key]
                row["tarifa_agua_r_m3"] = "" if water is None else f"{water:.2f}"
                row["tarifa_agua_fixa_minima_r"] = "" if water_fixed is None else f"{water_fixed:.2f}"
                row["tarifa_esgoto_r_m3"] = "" if sewer is None else f"{sewer:.2f}"
                row["tarifa_esgoto_fixa_minima_r"] = "" if sewer_fixed is None else f"{sewer_fixed:.2f}"
                row["esgoto_pct_sobre_agua"] = ""
                row["vigencia_saneamento"] = "Vigente desde julho de 2025"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["SANEACRE"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["observacao"] = (
                    "Estrutura residencial conciliada faixa a faixa com a tabela oficial SANEACRE 2025; "
                    "valores nominais de água e esgoto preservados conforme publicação."
                )
        # Alagoas possui quatro estruturas contratuais na amostra. Cada
        # município é associado ao prestador atual e à tabela/rampa oficial
        # pertinente, em lugar da antiga aproximação estadual única.
        if row.get("uf") == "AL" and row.get("categoria") == "Residencial normal" and row.get("saneamento_prestador") != "SAAE Coruripe":
            standard = {
                "0 a 10 m3": 7.39, "11 a 15 m3": 14.10, "16 a 20 m3": 16.30,
                "21 a 30 m3": 17.41, "31 a 40 m3": 17.98, "41 a 50 m3": 18.21,
                "51 a 90 m3": 18.33, "91 a 150 m3": 18.44, ">150 m3": 18.45,
            }
            rates_by_scope = {
                "CASAL": {
                    "0 a 10 m3": 7.28, "11 a 15 m3": 13.90, "16 a 20 m3": 16.069,
                    "21 a 30 m3": 17.169, "31 a 40 m3": 17.723, "41 a 50 m3": 17.957,
                    "51 a 90 m3": 18.075, "91 a 150 m3": 18.177, ">150 m3": 18.193,
                },
                "BRK Alagoas": {
                    "0 a 10 m3": 7.64, "11 a 15 m3": 14.61, "16 a 20 m3": 16.89,
                    "21 a 30 m3": 18.04, "31 a 40 m3": 18.63, "41 a 50 m3": 18.86,
                    "51 a 90 m3": 18.99, "91 a 150 m3": 19.09, ">150 m3": 19.10,
                },
                "Águas do Sertão": standard,
                "Verde Alagoas": {
                    "0 a 10 m3": 5.58, "11 a 15 m3": 10.25, "16 a 20 m3": 11.14,
                    "21 a 30 m3": 12.22, "31 a 40 m3": 12.64, "41 a 50 m3": 13.29,
                    "51 a 90 m3": 13.92, "91 a 150 m3": 13.96, ">150 m3": 13.97,
                },
            }
            city_overrides = {
                "Marechal Deodoro": {
                    "0 a 10 m3": 6.819, "11 a 15 m3": 12.70, "16 a 20 m3": 14.27,
                    "21 a 30 m3": 15.46, "31 a 40 m3": 15.97, "41 a 50 m3": 15.92,
                    "51 a 90 m3": 15.14, "91 a 150 m3": 16.96, ">150 m3": 19.88,
                },
                "Penedo": {
                    "0 a 10 m3": 6.14, "11 a 15 m3": 10.68, "16 a 20 m3": 12.17,
                    "21 a 30 m3": 13.72, "31 a 40 m3": 14.83, "41 a 50 m3": 15.57,
                    "51 a 90 m3": 15.95, "91 a 150 m3": 16.01, ">150 m3": 16.01,
                },
                "São Miguel dos Campos": {
                    "0 a 10 m3": 5.49, "11 a 15 m3": 10.48, "16 a 20 m3": 12.11,
                    "21 a 30 m3": 12.94, "31 a 40 m3": 13.36, "41 a 50 m3": 13.54,
                    "51 a 90 m3": 13.62, "91 a 150 m3": 13.70, ">150 m3": 13.71,
                },
            }
            band_key = unicodedata.normalize("NFKD", row.get("faixa_consumo_m3", "")).encode("ascii", "ignore").decode().strip()
            rates = city_overrides.get(row.get("municipio"), rates_by_scope.get(row.get("saneamento_prestador"), {}))
            if band_key in rates:
                water = rates[band_key]
                sewer_pct = 100 if row.get("municipio") == "Maceió" else 80
                row["tarifa_agua_r_m3"] = f"{water:.3f}" if row.get("saneamento_prestador") == "CASAL" else f"{water:.2f}"
                row["tarifa_agua_fixa_minima_r"] = ""
                row["tarifa_esgoto_r_m3"] = f"{water * sewer_pct / 100:.3f}" if row.get("saneamento_prestador") == "CASAL" else f"{water * sewer_pct / 100:.2f}"
                row["tarifa_esgoto_fixa_minima_r"] = ""
                row["esgoto_pct_sobre_agua"] = str(sewer_pct)
                evidence = SANITATION_EVIDENCE[row["saneamento_prestador"]]
                row["fonte_saneamento"] = evidence["url"]
                row["vigencia_saneamento"] = (
                    "Vigente desde 08/03/2026" if row.get("saneamento_prestador") in {"Águas do Sertão", "Verde Alagoas"}
                    else "Vigente desde dezembro de 2025"
                )
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO_POR_MUNICIPIO"
                row["observacao"] = (
                    "Prestador e nove faixas residenciais conciliados com a estrutura oficial aplicável ao município; "
                    f"esgoto = {sewer_pct}% da água quando a rede está disponível."
                )
        if row.get("saneamento_prestador") in {"Prolagos", "Águas de Juturnaíba"} and row.get("categoria") == "Residencial normal":
            prolagos_rates = {
                "0 a 10 m3": 17.04, "11 a 15 m3": 22.32, "16 a 25 m3": 35.74,
                "26 a 35 m3": 42.88, "36 a 45 m3": 51.46, "46 a 55 m3": 63.18,
                "56 a 65 m3": 80.25, ">65 m3": 91.26,
            }
            juturnaiba_rates = {
                "0 a 10 m3": 13.79, "11 a 15 m3": 17.71, "16 a 25 m3": 26.45,
                "26 a 35 m3": 33.10, "36 a 45 m3": 42.43, "46 a 55 m3": 51.93,
                "56 a 65 m3": 66.02, ">65 m3": 80.27,
            }
            band_key = unicodedata.normalize("NFKD", row.get("faixa_consumo_m3", "")).encode("ascii", "ignore").decode().strip()
            rates = juturnaiba_rates if row.get("saneamento_prestador") == "Águas de Juturnaíba" else prolagos_rates
            if band_key in rates:
                water = rates[band_key]
                row["tarifa_agua_r_m3"] = f"{water:.2f}"
                row["tarifa_agua_fixa_minima_r"] = ""
                row["tarifa_esgoto_r_m3"] = f"{water:.2f}"
                row["tarifa_esgoto_fixa_minima_r"] = ""
                row["esgoto_pct_sobre_agua"] = "100"
                row["vigencia_saneamento"] = "Vigente desde 01/12/2025"
                row["fonte_saneamento"] = SANITATION_EVIDENCE[row["saneamento_prestador"]]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["observacao"] = (
                    "Estrutura domiciliar conciliada faixa a faixa com a tabela oficial vigente; "
                    "esgoto modelado a 100% da tarifa de água conforme estrutura contratual usada no estudo."
                )
        if row.get("saneamento_prestador") == "Águas de Manaus" and row.get("categoria") == "Residencial normal":
            manaus_rates = {
                "0 a 10 m3": (6.4156, 5.1325), "11 a 20 m3": (12.4334, 9.9467),
                "21 a 30 m3": (18.9830, 15.1864), "31 a 40 m3": (25.8577, 20.6861),
                "41 a 60 m3": (29.8358, 23.8686), ">60 m3": (34.0186, 27.2149),
            }
            band_key = unicodedata.normalize("NFKD", row.get("faixa_consumo_m3", "")).encode("ascii", "ignore").decode().strip()
            if band_key in manaus_rates:
                water, sewer = manaus_rates[band_key]
                row["tarifa_agua_r_m3"] = f"{water:.4f}"
                row["tarifa_esgoto_r_m3"] = f"{sewer:.4f}"
                row["tarifa_agua_fixa_minima_r"] = ""
                row["tarifa_esgoto_fixa_minima_r"] = ""
                row["esgoto_pct_sobre_agua"] = "80"
                row["vigencia_saneamento"] = "Vigente desde fevereiro de 2026"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["Águas de Manaus"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["observacao"] = (
                    "Seis faixas residenciais de água e esgoto conciliadas com a tabela oficial após o reajuste de 5,52% de 2026."
                )
        if row.get("saneamento_prestador") == "SAAE Cacoal" and row.get("categoria") == "Residencial normal":
            cacoal_rates = {
                "0 a 10 m3": (None, 17.58), "11 a 15 m3": (2.109, None),
                "16 a 20 m3": (2.426, None), "21 a 25 m3": (2.788, None),
                "26 a 30 m3": (3.209, None), "31 a 50 m3": (3.689, None),
                ">50 m3": (4.057, None),
            }
            band_key = unicodedata.normalize("NFKD", row.get("faixa_consumo_m3", "")).encode("ascii", "ignore").decode().strip()
            if band_key in cacoal_rates:
                water, water_fixed = cacoal_rates[band_key]
                row["tarifa_agua_r_m3"] = "" if water is None else f"{water:.3f}"
                row["tarifa_agua_fixa_minima_r"] = "" if water_fixed is None else f"{water_fixed:.2f}"
                row["tarifa_esgoto_r_m3"] = "" if water is None else f"{water * 0.60:.4f}"
                row["tarifa_esgoto_fixa_minima_r"] = "" if water_fixed is None else f"{water_fixed * 0.60:.2f}"
                row["esgoto_pct_sobre_agua"] = "60"
                row["vigencia_saneamento"] = "Vigente desde 28/12/2025"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["SAAE Cacoal"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["observacao"] = (
                    "Sete faixas residenciais e esgoto a 60% conciliados com o Anexo I da Lei Municipal nº 5.693/2025."
                )
        if row.get("saneamento_prestador") == "SANEAR Colatina" and row.get("categoria") == "Residencial normal":
            sanear_rates = {
                "0 a 10 m3": (2.85, 2.28), "11 a 15 m3": (5.92, 4.74),
                "16 a 20 m3": (8.50, 6.80), "21 a 30 m3": (9.36, 7.49),
                "31 a 50 m3": (9.98, 7.98), ">50 m3": (10.41, 8.33),
            }
            band_key = unicodedata.normalize("NFKD", row.get("faixa_consumo_m3", "")).encode("ascii", "ignore").decode().strip()
            if band_key in sanear_rates:
                water, sewer = sanear_rates[band_key]
                row["tarifa_agua_r_m3"] = f"{water:.2f}"
                row["tarifa_esgoto_r_m3"] = f"{sewer:.2f}"
                row["tarifa_agua_fixa_minima_r"] = ""
                row["tarifa_esgoto_fixa_minima_r"] = ""
                row["esgoto_pct_sobre_agua"] = "80"
                row["vigencia_saneamento"] = "Vigente de 01/12/2025 a 30/11/2026"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["SANEAR Colatina"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["observacao"] = (
                    "Seis faixas residenciais de água e de coleta, afastamento e tratamento de esgoto "
                    "conciliadas diretamente com o Anexo I da Resolução ARSP nº 094/2025."
                )
        if row.get("saneamento_prestador") == "Águas Guariroba" and row.get("categoria") == "Residencial normal":
            guariroba_rates = {
                "Tarifa fixa": (None, 19.87, None, None),
                "1 a 10 m3": (8.03, None, 5.62, None),
                "11 a 15 m3": (10.28, None, 7.20, None),
                "16 a 20 m3": (10.46, None, 7.32, None),
                "21 a 25 m3": (11.57, None, 8.10, None),
                "26 a 30 m3": (14.23, None, 9.96, None),
                "31 a 50 m3": (17.02, None, 11.91, None),
                ">50 m3": (18.75, None, 13.13, None),
            }
            band_key = unicodedata.normalize("NFKD", row.get("faixa_consumo_m3", "")).encode("ascii", "ignore").decode().strip()
            if band_key in guariroba_rates:
                water, water_fixed, sewer, sewer_fixed = guariroba_rates[band_key]
                row["tarifa_agua_r_m3"] = "" if water is None else f"{water:.2f}"
                row["tarifa_agua_fixa_minima_r"] = "" if water_fixed is None else f"{water_fixed:.2f}"
                row["tarifa_esgoto_r_m3"] = "" if sewer is None else f"{sewer:.2f}"
                row["tarifa_esgoto_fixa_minima_r"] = "" if sewer_fixed is None else f"{sewer_fixed:.2f}"
                row["esgoto_pct_sobre_agua"] = "70"
                row["vigencia_saneamento"] = "Vigente desde 03/01/2026"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["Águas Guariroba"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["observacao"] = (
                    "Tarifa fixa e sete faixas residenciais de água e esgoto conciliadas com a estrutura "
                    "oficial de 2026, homologada pela Portaria nº 37/2025."
                )
        if row.get("saneamento_prestador") == "DMAE Poços de Caldas" and row.get("categoria") == "Residencial normal":
            water = num(row.get("tarifa_agua_r_m3"))
            if water is not None:
                row["tarifa_esgoto_r_m3"] = f"{water * 0.85:.6f}"
                row["tarifa_esgoto_fixa_minima_r"] = ""
                row["esgoto_pct_sobre_agua"] = "85"
                row["vigencia_saneamento"] = "Vigente desde 01/06/2026"
                row["fonte_saneamento"] = SANITATION_EVIDENCE["DMAE Poços de Caldas"]["url"]
                row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO"
                row["observacao"] = (
                    "Nove faixas residenciais de água conciliadas com a tabela oficial; tarifa de esgoto "
                    "corrigida para 85% da tarifa de água conforme regra expressa do DMAE."
                )
        if row.get("saneamento_prestador") == "RIC Ambiental" and row.get("categoria") == "Residencial normal":
            row["vigencia_saneamento"] = "Vigente desde abril de 2026"
            row["fonte_saneamento"] = SANITATION_EVIDENCE["RIC Ambiental"]["url"]
            row["status_saneamento"] = "OFICIAL_ATUAL_RECONCILIADO_POR_REAJUSTE"
            row["observacao"] = (
                "Estrutura residencial conciliada pela aplicação do reajuste linear oficial de 6,72% "
                "homologado pela Resolução AMAE nº 04/2026; tarifa mínima combinada verificada em R$ 34,49."
            )
        # A AGESPISA perdeu a concessão; a Águas do Piauí assumiu a operação
        # estadual em 2025. Os valores legados são preservados como referência
        # contratual até conciliação linha a linha com a tabela da concessionária.
        if row.get("uf") == "PI" and row.get("saneamento_prestador") == "AGESPISA":
            row["saneamento_prestador"] = "Águas do Piauí"
            row["agencia_reguladora"] = "AGRESPI / MRAE-PI"
            row["fonte_saneamento"] = SANITATION_EVIDENCE["Águas do Piauí"]["url"]
            row["status_saneamento"] = "OPERADOR_ATUAL_VERIFICADO_VALOR_CONTRATUAL_NAO_RECONCILIADO"
            row["observacao"] = (
                "Operador atualizado para Águas do Piauí; valor herdado da base contratual, "
                "pendente de conciliação com tabela tarifária vigente publicada."
            )
        if row.get("uf") == "AL" and row.get("municipio") == "Coruripe":
            row["saneamento_prestador"] = "DAESC Coruripe"
            row["agencia_reguladora"] = "Regulação municipal"
            row["fonte_saneamento"] = SANITATION_EVIDENCE["DAESC Coruripe"]["url"]
            row["status_saneamento"] = "OPERADOR_ATUAL_VERIFICADO_ATO_TARIFARIO_LOCALIZADO"
            row["observacao"] = (
                "Prestador corrigido para o Departamento de Água e Esgoto Sanitário de Coruripe (DAESC); "
                "valor legado ainda requer conciliação com o ato da tarifa-base."
            )
        city_key = key_text(row["municipio"])
        if len(by_key.get(city_key, [])) == 1:
            row["municipio"] = by_key[city_key][0]
        elif "�" in row["municipio"] or not by_key.get(city_key):
            best = max(geo_names, key=lambda n: SequenceMatcher(None, city_key, key_text(n)).ratio())
            if SequenceMatcher(None, city_key, key_text(best)).ratio() >= 0.82:
                row["municipio"] = best
    return rows


def audit(rows, aneel):
    groups = defaultdict(list)
    for row in rows:
        groups[(row["uf"], row["municipio"])].append(row)
    summaries = []
    audit_by_city = {}
    for (uf, city), items in sorted(groups.items()):
        base = items[0]
        volumetric = [r for r in items if num(r.get("tarifa_agua_r_m3")) is not None]
        first = min(volumetric, key=lambda r: num(r["tarifa_agua_r_m3"])) if volumetric else base
        water = num(first.get("tarifa_agua_r_m3"))
        sewer_pct = num(base.get("esgoto_pct_sobre_agua")) or 0.0
        model_energy = num(base.get("tarifa_eletricidade_b1_r_kwh"))
        distributor = base["energia_distribuidora"]
        agent = ANEEL_ALIASES.get(distributor)
        official = aneel.get(agent, {})
        official_energy = official.get("energia_aneel_sem_tributos_r_kwh")
        diff = ((model_energy / official_energy) - 1.0) * 100.0 if model_energy and official_energy else None

        status = " ".join(r.get("status_saneamento", "") for r in items).upper()
        vigency = " ".join(r.get("vigencia_saneamento", "") for r in items)
        source = base.get("fonte_saneamento", "")
        evidence = SANITATION_EVIDENCE.get(base["saneamento_prestador"], {})
        evidence_url = evidence.get("url", source)
        evidence_type = evidence.get(
            "tipo",
            "página oficial específica" if re.search(r"tarifa|tabela|resolu|delibera", source, re.I)
            else "página institucional informada na base",
        )
        reconciled = evidence.get("reconciliado")

        # Rubrica auditável (100 pontos): autoridade/especificidade da fonte
        # (35), atualidade (20), conciliação numérica (25), completude (15) e
        # consistência do operador (5).
        # Portais públicos frequentemente usam endpoints opacos (por exemplo,
        # ``/download/452504`` ou um diretório documental). A especificidade deve
        # considerar também a natureza registrada da evidência, não apenas as
        # palavras presentes no endereço eletrônico.
        source_specific = bool(re.search(
            r"\.pdf|tarifa|tabela|resolu|delibera|portaria|decreto|estrutura|matriz|repositório",
            evidence_url + " " + evidence_type,
            re.I,
        ))
        san_score = 35.0 if source_specific and evidence_url.startswith("http") else (24.0 if evidence_url.startswith("http") else 8.0)
        if re.search(r"2026|2027", evidence_type + " " + vigency):
            san_score += 20.0
        elif re.search(r"2025", evidence_type + " " + vigency):
            san_score += 15.0
        elif re.search(r"202[34]", evidence_type + " " + vigency):
            san_score += 8.0
        else:
            san_score += 5.0
        san_score += 25.0 if reconciled is True else (8.0 if reconciled is False else 12.0)
        san_score += 15.0 if len(volumetric) >= 2 else (8.0 if volumetric or any(num(r.get("tarifa_agua_fixa_minima_r")) for r in items) else 0.0)
        san_score += 2.0 if "OPERADOR_ATUAL_VERIFICADO" in status else 5.0
        if "FALLBACK" in status:
            san_score -= 15.0
        if "NAO_RECONCILIADO" in status:
            san_score -= 10.0
        san_score = max(0.0, min(100.0, san_score))

        if reconciled is True:
            audit_alert = "Valor reconciliado com a evidência primária indicada."
        elif reconciled is False:
            audit_alert = "Fonte primária localizada, mas o valor do modelo não foi conciliado integralmente; revisar antes de decisão local."
        else:
            audit_alert = "Fonte oficial localizada; conciliação numérica linha a linha ainda não documentada."

        aneel_status = official.get("energia_aneel_status_vigencia", "NÃO LOCALIZADA")
        if official_energy is not None and aneel_status == "VIGENTE":
            elec_score = 95.0 if diff is not None and -5 <= diff <= 45 else 82.0
            elec_note = "Referência ANEEL vigente localizada; diferença pode refletir tributos/bandeiras não incluídos na base ANEEL."
        elif official_energy is not None:
            elec_score = 75.0
            elec_note = f"Referência ANEEL mais recente localizada, porém {aneel_status.lower().replace('_', ' ')}; não tratada como tarifa vigente."
        elif base.get("energia_status") == "HISTORICO_AUTORIZADO":
            elec_score = 40.0
            elec_note = "Valor histórico do projeto; distribuidora não conciliada automaticamente com registro ANEEL vigente."
        else:
            elec_score = 55.0
            elec_note = "Declarado validado no legado, mas sem conciliação automática com a denominação vigente da ANEEL."
        overall = 0.60 * san_score + 0.40 * elec_score
        rationale = (
            f"Saneamento {grade(san_score)} ({san_score:.0f}/100); energia {grade(elec_score)} "
            f"({elec_score:.0f}/100). {audit_alert} {elec_note}"
        )
        bands = []
        for r in items:
            w = num(r.get("tarifa_agua_r_m3"))
            fixed = num(r.get("tarifa_agua_fixa_minima_r"))
            deduction = num(r.get("parcela_deduzir_agua_r"))
            if w is not None:
                deduction_note = f" − R$ {deduction:.2f}" if deduction not in (None, 0.0) else ""
                fixed_note = f" + R$ {fixed:.2f}/mês" if fixed not in (None, 0.0) else ""
                bands.append(f"{r['faixa_consumo_m3']}: R$ {w:.2f}/m³{fixed_note}{deduction_note}")
            elif fixed is not None:
                bands.append(f"{r['faixa_consumo_m3']}: R$ {fixed:.2f}/mês")

        record = {
            "regiao": base["regiao"], "uf": uf, "municipio": city,
            "prestador_saneamento": base["saneamento_prestador"],
            "agencia_reguladora": base["agencia_reguladora"],
            "categoria": base["categoria"],
            "tarifa_agua_primeira_faixa_r_m3": water,
            "tarifa_fixa_agua_r_mes": max((num(r.get("tarifa_agua_fixa_minima_r")) or 0 for r in items), default=0),
            "esgoto_pct_sobre_agua": sewer_pct,
            "tarifa_combinada_primeira_faixa_r_m3": round(water * (1 + sewer_pct / 100.0), 4) if water is not None else None,
            "faixas_completas": "; ".join(bands),
            "vigencia_saneamento": base["vigencia_saneamento"],
            "fonte_saneamento": source,
            "evidencia_saneamento_primaria": evidence_url,
            "evidencia_esgoto_primaria": evidence.get("url_esgoto", evidence_url),
            "tipo_evidencia_saneamento": evidence_type,
            "valor_reconciliado_com_evidencia": "SIM" if reconciled is True else ("NÃO" if reconciled is False else "PENDENTE"),
            "fonte_cruzada_cobertura_sinisa": SINISA_URL,
            "fonte_cruzada_tarifa_social_ana": ANA_SOCIAL_TARIFF_URL,
            "alerta_auditoria_saneamento": audit_alert,
            "status_saneamento_original": base["status_saneamento"],
            "confianca_saneamento_score": round(san_score, 1),
            "confianca_saneamento_grau": grade(san_score),
            "distribuidora_energia": distributor,
            "energia_modelo_referencia_aneel_sem_tributos_r_kwh": model_energy,
            "energia_aneel_sem_tributos_r_kwh": official_energy,
            "diferenca_modelo_vs_aneel_pct": round(diff, 2) if diff is not None else None,
            "energia_aneel_inicio_vigencia": official.get("energia_aneel_inicio_vigencia"),
            "energia_aneel_fim_vigencia": official.get("energia_aneel_fim_vigencia"),
            "energia_aneel_ato": official.get("energia_aneel_ato"),
            "energia_aneel_status_vigencia": aneel_status,
            "fonte_energia_aneel": ANEEL_DATA_URL,
            "metodologia_energia_aneel": ANEEL_METHOD_URL,
            "confianca_energia_score": round(elec_score, 1),
            "confianca_energia_grau": grade(elec_score),
            "confianca_global_score": round(overall, 1),
            "confianca_global_grau": grade(overall),
            "justificativa_confianca": rationale,
            "data_auditoria": AUDIT_DATE.isoformat(),
        }
        summaries.append(record)
        audit_by_city[(uf, city)] = record
    for row in rows:
        audit = audit_by_city[(row["uf"], row["municipio"])]
        row.update({
            "evidencia_saneamento_primaria": audit["evidencia_saneamento_primaria"],
            "tipo_evidencia_saneamento": audit["tipo_evidencia_saneamento"],
            "valor_reconciliado_com_evidencia": audit["valor_reconciliado_com_evidencia"],
            "fonte_cruzada_cobertura_sinisa": SINISA_URL,
            "fonte_cruzada_tarifa_social_ana": ANA_SOCIAL_TARIFF_URL,
            "alerta_auditoria_saneamento": audit["alerta_auditoria_saneamento"],
            "confianca_saneamento_score": audit["confianca_saneamento_score"],
            "confianca_saneamento_grau": audit["confianca_saneamento_grau"],
            "confianca_energia_score": audit["confianca_energia_score"],
            "confianca_energia_grau": audit["confianca_energia_grau"],
            "confianca_global_score": audit["confianca_global_score"],
            "confianca_global_grau": audit["confianca_global_grau"],
            "justificativa_confianca": audit["justificativa_confianca"],
            "energia_aneel_sem_tributos_r_kwh": audit["energia_aneel_sem_tributos_r_kwh"],
            "energia_aneel_ato": audit["energia_aneel_ato"],
            "energia_aneel_status_vigencia": audit["energia_aneel_status_vigencia"],
            "fonte_energia_aneel": ANEEL_DATA_URL,
            "metodologia_energia_aneel": ANEEL_METHOD_URL,
            "data_auditoria": AUDIT_DATE.isoformat(),
        })
    return rows, summaries


def write_csv(path, rows):
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main():
    rows = load_rows()
    aneel = load_aneel_current()
    detailed, summary = audit(rows, aneel)
    write_csv(DETAILED_OUT, detailed)
    write_csv(SUMMARY_OUT, summary)
    counts = defaultdict(int)
    for r in summary:
        counts[r["confianca_global_grau"]] += 1
    print(f"Detalhado: {len(detailed)} linhas -> {DETAILED_OUT}")
    print(f"Resumo: {len(summary)} municípios -> {SUMMARY_OUT}")
    print("Confiança global:", dict(counts))


if __name__ == "__main__":
    main()
