"""Bibliografia única do Netuno 5.

As citações já viveram soltas dentro das strings HTML da aba de
Documentação, duplicadas em português e inglês. Sete das dezesseis seções não
tinham citação nenhuma, e as que tinham escreviam a referência à mão nos dois
idiomas — de modo que uma correção precisava ser feita duas vezes, e nada
verificava se fora feita.

Aqui cada referência é **um registro só**, com DOI, e a lista exibida em cada
seção é gerada a partir dele. Três consequências práticas:

1. A promessa «pelo menos três citações por seção» passa a ser verificável por
   teste (`tests/unit/test_documentation_citations.py`), não por disciplina.
2. Corrigir uma referência corrige os dois idiomas de uma vez.
3. O campo ``recuperado_por`` obriga a dizer de onde veio o registro. O valor
   ``"memoria"`` é proibido pelo teste: toda referência tem de ter sido
   recuperada de uma base, nunca lembrada.

O campo ``recuperado_por`` registra a base de onde veio cada registro, e o teste
correspondente rejeita entradas sem essa marcação. Referência conferida contra
Crossref ou OpenAlex é o que separa uma bibliografia de uma lista de lembranças.
"""

from __future__ import annotations

import html
from dataclasses import dataclass, field
from datetime import date
from typing import Dict, Iterable, Literal, Optional, Tuple

TipoDeRegistro = Literal["artigo", "norma", "base_de_dados", "software", "relatorio", "livro"]

# Data em que os registros bibliográficos foram conferidos no Crossref/OpenAlex.
CONFERIDO_EM = date(2026, 9, 8)


@dataclass(frozen=True)
class Referencia:
    """Um registro bibliográfico conferido.

    ``nota_pt``/``nota_en`` dizem **o que a referência sustenta** neste
    programa. Sem isso, uma lista de referências vira ornamento: o leitor não
    sabe qual afirmação depende de qual fonte.
    """

    chave: str
    autores: str
    ano: int
    titulo: str
    veiculo: str
    tipo: TipoDeRegistro = "artigo"
    doi: Optional[str] = None
    url: Optional[str] = None
    detalhe: str = ""                     # volume, número, páginas
    acessado_em: Optional[date] = None    # obrigatório quando não é artigo
    recuperado_por: str = "crossref"      # crossref | openalex | scite | editor | usuario
    nota_pt: str = ""
    nota_en: str = ""

    @property
    def link(self) -> Optional[str]:
        if self.doi:
            return f"https://doi.org/{self.doi}"
        return self.url


def _r(**kwargs) -> Tuple[str, Referencia]:
    ref = Referencia(**kwargs)
    return ref.chave, ref


REFERENCIAS: Dict[str, Referencia] = dict(
    [
        # ------------------------------------------------------------------
        # Aproveitamento de água pluvial — fundamentos e revisões
        # ------------------------------------------------------------------
        _r(
            chave="campisano_2017",
            autores="CAMPISANO, A.; BUTLER, D.; WARD, S. et al.",
            ano=2017,
            titulo="Urban rainwater harvesting systems: research, implementation and future perspectives",
            veiculo="Water Research",
            detalhe="v. 115, p. 195–209",
            doi="10.1016/j.watres.2017.02.056",
            recuperado_por="openalex",
            nota_pt="Revisão de referência do campo; situa o balanço diário como método padrão de avaliação.",
            nota_en="Field-defining review; establishes daily water balance as the standard assessment method.",
        ),
        _r(
            chave="teston_2018",
            autores="TESTON, A.; GERALDI, M. S.; COLASIO, B. M.; GHISI, E.",
            ano=2018,
            titulo="Rainwater harvesting in buildings in Brazil: a literature review",
            veiculo="Water",
            detalhe="v. 10, n. 4, art. 471",
            doi="10.3390/w10040471",
            recuperado_por="openalex",
            nota_pt="Revisão do caso brasileiro: potencial de economia, legislação municipal e lacunas de pesquisa.",
            nota_en="Review of the Brazilian case: savings potential, municipal legislation and research gaps.",
        ),
        _r(
            chave="souza_ghisi_2012",
            autores="SOUZA, E. L.; GHISI, E.",
            ano=2012,
            titulo="Potable water savings by using rainwater for non-potable uses in houses",
            veiculo="Water",
            detalhe="v. 4, n. 3, p. 607–628",
            doi="10.3390/w4030607",
            recuperado_por="openalex",
            nota_pt="Aplica o próprio programa Netuno a treze cidades; mostra que a regularidade da chuva pesa mais que o total anual.",
            nota_en="Applies the Netuno programme itself to thirteen cities; shows rainfall regularity matters more than annual depth.",
        ),
        _r(
            chave="maykot_ghisi_2020",
            autores="MAYKOT, J. K.; GHISI, E.",
            ano=2020,
            titulo="Assessment of a rainwater harvesting system in a multi-storey residential building in Brazil",
            veiculo="Water",
            detalhe="v. 12, n. 2, art. 546",
            doi="10.3390/w12020546",
            recuperado_por="openalex",
            nota_pt=(
                "Usos finais medidos em apartamentos: chuveiro 54,2%, máquina de lavar 21,3%, "
                "torneira de cozinha 9,3%, bacia sanitária 9,2%, lavatório 2,6%. Simulações feitas com o Netuno 4."
            ),
            nota_en=(
                "Measured end uses in flats: shower 54.2%, washing machine 21.3%, kitchen tap 9.3%, "
                "toilet 9.2%, washbasin 2.6%. Simulations run with Netuno 4."
            ),
        ),
        _r(
            chave="semaan_2020",
            autores="SEMAAN, M.; DAY, S. D.; GARVIN, M.; RAMAKRISHNAN, N.; PEARCE, A.",
            ano=2020,
            titulo="Optimal sizing of rainwater harvesting systems for domestic water usages: a systematic literature review",
            veiculo="Resources, Conservation & Recycling: X",
            detalhe="v. 6, art. 100033",
            doi="10.1016/j.rcrx.2020.100033",
            recuperado_por="openalex",
            nota_pt=(
                "Revisão sistemática de dimensionamento. Registra que otimizar por máximo local é mais "
                "frequente que por simulação, e que a variação da demanda costuma ser ignorada."
            ),
            nota_en=(
                "Systematic review of sizing. Records that local-maximum optimisation is more common than "
                "simulation-based, and that demand variation is usually ignored."
            ),
        ),
        _r(
            chave="freni_liuzzo_2019",
            autores="FRENI, G.; LIUZZO, L.",
            ano=2019,
            titulo="Effectiveness of rainwater harvesting systems for flood reduction in residential urban areas",
            veiculo="Water",
            detalhe="v. 11, n. 7, art. 1389",
            doi="10.3390/w11071389",
            recuperado_por="openalex",
            nota_pt="Emprega explicitamente o algoritmo *yield-after-spillage* no balanço diário — a mesma ordem de operações adotada aqui.",
            nota_en="Explicitly uses the yield-after-spillage algorithm for the daily balance — the same order of operations adopted here.",
        ),
        _r(
            chave="raimondi_2023",
            autores="RAIMONDI, A.; QUINN, R.; ABHIJITH, G. R.; BECCIU, G.; OSTFELD, A.",
            ano=2023,
            titulo="Rainwater harvesting and treatment: state of the art and perspectives",
            veiculo="Water",
            detalhe="v. 15, n. 8, art. 1518",
            doi="10.3390/w15081518",
            recuperado_por="openalex",
            nota_pt="Estado da arte de captação e tratamento; discute escalas temporais de projeto e tecnologias de tratamento.",
            nota_en="State of the art of harvesting and treatment; covers design time scales and treatment technologies.",
        ),
        _r(
            chave="matos_2013",
            autores="MATOS, C.; SANTOS, C.; PEREIRA, S. et al.",
            ano=2013,
            titulo="Rainwater storage tank sizing: case study of a commercial building",
            veiculo="International Journal of Sustainable Built Environment",
            detalhe="v. 2, n. 2, p. 109–118",
            doi="10.1016/j.ijsbe.2014.04.004",
            recuperado_por="openalex",
            nota_pt="Dimensionamento em edifício comercial sob diferentes conjuntos de usos não potáveis.",
            nota_en="Sizing in a commercial building under different sets of non-potable end uses.",
        ),
        _r(
            chave="kisakye_2018",
            autores="KISAKYE, V.; VAN DER BRUGGEN, B.",
            ano=2018,
            titulo="Effects of climate change on water savings and water security from rainwater harvesting systems",
            veiculo="Resources, Conservation and Recycling",
            detalhe="v. 138, p. 49–63",
            doi="10.1016/j.resconrec.2018.07.009",
            recuperado_por="openalex",
            nota_pt="Sustenta por que a série pluviométrica de entrada precisa ser longa e datada: o desempenho muda com o regime.",
            nota_en="Supports why the input rainfall series must be long and dated: performance shifts with the regime.",
        ),
        _r(
            chave="belmeziti_2013",
            autores="BELMEZITI, A.; COUTARD, O.; DE GOUVELLO, B.",
            ano=2013,
            titulo="A new methodology for evaluating potential for potable water savings by using rainwater harvesting at the urban level",
            veiculo="Water",
            detalhe="v. 5, n. 1, p. 312–326",
            doi="10.3390/w5010312",
            recuperado_por="openalex",
            nota_pt="Define o potencial de economia de água potável como indicador e o escala do edifício para o município.",
            nota_en="Defines potable water savings potential as an indicator and scales it from building to municipality.",
        ),
        _r(
            chave="melville_shreeve_2016",
            autores="MELVILLE-SHREEVE, P.; WARD, S.; BUTLER, D.",
            ano=2016,
            titulo="Rainwater harvesting typologies for UK houses: a multi criteria analysis of system configurations",
            veiculo="Water",
            detalhe="v. 8, n. 4, art. 129",
            doi="10.3390/w8040129",
            recuperado_por="openalex",
            nota_pt="Aplica análise multicritério à escolha de configuração de sistema pluvial — o mesmo problema que a aba de decisão resolve.",
            nota_en="Applies multi-criteria analysis to rainwater system configuration choice — the same problem the decision tab solves.",
        ),
        _r(
            chave="vieira_2014",
            autores="VIEIRA, A. S.; BEAL, C. D.; GHISI, E.; STEWART, R. A.",
            ano=2014,
            titulo="Energy intensity of rainwater harvesting systems: a review",
            veiculo="Renewable and Sustainable Energy Reviews",
            detalhe="v. 34, p. 225–242",
            doi="10.1016/j.rser.2014.03.012",
            recuperado_por="scite",
            nota_pt=(
                "Intensidade energética publicada: mediana de 1,40 kWh/m³ nos estudos empíricos revisados, "
                "contra 0,48 kWh/m³ do abastecimento público. Sistemas de recalque direto ficam entre 2,00 e "
                "3,90 kWh/m³; sistemas por gravidade com reservatório elevado tendem à neutralidade energética."
            ),
            nota_en=(
                "Published energy intensity: median 1.40 kWh/m³ across the reviewed empirical studies, against "
                "0.48 kWh/m³ for mains supply. Direct-feed pumped systems range 2.00–3.90 kWh/m³; gravity "
                "systems with a header tank tend towards energy neutrality."
            ),
        ),
        # ------------------------------------------------------------------
        # Qualidade da água e descarte de primeira chuva
        # ------------------------------------------------------------------
        _r(
            chave="maykot_vaz_ghisi_2025",
            autores="MAYKOT, J. K.; MARTINS VAZ, I. C.; GHISI, E.",
            ano=2025,
            titulo="Characterisation of first flush for rainwater harvesting purposes in buildings",
            veiculo="Water",
            detalhe="v. 17, n. 12, art. 1772",
            doi="10.3390/w17121772",
            recuperado_por="crossref",
            nota_pt="Caracterização experimental do descarte de primeira chuva — base empírica do modelo de *wash-off*.",
            nota_en="Experimental characterisation of first flush — empirical basis of the wash-off model.",
        ),
        _r(
            chave="rahman_2014",
            autores="RAHMAN, S.; KHAN, M. T. R.; AKIB, S. et al.",
            ano=2014,
            titulo="Sustainability of rainwater harvesting system in terms of water quality",
            veiculo="The Scientific World Journal",
            detalhe="art. 721357",
            doi="10.1155/2014/721357",
            recuperado_por="openalex",
            nota_pt="Mede pH, turbidez, coliformes totais e termotolerantes em água pluvial — os parâmetros que a aba de qualidade avalia.",
            nota_en="Measures pH, turbidity, total and faecal coliforms in harvested rainwater — the parameters the quality tab assesses.",
        ),
        # ------------------------------------------------------------------
        # Análise de ciclo de vida
        # ------------------------------------------------------------------
        _r(
            chave="vaz_2023_acv",
            autores="MARTINS VAZ, I. C.; ISTCHUK, R. N.; ONEDA, T. M. S.; GHISI, E.",
            ano=2023,
            titulo="Sustainable rainwater management and life cycle assessment: challenges and perspectives",
            veiculo="Sustainability",
            detalhe="v. 15, n. 16, art. 12133",
            doi="10.3390/su151612133",
            recuperado_por="scite",
            nota_pt="Revisão de ACV aplicada à gestão de água pluvial: fronteiras, unidades funcionais e o que a literatura ainda não fecha.",
            nota_en="Review of LCA applied to rainwater management: boundaries, functional units and what the literature still leaves open.",
        ),
        _r(
            chave="ghimire_2014",
            autores="GHIMIRE, S. R.; JOHNSTON, J. M.; INGWERSEN, W. W.; HAWKINS, T. R.",
            ano=2014,
            titulo="Life cycle assessment of domestic and agricultural rainwater harvesting systems",
            veiculo="Environmental Science & Technology",
            detalhe="v. 48, n. 7, p. 4069–4077",
            doi="10.1021/es500189f",
            recuperado_por="scite",
            nota_pt="ACV completa de sistemas domésticos e agrícolas; identifica a bomba e a energia de bombeamento como os itens dominantes.",
            nota_en="Full LCA of domestic and agricultural systems; identifies the pump and pumping energy as the dominant items.",
        ),
        _r(
            chave="ghimire_2017",
            autores="GHIMIRE, S. R.; JOHNSTON, J. M.; INGWERSEN, W. W.; SOJKA, S.",
            ano=2017,
            titulo="Life cycle assessment of a commercial rainwater harvesting system compared with a municipal water supply system",
            veiculo="Journal of Cleaner Production",
            detalhe="v. 151, p. 74–86",
            doi="10.1016/j.jclepro.2017.02.025",
            recuperado_por="crossref",
            nota_pt="Compara sistema pluvial comercial com abastecimento público — a comparação que sustenta a emissão evitada por m³.",
            nota_en="Compares a commercial rainwater system with municipal supply — the comparison behind the avoided emission per m³.",
        ),
        _r(
            chave="wang_zimmerman_2015",
            autores="WANG, R.; ZIMMERMAN, J. B.",
            ano=2015,
            titulo="Economic and environmental assessment of office building rainwater harvesting systems in various U.S. cities",
            veiculo="Environmental Science & Technology",
            detalhe="v. 49, n. 3, p. 1768–1778",
            doi="10.1021/es5046887",
            recuperado_por="crossref",
            nota_pt="Junta desempenho econômico e ambiental num mesmo estudo, como faz a aba de decisão multicritério.",
            nota_en="Joins economic and environmental performance in one study, as the multi-criteria tab does.",
        ),
        _r(
            chave="hammond_jones_2008",
            autores="HAMMOND, G. P.; JONES, C. I.",
            ano=2008,
            titulo="Embodied energy and carbon in construction materials",
            veiculo="Proceedings of the Institution of Civil Engineers — Energy",
            detalhe="v. 161, n. 2, p. 87–98",
            doi="10.1680/ener.2008.161.2.87",
            recuperado_por="scite",
            nota_pt=(
                "Artigo que descreve a base ICE (Universidade de Bath). A Tabela 2 publica seis materiais — "
                "tijolo, cimento, concreto, vidro, aço e madeira — e sustenta aqui o fator do concreto. "
                "Os plásticos vêm de fontes próprias, listadas nesta mesma seção."
            ),
            nota_en=(
                "Paper describing the ICE database (University of Bath). Table 2 publishes six materials — "
                "brick, cement, concrete, glass, steel and timber — and supports the concrete factor here. "
                "Plastics are sourced separately, listed in this same section."
            ),
        ),
        _r(
            chave="khan_tee_2015",
            autores="KHAN, L. R.; TEE, K. F.",
            ano=2015,
            titulo="Quantification and comparison of carbon emissions for flexible underground pipelines",
            veiculo="Canadian Journal of Civil Engineering",
            detalhe="v. 42, n. 10, p. 728–736",
            doi="10.1139/cjce-2015-0156",
            recuperado_por="openalex",
            nota_pt="Emissões de ciclo de vida de tubulações de PVC, aço e ferro dúctil — referência para o fator do PVC.",
            nota_en="Life-cycle emissions of PVC, steel and ductile iron pipelines — reference for the PVC factor.",
        ),
        _r(
            chave="alsadi_matthews_2022",
            autores="ALSADI, A. A.; MATTHEWS, J. C.",
            ano=2022,
            titulo="Reduction of carbon emission is optimized during the life cycle of commonly used force main pipe materials",
            veiculo="Frontiers in Water",
            detalhe="v. 4, art. 735519",
            doi="10.3389/frwa.2022.735519",
            recuperado_por="openalex",
            nota_pt="ACV de tubos de PEAD, PVC e concreto ao longo de 100 anos, com as quatro fases separadas.",
            nota_en="LCA of HDPE, PVC and concrete pipes over 100 years, with the four phases separated.",
        ),
        _r(
            chave="ryan_garcia_2021",
            autores="RYAN, C.; GARCÍA-TAENGUA, E.",
            ano=2021,
            titulo="Fibre-reinforced concrete is sustainable and cost-effective for water-retaining structures",
            veiculo="Sustainability",
            detalhe="v. 13, n. 20, art. 11479",
            doi="10.3390/su132011479",
            recuperado_por="openalex",
            nota_pt="Pegada de carbono de estruturas de contenção de água em concreto — o caso do reservatório em concreto armado.",
            nota_en="Carbon footprint of concrete water-retaining structures — the reinforced-concrete tank case.",
        ),
        _r(
            chave="scolaro_ghisi_2025",
            autores="SCOLARO, T. P.; GHISI, E.",
            ano=2025,
            titulo="Assessing the energy and economic performance of green and cool roofs: a life cycle approach",
            veiculo="Sustainability",
            detalhe="v. 17, n. 13, art. 5782",
            doi="10.3390/su17135782",
            recuperado_por="openalex",
            nota_pt="Ciclo de vida de coberturas em três cidades brasileiras; sustenta a escolha do material de telhado.",
            nota_en="Life cycle of roofs across three Brazilian cities; supports the roof material choice.",
        ),
        _r(
            chave="vaz_2025_eletricidade",
            autores="MARTINS VAZ, I. C.; SCOLARO, T. P.; GHISI, E.",
            ano=2025,
            titulo=(
                "Understanding the environmental impact of residential electricity consumption "
                "in Brazil: integrating top-down and bottom-up approaches with life cycle assessment"
            ),
            veiculo="Science of the Total Environment",
            detalhe="v. 986, art. 179774",
            doi="10.1016/j.scitotenv.2025.179774",
            recuperado_por="usuario",
            nota_pt=(
                "Fonte do fator elétrico adotado e da distinção CO₂ × CO₂e. Modela a matriz "
                "brasileira em Ecoinvent 3.8 (método EF 3.1) e mostra que a intensidade sobe de "
                "~0,07 kg CO₂/kWh (SIRENE, só CO₂, só geração) para até 0,20 kg CO₂e/kWh quando "
                "entram os demais gases e processos. Reporta SIDAC = 0,070 kg CO₂/kWh e "
                "CaDI = 0,074 kg CO₂e/kWh para o Brasil."
            ),
            nota_en=(
                "Source of the adopted grid factor and of the CO₂ vs CO₂-eq distinction. Models "
                "the Brazilian matrix in Ecoinvent 3.8 (EF 3.1) and shows intensity rising from "
                "~0.07 kg CO₂/kWh (SIRENE, CO₂ only, generation only) to as much as 0.20 kg "
                "CO₂e/kWh once other gases and processes enter. Reports SIDAC = 0.070 kg CO₂/kWh "
                "and CaDI = 0.074 kg CO₂e/kWh for Brazil."
            ),
        ),
        _r(
            chave="acc_hdpe_2020",
            autores="FRANKLIN ASSOCIATES (para o American Chemistry Council, Plastics Division)",
            ano=2020,
            titulo="Cradle-to-gate life cycle analysis of high-density polyethylene (HDPE) resin",
            veiculo="American Chemistry Council, Washington DC",
            tipo="relatorio",
            detalhe="Tabela 6: 1.612 kg CO₂e por 1.000 kg de resina",
            url="https://www.americanchemistry.com/content/download/8059/file/Cradle-to-Gate-Life-Cycle-Analysis-of-High-Density-Polyethylene-HDPE-Resin.pdf",
            acessado_em=date(2026, 9, 8),
            recuperado_por="editor",
            nota_pt=(
                "Fonte do fator do PEAD: **1,612 kg CO₂e/kg** de resina, berço-ao-portão, "
                "TRACI 2.1 com GWP-100 do IPCC (2013), escopo Estados Unidos. Substitui o valor "
                "interno anterior de 3,00, que declarava a mesma fronteira sem fonte alguma."
            ),
            nota_en=(
                "Source of the HDPE factor: **1.612 kg CO₂e/kg** of resin, cradle-to-gate, "
                "TRACI 2.1 with IPCC (2013) GWP-100, US scope."
            ),
        ),
        _r(
            chave="acc_pvc_2021",
            autores="FRANKLIN ASSOCIATES (para o American Chemistry Council, Plastics Division)",
            ano=2021,
            titulo="Cradle-to-gate life cycle analysis of polyvinyl chloride (PVC) resin",
            veiculo="American Chemistry Council, Washington DC",
            tipo="relatorio",
            detalhe="Tabela 7: 2.095 kg CO₂e por 1.000 kg de resina",
            url="https://www.americanchemistry.com/content/download/10045/file/Cradle-to-Gate-Life-Cycle-Analysis-of-Polyvinyl-PVC-Resin.pdf",
            acessado_em=date(2026, 9, 8),
            recuperado_por="editor",
            nota_pt=(
                "Fonte do fator do PVC das tubulações: **2,095 kg CO₂e/kg** de resina, "
                "berço-ao-portão, TRACI 2.1 / IPCC 2013 GWP-100, escopo Estados Unidos."
            ),
            nota_en=(
                "Source of the pipe PVC factor: **2.095 kg CO₂e/kg** of resin, cradle-to-gate, "
                "TRACI 2.1 / IPCC 2013 GWP-100, US scope."
            ),
        ),
        _r(
            chave="epd_pvc_rxp_2022",
            autores="EPD AUSTRALASIA (operador). RXP PVC Pipes",
            ano=2022,
            titulo="Environmental product declaration: PVC pipes (Series 100 DWV e demais linhas)",
            veiculo="EPD Australasia, registro S-P-05503; EN 15804:2012+A2:2019 e ISO 14025",
            tipo="relatorio",
            detalhe="publicada em 25/11/2022; unidade declarada 1 kg de tubo instalado; Tabela 8, módulos A1–A3",
            url="https://www.environdec.com/library/epd5503",
            acessado_em=date(2026, 9, 8),
            recuperado_por="usuario",
            nota_pt=(
                "Fonte adotada para o fator das tubulações: **2,36 kg CO₂e/kg de tubo instalado** "
                "(GWP-total, módulos A1–A3), com as parcelas fóssil 2,38, biogênica −0,0178 e "
                "LULUC 0,0022 declaradas em separado. Preferida ao valor de resina do American "
                "Chemistry Council porque já inclui composto e extrusão — é o que se instala. "
                "Outras linhas da mesma EPD vão de 2,36 a 2,73 kg CO₂e/kg."
            ),
            nota_en=(
                "Adopted source for the pipe factor: **2.36 kg CO₂e/kg of installed pipe** "
                "(GWP-total, modules A1–A3), with fossil 2.38, biogenic −0.0178 and LULUC 0.0022 "
                "declared separately. Preferred over the American Chemistry Council resin figure "
                "because it already includes compounding and extrusion — what is actually "
                "installed. Other lines in the same EPD range from 2.36 to 2.73 kg CO₂e/kg."
            ),
        ),
        _r(
            chave="alsabri_2020",
            autores="ALSABRI, A.; AL-GHAMDI, S. G.",
            ano=2020,
            titulo="Carbon footprint and embodied energy of PVC, PE and PP piping: perspective on environmental performance",
            veiculo="Energy Reports",
            detalhe="v. 6, p. 364–370",
            doi="10.1016/j.egyr.2020.11.173",
            recuperado_por="crossref",
            nota_pt="Compara a pegada de carbono das três resinas de tubo mais usadas; corrobora a ordem de grandeza da EPD adotada.",
            nota_en="Compares the carbon footprint of the three commonest pipe resins; corroborates the order of magnitude of the adopted EPD.",
        ),
        _r(
            chave="du_2013",
            autores="DU, F.; WOODS, G. J.; KANG, D.; LANSEY, K. E.; ARNOLD, R. G.",
            ano=2013,
            titulo="Life cycle analysis for water and wastewater pipe materials",
            veiculo="Journal of Environmental Engineering (ASCE)",
            detalhe="v. 139, n. 5, p. 703–711",
            doi="10.1061/(ASCE)EE.1943-7870.0000638",
            recuperado_por="usuario",
            nota_pt=(
                "Compara o potencial de aquecimento global de seis materiais de tubo — PVC, ferro "
                "dúctil, ferro fundido, PEAD, concreto e concreto armado — ao longo de quatro fases "
                "do ciclo de vida, por quilômetro e por diâmetro."
            ),
            nota_en=(
                "Compares the global warming potential of six pipe materials — PVC, ductile iron, "
                "cast iron, HDPE, concrete and reinforced concrete — across four life-cycle phases, "
                "per kilometre and by diameter."
            ),
        ),
        _r(
            chave="garfi_2016",
            autores="GARFÍ, M.; CADENA, E.; SANCHEZ-RAMOS, D.; FERRER, I.",
            ano=2016,
            titulo="Life cycle assessment of drinking water: comparing conventional water treatment, reverse osmosis and mineral water in glass and plastic bottles",
            veiculo="Journal of Cleaner Production",
            detalhe="v. 137, p. 997–1003",
            doi="10.1016/j.jclepro.2016.07.218",
            recuperado_por="crossref",
            nota_pt=(
                "Sustenta a ordem de grandeza da emissão evitada por m³ de água potável. Unidade "
                "funcional de 1 m³. O tratamento convencional com osmose reversa doméstica dá "
                "0,512 kg CO₂e/m³ no caso base; o tratamento convencional sozinho fica abaixo "
                "disso. Os 0,35 kg CO₂e/m³ adotados pelo programa caem dentro dessa faixa."
            ),
            nota_en=(
                "Supports the order of magnitude of the avoided emission per m³ of potable water. "
                "Functional unit of 1 m³. Conventional treatment with domestic reverse osmosis "
                "gives 0.512 kg CO₂e/m³ in the base case; conventional treatment alone falls below "
                "that. The programme's 0.35 kg CO₂e/m³ sits inside that range."
            ),
        ),
        _r(
            chave="marinoski_ghisi_2018",
            autores="MARINOSKI, A. K.; GHISI, E.",
            ano=2018,
            titulo="Avaliação de viabilidade ambiental e econômica de sistemas de aproveitamento de água pluvial em habitação de baixo padrão: estudo de caso em Florianópolis, SC",
            veiculo="Ambiente Construído",
            detalhe="v. 18, n. 1, p. 423–443",
            doi="10.1590/s1678-86212018000100230",
            recuperado_por="usuario",
            nota_pt="Viabilidade ambiental e econômica conjunta de sistema pluvial em habitação de interesse social, no mesmo contexto climático e tarifário de Florianópolis.",
            nota_en="Joint environmental and economic feasibility of a rainwater system in social housing, in the same climatic and tariff context of Florianópolis.",
        ),
        _r(
            chave="silva_2023",
            autores="SILVA, M. P. da; GONZÁLEZ, J.; DA COSTA, B. B. F.; GARRIDO, C. et al.",
            ano=2023,
            titulo="Environmental impacts of rainwater harvesting systems in urban areas applying life cycle assessment",
            veiculo="Eng",
            detalhe="v. 4, n. 2, p. 1127–1143",
            doi="10.3390/eng4020065",
            recuperado_por="crossref",
            nota_pt="ACV de sistemas pluviais urbanos em contexto brasileiro; ponto de comparação direto para os resultados ambientais do programa.",
            nota_en="LCA of urban rainwater systems in a Brazilian context; a direct comparison point for the programme's environmental results.",
        ),
        _r(
            chave="chabhadiya_2026",
            autores="CHABHADIYA, K.; WŁÓKA, D.; SMOL, M.",
            ano=2026,
            titulo="Life cycle assessment of a domestic rainwater harvesting system: a case study of Poland",
            veiculo="Sustainability",
            detalhe="v. 18, n. 4, art. 2111",
            doi="10.3390/su18042111",
            recuperado_por="crossref",
            nota_pt="ACV recente de sistema pluvial doméstico; útil como contraste de matriz elétrica e regime pluviométrico europeus.",
            nota_en="Recent LCA of a domestic rainwater system; useful as a contrast in European electricity matrix and rainfall regime.",
        ),
        _r(
            chave="ghimire_2019",
            autores="GHIMIRE, S. R.; JOHNSTON, J. M.; GARLAND, J.; EDELEN, A.; MA, X.",
            ano=2019,
            titulo="Life cycle assessment of a rainwater harvesting system compared with an AC condensate harvesting system",
            veiculo="Resources, Conservation and Recycling",
            detalhe="v. 146, p. 536–548",
            doi="10.1016/j.resconrec.2019.01.043",
            recuperado_por="crossref",
            nota_pt="Compara o sistema pluvial a uma fonte alternativa de água no mesmo edifício, com fronteiras declaradas.",
            nota_en="Compares the rainwater system with an alternative water source in the same building, with declared boundaries.",
        ),
        _r(
            chave="abnt_5648",
            autores="ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS (ABNT)",
            ano=2018,
            titulo="NBR 5648: tubos e conexões de PVC-U com junta soldável para sistemas prediais de água fria — requisitos",
            veiculo="ABNT, Rio de Janeiro",
            tipo="norma",
            detalhe="diâmetro externo e espessura de parede por diâmetro nominal",
            url="https://www.abntcatalogo.com.br/",
            acessado_em=date(2026, 9, 9),
            recuperado_por="editor",
            nota_pt=(
                "Base geométrica das massas lineares dos tubos de pressão (DN 75, 85 e 110). "
                "Espessuras de parede de 1,5 mm no DN 20 a 6,1 mm no DN 110."
            ),
            nota_en=(
                "Geometric basis for the linear masses of pressure pipes (DN 75, 85 and 110). "
                "Wall thicknesses from 1.5 mm at DN 20 to 6.1 mm at DN 110."
            ),
        ),
        _r(
            chave="abnt_5688",
            autores="ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS (ABNT)",
            ano=2018,
            titulo="NBR 5688: tubos e conexões de PVC-U para sistemas prediais de água pluvial, esgoto sanitário e ventilação — requisitos",
            veiculo="ABNT, Rio de Janeiro",
            tipo="norma",
            detalhe="Tabela 1: diâmetro externo médio e espessura de parede, séries normal e reforçada",
            url="https://www.abntcatalogo.com.br/",
            acessado_em=date(2026, 9, 9),
            recuperado_por="editor",
            nota_pt=(
                "Base geométrica das linhas de captação e extravasamento (DN 100 e 150). A norma "
                "destina a **série reforçada** à água pluvial, e é essa a série adotada: parede de "
                "2,5 mm no DN 100 e 3,6 mm no DN 150."
            ),
            nota_en=(
                "Geometric basis for the catchment and overflow lines (DN 100 and 150). The standard "
                "assigns the **reinforced series** to rainwater, and that is the series adopted: "
                "2.5 mm wall at DN 100 and 3.6 mm at DN 150."
            ),
        ),
        _r(
            chave="amanco_wavin_2025",
            autores="AMANCO WAVIN",
            ano=2025,
            titulo="Ficha técnica FTC000021 — Água Fria Soldável",
            veiculo="Amanco Wavin (Orbia), Brasil",
            tipo="relatorio",
            detalhe="revisão de outubro de 2025; peso unitário por item e tabela dimensional",
            url="https://mediahub.wavin.com/m/1fdc60976edd69fd/original/FT-Soldavel-Agua-Fria.pdf",
            acessado_em=date(2026, 9, 9),
            recuperado_por="editor",
            nota_pt=(
                "Peso real de produto para os tubos DN 20 a 60, em barras de 3 e 6 m. Os seis pesos "
                "implicam densidade efetiva de 1,511 g/cm³, com dispersão de apenas 1,504 a 1,516 — "
                "é essa densidade que permite estender a conta aos diâmetros sem peso publicado."
            ),
            nota_en=(
                "Actual product weights for DN 20 to 60 pipes, in 3 m and 6 m lengths. The six weights "
                "imply an effective density of 1.511 g/cm³, spread over just 1.504 to 1.516 — that "
                "density is what allows the calculation to be extended to diameters with no published weight."
            ),
        ),
        _r(
            chave="fortlev_fibra",
            autores="FORTLEV",
            ano=2026,
            titulo="Catálogo técnico: caixa d'água em fibra de vidro",
            veiculo="Fortlev, Brasil",
            tipo="relatorio",
            detalhe="tabela de peso da caixa vazia por capacidade, de 310 a 25.000 L",
            url="https://www.fortlev.com.br/",
            acessado_em=date(2026, 9, 9),
            recuperado_por="usuario",
            nota_pt=(
                "Massa de reservatório em PRFV por capacidade. Os dados mostram economia de escala "
                "clara — de 20,3 kg/m³ a 1.000 L para 13,7 kg/m³ a 10.000 L —, de modo que tratar a "
                "massa como densidade constante superestimava um reservatório de 10.000 L em 46%. "
                "Fabricação conforme ABNT NBR 13210."
            ),
            nota_en=(
                "GRP tank mass by capacity. The data show clear economies of scale — from 20.3 kg/m³ "
                "at 1,000 L to 13.7 kg/m³ at 10,000 L — so treating mass as a constant density "
                "overestimated a 10,000 L tank by 46%. Manufactured to ABNT NBR 13210."
            ),
        ),
        _r(
            chave="sidac_concreto",
            autores="SIDAC — Sistema de Informação do Desempenho Ambiental da Construção",
            ano=2026,
            titulo="Inventário do concreto: emissões de CO₂ fóssil na produção de concreto dosado em central e em obra",
            veiculo="SIDAC, Brasil",
            tipo="base_de_dados",
            detalhe="emissões por m³ de concreto em função da resistência característica (fck)",
            url="https://sidac.org.br/",
            acessado_em=date(2026, 9, 9),
            recuperado_por="usuario",
            nota_pt=(
                "Inventário brasileiro que corrobora o fator do concreto adotado. Para concreto "
                "dosado em central, publica de cerca de 310 kg CO₂/m³ a 20 MPa até cerca de 480 a "
                "40 MPa. O fator do programa, 0,14 kg CO₂e/kg, equivale a 336 kg CO₂/m³ a 2.400 kg/m³, "
                "e cai dentro da faixa de um concreto de 25 a 30 MPa."
            ),
            nota_en=(
                "Brazilian inventory corroborating the adopted concrete factor. For ready-mix concrete "
                "it publishes from about 310 kg CO₂/m³ at 20 MPa to about 480 at 40 MPa. The "
                "programme's 0.14 kg CO₂e/kg equals 336 kg CO₂/m³ at 2,400 kg/m³, inside the range "
                "for a 25 to 30 MPa mix."
            ),
        ),
        _r(
            chave="composites_uk_2026",
            autores="COMPOSITES UK",
            ano=2026,
            titulo="Embodied carbon data for composites",
            veiculo="Composites UK, Reino Unido",
            tipo="relatorio",
            detalhe="atualizado em 22/04/2026",
            url="https://compositesuk.co.uk/industry-support/environmental/embodied-carbon-data-for-composites/",
            acessado_em=date(2026, 9, 9),
            recuperado_por="editor",
            nota_pt=(
                "Fonte do fator do PRFV: faixa típica de **2,5 a 4,0 kg CO₂e/kg** para peças de "
                "compósito de fibra de vidro, adotando-se o ponto médio de 3,25. Registra também "
                "que o valor de 8,1 kg CO₂e/kg, ainda encontrado em literatura antiga, vem da base "
                "ICE dos anos 1990 e foi removido na versão 4.0 dessa base."
            ),
            nota_en=(
                "Source of the GRP factor: typical range of **2.5 to 4.0 kg CO₂e/kg** for glass "
                "fibre composite parts, with the 3.25 midpoint adopted. It also records that the "
                "8.1 kg CO₂e/kg figure still found in older literature comes from the 1990s ICE "
                "database and was removed in version 4.0 of that database."
            ),
        ),
        _r(
            chave="worldstainless_2024",
            autores="WORLDSTAINLESS (World Steel Association)",
            ano=2024,
            titulo="Stainless steel CO₂ emissions report",
            veiculo="worldstainless, Bruxelas",
            tipo="relatorio",
            detalhe="divulgado em 24/09/2024; berço-ao-portão, escopos 1, 2 e 3",
            url="https://worldstainless.org/media/press-releases/stainless-steel-co2-emissions-report-1/",
            acessado_em=date(2026, 9, 9),
            recuperado_por="editor",
            nota_pt=(
                "Fonte do fator do aço inoxidável. A emissão depende fortemente do teor de sucata "
                "da carga: 1,95 kg CO₂/kg a 85% de sucata, 2,45 a 75%, **3,70 a 50%** e 6,80 a 30% "
                "— um fator de 3,5 entre os extremos. Adota-se o ponto de 50%. Um estudo que não "
                "declare o teor de sucata não é comparável, pela mesma razão que um fator de rede "
                "sem ano não é."
            ),
            nota_en=(
                "Source of the stainless steel factor. Emissions depend strongly on the scrap "
                "content of the charge: 1.95 kg CO₂/kg at 85% scrap, 2.45 at 75%, **3.70 at 50%** "
                "and 6.80 at 30% — a factor of 3.5 between the extremes. The 50% point is adopted. "
                "A study that does not declare its scrap content is not comparable, for the same "
                "reason a grid factor without a year is not."
            ),
        ),
        _r(
            chave="snis_2023",
            autores="BRASIL. Ministério das Cidades. Sistema Nacional de Informações sobre Saneamento (SNIS)",
            ano=2023,
            titulo="Diagnóstico temático dos serviços de água e esgoto: visão geral — ano-base 2022",
            veiculo="Ministério das Cidades, Brasília",
            tipo="relatorio",
            detalhe="indicador IN058, consumo de energia elétrica em sistemas de abastecimento de água",
            url="https://www.gov.br/cidades/pt-br/acesso-a-informacao/acoes-e-programas/saneamento/snis",
            acessado_em=date(2026, 9, 9),
            recuperado_por="usuario",
            nota_pt=(
                "Única fonte brasileira de intensidade energética do abastecimento: **0,67 kWh/m³** "
                "na média nacional de 2022, variando de 0,61 a 0,78 entre macrorregiões e de 0,64 a "
                "0,73 conforme a natureza do prestador. O esgotamento consome 0,29 kWh/m³ à parte, "
                "que **não** é evitado quando se usa água pluvial em bacia sanitária, porque a água "
                "vai para o esgoto do mesmo jeito. O SINISA de 2023 (indicador IAG2023) foi "
                "conferido em 16/09/2026: a mediana municipal, 0,74 kWh/m³, corrobora este valor, "
                "mas o total nacional publicado (18,02) é distorcido por erros de unidade."
            ),
            nota_en=(
                "The only Brazilian source for the energy intensity of water supply: **0.67 kWh/m³** "
                "as the 2022 national average, ranging from 0.61 to 0.78 across regions and 0.64 to "
                "0.73 by type of provider. Sewage consumes a further 0.29 kWh/m³, which is **not** "
                "avoided when rainwater is used for toilet flushing, since the water reaches the "
                "sewer either way."
            ),
        ),
        _r(
            chave="grundfos_epd_2025",
            autores="GRUNDFOS HOLDING A/S",
            ano=2025,
            titulo="Environmental Product Declaration: ALPHA1 25,32-40 130,180; ALPHA1 GO 15,20,25,32-40 130,180",
            veiculo="Institut Bauen und Umwelt e.V. (IBU), Berlim",
            tipo="relatorio",
            detalhe="EPD-GRU-20250340-CBA1-EN, emitida em 09/07/2025, válida até 08/07/2030; EN 15804+A2",
            url="https://ibudata.lca-data.com/resource/processes/c97a8776-b554-4aab-8e96-f875382ece1c/epd?version=00.02.000",
            acessado_em=date(2026, 9, 15),
            recuperado_por="editor",
            nota_pt=(
                "Fonte da intensidade de carbono das motobombas. Módulos A1-A3: GWP-total de "
                "**10,4 kg CO₂e** por unidade, massa de referência de 2,179 kg com embalagem, ou "
                "4,77 kg CO₂e por kg. É circulador europeu com eletrônica embarcada: serve como "
                "aproximação por quilo para bomba elétrica pequena, e não como inventário de "
                "centrífuga brasileira."
            ),
            nota_en=(
                "Source of the carbon intensity of pumps. Modules A1-A3: GWP-total of **10.4 kg "
                "CO₂e** per unit, reference mass 2.179 kg including packaging, or 4.77 kg CO₂e per "
                "kg. It is a European circulator with on-board electronics: a per-kilogram "
                "approximation for small electric pumps, not an inventory of a Brazilian "
                "centrifugal pump."
            ),
        ),
        _r(
            chave="dancor_catalogo_60hz",
            autores="DANCOR S.A. INDÚSTRIA MECÂNICA",
            ano=2021,
            titulo="Catálogo geral 60 Hz: Série CAM W-4C e CAM W-10, centrífugas de aplicação múltipla",
            veiculo="Dancor, Rio de Janeiro",
            tipo="relatorio",
            detalhe="tabelas de dados dimensionais, coluna «Peso (kg)»",
            url="https://www.dancor.com.br/wp-content/uploads/2021/11/cam-w10-pbe_cat-1.pdf",
            acessado_em=date(2026, 9, 15),
            recuperado_por="editor",
            nota_pt=(
                "Fonte das massas das motobombas monofásicas: 6,1 kg (1/4 CV), 6,4 kg (1/2 CV), "
                "13,5 kg (3/4 CV), 15,3 kg (1 CV), 17,5 kg (1 1/2 CV) e 20,7 kg (2 CV)."
            ),
            nota_en=(
                "Source of the single-phase pump masses: 6.1 kg (1/4 hp), 6.4 kg (1/2 hp), "
                "13.5 kg (3/4 hp), 15.3 kg (1 hp), 17.5 kg (1 1/2 hp) and 20.7 kg (2 hp)."
            ),
        ),
        _r(
            chave="mcti_sirene_fe",
            autores="BRASIL. Ministério da Ciência, Tecnologia e Inovação (MCTI). SIRENE",
            ano=2026,
            titulo="Fatores de emissão de CO₂ para inventários corporativos: fator médio de geração do Sistema Interligado Nacional",
            veiculo="Sistema de Registro Nacional de Emissões (SIRENE)",
            tipo="base_de_dados",
            detalhe="série anual 2006–2025; planilha Inventario_2026_janjul.xlsx",
            url="https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/sirene/dados-e-ferramentas/fatores-de-emissao",
            acessado_em=date(2026, 9, 8),
            recuperado_por="editor",
            nota_pt=(
                "Fonte do fator da rede elétrica. Arquivo arquivado em `data/fontes_externas/` com SHA-256; "
                "série lida por script em `netuno/data/fatores_emissao_rede_mcti.json`. É CO₂, não CO₂e."
            ),
            nota_en=(
                "Source of the grid factor. File archived in `data/fontes_externas/` with SHA-256; series read "
                "by script into `netuno/data/fatores_emissao_rede_mcti.json`. It is CO₂, not CO₂e."
            ),
        ),
        # ------------------------------------------------------------------
        # Decisão multicritério
        # ------------------------------------------------------------------
        _r(
            chave="hwang_yoon_1981",
            autores="HWANG, C.-L.; YOON, K.",
            ano=1981,
            titulo="Multiple attribute decision making: methods and applications — a state-of-the-art survey",
            veiculo="Springer, Berlim",
            tipo="livro",
            detalhe="Lecture Notes in Economics and Mathematical Systems, v. 186",
            doi="10.1007/978-3-642-48318-9",
            recuperado_por="crossref",
            nota_pt="Formulação original do TOPSIS: normalização vetorial, soluções ideais positiva e negativa, coeficiente de proximidade.",
            nota_en="Original TOPSIS formulation: vector normalisation, positive and negative ideal solutions, closeness coefficient.",
        ),
        _r(
            chave="opricovic_tzeng_2004",
            autores="OPRICOVIC, S.; TZENG, G.-H.",
            ano=2004,
            titulo="Compromise solution by MCDM methods: a comparative analysis of VIKOR and TOPSIS",
            veiculo="European Journal of Operational Research",
            detalhe="v. 156, n. 2, p. 445–455",
            doi="10.1016/s0377-2217(03)00020-1",
            recuperado_por="crossref",
            nota_pt=(
                "Define S, R e Q do VIKOR e as condições C1 (vantagem aceitável) e C2 (estabilidade aceitável). "
                "O motor deste programa calcula Q mas **não** aplica C1 e C2 — ver a nota na aba de decisão."
            ),
            nota_en=(
                "Defines VIKOR's S, R and Q and conditions C1 (acceptable advantage) and C2 (acceptable "
                "stability). This engine computes Q but does **not** apply C1 and C2 — see the decision tab note."
            ),
        ),
        _r(
            chave="opricovic_tzeng_2007",
            autores="OPRICOVIC, S.; TZENG, G.-H.",
            ano=2007,
            titulo="Extended VIKOR method in comparison with outranking methods",
            veiculo="European Journal of Operational Research",
            detalhe="v. 178, n. 2, p. 514–529",
            doi="10.1016/j.ejor.2006.01.020",
            recuperado_por="crossref",
            nota_pt="Extensão do VIKOR e comparação com métodos de sobreclassificação; discute a escolha do parâmetro v.",
            nota_en="VIKOR extension and comparison with outranking methods; discusses the choice of parameter v.",
        ),
        _r(
            chave="lahdelma_1998",
            autores="LAHDELMA, R.; HOKKANEN, J.; SALMINEN, P.",
            ano=1998,
            titulo="SMAA — stochastic multiobjective acceptability analysis",
            veiculo="European Journal of Operational Research",
            detalhe="v. 106, n. 1, p. 137–143",
            doi="10.1016/s0377-2217(97)00163-x",
            recuperado_por="crossref",
            nota_pt="Artigo que introduz a SMAA: em vez de exigir um vetor de pesos, amostra-se o espaço inteiro de preferências.",
            nota_en="Paper introducing SMAA: instead of demanding one weight vector, the whole preference space is sampled.",
        ),
        _r(
            chave="lahdelma_salminen_2001",
            autores="LAHDELMA, R.; SALMINEN, P.",
            ano=2001,
            titulo="SMAA-2: stochastic multicriteria acceptability analysis for group decision making",
            veiculo="Operations Research",
            detalhe="v. 49, n. 3, p. 444–454",
            doi="10.1287/opre.49.3.444.11220",
            recuperado_por="crossref",
            nota_pt="Define os índices de aceitabilidade por posto, o vetor central de pesos e o fator de confiança — as três saídas da aba estocástica.",
            nota_en="Defines rank acceptability indices, the central weight vector and the confidence factor — the three outputs of the stochastic tab.",
        ),
        _r(
            chave="tervonen_figueira_2007",
            autores="TERVONEN, T.; FIGUEIRA, J. R.",
            ano=2007,
            titulo="A survey on stochastic multicriteria acceptability analysis methods",
            veiculo="Journal of Multi-Criteria Decision Analysis",
            detalhe="v. 15, n. 1–2, p. 1–14",
            doi="10.1002/mcda.407",
            recuperado_por="crossref",
            nota_pt="Levantamento das variantes de SMAA e das exigências de amostragem — sustenta a escolha do número de simulações.",
            nota_en="Survey of SMAA variants and their sampling requirements — supports the choice of simulation count.",
        ),
        _r(
            chave="crispyn_2024",
            autores="BĄCZKIEWICZ, A.",
            ano=2024,
            titulo="crispyn: CRIteria Significance determining in PYthoN",
            veiculo="Repositório GitHub (energyinpython/crispyn), licença MIT",
            tipo="software",
            url="https://github.com/energyinpython/crispyn",
            acessado_em=date(2026, 9, 8),
            recuperado_por="editor",
            nota_pt=(
                "Biblioteca de referência que implementa `VIKOR` e `VIKOR_SMAA`. A implementação do Netuno é "
                "independente, escrita sobre NumPy; o repositório serve de base de comparação, não de origem "
                "do código. Não implementa TOPSIS."
            ),
            nota_en=(
                "Reference library implementing `VIKOR` and `VIKOR_SMAA`. Netuno's implementation is "
                "independent, written on NumPy; the repository serves as a comparison baseline, not as the "
                "code's origin. It does not implement TOPSIS."
            ),
        ),
        # ------------------------------------------------------------------
        # Índices pluviométricos
        # ------------------------------------------------------------------
        # ------------------------------------------------------------------
        # Coberturas, normas e fontes de dados nacionais
        # ------------------------------------------------------------------
        _r(
            chave="marinoski_2020",
            autores="MARINOSKI RIBEIRO, A. K.; MARINOSKI, D. L.",
            ano=2020,
            titulo="Estudo sobre materiais para coberturas utilizadas em sistemas de aproveitamento de água pluvial residenciais",
            veiculo="MIX Sustentável",
            detalhe="v. 6, n. 2, p. 53–66",
            doi="10.29183/2447-3073.MIX2020.v6.n2.53-66",
            url="https://ojs.sites.ufsc.br/index.php/mixsustentavel/article/view/4080",
            acessado_em=date(2026, 9, 8),
            recuperado_por="editor",
            nota_pt=(
                "Origem dos coeficientes de escoamento por material de telhado. Compara telhado vegetado, "
                "telha cerâmica, de concreto e metálica. O DOI não consta do Crossref; o registro foi "
                "conferido na página do periódico."
            ),
            nota_en=(
                "Source of the runoff coefficients by roof material. Compares green roof, ceramic, concrete "
                "and metal tiles. The DOI is not indexed by Crossref; the record was checked on the "
                "journal page."
            ),
        ),
        _r(
            chave="yaziz_1989",
            autores="YAZIZ, M. I.; GUNTING, H.; SAPARI, N.; GHAZALI, A. W.",
            ano=1989,
            titulo="Variations in rainwater quality from roof catchments",
            veiculo="Water Research",
            detalhe="v. 23, n. 6, p. 761–765",
            doi="10.1016/0043-1354(89)90211-x",
            recuperado_por="crossref",
            nota_pt="Estudo clássico da variação da qualidade da água pluvial por tipo de cobertura e ao longo do evento.",
            nota_en="Classic study of rainwater quality variation by roof type and along the event.",
        ),
        _r(
            chave="abnt_15527",
            autores="ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS (ABNT)",
            ano=2019,
            titulo="NBR 15527: aproveitamento de água de chuva de coberturas para fins não potáveis — requisitos",
            veiculo="ABNT, Rio de Janeiro",
            tipo="norma",
            detalhe="revisão de 2019, que substitui a de 2007",
            url="https://www.abntcatalogo.com.br/",
            acessado_em=date(2026, 9, 8),
            recuperado_por="editor",
            nota_pt=(
                "Norma brasileira de referência. O item 4.6.3, Tabela 1, fixa os parâmetros mínimos de "
                "qualidade — E. coli, turbidez e pH — e o item 4.6.5, a faixa de cloro residual livre. "
                "O item 4.3.5 recomenda descarte de 2 mm do escoamento inicial na falta de dados, e o "
                "item 4.1.6 dá a disponibilidade por P x A x C x eta, com eta = 0,85 recomendado."
            ),
            nota_en=(
                "Brazilian reference standard. Clause 4.6.3, Table 1, sets the minimum quality parameters — "
                "E. coli, turbidity and pH — and clause 4.6.5 the free residual chlorine range. Clause "
                "4.3.5 recommends a 2 mm first-flush discard where data are lacking, and clause 4.1.6 "
                "gives availability as P x A x C x eta, with eta = 0.85 recommended."
            ),
        ),
        _r(
            chave="abnt_16783",
            autores="ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS (ABNT)",
            ano=2019,
            titulo="NBR 16783: uso de fontes alternativas de água não potável em edificações",
            veiculo="ABNT, Rio de Janeiro",
            tipo="norma",
            url="https://www.abntcatalogo.com.br/",
            acessado_em=date(2026, 9, 8),
            recuperado_por="editor",
            nota_pt="Define usos admissíveis de água não potável em edificações; complementa a NBR 15527.",
            nota_en="Defines admissible non-potable water uses in buildings; complements NBR 15527.",
        ),
        _r(
            chave="portaria_888_2021",
            autores="BRASIL. Ministério da Saúde",
            ano=2021,
            titulo=(
                "Portaria GM/MS n.º 888, de 4 de maio de 2021: altera o Anexo XX da Portaria de "
                "Consolidação GM/MS n.º 5/2017, para dispor sobre os procedimentos de controle e de "
                "vigilância da qualidade da água para consumo humano e seu padrão de potabilidade"
            ),
            veiculo="Diário Oficial da União, Brasília",
            tipo="norma",
            url="https://bvsms.saude.gov.br/bvs/saudelegis/gm/2021/prt0888_07_05_2021.html",
            acessado_em=date(2026, 9, 8),
            recuperado_por="editor",
            nota_pt=(
                "Padrão de potabilidade brasileiro. Citada como **contraste**: a água pluvial deste "
                "programa destina-se a usos não potáveis, e comparar seus limites com os desta portaria "
                "sugeriria falha num requisito que o sistema não se propõe a atender."
            ),
            nota_en=(
                "Brazilian drinking-water standard. Cited as a **contrast**: the rainwater here is for "
                "non-potable uses, and comparing its limits with this regulation would suggest failure "
                "against a requirement the system never set out to meet."
            ),
        ),
        _r(
            chave="inmet_bdmep",
            autores="INSTITUTO NACIONAL DE METEOROLOGIA (INMET)",
            ano=2026,
            titulo="Banco de Dados Meteorológicos para Ensino e Pesquisa (BDMEP)",
            veiculo="INMET, Brasília",
            tipo="base_de_dados",
            url="https://bdmep.inmet.gov.br/",
            acessado_em=date(2026, 9, 8),
            recuperado_por="editor",
            nota_pt="Origem das séries pluviométricas diárias distribuídas com o programa.",
            nota_en="Source of the daily rainfall series distributed with the programme.",
        ),
        _r(
            chave="zhang_2011",
            autores="ZHANG, X.; ALEXANDER, L.; HEGERL, G. C. et al.",
            ano=2011,
            titulo="Indices for monitoring changes in extremes based on daily temperature and precipitation data",
            veiculo="WIREs Climate Change",
            detalhe="v. 2, n. 6, p. 851–870",
            doi="10.1002/wcc.147",
            recuperado_por="crossref",
            nota_pt=(
                "Define os índices do ETCCDI e discute a escolha do período-base do percentil — questão que "
                "afeta diretamente o cálculo do R95p neste programa."
            ),
            nota_en=(
                "Defines the ETCCDI indices and discusses the percentile base period — a question that "
                "directly affects how R95p is computed here."
            ),
        ),
        _r(
            chave="walsh_lawler_1981",
            autores="WALSH, R. P. D.; LAWLER, D. M.",
            ano=1981,
            titulo="Rainfall seasonality: description, spatial patterns and change through time",
            veiculo="Weather",
            detalhe="v. 36, n. 7, p. 201–208",
            doi="10.1002/j.1477-8696.1981.tb05400.x",
            recuperado_por="crossref",
            nota_pt=(
                "Origem do Índice de Sazonalidade, que compõe o conjunto de nove ao lado dos oito índices do "
                "ETCCDI: mede a concentração da chuva entre os meses, que é o que governa a reservação."
            ),
            nota_en=(
                "Origin of the Seasonality Index, which completes the set of nine alongside the eight ETCCDI "
                "indices: it measures how concentrated rainfall is across the months, which governs storage."
            ),
        ),
    ]
)


# ---------------------------------------------------------------------------
# Mapa seção → referências
# ---------------------------------------------------------------------------

# A aba de uso pela linha de comando é documentação de operação, não afirmação
# científica: exigir citação ali produziria citação decorativa, que é o oposto
# do que se quer. A isenção é explícita para que não passe por esquecimento.
SECOES_ISENTAS: Tuple[str, ...] = ("cli",)

MINIMO_DE_CITACOES = 3

REFERENCIAS_POR_SECAO: Dict[str, Tuple[str, ...]] = {
    "metodologia": ("campisano_2017", "freni_liuzzo_2019", "semaan_2020", "souza_ghisi_2012"),
    "topsis": (
        "hwang_yoon_1981",
        "opricovic_tzeng_2004",
        "opricovic_tzeng_2007",
        "lahdelma_1998",
        "lahdelma_salminen_2001",
        "tervonen_figueira_2007",
        "melville_shreeve_2016",
        "crispyn_2024",
    ),
    "telhados": ("marinoski_2020", "scolaro_ghisi_2025", "campisano_2017", "raimondi_2023"),
    "indices": ("zhang_2011", "walsh_lawler_1981", "inmet_bdmep", "kisakye_2018"),
    "hidrologia": ("inmet_bdmep", "kisakye_2018", "campisano_2017", "souza_ghisi_2012", "semaan_2020"),
    "demanda": ("maykot_ghisi_2020", "teston_2018", "belmeziti_2013"),
    "reservatorios": ("semaan_2020", "matos_2013", "vieira_2014", "freni_liuzzo_2019", "abnt_15527", "epd_pvc_rxp_2022", "abnt_5648", "abnt_5688", "amanco_wavin_2025", "fortlev_fibra"),
    "qualidade": ("maykot_vaz_ghisi_2025", "yaziz_1989", "rahman_2014", "raimondi_2023", "abnt_15527", "abnt_16783", "portaria_888_2021"),
    "indicadores": ("belmeziti_2013", "souza_ghisi_2012", "campisano_2017"),
    "economico": ("maykot_ghisi_2020", "wang_zimmerman_2015", "matos_2013", "marinoski_ghisi_2018"),
    "discussao": ("semaan_2020", "souza_ghisi_2012", "kisakye_2018", "marinoski_ghisi_2018"),
    "tarifas": ("teston_2018", "wang_zimmerman_2015", "maykot_ghisi_2020"),
    "acv": (
        "vaz_2023_acv",
        "vaz_2025_eletricidade",
        "acc_hdpe_2020",
        "acc_pvc_2021",
        "epd_pvc_rxp_2022",
        "amanco_wavin_2025",
        "abnt_5648",
        "abnt_5688",
        "fortlev_fibra",
        "sidac_concreto",
        "composites_uk_2026",
        "worldstainless_2024",
        "grundfos_epd_2025",
        "dancor_catalogo_60hz",
        "snis_2023",
        "alsabri_2020",
        "du_2013",
        "garfi_2016",
        "silva_2023",
        "ghimire_2019",
        "chabhadiya_2026",
        "ghimire_2014",
        "ghimire_2017",
        "hammond_jones_2008",
        "khan_tee_2015",
        "alsadi_matthews_2022",
        "ryan_garcia_2021",
        "vieira_2014",
        "mcti_sirene_fe",
    ),
    "esg": ("teston_2018", "vaz_2023_acv", "wang_zimmerman_2015", "abnt_16783", "silva_2023"),
    "cli": (),
}


# ---------------------------------------------------------------------------
# Renderização para o QTextBrowser
# ---------------------------------------------------------------------------

_TITULO_DO_BLOCO = {
    "pt": "Referências desta seção",
    "en": "References for this section",
}

_ROTULO_ACESSO = {"pt": "acesso em", "en": "accessed"}


def _formatar(ref: Referencia, lang: str) -> str:
    """Uma entrada, em HTML aceito pelo QTextBrowser (HTML 4 / CSS 2.1)."""
    partes = [f"<b>{html.escape(ref.autores)}</b> ({ref.ano})."]
    partes.append(f" {html.escape(ref.titulo)}.")
    veiculo = html.escape(ref.veiculo)
    if ref.detalhe:
        veiculo += f", {html.escape(ref.detalhe)}"
    partes.append(f" <i>{veiculo}</i>.")

    if ref.link:
        partes.append(
            f" <a href='{html.escape(ref.link, quote=True)}' style='color: #0284c7;'>"
            f"{html.escape(ref.doi or ref.link)}</a>."
        )
    if ref.acessado_em:
        partes.append(
            f" <span style='color: #64748b;'>({_ROTULO_ACESSO.get(lang, _ROTULO_ACESSO['en'])} "
            f"{ref.acessado_em.strftime('%d/%m/%Y')})</span>"
        )

    nota = ref.nota_pt if lang == "pt" else (ref.nota_en or ref.nota_pt)
    if nota:
        partes.append(
            f"<br/><span style='color: #475569;'>{nota}</span>"
        )
    return "".join(partes)


def referencias_da_secao(secao: str) -> Tuple[Referencia, ...]:
    """As referências de uma seção, na ordem declarada."""
    if secao not in REFERENCIAS_POR_SECAO:
        raise KeyError(f"Seção desconhecida na bibliografia: {secao!r}")
    return tuple(REFERENCIAS[chave] for chave in REFERENCIAS_POR_SECAO[secao])


def render_bloco_da_secao(secao: str, lang: str = "pt") -> str:
    """Bloco «Referências desta seção», pronto para concatenar ao HTML da aba.

    Vai **depois** do conteúdo, fora do alcance do pré-processador de equações
    de `_create_browser`, que reescreve parágrafos contendo `<code>` com `=`.
    """
    refs = referencias_da_secao(secao)
    if not refs:
        return ""

    titulo = _TITULO_DO_BLOCO.get(lang, _TITULO_DO_BLOCO["en"])
    itens = "".join(
        f"<li style='margin-bottom: 8px;'>{_formatar(ref, lang)}</li>" for ref in refs
    )
    return (
        "<hr style='border: none; border-top: 1px solid #cbd5e1; margin: 18px 0 10px 0;'/>"
        f"<h4 style='color: #0284c7; margin: 0 0 8px 0;'>{titulo}</h4>"
        f"<ol style='margin-top: 0;'>{itens}</ol>"
    )


def render_bibliografia_completa(lang: str = "pt") -> str:
    """Lista geral, ordenada por autor e ano, para a página de Referências."""
    ordenadas = sorted(REFERENCIAS.values(), key=lambda r: (r.autores.lower(), r.ano))
    itens = "".join(
        f"<li style='margin-bottom: 10px;'>{_formatar(ref, lang)}</li>" for ref in ordenadas
    )
    return f"<ol style='margin-top: 0;'>{itens}</ol>"
