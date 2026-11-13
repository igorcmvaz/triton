# Roadmap do Triton

O que vem depois da versão 0.2.0 (beta). Vale para as três edições (Brasil, Internacional e Ibérica), que compartilham o
mesmo motor e a mesma numeração de versões. Cada item é uma entrega pontual; não há datas, e a ordem dentro de cada parte
é a de prioridade.

## Parte 1 — Plataformas e distribuição

Hoje o Triton tem instalador só para Windows (PyInstaller + Inno Setup). Pelo código-fonte, já roda em Linux e macOS com
Python e Qt (ver `infos_licenses/README.md`).

| # | Entrega | O que muda para quem usa |
| :-- | :-- | :-- |
| 1.1 | **Linux: AppImage x86-64** das três edições, gerado em Ubuntu LTS | instala sem Python, em qualquer distribuição recente |
| 1.2 | **macOS: aplicativo `.dmg`** para Apple Silicon e Intel, assinado e notarizado pela Apple | abre sem o aviso de «desenvolvedor não identificado» |
| 1.3 | **Windows: instalador assinado** (certificado de assinatura de código) | some o alerta do SmartScreen na primeira execução |
| 1.4 | **Instalador menor na Edição Brasil**: a base CLIMBra (19 modelos, ~784 MB) baixada sob demanda, por modelo, com conferência de SHA-256 | o instalador cai de 860 MB para menos de 100 MB |
| 1.5 | **Build automático no GitHub Actions** a cada tag: os instaladores de Windows, Linux e macOS, com o `SHA256SUMS.txt` | cada versão sai com os mesmos passos e os hashes publicados |
| 1.6 | **Pacote no PyPI** (`pip install triton-rwh`) com o motor e a linha de comando, sem interface gráfica | estudos em lote em servidor ou notebook, sem instalar o programa |
| 1.7 | **Imagem Docker** da linha de comando | estudos reprodutíveis em qualquer máquina, com a versão fixada |
| 1.8 | **Versão web de consulta** (manual, exemplos e resultados exportados), que abre no navegador do celular | iOS e Android pelo navegador; o Qt de desktop não roda em iOS |

## Parte 2 — A ferramenta

**Decisão multicritério**

| # | Entrega |
| :-- | :-- |
| 2.1 | Tolerância da faixa de escolha ajustável na interface (hoje fixa em 5% na interface; na linha de comando já é `--score-band`) |
| 2.2 | Refinamento automático da varredura dentro da faixa: com passo grosso, a faixa costuma ter um volume só |
| 2.3 | Condições C1 e C2 do VIKOR (vantagem e estabilidade aceitáveis), com o conjunto de compromisso quando falham |
| 2.4 | Pesos CRITIC também como centro do sorteio do SMAA |
| 2.5 | SMAA-PROMETHEE, para fechar o par estocástico dos três métodos |

**Simulação e dados**

| # | Entrega |
| :-- | :-- |
| 2.6 | Passo subdiário (horário) no balanço hídrico, com séries horárias onde houver |
| 2.7 | Nova rodada climática com o CMIP7, em parceria com a USP |
| 2.8 | Conferir na fonte as tarifas dos sete municípios da Espanha hoje marcados «não conferido» |
| 2.9 | Um país novo com dados, tarifas e idioma próprios, no modelo da Edição Ibérica |
| 2.10 | Outras soluções de drenagem sustentável (telhado verde, vala de infiltração, reservatório de retenção) no mesmo balanço |
| 2.11 | Mais casos analíticos de verificação do balanço hídrico, incluindo os de dois reservatórios |

**Resultados e relatórios**

| # | Entrega |
| :-- | :-- |
| 2.12 | Versão do programa e da base de dados registradas em toda saída JSON, CSV e HTML |
| 2.13 | Peso do sistema com limites por norma (NBR 6120 e Eurocódigo 1), além dos limiares de atenção do programa |
| 2.14 | Visualizador 3D mais leve, que abre em máquinas sem placa de vídeo dedicada |
| 2.15 | Laudos com a faixa de escolha e o gráfico de decisão da interface |
