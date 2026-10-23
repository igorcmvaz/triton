# Ficheiros de projeto do manual (Edição Ibérica)

Cada ficheiro reproduz um resultado impresso no manual. Abra-o com **Ficheiro > Abrir projeto** e carregue em **Simular**.

A chuva de Lisboa e do Porto é a da base E-OBS por concelho (normal 1991-2020, `data/portugal_eobs.db`): o ficheiro guarda a referência da série e a impressão digital dos valores, e o programa recompõe-na da base ao abrir. O Funchal usa a série ERA5 de `data/rainfall/Funchal.csv`, incorporada no ficheiro. O caso dos dez dias traz os seus dez valores dentro do ficheiro. Cidades: Lisboa (o tutorial), Porto e Funchal; cada ficheiro leva o tarifário de água e saneamento da sua cidade, transcrito em `triton/data/portugal_tarifarios.json`.

Os custos são **ilustrativos, não são preços de mercado**: só os ficheiros do tutorial de Lisboa (01, 04, 06, 09 e 10) os trazem, em euros, como valores redondos para acompanhar o método. Os outros ficheiros comparam chuva, procura e tarifário e deixam os custos a zero. Introduza os seus na etapa 5 antes de tirar qualquer conclusão económica.

Os ficheiros 09 e 10 abrem com a **Modulação Probabilística** (etapa 13) já montada: vá à etapa 13 e carregue em **Simular**. Os restantes têm volume fixo, com exceção do 04, e por isso a ferramenta de modulação mostra neles só o volume do estudo.

| Ficheiro | Secção | O que demonstra | Resultado |
| :--- | :--- | :--- | ---: |
| `01_tutorial_lisboa.triton` | 4.1 a 4.10 | o projeto fechado do tutorial em Lisboa: cisterna de 5.000 L em polietileno e elevação para um reservatório superior de 1.000 L (custos ilustrativos, não são preços de mercado) | 17,88% com 5 000 L |
| `02_porto.triton` | 3.1 | a moradia do tutorial levada ao Porto, com a chuva E-OBS do Porto e o tarifário da Águas e Energia do Porto (sem custos definidos) | 22,04% com 5 000 L |
| `03_funchal.triton` | 3.1 | a moradia do tutorial levada ao Funchal, com a chuva ERA5 do Funchal, o tarifário da Câmara Municipal do Funchal e a eletricidade da EEM (sem custos definidos) | 12,98% com 5 000 L |
| `04_tutorial_varredura.triton` | 4.4 e 2.2 | o projeto antes do reservatório superior, em modo varredura, de 0 a 20.000 L em passos de 1.000 L (Lisboa) | volume ideal 5 000 L, 17,49% |
| `05_dez_dias.triton` | 2.1 | o caso didático de dez dias, 11 a 20 de dezembro de 2019 da série de Lisboa, que cabe numa folha de cálculo | 24,43% com 2 000 L |
| `06_reservatorio_superior.triton` | 4.5 | 5.000 L em baixo mais 1.000 em cima, a comparação da secção 4.5 contra os 6.000 L de um reservatório só (Lisboa) | 17,88% com 5 000 L |
| `07_escola_semanal.triton` | 3.4 e 3.5 | uma escola do Porto, com 300 alunos e procura modulada por dia da semana | 23,03% com 30 000 L |
| `08_hotel_mensal.triton` | 3.4 | um hotel de Lisboa com ocupação mensal ilustrativa, concentrada no verão seco | 10,36% com 25 000 L |
| `09_modulacao_tutorial.triton` | 7.3 e 7.4 | a varredura do tutorial com a Modulação Probabilística montada: as três variáveis de consumo, a chuva, o tarifário e o investimento, mil realizações, semente 42 | volume ideal 5 000 L, 17,49% |
| `10_modulacao_captacao.triton` | 7.4 | a mesma varredura com a incerteza na captação (área, coeficiente de escoamento, descarte), o fator de chuva sobre a série de Lisboa, o tarifário e o investimento; mil realizações, semente 42 | volume ideal 5 000 L, 17,49% |

Os números da última coluna obtêm-se **relendo o ficheiro gravado** e simulando o que foi relido. Se um campo não sobreviver ao ficheiro, o número muda e o teste correspondente falha.
