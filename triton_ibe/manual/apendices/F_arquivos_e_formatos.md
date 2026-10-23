# Ficheiros, pastas e formatos

Tudo o que o programa lê e escreve, e onde cada coisa fica.

---

## O que o programa lê

<!-- tabela: Formatos que o programa lê e onde cada um é carregado -->
| Formato | Extensão | O que é | Onde se carrega |
| :--- | :--- | :--- | :--- |
| projeto | `.triton` | um estudo completo, com a chuva dentro | Abrir projeto |
| projeto antigo | `.json` | projeto de versão anterior, mesmo conteúdo | Abrir projeto |
| projeto legado | `.csv` | projeto guardado como tabela por uma versão inicial do programa | Abrir projeto |
| série de chuva | `.csv` | uma coluna de milímetros por dia (a edição traz um exemplo em `data/rainfall`) | etapa 1. Projeto e Chuva |
| procura diária | `.csv` | consumo medido, dia a dia | etapa 2. Edificação e Consumo |
| cenários | `.xlsx` | uma linha por cenário | menu Cenários & Ferramentas |

**A série de chuva em CSV** é o formato mais simples possível: uma linha por dia, com
a lâmina em milímetros. O programa aceita ponto ou vírgula como separador decimal, e
ignora uma linha de cabeçalho se houver. Ano incompleto é descartado na leitura, para
não enviesar os totais anuais.

> **Projeto legado em CSV.** O formato antigo não guarda tudo o que a versão atual
> usa: modulação de procura, materiais, pesos do multicritério e a série de chuva
> ficam de fora. Ao abrir um ficheiro desses, o programa avisa e adota os valores
> padrão para o que falta. A secção {{n:21}} mostra o que conferir depois de importar.

---

## O que o programa escreve

<!-- tabela: Formatos que o programa escreve e onde cada um é gerado -->
| Formato | Extensão | O que leva | Onde se gera |
| :--- | :--- | :--- | :--- |
| projeto | `.triton` | todos os parâmetros e a série de chuva | Guardar projeto |
| relatório | `.pdf` | o estudo completo, pronto para entregar | etapa 9. Relatórios PDF |
| folha de cálculo | `.xlsx` | série diária, varrimento e indicadores | etapa 10. Exportação |
| tabela | `.csv` | os mesmos dados, em texto delimitado | etapa 10. Exportação |
| dados | `.json` | os resultados, para reprocessar | etapa 10. Exportação |
| desenho | `.dxf` | o esquema hidráulico, para CAD | etapa 10. Exportação |
| desenho | `.svg` | o mesmo esquema, como imagem vetorial | etapa 10. Exportação |

Na exportação em CSV escolhe-se o separador: **ponto e vírgula** para abrir numa folha de cálculo
configurada em português, **vírgula** para o padrão internacional. Escolher mal faz a folha de
cálculo abrir tudo numa coluna só.

O desenho sai em três apresentações: **prancha técnica A3**, **esquemático simples** e
**biblioteca de blocos**, esta última acompanhada de um ficheiro JSON com as
propriedades dos componentes, para compatibilização BIM. A secção {{n:22}} trata de todos.

---

## O ficheiro de projeto, por dentro

O `.triton` é um ficheiro de texto no formato JSON. Pode ser aberto em qualquer editor
de texto, e isso é deliberado: um estudo publicado precisa ser inspecionável sem o
programa.

Ele tem sete secções:

<!-- tabela: As sete secções do ficheiro de projeto e o que cada uma guarda -->
| Secção | O que guarda |
| :--- | :--- |
| `metadata` | nome do projeto, identificador e datas |
| `rainfall` | a cidade, o período e a **série diária inteira** |
| `building_and_demand` | área, coeficiente, ocupantes, consumo e fração |
| `demand_modulation` | os perfis semanal, mensal e diário, quando houver |
| `reservoirs_and_pumping` | volumes, limiares e a eletrobomba |
| `water_quality_and_etap` | classe-alvo, desinfeção e tratamento |
| `financial_and_economic` | tarifas, impostos, atualizações e prazo |

O apêndice {{n:A}} lista todos os parâmetros, com o nome exato de cada campo.

> **A série de chuva vai dentro do ficheiro.** É o que torna o projeto reproduzível:
> quem receber o ficheiro obtém exatamente os seus números, mesmo sem ter a base
> climática instalada. Em compensação, um projeto com trinta anos de série ocupa
> cerca de 160 kB — o que é pouco para um ficheiro e muito para um anexo de e-mail com
> vinte deles.

---

## Onde ficam as coisas

<!-- tabela: Localização dos ficheiros do programa e dos ficheiros do utilizador -->
| O que | Onde |
| :--- | :--- |
| o programa | `C:\Program Files\Triton` |
| as séries de chuva que acompanham | na pasta do programa, em `data\rainfall` |
| os tarifários transcritos (Lisboa, Porto e Funchal) | dentro do programa, em `triton\data\portugal_tarifarios.json` |
| os casos do manual | na pasta do programa, em `casos` |
| os três projetos de exemplo (Lisboa, Porto e Funchal) | na pasta do programa, em `examples\portugal` |
| a base de precipitação por concelho (E-OBS) | na pasta do programa, em `data\portugal_eobs.db` |
| **os seus projetos e relatórios** | **onde escolher ao guardar** |

O programa não cria pasta de trabalho nem guarda ficheiros escondidos. Cada gravação
pergunta o destino, e nada do que se produz fica dentro da pasta de instalação — o
que significa que reinstalar ou atualizar o programa não apaga nada do que é seu.

---

## Compatibilidade entre versões

<!-- tabela: Compatibilidade entre versões do ficheiro de projeto -->
| Situação | O que acontece |
| :--- | :--- |
| projeto de versão anterior | abre; campos novos assumem o valor por defeito |
| projeto desta versão em versão anterior | pode não abrir, ou perder campos |
| projeto legado em CSV | abre com aviso; confira o que a secção {{n:21}} lista |
| ficheiro JSON de outro programa | **recusado**, com mensagem própria |

A última linha merece explicação. Um ficheiro JSON que não seja um projeto do Triton
poderia, em princípio, ser aceito e preenchido com valores por defeito — e o utilizador
simularia 100 m² acreditando simular os 180 m² que o ficheiro descreve. O programa
prefere interromper a abertura com mensagem própria, o que é incômodo e é correto: um
projeto aberto errado produz um estudo inteiro errado.
