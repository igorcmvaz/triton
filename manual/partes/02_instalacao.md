# 2. Instalação e primeira execução

> Ao terminar este capítulo você terá o programa rodando e uma simulação concluída.

---

## 2.1. Requisitos

| Requisito | Versão |
| :--- | :--- |
| Python | 3.10, 3.11, 3.12 ou 3.13 |
| interface gráfica | PySide6, Qt 6 |
| licença | GPL v3 |

Instale as dependências:

```bash
pip install -r requirements.txt
```

E execute:

```bash
python main.py
```

---

## 2.2. O que é opcional, e o que acontece sem ele

O programa degrada de forma previsível quando um componente opcional falta. Nenhuma
ausência impede o cálculo.

| Componente | Sem ele |
| :--- | :--- |
| **Numba** | o mesmo laço diário roda em Python puro, com resultado **idêntico**; a suíte verifica a paridade com tolerância de 10⁻⁹ |
| **Qt WebEngine** | a conversão para PDF cai no gerador alternativo, com o mesmo conteúdo |
| **PySide6** | a interface não abre, mas a linha de comando e o núcleo funcionam |
| **base climática** | a aba de Projeto oferece só arquivo próprio |

A degradação sem PySide6 é deliberada: permite verificar o núcleo em ambiente mínimo,
sem a pilha gráfica.

---

## 2.3. A base climática

Seis vírgula cinco gigabytes em cerca de 37 mil arquivos, com 652 cidades, 19
modelos do CMIP6 e 3 cenários. É **distribuída à parte** do programa, e instalada no
diretório que ele indica.

Sem ela, o programa continua inteiramente funcional com séries próprias — e quatro
séries históricas longas já acompanham a instalação, em `data/rainfall/`:
Florianópolis, Brasília, Manaus e São Paulo, três arquivos cada.

O apêndice E traz os detalhes.

---

## 2.4. Os arquivos que acompanham o manual

| Arquivo | Para que serve |
| :--- | :--- |
| `manual/casos/cap23_dez_dias.netuno` | o caso resolvido do capítulo 23 |
| `manual/casos/cap23_dez_dias.csv` | a série de dez dias desse caso |
| `data/rainfall/Florianopolis1.csv` | a série do tutorial da Parte 2 |
| `examples/*.netuno` | três estudos de caso completos |

Abra o caso do capítulo 23, rode, e compare com a tabela impressa. Se algum número
divergir, o manual está desatualizado em relação ao programa — e a suíte de testes já
terá avisado, porque cada número daquela tabela tem asserção correspondente.

---

## 2.5. A primeira simulação, em cinco minutos

1. Abra o programa.
2. Na aba **Projeto**, carregue `data/rainfall/Florianopolis1.csv`.
3. Informe área de captação de 150 m², coeficiente de 0,85 e descarte de 2,0 mm.
4. Na aba **Edificação**, escolha residencial unifamiliar, 4 moradores, 150 L por
   habitante e dia, e fração atendível de 40%.
5. Na aba **Simulação**, informe volume fixo de 5.000 L e rode.

Você deve obter potencial de economia próximo de **37%**. O capítulo 6 explica o que
esse número significa, e o 7 pergunta se 5.000 L é o volume certo.

---

## 2.6. A linha de comando

O mesmo núcleo, sem tela:

```bash
python -m netuno.cli run projeto.netuno --analysis all
```

Comece por `validate`, que confere a estrutura e as premissas antes de simular:

```bash
python -m netuno.cli validate projeto.netuno
```

O guia 19 trata do uso em lote, e o apêndice F traz a referência completa das opções.

---

## 2.7. Verificar a instalação

```bash
python -m pytest -q
```

A suíte tem novecentas asserções. Se ela passar inteira, a instalação está íntegra.
Sem PySide6, os módulos de interface não são coletados e o restante roda normalmente.
