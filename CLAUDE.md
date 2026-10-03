# Instruções para quem trabalha neste repositório

## Material recebido do usuário (PDFs, planilhas, páginas salvas)

Todo arquivo que o usuário enviar para a base tarifária, ou como referência, é
registrado **antes** de ser usado:

1. `python tarifas/registro_de_fontes.py conferir ARQUIVO` — se já veio, diga ao
   usuário quando e com que item, e não transcreva de novo.
2. `python tarifas/registro_de_fontes.py registrar ARQUIVO --prestador ... --conteudo ...
   [--vigencia ...]` — guarda o arquivo em `tarifas/fontes/<prestador>/` e o registra.
   Material licenciado ou de terceiros que não se redistribui (normas, manuais alheios)
   leva `--nao-guardar --motivo "..."`.
3. Depois de transcrever: `python tarifas/registro_de_fontes.py situacao ID
   --situacao transcrito --uso "<arquivo da base que recebeu o dado>"`.

`tarifas/fontes/REGISTRO.md` é gerado do registro e diz o que já chegou e o que falta
coletar, por prestador. `tests/unit/test_registro_de_fontes.py` recusa arquivo em
`tarifas/fontes` sem registro.

## Tarifas

- Categoria não residencial só entra com a tabela oficial do prestador (campo
  `categorias` do registro do município); nunca por multiplicador sobre a residencial.
- Cada transcrição cita documento e vigência e tem teste contra um valor impresso na
  própria tabela (ver `tests/unit/test_categorias_corsan.py`).

## Manual

- O manual em inglês (`manual/en`) acompanha o português seção a seção;
  `python manual/en/conferir.py` confere a estrutura.
- Os apêndices A, B e D e as tabelas `_tabelas` são gerados; não se editam à mão.
