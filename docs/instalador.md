# Como gerar o instalador do Netuno 5

O instalador é gerado em duas etapas: o PyInstaller compila o programa na pasta
`dist\Netuno`, e o Inno Setup 6 empacota essa pasta em `dist\Netuno_Setup_<versão>.exe`.
O script `build_exe.py` faz as duas.

## Pré-requisitos

- Windows 10 ou 11, 64 bits.
- Python do ambiente de desenvolvimento, com as dependências do projeto e o PyInstaller.
- Inno Setup 6 (https://jrsoftware.org/isdl.php). O `build_exe.py` procura o `ISCC.exe`
  no `PATH` e em `C:\Program Files (x86)\Inno Setup 6`.

## Passo a passo

1. Confira a versão em `netuno/__init__.py` (`__version__`). É ela que vai para o nome
   do instalador, para a janela «Sobre» e para o registro do Windows.
2. Na raiz do projeto:

   ```
   python build_exe.py --clean --installer
   ```

   O comando regera o manual (tabelas, figuras e PDF), compila o programa e gera o
   instalador. Para pular a regeneração do manual, acrescente `--sem-manual`.
3. Antes de chamar o Inno Setup, o script confere se a compilação trouxe o executável,
   os pacotes de idioma e o PDF do manual, e interrompe com a lista do que falta.
4. O instalador sai em `dist\Netuno_Setup_5_0_0.exe` (para a versão 5.0.0).

Para compilar só o instalador, com `dist\Netuno` já pronto:

```
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" /DMyAppVersion=5.0.0 setup_script.iss
```

## O que o instalador faz

| Item | Comportamento |
| :--- | :--- |
| pasta | `C:\Program Files\Netuno 5`, ou a pasta do usuário se a instalação for feita sem administrador (o instalador pergunta) |
| licença | GPL v3, do arquivo `LICENSE` |
| idiomas do instalador | português, inglês e espanhol |
| componentes | programa, manual, casos e exemplos (obrigatório); pacotes de idioma espanhol e chinês; base climática |
| atalhos | Menu Iniciar (programa e manual em PDF); área de trabalho, opcional |
| arquivos `.netuno` | associados ao programa, opcional e marcado por padrão: o duplo clique abre o projeto |
| desinstalação | remove a pasta do programa e o `avisos_qt.log` que ele cria; os projetos do usuário ficam onde foram salvos |

## A base climática

A base CLIMBra ocupa cerca de 6,5 GB em 37.164 arquivos e **não vai dentro do
instalador**. Para distribuí-la junto:

1. Copie a pasta `climbra_data` (ou o nome legado `Netuno future files for 652 cities`) para o **mesmo diretório** do
   `Netuno_Setup_*.exe` (um pendrive, uma pasta de rede, um disco).
2. Na instalação, escolha «Instalação completa» ou marque o componente «Base climática
   nacional CLIMBra».

O instalador copia a pasta para dentro da pasta do programa, onde o Netuno a procura. Se
a pasta não estiver ao lado do instalador, o componente aparece como «não encontrada» e é
ignorado, e o programa funciona com séries próprias.

A base também pode ficar fora da pasta do programa: basta definir a variável de ambiente
`NETUNO_CLIMATE_DATA_DIR` com o caminho da pasta `climbra_data` (ou `Netuno future files for 652 cities`).

## Conferência depois de instalar

- O programa abre, e a janela «Sobre» mostra a versão correta.
- **Ajuda → Manual** abre o PDF.
- **Ajuda → Relatório de Verificação Técnica e Computacional** abre o relatório.
- Um duplo clique num `.netuno` de `casos` abre o projeto e reproduz o número do
  apêndice de arquivos de exemplo do manual.
- Com a base instalada, a etapa 1 lista as 652 cidades.
