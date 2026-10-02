; Script de instalação do Netuno 5 para o Inno Setup 6
; Grupo de Pesquisa em Ambientes Sustentáveis (UFSC)
;
; Como gerar o instalador: veja docs/instalador.md. Em resumo,
;   python build_exe.py --installer
; compila o programa com o PyInstaller em dist\Netuno e chama o ISCC com a
; versão lida de netuno/__init__.py. Para compilar à mão:
;   ISCC /DMyAppVersion=5.0.0 setup_script.iss                 (Edição Brasil)
;   ISCC /DMyAppVersion=5.0.0 /DEdition=INT setup_script.iss   (International Edition)
;
; As duas edições têm AppId, pasta, atalhos e associação próprios: instalam-se
; lado a lado. A Brasil empacota dist\Netuno; a Internacional, dist\Netuno_INT.
;
; Base climática CLIMBra: o banco compilado data/climbra.db (652 cidades, todos os
; modelos e cenários) vai embutido no programa, em _internal\data\climbra.db. Os CSV
; brutos de origem (~6,5 GB) não são oferecidos: o programa lê o banco, e eles só
; serviriam para recompilá-lo (scripts/compilar_base_climbra.py).

#ifndef Edition
  #define Edition "BRL"
#endif
#if Edition == "INT"
  #define MyAppName "Netuno 5 — International Edition"
  #define MyAppDir "Netuno 5 International"
  #define MyAppExeName "Netuno_INT.exe"
  #define DistDir "dist\Netuno_INT"
  #define ProgId "Netuno.Projeto.INT"
  #define AppGuid "{{7B1E4C2A-5D3F-4A8B-9C61-2E0F8D4A6B13}"
  #define SetupName "Netuno_INT_Setup_"
  #define CoreDesc "Netuno application (International Edition: no Brazilian data), manual, cases and examples"
  #define AssocFlags "; Flags: unchecked"
#else
  #define MyAppName "Netuno 5 — Edição Brasil"
  #define MyAppDir "Netuno 5"
  #define MyAppExeName "Netuno.exe"
  #define DistDir "dist\Netuno"
  #define ProgId "Netuno.Projeto"
  #define AppGuid "{{D69F06B0-943D-4E4D-AAB2-350D616A06F5}"
  #define SetupName "Netuno_Setup_"
  #define CoreDesc "Aplicativo Netuno, base climática nacional CLIMBra (652 cidades, embutida), manual, casos e exemplos"
  #define AssocFlags ""
#endif
#ifndef MyAppVersion
  #define MyAppVersion "5.0.0"
#endif
#define MyAppPublisher "Grupo de Pesquisa em Ambientes Sustentáveis (UFSC)"
#define MyAppURL "https://sustainability.ufsc.br/"
#define MyAppIcon "icons\netuno5.ico"

[Setup]
; ID único: mantém atualizações sobre a mesma instalação
AppId={#AppGuid}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
VersionInfoVersion={#MyAppVersion}
VersionInfoDescription=Instalador do {#MyAppName}
VersionInfoCompany={#MyAppPublisher}

; Pasta padrão: C:\Program Files\Netuno 5, ou a pasta do usuário quando a
; instalação é feita sem privilégio de administrador.
DefaultDirName={autopf}\{#MyAppDir}
DefaultGroupName={#MyAppDir}
DisableProgramGroupPage=yes
UninstallDisplayIcon={app}\icons\netuno5.ico
UninstallDisplayName={#MyAppName} {#MyAppVersion}
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog commandline
ChangesAssociations=yes
MinVersion=10.0

; 64 bits nativo
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

; Licença (GPL v3) e avisos antes e depois da instalação
LicenseFile=LICENSE
InfoBeforeFile=infos_licenses\info_before.txt
InfoAfterFile=infos_licenses\info_after.txt

; Compilação e aparência
OutputDir=dist
OutputBaseFilename={#SetupName}{#StringChange(MyAppVersion, '.', '_')}
SetupIconFile={#MyAppIcon}
SolidCompression=yes
Compression=lzma2/ultra64
WizardStyle=modern dynamic windows11

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Types]
Name: "standard"; Description: "Instalação padrão (todos os idiomas)"
Name: "custom"; Description: "Instalação personalizada"; Flags: iscustom

[Components]
Name: "core"; Description: "{#CoreDesc}"; Types: standard custom; Flags: fixed
Name: "lang_es"; Description: "Pacote de idioma: Español"; Types: standard custom
Name: "lang_zh"; Description: "Pacote de idioma: 中文（简体）"; Types: standard custom

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
; Na Internacional, a associação vem desmarcada para não tomar os .netuno da Brasil.
Name: "assocnetuno"; Description: "Abrir arquivos .netuno com o {#MyAppName}"; GroupDescription: "Associação de arquivos:"{#AssocFlags}

[Files]
; Programa compilado pelo PyInstaller. Os pacotes de idioma opcionais saem
; daqui e entram pelos componentes abaixo.
Source: "{#DistDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs; \
  Excludes: "simulation_outputs\*,\simulation_outputs,Dados.txt,\_internal\data\languages\es.json,\_internal\data\languages\zh.json,exemplos\netuno-cli-template.netuno,avisos_qt.log"
Source: "{#DistDir}\_internal\data\languages\es.json"; DestDir: "{app}\_internal\data\languages"; Components: lang_es; Flags: ignoreversion
Source: "{#DistDir}\_internal\data\languages\zh.json"; DestDir: "{app}\_internal\data\languages"; Components: lang_zh; Flags: ignoreversion

; A licença acompanha o programa instalado, e não só a página do instalador: a GPL
; pede que quem recebe o executável receba também o texto dela. Licence.txt traz o
; aviso de copyright do Netuno seguido do texto integral da GPL v3.
Source: "Licence.txt"; DestDir: "{app}"; DestName: "LICENSE.txt"; Flags: ignoreversion
; Licenças do Python, do Qt (LGPL) e das bibliotecas empacotadas, geradas no build.
Source: "infos_licenses\AVISOS_DE_TERCEIROS.txt"; DestDir: "{app}"; Flags: ignoreversion

; Ícones para os atalhos e sistema
Source: "icons\*"; DestDir: "{app}\icons"; Flags: ignoreversion recursesubdirs createallsubdirs

[Registry]
; Associação dos arquivos .netuno. HKA grava em HKLM numa instalação para todos
; os usuários e em HKCU numa instalação só para o usuário atual.
Root: HKA; Subkey: "Software\Classes\.netuno"; ValueType: string; ValueName: ""; ValueData: "{#ProgId}"; Flags: uninsdeletevalue; Tasks: assocnetuno
Root: HKA; Subkey: "Software\Classes\.netuno\OpenWithProgids"; ValueType: string; ValueName: "{#ProgId}"; ValueData: ""; Flags: uninsdeletevalue; Tasks: assocnetuno
Root: HKA; Subkey: "Software\Classes\{#ProgId}"; ValueType: string; ValueName: ""; ValueData: "Projeto do Netuno"; Flags: uninsdeletekey; Tasks: assocnetuno
Root: HKA; Subkey: "Software\Classes\{#ProgId}\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\icons\netuno5.ico,0"; Tasks: assocnetuno
Root: HKA; Subkey: "Software\Classes\{#ProgId}\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""; Tasks: assocnetuno
Root: HKA; Subkey: "Software\Classes\Applications\{#MyAppExeName}\SupportedTypes"; ValueType: string; ValueName: ".netuno"; ValueData: ""; Tasks: assocnetuno

[Icons]
; A pasta de trabalho é a do programa.
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; IconFilename: "{app}\icons\netuno5.ico"
Name: "{autoprograms}\Manual do {#MyAppName}"; Filename: "{app}\_internal\manual\Manual-Netuno-5.pdf"; Check: FileExists(ExpandConstant('{app}\_internal\manual\Manual-Netuno-5.pdf')); IconFilename: "{app}\icons\netuno5.ico"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; Tasks: desktopicon; IconFilename: "{app}\icons\netuno5.ico"

[Run]
Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Arquivos que o próprio programa cria na pasta de instalação
Type: files; Name: "{app}\avisos_qt.log"
