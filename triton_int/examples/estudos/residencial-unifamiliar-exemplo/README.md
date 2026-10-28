# Example study: the tutorial house in three cities

A batch study of three cases that runs end to end with the projects shipped in `examples/`: the tutorial
house of the International Edition in New York, London and Cape Town (`new_york.triton`, `london.triton`,
`cape_town.triton`). Each case cites its own project, so each keeps its rainfall series (ERA5 reanalysis,
Open-Meteo, CC BY 4.0), its illustrative tariff and its currency. No number was invented for this study.

```powershell
python -m triton.cli estudo validate examples\estudos\residencial-unifamiliar-exemplo\estudo.json
python -m triton.cli estudo run examples\estudos\residencial-unifamiliar-exemplo\estudo.json --saida out\example
python -m triton.cli estudo texto out\example --modelo examples\estudos\residencial-unifamiliar-exemplo\modelo_texto.md
```

The output folder gets `resultados.csv` (tidy, one row per case and metric), `resultados.json` (with the
provenance), `tabela.md`, `tabela.tex` (booktabs), `resumo.md` and `texto.md`. The analysis is `economic`, but
the example projects have **no costs set** (see `examples/LEIA.md`), so the study asks only for the potable
water saving, the rainwater used, the overflow and the annual saving on the water bill. The three currencies
differ (USD, GBP, ZAR): the summary says the monetary values are not comparable.

To study other buildings, copy `estudo.json`, change `id`, `tipologia` and the cases, and fill in the `substituicoes`
with data of your own, each with its source (`triton estudo apelidos` lists the aliases and metrics;
`triton estudo init <folder> --tipologia escolar` creates an empty skeleton).
