# Arquitetura do Núcleo Triton (`triton.core`)

O núcleo de engenharia do **Triton** é organizado em 10 subdomínios temáticos especializados:

```
triton/core/
│
├── hydrology/      # Balanço hídrico diário YAS, demandas estocásticas e qualidade
├── climate/        # Séries pluviométricas históricas e projeções climáticas CMIP6
├── economics/      # Engenharia econômica, fluxo de caixa, VPL, TIR e custos
├── tariffs/        # Estruturas tarifárias em cascata e bancos de tarifas (BR/PT)
├── lca/            # Avaliação do Ciclo de Vida (ACV), emissões GEE e certificações
├── mcda/           # Decisão multicritério (TOPSIS, VIKOR, SMAA-VIKOR, PROMETHEE II)
├── hydraulics/     # Bombas, pressurizadores, arranjos de recalque e redes
├── cad_bim/        # Exportação vetorial DXF, modelos BIM (IFC) e visualização 3D
├── reporting/      # Laudos técnicos em PDF/HTML, consolidação de estudos e Excel
└── system/         # Configuração central (.triton), serialização, diagnósticos
```

### Retrocompatibilidade Absoluta
Todos os módulos podem ser importados tanto diretamente do seu subdomínio moderno quanto da raiz de `triton.core`:

```python
# Import moderno canônico:
from triton.core.hydrology.simulation import run_daily_simulation
from triton.core.mcda.mcdm_methods import run_promethee
from triton.core.economics.economic import run_economic_analysis

# Import legado (100% compatível através dos shims com proxy de identidade):
from triton.core.simulation import run_daily_simulation
from triton.core.mcdm_methods import run_promethee
from triton.core.economic import run_economic_analysis
```
