"""
Pipeline completo:
1. Recálculo das 39 milhões de simulações com tarifas municipais reais das 652 cidades.
2. Geração das 12 figuras analíticas e relatório estatístico avançado.
"""
import time
import subprocess
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

print("=" * 90)
print("INICIANDO PIPELINE COMPLETO NETUNO 5 (RECÁLCULO + SUÍTE DE ANÁLISE E FIGURAS)")
print("=" * 90)

t0 = time.time()

# 1. Recalcular simulações
print("\n>>> ETAPA 1/2: Recalculando simulações com tarifas reais...")
ret1 = subprocess.run([sys.executable, os.path.join(BASE_DIR, "scripts", "recalc_full_study_with_real_tariffs.py")], check=True)

# 2. Gerar análises e figuras
print("\n>>> ETAPA 2/2: Gerando figuras analíticas e relatório estatístico...")
ret2 = subprocess.run([sys.executable, os.path.join(BASE_DIR, "scripts", "analyze_vaz_parquet.py")], check=True)

t_total = time.time() - t0
print("=" * 90)
print(f"[SUCESSO TOTAL] PIPELINE COMPLETO CONCLUÍDO EM {t_total/60.0:.2f} MINUTOS ({t_total:.1f}s)!")
print("=" * 90)
