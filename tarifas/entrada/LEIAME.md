# Caixa de entrada do material tarifário

Cole aqui as páginas e os documentos coletados, do jeito que vierem. Daqui eles não são
usados: cada arquivo é conferido e registrado por `tarifas/registro_de_fontes.py`
(impressão digital, data, prestador, conteúdo), vai para `tarifas/fontes/<prestador>/`
e só então é transcrito para a base. Arquivo já recebido é reconhecido mesmo com outro
nome, e não é transcrito de novo.

Para facilitar:

- **Uma pasta por prestador** (`sabesp/`, `copasa/`, `embasa/`...), ou o nome do
  prestador no início do arquivo.
- **HTML: salve a página completa** (no navegador, «Salvar como → Página da Web,
  completa»), para que as tabelas venham junto. Se a página só tiver um link para a
  resolução ou para a tabela em PDF, baixe o PDF também: ele é a fonte primária.
- **Anote a URL** de onde veio, num `fontes.txt` na mesma pasta, uma linha por arquivo:
  `arquivo.html  https://...`. A URL vai para o registro e para o apêndice D do manual.
- O que mais rende é a **resolução ou deliberação tarifária vigente** do prestador, com
  todas as categorias (residencial, social, comercial, industrial, pública).

O que falta coletar, por prestador, está em `tarifas/fontes/REGISTRO.md`.
