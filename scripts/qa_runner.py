"""
Agente de QA & Runner de Testes do Netuno 5.

Executa a suíte por camadas (unit, integration, invariants, ciencia, ui), aplica portões
de qualidade (cobertura mínima agregada e por módulo), registra a impressão digital do
ambiente e pode rodar em observação contínua.

O registro do ambiente não é acessório: `netuno.core.simulation` seleciona entre dois
kernels de balanço hídrico conforme `numba` esteja ou não instalado. Um relatório de QA
que não diga qual kernel foi exercitado é ambíguo. Ver `docs/verificacao_e_validacao.md`, §4.

Exemplos
--------
    python scripts/qa_runner.py                          # suíte completa + portões
    python scripts/qa_runner.py --layer ciencia          # só as propriedades científicas
    python scripts/qa_runner.py --cov-min 85             # eleva o portão de cobertura
    python scripts/qa_runner.py --no-gate                # mede sem reprovar
    python scripts/qa_runner.py --loop 300               # observação contínua
"""

import argparse
import json
import os
import platform
import subprocess
import sys
import time
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Cobertura mínima agregada do núcleo de cálculo.
COBERTURA_MINIMA_PADRAO = 80

# Piso por modulo. Modulos abaixo do piso reprovam o portão individualmente, mesmo que a
# média agregada passe — a média esconde concentração de risco.
PISO_POR_MODULO = 50

# Módulos sabidamente abaixo do piso em 5.0.7, com correção planejada. Enquanto constarem
# aqui, não reprovam a execução, mas são sempre listados no relatório.
DIVIDA_TECNICA_CONHECIDA = {
    "netuno/core/excel_scenarios.py",
    "netuno/core/scenarios.py",
    "netuno/core/tariff_updater/change_detector.py",
}

CAMADAS = {
    "all": ["tests"],
    "unit": ["tests/unit"],
    "integration": ["tests/integration"],
    "invariants": ["tests/invariants"],
    "ciencia": ["tests/invariants/test_scientific_properties.py",
                "tests/invariants/test_mass_conservation.py",
                "tests/invariants/test_numba_python_parity.py"],
    "ui": ["tests/ui"],
    "benchmarking": ["tests/benchmarking"],
}


def impressao_digital_do_ambiente() -> dict:
    """Coleta o que determina a reprodutibilidade de uma rodada de QA."""
    try:
        from netuno.core import simulation
        kernel = "JIT (numba)" if simulation.HAS_NUMBA else "Python (referência)"
    except Exception as erro:  # pragma: no cover - diagnóstico
        kernel = f"indeterminado ({erro})"

    try:
        from netuno import __version__ as versao
    except Exception:  # pragma: no cover - diagnóstico
        versao = "indeterminada"

    versoes = {}
    for pacote in ("numpy", "pandas", "matplotlib", "numba"):
        try:
            versoes[pacote] = __import__(pacote).__version__
        except ImportError:
            versoes[pacote] = "ausente"

    return {
        "versao_netuno": versao,
        "kernel_de_simulacao": kernel,
        "python": platform.python_version(),
        "sistema": f"{platform.system()} {platform.release()}",
        "dependencias": versoes,
    }


def _imprimir_ambiente(ambiente: dict) -> None:
    print("\n" + "=" * 72)
    print("  AMBIENTE DA EXECUÇÃO")
    print("=" * 72)
    print(f"  Netuno              : {ambiente['versao_netuno']}")
    print(f"  Kernel de simulação : {ambiente['kernel_de_simulacao']}")
    print(f"  Python              : {ambiente['python']}  ({ambiente['sistema']})")
    deps = "  ".join(f"{k}={v}" for k, v in ambiente["dependencias"].items())
    print(f"  Dependências        : {deps}")
    if ambiente["kernel_de_simulacao"].startswith("Python"):
        print("\n  Nota: sem numba, os kernels JIT não são exercitados. Os testes de")
        print("        paridade em test_numba_python_parity.py serão ignorados (skip).")
    print("=" * 72)


def _montar_comando(camada: str, cobertura: bool, cov_min: int, aplicar_portao: bool) -> list:
    cmd = [sys.executable, "-m", "pytest", *CAMADAS[camada]]
    if cobertura:
        cmd += ["--cov=netuno.core", "--cov-report=term-missing",
                f"--cov-report=json:{os.path.join(BASE_DIR, 'reports', 'cobertura.json')}",
                f"--cov-report=html:{os.path.join(BASE_DIR, 'reports', 'coverage')}"]
        if aplicar_portao:
            cmd.append(f"--cov-fail-under={cov_min}")
    cmd += ["-q", "--color=yes"]
    return cmd


def _avaliar_portao_por_modulo(aplicar_portao: bool) -> int:
    """Verifica o piso individual de cobertura. Devolve o número de reprovações."""
    caminho = os.path.join(BASE_DIR, "reports", "cobertura.json")
    if not os.path.exists(caminho):
        return 0

    with open(caminho, encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    abaixo_do_piso, divida = [], []
    for modulo, medidas in sorted(dados.get("files", {}).items()):
        percentual = medidas["summary"]["percent_covered"]
        if percentual < PISO_POR_MODULO:
            normalizado = modulo.replace("\\", "/")
            if any(normalizado.endswith(conhecido) for conhecido in DIVIDA_TECNICA_CONHECIDA):
                divida.append((normalizado, percentual))
            else:
                abaixo_do_piso.append((normalizado, percentual))

    if divida:
        print(f"\n  Dívida técnica conhecida (abaixo de {PISO_POR_MODULO}%, não reprova):")
        for modulo, percentual in divida:
            print(f"    - {modulo}: {percentual:.0f}%")

    if abaixo_do_piso:
        rotulo = "[PORTÃO]" if aplicar_portao else "[informativo]"
        print(f"\n  {rotulo} Módulos abaixo do piso de {PISO_POR_MODULO}% e não previstos:")
        for modulo, percentual in abaixo_do_piso:
            print(f"    ! {modulo}: {percentual:.0f}%")
        if aplicar_portao:
            return len(abaixo_do_piso)

    return 0


def executar(camada: str = "all", cobertura: bool = True,
             cov_min: int = COBERTURA_MINIMA_PADRAO, aplicar_portao: bool = True) -> int:
    ambiente = impressao_digital_do_ambiente()
    _imprimir_ambiente(ambiente)

    # Os portões de cobertura só fazem sentido sobre a suíte completa: numa camada
    # parcial a cobertura é baixa por construção (rodar só as propriedades científicas
    # não exercita o parser), e reprovar por isso seria um falso negativo.
    if aplicar_portao and camada != "all":
        print(f"\n[QA] Camada parcial ('{camada}'): portões de cobertura suspensos.")
        print("[QA] Use --layer all para a avaliação com portões.")
        aplicar_portao = False

    os.makedirs(os.path.join(BASE_DIR, "reports"), exist_ok=True)
    cmd = _montar_comando(camada, cobertura, cov_min, aplicar_portao)

    print(f"\n[QA] {datetime.now():%Y-%m-%d %H:%M:%S} — camada: {camada.upper()}")
    if cobertura and aplicar_portao:
        print(f"[QA] Portões: cobertura agregada >= {cov_min}%, piso por módulo >= {PISO_POR_MODULO}%")
    print(f"[QA] {' '.join(cmd)}\n")

    codigo = subprocess.run(cmd, cwd=BASE_DIR).returncode

    if cobertura:
        reprovacoes = _avaliar_portao_por_modulo(aplicar_portao)
        if reprovacoes and codigo == 0:
            codigo = 1

    print("\n" + "=" * 72)
    if codigo == 0:
        print(f"  QA APROVADO — kernel exercitado: {ambiente['kernel_de_simulacao']}")
    else:
        print(f"  QA REPROVADO (código {codigo}) — kernel: {ambiente['kernel_de_simulacao']}")
    print("=" * 72)
    return codigo


def main():
    analisador = argparse.ArgumentParser(
        description="Agente de QA do Netuno 5",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    analisador.add_argument("--layer", choices=sorted(CAMADAS), default="all",
                            help="camada de testes a executar")
    analisador.add_argument("--no-cov", action="store_true",
                            help="desativa a medição de cobertura")
    analisador.add_argument("--cov-min", type=int, default=COBERTURA_MINIMA_PADRAO,
                            help=f"cobertura agregada mínima (padrão: {COBERTURA_MINIMA_PADRAO}%%)")
    analisador.add_argument("--no-gate", action="store_true",
                            help="mede a cobertura mas não reprova a execução por ela")
    analisador.add_argument("--loop", type=int, default=0,
                            help="observação contínua com intervalo de N segundos")
    argumentos = analisador.parse_args()

    parametros = dict(
        camada=argumentos.layer,
        cobertura=not argumentos.no_cov,
        cov_min=argumentos.cov_min,
        aplicar_portao=not argumentos.no_gate,
    )

    if argumentos.loop > 0:
        print(f"[QA] Observação contínua a cada {argumentos.loop}s. Ctrl+C encerra.")
        try:
            ciclo = 1
            while True:
                print(f"\n{'=' * 24} CICLO DE QA #{ciclo} {'=' * 24}")
                executar(**parametros)
                time.sleep(argumentos.loop)
                ciclo += 1
        except KeyboardInterrupt:
            print("\n[QA] Observação encerrada pelo usuário.")
    else:
        sys.exit(executar(**parametros))


if __name__ == "__main__":
    main()
