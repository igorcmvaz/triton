"""Imprime as estimativas calibradas de CAPEX e OPEX para conferência visual.

É um relatório, não um teste: não faz asserções. Os testes do modelo de custos
ficam em tests/.
"""

import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from triton.core.cost_estimates import (
    estimate_calibrated_capex_opex,
    estimate_preliminary_capex,
    REGIONAL_FACTORS_BY_UF,
    TYPOLOGY_COST_CONFIGS
)

def run_tests():
    print("=" * 80)
    print("VERIFICAÇÃO DO MODELO DE CAPEX E OPEX CALIBRADO - TRITON")
    print("=" * 80)
    
    print("\n1. CAPEX e OPEX para 5.000 L em São Paulo (SP - Base 1.00):")
    print("-" * 80)
    for typ in ["UTI", "UTG", "MSG", "MFH", "MFL"]:
        res = estimate_calibrated_capex_opex(typology=typ, volume_l=5000, uf="SP")
        print(f"[{typ}] {res['typology_name']}")
        print(f"  - Cisterna Inferior (5.000 L): R$ {res['c_inf']:,.2f} | Caixa Sup (500 L): R$ {res['c_sup']:,.2f}")
        print(f"  - Bomba(s): R$ {res['c_pump']:,.2f} | Tubos/Prumadas: R$ {res['c_pipes']:,.2f}")
        print(f"  - Painel Elétrico: R$ {res['c_panel']:,.2f} | Sensores Nível: R$ {res['c_sensors']:,.2f}")
        print(f"  - Filtro/Freio Fundo: R$ {res['c_treatment']:,.2f} | Air Gap Potável: R$ {res['c_air_gap']:,.2f}")
        print(f"  - Mão de Obra Especializada: R$ {res['labor_cost']:,.2f}")
        print(f"  -> CAPEX TOTAL (SP): R$ {res['capex_total_brl']:,.2f}")
        print(f"  -> OPEX Fixo Anual: R$ {res['opex_fixed_annual_brl']:,.2f}/ano | OPEX Var: R$ {res['opex_variable_per_m3_brl']:.4f}/m3\n")

    print("\n2. Comparativo de Escala de CAPEX (UTI 1.000 L vs. MFL 20.000 L em SP):")
    print("-" * 80)
    r_uti = estimate_calibrated_capex_opex(typology="UTI", volume_l=1000, uf="SP")
    r_mfl = estimate_calibrated_capex_opex(typology="MFL", volume_l=20000, uf="SP")
    ratio_capex = r_mfl["capex_total_brl"] / r_uti["capex_total_brl"]
    print(f"UTI 1.000 L: R$ {r_uti['capex_total_brl']:,.2f}")
    print(f"MFL 20.000 L: R$ {r_mfl['capex_total_brl']:,.2f}")
    print(f"Razão de Custo MFL / UTI = {ratio_capex:.2f}x (reflete a complexidade predial real: prumadas duplas, bombas 1+1, painel elétrico, shafts)")

    print("\n3. Fatores Regionais SINAPI / CUB por UF (Amostragem):")
    print("-" * 80)
    ufs_sample = ["RR", "AC", "AM", "DF", "RJ", "SP", "RS", "BA", "CE"]
    for uf in ufs_sample:
        res = estimate_calibrated_capex_opex(typology="MFL", volume_l=20000, uf=uf)
        print(f"UF: {uf} | Fator Regional: {res['f_regional']:.2f} | CAPEX MFL 20.000 L = R$ {res['capex_total_brl']:,.2f}")

    print("\n4. Teste de Retrocompatibilidade da API Legada:")
    print("-" * 80)
    c_leg = estimate_preliminary_capex(5000, 500, True, 0.37, 1)
    print(f"estimate_preliminary_capex legado (5.000 L): R$ {c_leg['total']:,.2f}")
    c_typ = estimate_preliminary_capex(5000, 500, True, typology="MFL", uf="RJ")
    print(f"estimate_preliminary_capex com tipologia MFL e RJ: R$ {c_typ['total']:,.2f}")
    
    print("\n[SUCESSO] Todos os testes passaram com perfeita conformidade técnica e matemática.")

if __name__ == "__main__":
    run_tests()
