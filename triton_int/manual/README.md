# Manual do Usuário do Triton

O manual mora aqui, ao lado do código, e não num processador de texto. Três razões,
e as três vieram de defeitos reais deste projeto:

1. **Uma correção de fórmula pode atualizar texto e número na mesma alteração.** A
   correção da energia de bombeamento desta versão mudou o consumo da motobomba em
   65%. Num manual separado, esse número ficaria errado por anos.
2. **Os apêndices são gerados do fonte**, não transcritos. O apêndice A tem 102
   parâmetros e o B tem 24 processos; transcrever à mão significa divergir no dia
   seguinte.
3. **Os números publicados nos estudos de caso são testes.** Cada resultado que
   aparece impresso tem uma asserção correspondente em
   `tests/unit/test_manual_confere_com_o_programa.py`. Quando o programa muda, o
   teste falha e aponta a página.

## Estrutura

```
manual/
  README.md                  este arquivo
  00_frontmatter.md          rosto, ficha, sumário
  partes/                    os 37 capítulos, um arquivo cada
  casos/                     os 9 estudos de caso e seus arquivos .triton
  apendices/                 A e B gerados; C a G escritos
  figuras/                   capturas de tela e gráficos
  gerar.py                   monta o manual inteiro
  gerar_apendices.py         gera os apêndices A e B do fonte
  gerar_tabelas.py           gera as tabelas numéricas dos capítulos
```

## O que já vem pronto no repositório

Estes arquivos são gerados pelos scripts acima, e mesmo assim vão para o controle de
versão: são o que se manda para alguém ler, e quem clona o repositório chega ao texto
sem montar nada.

```
manual/
  Manual-Triton.md         o manual inteiro, em Markdown
  Manual-Triton.pdf        o manual inteiro, em PDF
  mini/                      os sete volumes avulsos, em Markdown e PDF
  en/Triton-User-Manual.*  o manual inteiro em inglês, em Markdown e PDF
  site/                      o site de documentação, pronto para hospedar
```

O site abre direto do disco, em `manual/site/index.html`, sem servidor. Para hospedar,
basta servir a pasta inteira: ela é autocontida, com as figuras, as capas e os PDFs.

Depois de mexer no texto, no código ou numa figura, regere tudo na ordem:

```bash
python manual/gerar.py                # o manual em Markdown
python manual/gerar_changelog.py      # o CHANGELOG.md da raiz
python manual/gerar_pdf.py            # o PDF completo
python manual/gerar_mini_manuais.py   # os sete volumes
python manual/gerar_site.py           # o site
```

E o manual em inglês, que a edição Internacional instala e abre:

```bash
# NÃO rode manual/en/traduzir_tabelas.py: ele sobrescreve tabelas revisadas e corrompe o capítulo 38 em inglês.
python manual/gerar_tabelas.py       # as tabelas geradas (grava em partes/_tabelas e en/partes/_tabelas)
python manual/en/apendices_en.py      # os apêndices A, B e D, em inglês
python manual/gerar.py --idioma en    # manual/en/Triton-User-Manual.md
python manual/gerar_pdf.py --idioma en
python manual/en/conferir.py          # a estrutura segue a do português?
```

O texto inglês fica em `manual/en/partes` e `manual/en/apendices`, um arquivo por seção,
com o mesmo nome do português. Mudou uma seção em português, mude a inglesa: o
`conferir.py` e `tests/unit/test_manual_en.py` recusam títulos, figuras, equações,
remissões ou tabelas que não batam, e português esquecido no texto inglês.

`build_exe.py` roda a mesma sequência antes de empacotar o instalador.

## Como lançar uma versão

O número da versão vive num lugar só, `triton/__init__.py`, e todo o resto o lê de
lá: o pacote, o instalador, a capa do manual, o rodapé do PDF e o site.

1. Escreva a entrada da versão no capítulo de histórico,
   `partes/38_historico_de_versoes.md`, no formato `## Versão X.Y.Z — data`, com as
   duas listas: o que altera resultados e o que não altera. A entrada nova vem
   primeiro.
2. Troque `__version__` em `triton/__init__.py`.
3. Regere tudo na ordem acima. O `CHANGELOG.md` da raiz sai do capítulo, e não se
   escreve à mão.
4. Rode a suíte. `tests/unit/test_changelog.py` recusa lançar sem entrada, sem data
   ou com o changelog fora de dia; `tests/unit/test_o_que_se_comunica.py` recusa
   documento distribuído que cite outra versão.

Enquanto `pyproject.toml` declarar `Development Status :: 4 - Beta`, o manual escreve
«(beta)» junto da versão e a regra de citar só a versão atual fica suspensa. O
lançamento da 1.0.0, a primeira versão oficial, sairá desse estado.

## O que não está aqui

O material de terceiros consultado para escrever o manual — dissertações, artigos,
manuais de outros programas e o texto das normas — **não é redistribuído neste
repositório**. As referências completas estão no apêndice de bibliografia, e cada
número publicado declara a fonte no ponto em que aparece.

## Como montar

```bash
python manual/gerar_apendices.py      # apêndices A e B, do fonte
python manual/gerar_tabelas.py        # tabelas numéricas dos capítulos
python manual/gerar.py                # junta tudo em manual/Manual-Triton.md
```

O plano editorial completo, com as páginas por capítulo e o que já existe escrito no
repositório, está em [`docs/plano_do_manual.html`](../docs/plano_do_manual.html).

## Convenções de escrita

- **Português do Brasil.** O manual do Netuno 4 é em português, e este é o sucessor.
- **Número impresso é número calculado.** Nenhum valor no texto sai da cabeça de
  quem escreve: ou vem de tabela gerada, ou tem asserção no teste.
- **Cada capítulo abre dizendo o que o leitor vai conseguir fazer** ao terminá-lo.
- **Quadros marcados com «Atenção»** guardam as armadilhas: o dia de chuva que se
  perde inteiro, o extravasamento calculado antes da demanda, a potência de placa que
  é de eixo.
- **Nada de promessa vaga.** Onde o programa não serve, o capítulo 34 diz.
