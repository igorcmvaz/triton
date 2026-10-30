# Estudos de caso de Santa Catarina (JSON `triton-estudo`)

Seis estudos, um por tipologia, com a mesma estrutura: arquétipo de edificação em `padroes`, tarifas do catálogo do programa e `expansao` município × modelo × recorte da CLIMBra. Gerados por `scripts/gerar_estudos_sc.py` a partir de `_fontes/`.

| Estudo | Pasta | Municípios | Casos (× 19 modelos × 7 recortes) |
| --- | --- | ---: | ---: |
| escolar | `escolar` | 32 | 4256 |
| comercial | `comercial` | 32 | 4256 |
| residencial-unifamiliar | `residencial-unifamiliar` | 32 | 4256 |
| residencial-multifamiliar | `residencial-multifamiliar` | 32 | 4256 |
| hospitalar | `hospitalar` | 32 | 4256 |
| aeroportuario | `aeroportos` | 21 | 2793 |

Total: 24073 simulações.

## Municípios: 32 de 295 estão na CLIMBra

A CLIMBra do programa tem 652 cidades brasileiras; 32 são de Santa Catarina (nome conferido com o IBGE, código 42xxxxx, e UF = SC no catálogo de tarifas). Os nomes repetidos em outras UFs foram excluídos: Ipirá (BA), Irati (PR), Praia Grande (SP), São Carlos (SP). Os outros 263 municípios de SC não têm série na CLIMBra do programa (lista em `_fontes/municipios_sc_climbra.json`).

## Fontes (URL, data de acesso e SHA-256 em `_fontes/FONTES.json`)

- IBGE, API de localidades (municípios de SC).
- ANAC, dados abertos: Lista de Aeródromos Públicos e Voo Regular Ativo (VRA) 2025.
- CLIMBra (doi:10.1038/s41597-023-01956-z), tarifas e custos: os do programa.

## Decisão de clima

Modelos: os 19 da CLIMBra. Recortes: os sugeridos pelo programa (`RECORTES_SUGERIDOS`): histórico 1981–2010 (trinta anos, como os futuros) e futuros 2021–2050, 2041–2070 e 2071–2100 em SSP2-4.5 e SSP5-8.5. A CLIMBra não traz série observada por município (o histórico é simulado). Alternativa: trocar `expansao.modelos` por um modelo (o padrão do programa é INM-CM4) e/ou `recortes` pelos recortes de série completa.

## Custo da varredura completa (medido em 29/10/2026, 1 processo, com outra suíte rodando na máquina)

| Estudo | Simulações | s por simulação | Tempo estimado (1 processo) | Disco estimado |
| --- | ---: | ---: | ---: | ---: |
| escolar | 4256 | 0.043 | 4 min | 58 MB |
| comercial | 4256 | 0.028 | 2 min | 58 MB |
| residencial-unifamiliar | 4256 | 0.112 | 8 min | 58 MB |
| residencial-multifamiliar | 4256 | 0.137 | 10 min | 58 MB |
| hospitalar | 4256 | 0.142 | 11 min | 58 MB |
| aeroportos | 2793 | 0.166 | 8 min | 38 MB |

Total: 21812 simulações, cerca de 35 a 40 min com 1 processo (`--paralelo 4` deve cortar para um quarto a um terço; não medido) e cerca de 0,3 GB (com `gravar_analise: false`; cada caso grava só o `resultado.json`). O tempo vem de 39 casos espaçados de cada estudo, com o primeiro descartado (aquecimento); inclui a montagem do caso, não a gravação.

Para rodar tudo (um estudo por vez, retomável), na pasta `triton_brl`:

```powershell
foreach ($e in 'escolar','comercial','residencial-unifamiliar','residencial-multifamiliar','hospitalar','aeroportos') {
  python -m triton.cli estudo run estudos/santa-catarina/$e/estudo.json --saida estudos/santa-catarina/_saida/$e --paralelo 4 --retomar
}
```
