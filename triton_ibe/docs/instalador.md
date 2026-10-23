# Como gerar o instalador do Triton

O instalador é gerado em duas etapas: o PyInstaller compila o programa na pasta
`dist\Triton`, e o Inno Setup 6 empacota essa pasta em `dist\Triton_Setup_<versão>.exe`.
O script `build_exe.py` faz as duas. Isto vale para a Edição Brasil; a International
segue os mesmos passos com `build_exe.py`, dentro de `triton_int` (seção «A base climática» abaixo, e o mapa
das edições em [`edicoes.md`](edicoes.md)).

## Pré-requisitos

- Windows 10 ou 11, 64 bits.
- Python do ambiente de desenvolvimento, com as dependências do projeto e o PyInstaller.
- Inno Setup 6 (https://jrsoftware.org/isdl.php). O `build_exe.py` procura o `ISCC.exe`
  no `PATH` e em `C:\Program Files (x86)\Inno Setup 6`.

## Passo a passo

1. Confira a versão em `triton/__init__.py` (`__version__`). É ela que vai para o nome
   do instalador, para a janela «Sobre» e para o registro do Windows.
2. Na raiz do projeto:

   ```
   python build_exe.py --clean --installer
   ```

   O comando regera o manual (tabelas, figuras e PDF), compila o programa e gera o
   instalador. Para pular a regeneração do manual, acrescente `--sem-manual`.
3. Antes de chamar o Inno Setup, o script confere se a compilação trouxe o executável,
   os pacotes de idioma, o PDF do manual e a base CLIMBra (`_internal\data\climbra.db`), e interrompe com a lista do que falta.
4. O instalador sai em `dist\Triton_Setup_0_1_0.exe` (para a versão 0.1.0).

Para compilar só o instalador, com `dist\Triton` já pronto:

```
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" /DMyAppVersion=0.1.0 setup_script.iss
```

## O que o instalador faz

| Item | Comportamento |
| :--- | :--- |
| pasta | `C:\Program Files\Triton`, ou a pasta do usuário se a instalação for feita sem administrador (o instalador pergunta) |
| licença | o texto de `LICENSE.md` (código-fonte disponível para fins acadêmicos), na página de licença e instalado na pasta do programa, com as licenças de terceiros (`AVISOS_DE_TERCEIROS.txt`) |
| idiomas do instalador | português, inglês e espanhol |
| componentes | programa (na Edição Brasil, com a base CLIMBra compilada e a pasta `tarifas` sem a `entrada`), manual, casos e exemplos (obrigatório); pacotes de idioma espanhol e chinês |
| atalhos | Menu Iniciar (programa e manual em PDF); área de trabalho, opcional |
| arquivos `.triton` | associados ao programa, opcional e marcado por padrão: o duplo clique abre o projeto |
| desinstalação | remove a pasta do programa e o `avisos_qt.log` que ele cria; os projetos do usuário ficam onde foram salvos |

## A base climática

Cada edição tem o seu instalador, gerado pelo mesmo `setup_script.iss` com
`/DEdition=BRL` ou `/DEdition=INT`. O `python build_exe.py --installer`, dentro de `triton_int`, gera o
`Triton_INT_Setup_*.exe`, a partir de `dist\Triton_INT`. As duas edições têm AppId,
pasta (`Triton` e `Triton International`), atalhos e ProgId próprios, e por isso
instalam-se lado a lado. Na Internacional, a associação dos `.triton` vem desmarcada.

A Edição Brasil (`Triton.exe`) sai com a base CLIMBra
**embutida**: o banco compilado `data/climbra.db` (cerca de 784 MB, 652 cidades,
modelos e cenários CMIP6) entra no executável em `_internal\data\climbra.db`, e o
programa já abre com as cidades no seletor da Etapa 1. A Edição Internacional
(`--edition int`, em `dist\Triton_INT`) sai **sem** o banco, que cobre só cidades
brasileiras, e trabalha com séries de chuva próprias.

O banco fica fora do git, por isso cada máquina de compilação o gera uma vez:

```
python scripts/compilar_base_climbra.py --input climbra_data --output data/climbra.db
```

O `build_exe.py` confere isso antes de compilar a Edição Brasil. Se `data/climbra.db`
faltar e a pasta `climbra_data` (ou o nome legado `Triton future files for 652 cities`)
estiver na raiz, ele compila o banco; se nenhum dos dois existir, **interrompe** em vez
de gerar um instalador sem a base. A conferência anterior ao Inno Setup também exige
`dist\Triton\_internal\data\climbra.db`. A opção `--sem-base-climatica` compila um
pacote de teste sem a base e não gera instalador.

Os CSV brutos (cerca de 6,5 GB em 37.164 arquivos) não são distribuídos: o banco
contém todas as séries, e os CSV só servem para recompilá-lo. Por isso o instalador não
oferece o componente da base em CSV. Para desenvolvimento, a base pode ficar fora da
pasta do programa, com as variáveis de ambiente `TRITON_CLIMBRA_DB` (o banco) ou
`TRITON_CLIMATE_DATA_DIR` (a pasta de CSV, lida só quando não há banco).

Rodando do código-fonte sem a base, a Etapa 1 abre com a série de exemplo de
Florianópolis e avisa que a base não está instalada.

## O código que vai no pacote

Antes de compilar, o `build_exe.py` confere a pasta:

- **Pasta atrás do `origin/main`:** recusa compilar. Isso acontece quando um `git pull`
  é interrompido por alterações locais, e a pasta fica na versão anterior sem aviso.
  Rode `git stash` e `git pull` e compile de novo. A opção `--ignorar-git` passa por
  cima da conferência.
- **Commit compilado:** fica gravado no arquivo `revisao.json`, na pasta `triton/data` (criado pelo build e fora do git). O `--diagnostico`
  mostra esse commit, e avisa quando havia alterações locais não commitadas.
- **`.spec` do PyInstaller:** vai para `build/`, e não sobrescreve o `Triton.spec`
  versionado.
- **Arquivos regerados pelo build:** o manual, o site, o changelog e os avisos de
  terceiros voltam ao estado do commit depois do empacotamento. Assim o próximo
  `git pull` não para. Alterações suas, feitas antes do build, não são tocadas.

## Conferência depois de instalar

O `build_exe.py` roda o executável gerado com `--diagnostico` antes de declarar sucesso.
O diagnóstico confere:

- o visualizador 3D e o QtWebEngine;
- a geração do arranjo e da volumetria;
- a base CLIMBra;
- o banco tarifário, com a CORSAN na fórmula exponencial;
- o manual.

Um pacote sem o 3D ou com o banco tarifário antigo é recusado. Na Edição Brasil, a
falta da base também reprova o pacote, salvo com `--sem-base-climatica`. Na máquina
instalada, `Triton.exe --diagnostico` mostra o mesmo relatório e o grava em
`%TEMP%\triton_diagnostico.txt`.

- O programa abre, e a janela «Sobre» mostra a versão correta.
- **Ajuda → Manual** abre o PDF.
- **Ajuda → Relatório de Verificação Técnica e Computacional** abre o relatório.
- Um duplo clique num `.triton` de `casos` abre o projeto e reproduz o número do
  apêndice de arquivos de exemplo do manual.
- Com a base instalada, a etapa 1 lista as 652 cidades.
