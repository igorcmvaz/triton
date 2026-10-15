# Documentação do Triton

Ponto de entrada único da documentação. Antes desta versão os documentos estavam
distribuídos por sete diretórios sem índice; este arquivo mapeia todos eles.

---

## Por onde começar

| Se você quer… | Leia |
| :--- | :--- |
| instalar e executar o programa | [`../README.md`](../README.md) |
| **saber o que é da Edição Brasil e o que é da International** | [`edicoes.md`](edicoes.md) |
| entender as equações e as fronteiras do modelo | [`metodologia.md`](metodologia.md) |
| saber o que foi verificado e o que não foi | [`verificacao_e_validacao.md`](verificacao_e_validacao.md) |
| gerar novos casos de referência no Netuno 4 | [`protocolo_netuno4.md`](protocolo_netuno4.md) |
| **conferir as contas dos casos analíticos** | [`conferencia_dos_casos_analiticos.md`](conferencia_dos_casos_analiticos.md) |
| ver o encadeamento do cálculo em diagramas | [`../triton/docs/fluxogramas_metodologicos.md`](../triton/docs/fluxogramas_metodologicos.md) |
| conferir um cálculo à mão | [`../examples/ESTUDO_DE_CASO_TRES_MODELOS_REFERENCIA.md`](../examples/ESTUDO_DE_CASO_TRES_MODELOS_REFERENCIA.md) |
| usar a linha de comando | [`../infos_licenses/CLI_USAGE.md`](../infos_licenses/CLI_USAGE.md) |
| rodar ou estender os testes | [`../tests/README.md`](../tests/README.md) |

---

## Mapa completo

### Metodologia e ciência do modelo

| Documento | Conteúdo |
| :--- | :--- |
| [`metodologia.md`](metodologia.md) | Equações, premissas e fronteiras do modelo em 9 seções: chuva efetiva, balanço diário, CAPEX, bombeamento, economia, ACV, TOPSIS |
| [`normas_nbr_x_en16941.md`](normas_nbr_x_en16941.md) | Diferenças entre a NBR 15527/5626 e a EN 16941-1:2024, item a item, e o que o Triton faz em cada uma |
| [`../triton/docs/fluxogramas_metodologicos.md`](../triton/docs/fluxogramas_metodologicos.md) | Atlas de 22 fluxogramas do encadeamento implementado |
| [`../examples/PARAMETROS_DEPENDENTES_DO_VOLUME_RESERVATORIO.md`](../examples/PARAMETROS_DEPENDENTES_DO_VOLUME_RESERVATORIO.md) | O que depende e o que não depende do volume da cisterna |
| [`../triton/docs/proximos_passos_decisao_robusta.md`](../triton/docs/proximos_passos_decisao_robusta.md) | Roteiro técnico de maturidade da decisão robusta |

### Verificação, validação e qualidade

| Documento | Conteúdo |
| :--- | :--- |
| [`verificacao_e_validacao.md`](verificacao_e_validacao.md) | **Relatório principal de V&V**: propriedades científicas, cobertura, replicação, defeitos, limitações |
| [`protocolo_netuno4.md`](protocolo_netuno4.md) | Roteiro para gerar casos de referência na interface do Netuno 4 |
| [`conferencia_dos_casos_analiticos.md`](conferencia_dos_casos_analiticos.md) | **Pede revisão humana** — as nove derivações analíticas em forma conferível |
| [`../triton/docs/relatorio_validacao.md`](../triton/docs/relatorio_validacao.md) | Relatório de verificação técnica dos algoritmos (PT) |
| [`../triton/docs/relatorio_validacao_en.md`](../triton/docs/relatorio_validacao_en.md) | Idem, em inglês |
| [`../tests/README.md`](../tests/README.md) | Organização da suíte de testes por camadas |

### Casos de referência e verificação manual

| Documento | Conteúdo |
| :--- | :--- |
| [`../examples/ESTUDO_DE_CASO_TRES_MODELOS_REFERENCIA.md`](../examples/ESTUDO_DE_CASO_TRES_MODELOS_REFERENCIA.md) | Verificação manual de três modelos de referência |
| [`../examples/DETALHAMENTO_COMPLETO_TRES_MODELOS.md`](../examples/DETALHAMENTO_COMPLETO_TRES_MODELOS.md) | Detalhamento completo dos mesmos três modelos |

### Edições

| Documento | Conteúdo |
| :--- | :--- |
| [`edicoes.md`](edicoes.md) | As duas edições: o que o usuário vê em cada uma, onde está no código, o que vai em cada pacote, que documentos são só da Brasil |
| [`en/editions.md`](en/editions.md) | Idem, em inglês |
| [`instalador.md`](instalador.md) | Como gerar os instaladores das duas edições |

### Base tarifária (só Edição Brasil)

| Documento | Conteúdo |
| :--- | :--- |
| [`../tarifas/FONTES_E_METODOLOGIA.md`](../tarifas/FONTES_E_METODOLOGIA.md) | Procedência e método de auditoria das tarifas |
| [`../tarifas/PANORAMA_TARIFAS_E_CONFIABILIDADE.md`](../tarifas/PANORAMA_TARIFAS_E_CONFIABILIDADE.md) | Panorama e confiabilidade por prestador |
| [`../tarifas/README.md`](../tarifas/README.md) | Catálogo auditado de 652 municípios |

### Base de dados CLIMBra (CMIP6; só Edição Brasil)

| Documento | Conteúdo |
| :--- | :--- |
| [`base_climatica_climbra.md`](base_climatica_climbra.md) | Procedência do CLIMBra (Nature Scientific Data), 19 modelos CMIP6, correção QDM e arquitetura SQLite de alta densidade |

### Operação e integrações

| Documento | Conteúdo |
| :--- | :--- |
| [`../infos_licenses/CLI_USAGE.md`](../infos_licenses/CLI_USAGE.md) | Uso da interface de linha de comando |
| [`../templates/README.md`](../templates/README.md) | Modelos de projeto e planilhas de entrada |
| [`../additional_material/integrations/revit/README.md`](../additional_material/integrations/revit/README.md) | Integração BIM com Revit |

### Material de referência externo

| Documento | Conteúdo |
| :--- | :--- |
| Manual do Netuno 4 (junho de 2014; documento de terceiros, fora do repositório) | Manual do Netuno 4, software antecessor |
| ROCHA, V. L. *Validação do algoritmo do programa Triton para avaliação do potencial de economia de água potável e dimensionamento de reservatórios de sistemas de aproveitamento de água pluvial em edificações*. Dissertação (Mestrado em Engenharia Civil) — UFSC, 2009. [Registro institucional](https://repositorio.ufsc.br/handle/123456789/92966). | Dissertação de referência (validação do algoritmo original) |

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
