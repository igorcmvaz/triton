# LegadoWeb — versão web descontinuada

Arquivo histórico da tentativa de usar o **Chrome/Chromium como interface do Netuno**, em
paralelo à interface desktop nativa. Essa linha de desenvolvimento foi **descontinuada**.

**O Netuno 5 é exclusivamente desktop (PySide6/Qt).**

## Conteúdo

`netuno_web_legado.tar.xz` (compressão sólida LZMA2, preset 9 EXTREME) — 53 arquivos, 1,03 MB → 240 KB.

| Caminho no arquivo | Descrição |
| :--- | :--- |
| `netuno_web/backend/` | API REST FastAPI (rotas, serviços, exportação de relatórios) |
| `netuno_web/frontend/src/` | Interface React/TypeScript (Vite) |
| `netuno_web/frontend/dist/` | Build compilado do frontend (pronto para servir) |
| `netuno_web/worker/` | Processamento de simulações em segundo plano |
| `netuno_web/docker/`, `docker-compose.yml` | Orquestração de contêineres |
| `netuno_web/tests/` | Testes da API |
| `netuno/ui/web_window.py` | Janela desktop que embutia a interface web via QtWebEngine |

## O que foi deixado de fora (descartável, regenerável)

- `frontend/node_modules/` — 152 MB; recuperável com `pnpm install` a partir do `pnpm-lock.yaml` incluído.
- `.runtime/` — resultados de execuções locais de teste.
- `__pycache__/`, `*.tsbuildinfo` — caches de compilação.

## Como restaurar

```bash
tar -xJf netuno_web_legado.tar.xz
```

Para voltar a executar o frontend seria necessário `pnpm install` dentro de `netuno_web/frontend/`
e reinstalar as dependências `fastapi` e `uvicorn`, removidas do projeto desktop.

## Alterações feitas no programa desktop ao arquivar

- `pyproject.toml` — `netuno_web` removido da lista de pacotes; `fastapi` e `uvicorn` removidos das dependências.
- `requirements.txt` — `fastapi` e `uvicorn` removidos.
- `tests/unit/test_report_service.py` — removido o teste de paridade entre relatório web e desktop
  (`test_web_uses_the_same_official_report_contract`); os testes do contrato desktop foram mantidos.
- `README.md` — seção de execução web removida da documentação principal.
- `netuno/ui/web_window.py` — removido do pacote (estava órfão: nenhum módulo o importava).
- `.gitignore` — entradas de `netuno_web/` removidas.
- `.dockerignore` — excluído: toda a stack Docker pertencia à versão web e nenhum Dockerfile restou.

Após o arquivamento a suíte completa de testes passa (236 testes, 1 skip).
