# Sistema visual compartilhado — Triton Web e Desktop

A edição web é a referência oficial de identidade visual. O desktop reproduz a mesma hierarquia com componentes nativos PySide6; o núcleo científico permanece independente em `triton/core`.

## Tokens principais

- Fundo do aplicativo: `#f2f6f3`
- Superfície/cartão: `#ffffff`
- Verde profundo da navegação: `#063c36`
- Verde de ação: `#087f6b`
- Texto principal: `#17332c`
- Título editorial: `#133c32`
- Texto secundário: `#647b73`
- Borda: `#d7e3df`
- Fundo de campo: `#fcfefd`
- Raio de campo/botão: 9 px
- Raio de cartão: 16 px
- Tipografia de interface: Segoe UI
- Tipografia de títulos de etapa: Georgia

## Estrutura

1. Sidebar verde-escura com 278 px, marca no topo, 11 etapas em lista única e estado ativo com realce discreto.
2. Barra contextual branca com projeto atual, orientação curta e acesso à simulação.
3. Conteúdo sobre fundo verde muito claro, com margens internas amplas.
4. Título editorial da etapa seguido de descrição e cartões brancos.
5. Ação primária verde; ações secundárias brancas com borda.

## Regras de manutenção

- Novas telas desktop devem usar o QSS global de `triton/ui/theme.py` e evitar cores azuis locais.
- Cores de dados em gráficos podem usar azul, laranja ou roxo quando distinguem séries; cores de navegação e ação permanecem verdes.
- Não duplicar fórmulas ou contratos de dados para atender à apresentação.
- Comparar visualmente em 1280×720 e 1440×900, além da largura mínima suportada.
- Textos longos devem quebrar linha; tabelas e gráficos podem rolar, mas ações primárias devem permanecer visíveis.

## Relatórios e arquivos auditáveis

- O desktop é a implementação de referência para os relatórios oficiais.
- Desktop e web chamam `triton/core/report_service.py`; seletores e templates não devem ser duplicados nas interfaces.
- A pré-visualização desktop mostra o mesmo HTML oficial usado na exportação, e não um resumo textual paralelo.
- O nome do projeto integra os cabeçalhos dos laudos e é persistido no arquivo `.triton`.
- Projetos e artefatos exportados recebem nome legível do projeto, data/hora e hash estável da referência no nome do arquivo.
