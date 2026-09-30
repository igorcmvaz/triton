# Visualizador 3D da volumetria

Código-fonte do visualizador WebGL da volumetria (three.js). O Python monta a
cena (`netuno/core/volumetry.py`) e a entrega como JSON (`scene_payload`); este
visualizador desenha as peças detalhadas, com materiais físicos, céu HDRI,
sombras, corte por cota, medição, fluxo animado e ficha técnica.

O mesmo pacote serve:

* o HTML exportado (`write_html_viewer`), que leva o pacote, o céu e a cena
  num arquivo só, sem internet;
* a aba «Volumetria 3D» do programa (`netuno/ui/volumetry_web.py`, por
  QtWebEngine). Sem WebGL, a aba usa o visualizador em QPainter.

## Gerar o pacote

O pacote gerado é versionado em `netuno/data/volumetria/netuno_volumetria.js`,
de modo que compilar o programa não exige Node. Depois de mudar
`src/viewer.js`:

```
cd web/volumetria
npm ci
npm run build
```

O cabeçalho do pacote leva o SHA-256 do fonte; o teste
`tests/unit/test_volumetria_web.py` falha se o pacote não corresponder ao
fonte atual.

Licenças de terceiros: `netuno/data/volumetria/LICENCAS.md`.
