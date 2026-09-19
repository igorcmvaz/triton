# Arquivos de projeto do manual

Cada arquivo reproduz um resultado impresso no manual. Abra pelo menu
**Arquivo, Abrir projeto**, e rode.

A série de chuva está **dentro** do arquivo: ele abre sem o CSV original,
em qualquer máquina.

| Arquivo | Seção | O que demonstra | Resultado |
| :--- | :--- | :--- | ---: |
| `01_tutorial_florianopolis.netuno` | 4.1 a 4.10 | o projeto fechado do tutorial: cisterna de 4.000 L em polietileno e recalque para caixa superior de 1.000 L | 27,30% com 4.000 L |
| `02_tutorial_varredura.netuno` | 4.4 e 2.2 | o projeto antes da caixa superior, em modo varredura, de 0 a 20.000 L, passo de 1.000 L | volume ideal 4.000 L, 27,12% |
| `03_dez_dias.netuno` | 2.1 | o caso didático de dez dias, que cabe numa planilha | 36,00% com 2.000 L |
| `04_reservatorio_superior.netuno` | 4.5 | 4.000 L embaixo mais 1.000 em cima, a comparação da seção 4.5 contra os 5.000 L de um tanque só | 27,30% com 4.000 L |
| `05_manaus.netuno` | 3.1 | o projeto do tutorial levado a Manaus, que chove mais e rende menos | 20,96% com 4.000 L |
| `06_brasilia.netuno` | 3.1 | o projeto do tutorial levado a Brasília, de estação seca marcada | 15,45% com 4.000 L |
| `07_saopaulo.netuno` | 3.1 | o projeto do tutorial levado a São Paulo | 25,74% com 4.000 L |
| `08_escola_semanal.netuno` | 3.4 e 3.5 | escola de 300 alunos com demanda modulada por dia da semana | 34,34% com 30.000 L |
| `09_hotel_mensal.netuno` | 3.4 | hotel de litoral com ocupação mensal em fase com a chuva | 32,11% com 25.000 L |

Os números da última coluna são obtidos **relendo o arquivo gravado** e
simulando o que foi relido. Se um campo não sobreviver ao arquivo, o
número muda e o teste correspondente falha.
