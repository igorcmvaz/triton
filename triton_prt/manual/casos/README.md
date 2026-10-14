# Arquivos de projeto do manual

Cada arquivo reproduz um resultado impresso no manual. Abra pelo menu
**Arquivo, Abrir projeto**, e rode.

A série de chuva está **dentro** do arquivo: ele abre sem o CSV original,
em qualquer máquina. A exceção é o `11_modulacao_climbra.triton`, com a
chuva da base CLIMBra: ele guarda a referência da série e a impressão
digital dos valores, e o programa a recompõe da base ao abrir.

Os casos 10 e 11 abrem com a **Modulação Probabilística** (etapa 13) já
montada: basta ir à etapa 13 e clicar em **Simular**. Os demais têm volume
fixo, com exceção do 02, e por isso a modulação mostra neles só o volume
do estudo.

| Arquivo | Seção | O que demonstra | Resultado |
| :--- | :--- | :--- | ---: |
| `01_tutorial_florianopolis.triton` | 4.1 a 4.10 | o projeto fechado do tutorial: cisterna de 4.000 L em polietileno e recalque para caixa superior de 1.000 L | 27,30% com 4.000 L |
| `02_tutorial_varredura.triton` | 4.4 e 2.2 | o projeto antes da caixa superior, em modo varredura, de 0 a 20.000 L, passo de 1.000 L | volume ideal 4.000 L, 27,12% |
| `03_dez_dias.triton` | 2.1 | o caso didático de dez dias, que cabe numa planilha | 36,00% com 2.000 L |
| `04_reservatorio_superior.triton` | 4.5 | 4.000 L embaixo mais 1.000 em cima, a comparação da seção 4.5 contra os 5.000 L de um tanque só | 27,30% com 4.000 L |
| `05_manaus.triton` | 3.1 | o projeto do tutorial levado a Manaus, que chove mais e rende menos | 20,96% com 4.000 L |
| `06_brasilia.triton` | 3.1 | o projeto do tutorial levado a Brasília, de estação seca marcada | 15,45% com 4.000 L |
| `07_saopaulo.triton` | 3.1 | o projeto do tutorial levado a São Paulo | 25,74% com 4.000 L |
| `08_escola_semanal.triton` | 3.4 e 3.5 | escola de 300 alunos com demanda modulada por dia da semana | 34,34% com 30.000 L |
| `09_hotel_mensal.triton` | 3.4 | hotel de litoral com ocupação mensal em fase com a chuva | 32,11% com 25.000 L |
| `10_modulacao_tutorial.triton` | 7.3 e 7.4 | a varredura do tutorial com a Modulação Probabilística montada: as três variáveis de consumo, a chuva, a tarifa e o investimento, mil realizações, semente 42 | volume ideal 4.000 L, 27,12% |
| `11_modulacao_climbra.triton` | 7.4 | a mesma varredura com a chuva da CLIMBra (Florianópolis, SSP2-4.5, 2025 a 2054) e os dezenove modelos climáticos marcados; o arquivo guarda a referência da série, e não os valores | volume ideal 4.000 L, 26,57% |

Os números da última coluna são obtidos **relendo o arquivo gravado** e
simulando o que foi relido. Se um campo não sobreviver ao arquivo, o
número muda e o teste correspondente falha.
