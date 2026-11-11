# Triton documentation (International Edition)

Single entry point to the documentation. English documents are under [`en/`](en/); the
documents marked «(Portuguese)» exist only in Portuguese.

## Where to start

| If you want to… | Read |
| :--- | :--- |
| install and run the program | [`../README.md`](../README.md) |
| know what is specific to this edition | [`en/editions.md`](en/editions.md) |
| understand the equations and the limits of the model | [`en/model.md`](en/model.md) |
| know what was verified and what was not | [`en/verification.md`](en/verification.md) |
| run a first project | [`en/getting-started.md`](en/getting-started.md) |
| use the command line | [`../infos_licenses/CLI_USAGE.md`](../infos_licenses/CLI_USAGE.md) |
| run or extend the tests | [`../tests/README.md`](../tests/README.md) |

## Full map

| Document | Content |
| :--- | :--- |
| [`en/model.md`](en/model.md), [`metodologia.md`](metodologia.md) (Portuguese) | equations, assumptions and boundaries of the model |
| [`equacoes_balanco.md`](equacoes_balanco.md) (Portuguese) | the daily balance equations |
| [`../triton/docs/fluxogramas_metodologicos.md`](../triton/docs/fluxogramas_metodologicos.md) | atlas of the implemented flowcharts |
| [`../triton/docs/proximos_passos_decisao_robusta.md`](../triton/docs/proximos_passos_decisao_robusta.md) | technical roadmap of robust decision-making |
| [`en/verification.md`](en/verification.md), [`verificacao_e_validacao.md`](verificacao_e_validacao.md) (Portuguese) | verification and validation report |
| [`conferencia_dos_casos_analiticos.md`](conferencia_dos_casos_analiticos.md) (Portuguese) | the analytical cases in a form that can be checked by hand |
| [`../triton/docs/relatorio_validacao_en.md`](../triton/docs/relatorio_validacao_en.md) | technical verification of the algorithms |
| [`certificacao_edge.md`](certificacao_edge.md) (Portuguese) | EDGE certification and the water credit |
| [`en/editions.md`](en/editions.md), [`edicoes.md`](edicoes.md) (Portuguese) | the edition map: what the user sees and where it is in the code |
| [`../infos_licenses/CLI_USAGE.md`](../infos_licenses/CLI_USAGE.md) | command-line usage |

## Running the verification

```bash
cd triton_int
pip install -r requirements.txt -r requirements-dev.txt
TRITON_EDITION=INT python -m pytest tests/unit tests/test_essencial.py
```

## Conventions

- **Verification** and **validation** are distinct; see the note in
  [`verificacao_e_validacao.md`](verificacao_e_validacao.md).
- Costs, tariffs, doses and environmental factors are **editable assumptions**, not
  normative values.
- Every quantitative statement should state the date and environment of its measurement.
