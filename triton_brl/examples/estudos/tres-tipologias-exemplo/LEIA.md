# Estudo de exemplo: três edifícios dos casos de referência

Um estudo em lote de três casos que roda de ponta a ponta com os projetos de `examples/`: a residência unifamiliar de
Florianópolis (`estudo_caso_1_florianopolis1.triton`), o edifício corporativo de Brasília (`estudo_caso_2_brasilia2.triton`)
e a escola de tempo integral de Manaus (`estudo_caso_3_manaus3.triton`). Cada um é um `grupo` (tipologia) do estudo,
com o seu próprio projeto e a sua série de chuva. Nenhum número foi inventado para este estudo.

```powershell
python -m triton.cli estudo validate examples\estudos\tres-tipologias-exemplo\estudo.json
python -m triton.cli estudo run examples\estudos\tres-tipologias-exemplo\estudo.json --saida saida\exemplo
python -m triton.cli estudo texto saida\exemplo --modelo examples\estudos\tres-tipologias-exemplo\modelo_texto.md
```

A pasta de saída recebe `resultados.csv` (formato tidy, uma linha por caso e métrica), `resultados.json` (com a
proveniência), `tabela.md`, `tabela.tex` (booktabs), `resumo.md` e `texto.md`. A análise é `economic`, com os custos de
referência que cada projeto traz; o estudo pede também o valor presente líquido e o payback descontado. Os projetos
guardam a série de chuva dentro do `.triton`; registre a fonte e o período dela no protocolo do estudo.

Para estudar outros edifícios, copie o `estudo.json`, mude `id`, `tipologia` e os casos, e preencha as `substituicoes` com dados
seus, cada um com a respectiva fonte (`triton estudo apelidos` lista os apelidos e as métricas; `triton estudo init <pasta> --tipologia escolar`
cria um esqueleto vazio).
