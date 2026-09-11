# Arquivos de projeto do manual

Cada arquivo reproduz um resultado impresso no manual. Abra pelo menu
**Arquivo, Abrir projeto**, e rode.

A série de chuva está **dentro** do arquivo: ele abre sem o CSV original,
em qualquer máquina.

| Arquivo | Capítulo | O que demonstra | Resultado |
| :--- | :--- | :--- | ---: |
| `01_tutorial_florianopolis.netuno` | 4 a 13 | o projeto do tutorial, com a cisterna escolhida no capítulo 12 | 37,46% com 5 000 L |
| `02_tutorial_varredura.netuno` | 7 e 24 | o mesmo projeto em modo varredura, de 0 a 20.000 L, passo de 1.000 L | volume ideal 5 000 L, 37,46% |
| `03_dez_dias.netuno` | 23 | o caso didático de dez dias, que cabe numa planilha | 36,00% com 2 000 L |
| `04_reservatorio_superior.netuno` | 8 | 5.000 L embaixo mais 1.000 em cima, a comparação do capítulo 8 contra os 6.000 L de um tanque só | 37,76% com 5 000 L |
| `05_manaus.netuno` | 14 | o projeto do tutorial levado a Manaus, que chove mais e rende menos | 27,92% com 5 000 L |
| `06_brasilia.netuno` | 14 | o projeto do tutorial levado a Brasília, de estação seca marcada | 20,80% com 5 000 L |
| `07_saopaulo.netuno` | 14 | o projeto do tutorial levado a São Paulo | 34,77% com 5 000 L |
| `08_escola_semanal.netuno` | 17 e 18 | escola de 300 alunos com demanda modulada por dia da semana | 34,34% com 30 000 L |
| `09_hotel_mensal.netuno` | 17 | hotel de litoral com ocupação mensal em fase com a chuva | 32,11% com 25 000 L |

Os números da última coluna são obtidos **relendo o arquivo gravado** e
simulando o que foi relido. Se um campo não sobreviver ao arquivo, o
número muda e o teste correspondente falha.
