# Site de documentação técnica (mkdocs)

Ferramenta **só de desenvolvimento**: nada disto entra no instalador, em `requirements.txt`, em `Triton.spec` ou em
`build_exe.py`. Não há deploy nem GitHub Pages; o site é gerado e visto na própria máquina.

## Instalar

Da raiz do monorepo:

```
pip install -r requirements-docs.txt
```

O arquivo fixa `mkdocs-material==9.8.0` e `mkdocs<2`. O autor do tema declarou que só publica correções críticas até
05/05/2027, por isso o site é descartável: se a ferramenta parar de funcionar, o conteúdo continua em arquivos `.md`
legíveis sem ela. Os mesmos pacotes estão no extra `docs` de cada edição (`pip install -e "triton_int[docs]"`).

## Ver e gerar

```
mkdocs serve          # servidor local em http://127.0.0.1:8000, recarrega ao salvar
mkdocs build          # gera a pasta site/ (ignorada pelo Git)
mkdocs build --strict # trata os avisos como erro
```

Rode sempre da raiz do monorepo, onde está o `mkdocs.yml`. O `--strict` pode falhar enquanto houver links relativos
dos documentos das edições que apontam para fora do site (README, código-fonte): no `mkdocs.yml` eles estão
configurados como informação, mas confira a saída antes de usar o modo estrito num fluxo automatizado.

## Como o conteúdo entra

- `docs/` da raiz é o `docs_dir`: contém `index.md`, este texto e o [grafo de dependências](grafo_de_dependencias.md).
- Os documentos técnicos de `triton_int/` ficam onde estão (são os que o instalador leva). O gancho
  `scripts/mkdocs_hooks.py` os acrescenta ao site sem copiá-los, conforme `extra.docs_externos` do `mkdocs.yml`.
- A navegação (`nav`) é enxuta de propósito. Para incluir outro documento, declare-o em `extra.docs_externos` (se
  estiver fora de `docs/`) e acrescente-o ao `nav`.
- Mermaid e MathJax estão habilitados (`pymdownx.superfences` e `pymdownx.arithmatex`). O MathJax é carregado de um
  CDN, então as equações só aparecem com rede.

## Teste que não precisa do mkdocs

`tests/unit/test_docs_mkdocs.py` valida o `mkdocs.yml` como YAML e confere que todo arquivo do `nav` existe em
`docs/` ou é um original declarado em `extra.docs_externos`, sem importar o pacote `mkdocs`.
