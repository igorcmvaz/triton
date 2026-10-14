# Triton, International Edition (INT): versão 1.0.0

O Triton é o filho do Netuno: o mesmo motor de cálculo, com nome, logo, versionamento e repositório próprios.
Esta pasta é o programa da edição **Triton, International Edition (INT)**; as outras duas edições ficam em pastas e repositórios separados.
Foi gerada por `scripts/separar_edicoes.py` do repositório principal do Netuno (versão 5.0.1).
**Não edite o motor aqui**: corrija no principal e gere de novo, senão as três cópias divergem.

- Ponto de entrada: `main_int.py` (`python main_int.py`). Compilação: `python build_exe_int.py`.
- O pacote Python é `triton`; os projetos têm a extensão `.triton`.
- Arquivos: 908; tamanho antes da renomeação: 120 MB.
- Variável de ambiente da edição: `TRITON_EDITION`.

## O que ficou de fora desta edição

- `build_exe_brl.py`: ponto de entrada da edição BRL
- `build_exe_por.py`: ponto de entrada da edição PRT
- `data/brazilSHP`: só da Edição Brasil
- `data/climbra.db`: só da Edição Brasil
- `data/portugal_eobs.db`: só da Edição Portugal
- `main_brl.py`: ponto de entrada da edição BRL
- `main_por.py`: ponto de entrada da edição PRT
- `tarifas`: só da Edição Brasil
- `tarifas_portugal`: só da Edição Portugal
- as fontes brutas de Portugal (`data/portugal`), a pasta `tarifas/entrada`, `.git` (o repositório é novo), `build`, `dist` e caches

## O que ainda diz «Netuno», de propósito

O Netuno é o programa-pai. Continuam com o nome dele: «Netuno 1» a «Netuno 4» (o programa anterior, comparado no
manual e citado nos estudos), o importador do formato de arquivo do Netuno 4 (`netuno_csv`), os documentos de terceiros
(`tarifas/fontes`) e, nas listas de referências e na bibliografia do programa, o «Netuno» sem número, que cita estudos
que usaram o Netuno. Figuras e capturas de tela do manual que têm «Netuno» desenhado continuam como estão até serem refeitas.

## Logo e versionamento

O logo é o do Netuno com um globo terrestre «tatuado» no planeta (`scripts/gerar_logos_edicoes.py`). A numeração começa em
1.0.0 no lançamento oficial das três edições, e o histórico de versões começa do zero. O histórico do Netuno
(5.0.0 e 5.0.1) fica no Netuno.

Os arquivos `.netuno` do Netuno não abrem no Triton sem renomear a extensão para `.triton`.

Mapa completo das edições: `docs/edicoes.md`.
