# Estudo de exemplo: a moradia do tutorial em três cidades

Um estudo em lote de três casos que corre de ponta a ponta com os projetos distribuídos em `examples/portugal/`:
a moradia do tutorial em Lisboa, no Porto e no Funchal (`lisboa.triton`, `porto.triton`, `funchal.triton`).
Cada caso cita o seu próprio projeto, e por isso mantém a sua série de chuva (E-OBS em Lisboa e no Porto, ERA5 no
Funchal), o seu tarifário ilustrativo e a sua moeda. Nenhum número foi inventado para este estudo.

```powershell
python -m triton.cli estudo validate examples\estudos\residencial-unifamiliar-exemplo\estudo.json
python -m triton.cli estudo run examples\estudos\residencial-unifamiliar-exemplo\estudo.json --saida saida\exemplo
python -m triton.cli estudo texto saida\exemplo --modelo examples\estudos\residencial-unifamiliar-exemplo\modelo_texto.md
```

A pasta de saída recebe `resultados.csv` (formato tidy, uma linha por caso e métrica), `resultados.json` (com a
proveniência), `tabela.md`, `tabela.tex` (booktabs), `resumo.md` e `texto.md`. **A E-OBS só pode ser usada em pesquisa
e educação não comerciais**: o aviso e a citação da licença vão no resumo, nas tabelas e no JSON. A análise é
`economic`, mas os projetos de exemplo **não têm custos definidos** (ver `examples/LEIA.md`); por isso o estudo pede só a
poupança de água potável, a água de chuva aproveitada, o extravasamento e a poupança anual na fatura de água.

Para estudar outros edifícios, copie o `estudo.json`, mude `id`, `tipologia` e os casos, e preencha as `substituicoes` com dados
seus, cada um com a respetiva fonte (`triton estudo apelidos` lista os apelidos e as métricas; `triton estudo init <pasta> --tipologia escolar`
cria um esqueleto vazio).
