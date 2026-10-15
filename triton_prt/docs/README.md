# Documentação do Triton (Edição Portugal)

Ponto de entrada único da documentação.

## Por onde começar

| Se quer… | Leia |
| :--- | :--- |
| instalar e executar o programa | [`../README.md`](../README.md) |
| saber o que é específico desta edição | [`edicoes.md`](edicoes.md) |
| perceber as equações e as fronteiras do modelo | [`metodologia.md`](metodologia.md) |
| saber o que foi verificado e o que não foi | [`verificacao_e_validacao.md`](verificacao_e_validacao.md) |
| conferir as contas dos casos analíticos | [`conferencia_dos_casos_analiticos.md`](conferencia_dos_casos_analiticos.md) |
| ver o encadeamento do cálculo em diagramas | [`../triton/docs/fluxogramas_metodologicos.md`](../triton/docs/fluxogramas_metodologicos.md) |
| usar a linha de comandos | [`../infos_licenses/CLI_USAGE.md`](../infos_licenses/CLI_USAGE.md) |
| correr ou estender os testes | [`../tests/README.md`](../tests/README.md) |

## Mapa completo

| Documento | Conteúdo |
| :--- | :--- |
| [`metodologia.md`](metodologia.md) | equações, pressupostos e fronteiras do modelo |
| [`equacoes_balanco.md`](equacoes_balanco.md) | as equações do balanço diário |
| [`../triton/docs/fluxogramas_metodologicos.md`](../triton/docs/fluxogramas_metodologicos.md) | atlas dos fluxogramas do encadeamento implementado |
| [`../triton/docs/proximos_passos_decisao_robusta.md`](../triton/docs/proximos_passos_decisao_robusta.md) | roteiro técnico da decisão robusta |
| [`verificacao_e_validacao.md`](verificacao_e_validacao.md) | relatório de verificação e validação |
| [`conferencia_dos_casos_analiticos.md`](conferencia_dos_casos_analiticos.md) | os casos analíticos em forma conferível à mão |
| [`../triton/docs/relatorio_validacao.md`](../triton/docs/relatorio_validacao.md) | verificação técnica dos algoritmos |
| [`certificacao_edge.md`](certificacao_edge.md) | certificação EDGE e o crédito de água |
| [`edicoes.md`](edicoes.md), [`en/editions.md`](en/editions.md) | o mapa das edições: o que o utilizador vê e onde está no código |
| [`instalador.md`](instalador.md) | como gerar o instalador |
| [`en/README.md`](en/README.md) | resumo em inglês |

## Executar a verificação

```bash
python scripts/qa_runner.py
python scripts/qa_runner.py --layer ciencia
python docs/gerar_figuras.py
```

## Convenções

- **Verificação** e **validação** são distintas; ver a nota em
  [`verificacao_e_validacao.md`](verificacao_e_validacao.md).
- Custos, tarifas, doses e fatores ambientais são **pressupostos editáveis**, não valores normativos.
- Toda a afirmação quantitativa deve indicar a data e o ambiente da medição.
