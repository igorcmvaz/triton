# Documentação do Netuno 5

Ponto de entrada único da documentação. Antes desta versão os documentos estavam
distribuídos por sete diretórios sem índice; este arquivo mapeia todos eles.

---

## Por onde começar

| Se você quer… | Leia |
| :--- | :--- |
| instalar e executar o programa | [`../README.md`](../README.md) |
| entender as equações e as fronteiras do modelo | [`metodologia.md`](metodologia.md) |
| saber o que foi verificado e o que não foi | [`verificacao_e_validacao.md`](verificacao_e_validacao.md) |
| gerar novos casos de referência no Netuno 4 | [`protocolo_netuno4.md`](protocolo_netuno4.md) |
| **conferir as contas dos casos analíticos** | [`conferencia_dos_casos_analiticos.md`](conferencia_dos_casos_analiticos.md) |
| ver o encadeamento do cálculo em diagramas | [`../netuno/docs/fluxogramas_metodologicos.md`](../netuno/docs/fluxogramas_metodologicos.md) |
| conferir um cálculo à mão | [`../examples/ESTUDO_DE_CASO_TRES_MODELOS_REFERENCIA.md`](../examples/ESTUDO_DE_CASO_TRES_MODELOS_REFERENCIA.md) |
| usar a linha de comando | [`../infos_licenses/CLI_USAGE.md`](../infos_licenses/CLI_USAGE.md) |
| rodar ou estender os testes | [`../tests/README.md`](../tests/README.md) |

---

## Mapa completo

### Metodologia e ciência do modelo

| Documento | Conteúdo |
| :--- | :--- |
| [`metodologia.md`](metodologia.md) | Equações, premissas e fronteiras do modelo em 9 seções: chuva efetiva, balanço YAS, CAPEX, bombeamento, economia, ACV, TOPSIS |
| [`../netuno/docs/fluxogramas_metodologicos.md`](../netuno/docs/fluxogramas_metodologicos.md) | Atlas de 22 fluxogramas do encadeamento implementado |
| [`../examples/PARAMETROS_DEPENDENTES_DO_VOLUME_RESERVATORIO.md`](../examples/PARAMETROS_DEPENDENTES_DO_VOLUME_RESERVATORIO.md) | O que depende e o que não depende do volume da cisterna |
| [`../netuno/docs/proximos_passos_decisao_robusta.md`](../netuno/docs/proximos_passos_decisao_robusta.md) | Roteiro técnico de maturidade da decisão robusta |

### Verificação, validação e qualidade

| Documento | Conteúdo |
| :--- | :--- |
| [`verificacao_e_validacao.md`](verificacao_e_validacao.md) | **Relatório principal de V&V**: propriedades científicas, cobertura, replicação, defeitos, limitações |
| [`protocolo_netuno4.md`](protocolo_netuno4.md) | Roteiro para gerar casos de referência na interface do Netuno 4 |
| [`conferencia_dos_casos_analiticos.md`](conferencia_dos_casos_analiticos.md) | **Pede revisão humana** — as nove derivações analíticas em forma conferível |
| [`../netuno/docs/relatorio_validacao.md`](../netuno/docs/relatorio_validacao.md) | Relatório de verificação técnica dos algoritmos (PT) |
| [`../netuno/docs/relatorio_validacao_en.md`](../netuno/docs/relatorio_validacao_en.md) | Idem, em inglês |
| [`../tests/README.md`](../tests/README.md) | Organização da suíte de testes por camadas |

### Casos de referência e verificação manual

| Documento | Conteúdo |
| :--- | :--- |
| [`../examples/ESTUDO_DE_CASO_TRES_MODELOS_REFERENCIA.md`](../examples/ESTUDO_DE_CASO_TRES_MODELOS_REFERENCIA.md) | Verificação manual de três modelos de referência |
| [`../examples/DETALHAMENTO_COMPLETO_TRES_MODELOS.md`](../examples/DETALHAMENTO_COMPLETO_TRES_MODELOS.md) | Detalhamento completo dos mesmos três modelos |

### Base tarifária

| Documento | Conteúdo |
| :--- | :--- |
| [`../tarifas/FONTES_E_METODOLOGIA.md`](../tarifas/FONTES_E_METODOLOGIA.md) | Procedência e método de auditoria das tarifas |
| [`../tarifas/PANORAMA_TARIFAS_E_CONFIABILIDADE.md`](../tarifas/PANORAMA_TARIFAS_E_CONFIABILIDADE.md) | Panorama e confiabilidade por prestador |
| [`../tarifas/README.md`](../tarifas/README.md) | Catálogo auditado de 652 municípios |

### Base de dados CLIMBra (CMIP6)

| Documento | Conteúdo |
| :--- | :--- |
| [`base_climatica_climbra.md`](base_climatica_climbra.md) | Procedência do CLIMBra (Nature Scientific Data), 19 modelos CMIP6, correção QDM e arquitetura SQLite de alta densidade |

### Operação e integrações

| Documento | Conteúdo |
| :--- | :--- |
| [`../infos_licenses/CLI_USAGE.md`](../infos_licenses/CLI_USAGE.md) | Uso da interface de linha de comando |
| [`../templates/README.md`](../templates/README.md) | Modelos de projeto e planilhas de entrada |
| [`../integrations/revit/README.md`](../integrations/revit/README.md) | Integração BIM com Revit |
| [`../LegadoWeb/README.md`](../LegadoWeb/README.md) | Versão web descontinuada (arquivo histórico) |

### Material de referência externo

| Documento | Conteúdo |
| :--- | :--- |
| `../additional_material/documentation/Manual-Netuno-4_Junho2014.pdf` | Manual do Netuno 4, software antecessor |
| `../additional_material/documentation/Dissertacao_Vinicius Rocha.pdf` | Dissertação de referência |

---

## Executando a verificação

```bash
# suíte completa com portões de qualidade
python scripts/qa_runner.py

# apenas as propriedades científicas do motor hidrológico
python scripts/qa_runner.py --layer ciencia

# regerar as figuras do relatório de V&V
python docs/gerar_figuras.py
```

---

## Convenções desta documentação

- **Verificação** e **validação** são distintas e não intercambiáveis; ver a nota
  terminológica em [`verificacao_e_validacao.md`](verificacao_e_validacao.md).
- Valores de custos, tarifas, doses e fatores ambientais são **premissas editáveis**, não
  valores normativos.
- Toda afirmação quantitativa neste conjunto deve indicar a data de apuração e o ambiente
  em que foi medida.
