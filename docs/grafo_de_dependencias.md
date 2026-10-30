# Grafo de dependências entre módulos

Ferramenta só de desenvolvimento: o grafo mostra quem importa quem dentro do pacote `triton` de cada edição. Nada disto entra no instalador nem no `requirements.txt`.

## Como gerar

1. Instale o extra `grafo` (traz o `pydeps`): `pip install -e "triton_int[grafo]"` (ou `pip install pydeps`).
2. Para o SVG, instale também o **Graphviz** e confirme que o comando `dot` está no `PATH` (`dot -V`). Sem ele o script grava só o texto DOT e avisa.
3. Da raiz do monorepo:

```
python scripts/grafo_dependencias.py                                    # 3 edições, grafo de pacotes
python scripts/grafo_dependencias.py --edicao ibe                       # só a Ibérica
python scripts/grafo_dependencias.py --edicao int --modulo triton.core.estudo --modulo triton.cli
python scripts/grafo_dependencias.py --edicao int --show-dot            # só imprime o DOT
python scripts/grafo_dependencias.py --help
```

A saída vai para `docs/figuras/grafo_<edição>_pacotes.dot` (e `.svg`) e, por módulo, `grafo_<edição>_<módulo>.dot`. O texto DOT pode ser colado em qualquer visualizador de Graphviz.

## Como ler

- Uma seta `A -> B` quer dizer «B importa A» (a seta sai do módulo importado e chega a quem o usa; é a convenção do `pydeps`). A profundidade padrão é 2 (`triton.core`, `triton.ui`, `triton.cli`...); `--profundidade 3` abre mais.
- O `pydeps` lê **todos** os `import`, inclusive os escritos dentro de funções. Por isso o grafo de pacotes mostra `ui` e `cli` ligados ao `core` nos dois sentidos: o sentido `ui -> core` (o núcleo importa a interface) vem de importações tardias (para não carregar o Qt antes da hora). O isolamento dos **imports de topo** do núcleo continua garantido por `tests/unit/test_architecture_audit.py`, e os imports internos de função são declarados ao empacotador (`tests/unit/test_empacotamento.py`).
- O núcleo `triton/` é idêntico nas três edições; os grafos só diferem pelos módulos próprios de uma edição (por exemplo `triton.core.base_climatica_iberica` e `tarifarios_espanha` na Ibérica).

## Limitações

- Sem Graphviz não há SVG. O script não instala nada.
- Importações dinâmicas (`importlib.import_module`, como as de `triton.core._opcional`) não aparecem.
- Os arquivos gerados em `docs/figuras/` são descartáveis; regenere-os quando o código mudar.
