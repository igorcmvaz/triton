# Arquivos, pastas e formatos

Tudo o que o programa lê e escreve, e onde cada coisa fica.

---

## O que o programa lê

| Formato | Extensão | O que é | Onde se carrega |
| :--- | :--- | :--- | :--- |
| projeto | `.netuno` | um estudo completo, com a chuva dentro | Abrir projeto |
| projeto antigo | `.json` | projeto de versão anterior, mesmo conteúdo | Abrir projeto |
| projeto legado | `.csv` | projeto do Netuno 4 ou da série 5.0 inicial | Abrir projeto |
| série de chuva | `.csv` | uma coluna de milímetros por dia | Projeto e Chuva |
| demanda diária | `.csv` | consumo medido, dia a dia | Edificação e Consumo |
| cenários | `.xlsx` | uma linha por cenário | Multi-Critério |

**A série de chuva em CSV** é o formato mais simples possível: uma linha por dia, com
a lâmina em milímetros. O programa aceita ponto ou vírgula como separador decimal, e
ignora uma linha de cabeçalho se houver. Ano incompleto é descartado na leitura, para
não enviesar os totais anuais.

> **Projeto legado em CSV.** O formato antigo não guarda tudo o que a versão atual
> usa: modulação de demanda, materiais, pesos do multicritério e a série de chuva
> ficam de fora. Ao abrir um arquivo desses, o programa avisa e adota os valores
> padrão para o que falta. A seção {{n:21}} mostra o que conferir depois de importar.

---

## O que o programa escreve

| Formato | Extensão | O que leva | Onde se gera |
| :--- | :--- | :--- | :--- |
| projeto | `.netuno` | todos os parâmetros e a série de chuva | Salvar projeto |
| relatório | `.pdf` | o estudo completo, pronto para entregar | Relatórios PDF |
| planilha | `.xlsx` | série diária, varredura e indicadores | Central de Exportação |
| tabela | `.csv` | os mesmos dados, em texto delimitado | Central de Exportação |
| dados | `.json` | os resultados, para reprocessar | Central de Exportação |
| desenho | `.dxf` | o esquema hidráulico, para CAD | Central de Exportação |
| desenho | `.svg` | o mesmo esquema, como imagem vetorial | Central de Exportação |

Na exportação em CSV você escolhe o separador: **ponto e vírgula** para abrir no Excel
em português, **vírgula** para o padrão internacional. Escolher errado faz a planilha
abrir tudo numa coluna só.

O desenho sai em três apresentações: **prancha técnica A3**, **esquemático simples** e
**biblioteca de blocos**, esta última acompanhada de um arquivo JSON com as
propriedades dos componentes, para compatibilização BIM. A seção {{n:22}} trata de todos.

---

## O arquivo de projeto, por dentro

O `.netuno` é um arquivo de texto no formato JSON. Pode ser aberto em qualquer editor
de texto, e isso é deliberado: um estudo publicado precisa ser inspecionável sem o
programa.

Ele tem sete seções:

| Seção | O que guarda |
| :--- | :--- |
| `metadata` | nome do projeto, identificador e datas |
| `rainfall` | a cidade, o período e a **série diária inteira** |
| `building_and_demand` | área, coeficiente, ocupantes, consumo e fração |
| `demand_modulation` | os perfis semanal, mensal e diário, quando houver |
| `reservoirs_and_pumping` | volumes, limiares e a motobomba |
| `water_quality_and_etap` | classe-alvo, desinfecção e tratamento |
| `financial_and_economic` | tarifas, impostos, reajustes e prazo |

A seção {{n:A}} lista os 103 parâmetros, com o nome exato de cada campo.

> **A série de chuva vai dentro do arquivo.** É o que torna o projeto reproduzível:
> quem receber o arquivo obtém exatamente os seus números, mesmo sem ter a base
> climática instalada. Em compensação, um projeto com trinta anos de série ocupa
> cerca de 160 kB — o que é pouco para um arquivo e muito para um anexo de e-mail com
> vinte deles.

---

## Onde ficam as coisas

| O que | Onde |
| :--- | :--- |
| o programa | `C:\Program Files\Netuno 5` |
| as séries de chuva que acompanham | na pasta do programa, em `data\rainfall` |
| a base de tarifas dos 652 municípios | dentro do programa |
| os casos do manual | na pasta do programa, em `casos` |
| os três estudos de referência | na pasta do programa, em `exemplos` |
| a base climática nacional, se instalada | onde o instalador dela indicar |
| **os seus projetos e relatórios** | **onde você escolher ao salvar** |

O programa não cria pasta de trabalho nem guarda arquivos escondidos. Cada gravação
pergunta o destino, e nada do que você produz fica dentro da pasta de instalação — o
que significa que reinstalar ou atualizar o programa não apaga nada seu.

---

## Compatibilidade entre versões

| Situação | O que acontece |
| :--- | :--- |
| projeto de versão anterior | abre; campos novos assumem o padrão |
| projeto desta versão em versão anterior | pode não abrir, ou perder campos |
| projeto do Netuno 4 em CSV | abre com aviso; confira o que a seção {{n:21}} lista |
| arquivo JSON de outro programa | **recusado**, com mensagem própria |

A última linha merece explicação. Um arquivo JSON que não seja um projeto do Netuno
poderia, em princípio, ser aceito e preenchido com valores padrão — e o usuário
simularia 100 m² acreditando simular os 180 m² que o arquivo descreve. O programa
prefere interromper a abertura com mensagem própria, o que é incômodo e é correto: um
projeto aberto errado produz um estudo inteiro errado.
