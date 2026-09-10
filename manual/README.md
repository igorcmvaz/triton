# Manual do Usuário do Netuno 5

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
  casos/                     os 9 estudos de caso e seus arquivos .netuno
  apendices/                 A e B gerados; C a G escritos
  figuras/                   capturas de tela e gráficos
  gerar.py                   monta o manual inteiro
  gerar_apendices.py         gera os apêndices A e B do fonte
  gerar_tabelas.py           gera as tabelas numéricas dos capítulos
```

## Como montar

```bash
python manual/gerar_apendices.py      # apêndices A e B, do fonte
python manual/gerar_tabelas.py        # tabelas numéricas dos capítulos
python manual/gerar.py                # junta tudo em manual/Manual-Netuno-5.md
```

O plano editorial completo, com as páginas por capítulo e o que já existe escrito no
repositório, está em [`docs/plano_do_manual.md`](../docs/plano_do_manual.md).

## Convenções de escrita

- **Português do Brasil.** O manual do Netuno 4 é em português, e este é o sucessor.
- **Número impresso é número calculado.** Nenhum valor no texto sai da cabeça de
  quem escreve: ou vem de tabela gerada, ou tem asserção no teste.
- **Cada capítulo abre dizendo o que o leitor vai conseguir fazer** ao terminá-lo.
- **Quadros marcados com «Atenção»** guardam as armadilhas: o dia de chuva que se
  perde inteiro, o extravasamento calculado antes da demanda, a potência de placa que
  é de eixo.
- **Nada de promessa vaga.** Onde o programa não serve, o capítulo 34 diz.
