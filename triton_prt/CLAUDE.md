# Instruções para quem trabalha neste repositório

## Material recebido do usuário (PDFs, planilhas, páginas salvas)

O usuário solta o material em `tarifas/entrada/`, com qualquer nome. A entrada fica só
com o que ainda não foi processado.

1. `python tarifas/processar_entrada.py` — identifica o prestador pelo nome do arquivo
   (regras em `REGRAS`, nome do prestador ou do município) ou, em último caso, pelo
   município mais citado no conteúdo, e registra pela impressão digital SHA-256 e **move** o arquivo para
   `tarifas/fontes/<prestador>/`; arquivo já registrado só sai da entrada. O que não for
   identificado vai para `entrada/_a_identificar/`. **Confira o conteúdo** antes de
   transcrever: o nome do arquivo engana (já houve tabela da CAESB registrada como SAAE
   Jaboticabal). Prestador errado: `python tarifas/registro_de_fontes.py reatribuir ID
   --prestador ...`.
2. Registro avulso: `python tarifas/registro_de_fontes.py conferir ARQUIVO` e
   `registrar ARQUIVO --prestador ... --conteudo ... [--vigencia ...]`. Material licenciado
   ou de terceiros que não se redistribui leva `--nao-guardar --motivo "..."`.
3. Transcrição: um `tarifas/transcricoes/<prestador>.json` por documento (formato no
   docstring de `tarifas/aplicar_transcricoes.py`), com a lista de municípios de cada
   tabela e, em `conferencia`, contas calculadas com números impressos no documento. Só
   entra município que o documento cobre. **Documento geral** (sem lista de municípios):
   vale para todos os municípios do prestador só quando o próprio documento se declara a
   tabela única dele («municípios atendidos pela Cosanpa», uma só TRA da concessão) ou dá
   a regra de enquadramento (lista de localidades A/B); a tabela leva a lista explícita
   e, em `abrangencia`, a regra. Prestador com tabelas regionais sem o mapa município →
   região: documenta só o município nomeado (nunca estender por semelhança). Documento que desmente a base sem trazer a tabela vira
   `"situacao": "ruim"` com `motivo`. Documento consultado sem dado útil:
   `registro_de_fontes.py situacao ID --situacao consultado --uso "consultado: <por quê>"`.
4. Leia o documento **inteiro** antes de transcrever, inclusive as imagens salvas com a página
   (`*_files/`) e a última página: tabelas de outros municípios costumam vir no fim (o Bloco A
   da BRK Alagoas traz Marechal Deodoro na última página). `tarifas/auditar_cobertura.py`
   (`transcricoes/COBERTURA.md`) lista os municípios pendentes que algum documento já
   recebido cita; `tests/unit/test_transcricoes.py` exige que todo município transcrito seja
   nomeado no documento ou tenha a regra em `abrangencia`.
   Ao baixar material da web: só de fonte oficial; confira que o PDF começa com `%PDF` e
   que o HTML não é página de erro («Página não encontrada»); salve o endereço em
   `entrada/fontes.txt`. Página que só tem botão de formulário («Baixar arquivo») fica
   para o autor baixar pelo navegador.
5. `python tarifas/aplicar_transcricoes.py` (confere) e `--aplicar` (grava banco,
   `transcricoes/historico.json`, `ALTERACOES.md`, registro, `FILA.md` e a lista de coleta).

`tarifas/o_que_buscar.html` é a página de coleta do usuário (gerada por
`gerar_o_que_buscar.py`, junto com a lista de coleta). `tarifas/transcricoes/FILA.md` diz o que falta transcrever, o que foi consultado sem
render dado e o que está com vigência antiga. `tests/unit/test_registro_de_fontes.py`
recusa arquivo em `tarifas/fontes` sem registro; `tests/unit/test_transcricoes.py` exige
que o banco reproduza cada conta conferida.

## Tarifas

- `tests/unit/test_processo_tarifario.py` confere os elos registro ↔ arquivo ↔ transcrição ↔
  banco ↔ histórico; nada fica «recebido» sem destino, e «consultado» sempre diz por quê.
- Formas na transcrição: `fixo`/`franquia`/`piso`, `retroativa` (conta mínima com o volume
  todo pelas faixas acima dela), `exponencial` (PB × Cⁿ, CORSAN, COMUSA, DMAE POA),
  `direta` (todo o volume pelo preço da faixa: Americana, Valinhos, Lucas do Rio Verde),
  `fixo_por_faixa` (parcela fixa pela faixa do consumo total, CESAN),
  `representativa` + `variantes` (tarifa por bairro ou «Tarifa 1»). Tabela `situacao: ruim`
  leva `espera` (contas impressas) para não derrubar a transcrição que já as reproduz.
- Esgoto: procure-o também nas imagens e na fatura-modelo do prestador; sem serviço de
  esgoto cobrado (fonte oficial ou SINISA), o esgoto é 0%, com a fonte na nota.

- Categoria não residencial só entra com a tabela oficial do prestador (campo
  `categorias` do registro do município); nunca por multiplicador sobre a residencial.
- Cada transcrição cita documento e vigência e tem teste contra um valor impresso na
  própria tabela (`conferencia`, conferida por `tests/unit/test_transcricoes.py`).
- Município com `fonte_registro` só muda por nova transcrição; o atualizador automático
  não o sobrescreve.

## Edições Brasil (BRL) e International (INT)

- Dado brasileiro (tarifa, custo em reais, fator de emissão, clima CLIMBra, certificação
  nacional) só aparece depois de `usa_dados_do_brasil()`; na International o campo começa
  vazio ou zerado. O mapa está em `docs/edicoes.md` (e `docs/en/editions.md`):
  `tests/unit/test_edicoes_documentadas.py` exige que todo arquivo que pergunta pela
  edição esteja listado nele.
- No manual, o que é só da Brasil leva «> **Só na Edição Brasil (BRL).**» /
  «> **Brazil Edition (BRL) only.**», e o modo de seguir na International,
  «> **Na International Edition (INT).**» / «> **In the International Edition (INT).**»,
  nos mesmos lugares das duas línguas (`manual/en/conferir.py` confere).

## Manual

- O manual em inglês (`manual/en`) acompanha o português seção a seção;
  `python manual/en/conferir.py` confere a estrutura.
- Os apêndices A, B e D e as tabelas `_tabelas` são gerados; não se editam à mão.
