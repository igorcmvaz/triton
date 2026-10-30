; Script de instalação do Triton para o Inno Setup 6
; Grupo de Pesquisa em Ambientes Sustentáveis (UFSC)
;
; Como gerar o instalador: veja docs/instalador.md. Em resumo,
;   python build_exe.py --installer
; compila o programa com o PyInstaller em dist\Triton e chama o ISCC com a
; versão lida de triton/__init__.py. Para compilar à mão:
;   ISCC /DMyAppVersion=0.1.0 setup_script.iss                 (Edição Brasil)
;   ISCC /DMyAppVersion=0.1.0 /DEdition=INT setup_script.iss   (International Edition)
;   ISCC /DMyAppVersion=0.1.0 /DEdition=IBE setup_script.iss   (Edição Ibérica, IBE)
;
; As três edições têm AppId, pasta, atalhos e associação próprios: instalam-se
; lado a lado. A Brasil empacota dist\Triton; a Internacional, dist\Triton_INT; a
; Portugal, dist\Triton_IBE.
;
; Bases climáticas embutidas (só nas edições a que pertencem):
;  - Brasil: a base CLIMBra compilada, um banco por modelo CMIP6 (data\climbra_<modelo>.db,
;    19 arquivos, 652 cidades, todos os cenários), em _internal\data. O climbra.db único das
;    versões antigas não vai (seria o mesmo conteúdo em dobro). Os CSV brutos de origem
;    (~6,5 GB) não são oferecidos: o programa lê os bancos, e os CSV só servem para
;    recompilá-los (scripts/compilar_base_climbra.py).
;  - Portugal: a base E-OBS por concelho (data\portugal_eobs.db).
; Os bancos de documentos de terceiros (tarifas_fontes.db e semelhantes) não vão em nenhuma edição.

#define MyAppUserModelID "ufsc.ges.triton.ibe.0.1"
#ifndef Edition
  #define Edition "BRL"
#endif
#if Edition == "INT"
  #define MyAppName "Triton INT"
  #define MyAppDir "Triton International"
  #define MyAppExeName "Triton_INT.exe"
  #define DistDir "dist\Triton_INT"
  #define ProgId "Triton.Projeto.INT"
  #define AppGuid "{{FF7732C7-6FDB-50ED-A3C7-DEDB4BD0364E}"
  #define SetupName "Triton_INT_Setup_"
  #define CoreDesc "Triton application (International Edition: no Brazilian data), manual, cases and examples"
  #define AssocFlags "; Flags: unchecked"
  #define ExcluirBases "*\climbra.db,*\climbra_*.db,*\climbra_partes.json,*\portugal_eobs.db"
  #define ExcluirIcones "CLIMBra.*"
  #define ManualPdf "_internal\manual\en\Triton-User-Manual.pdf"
  #define ManualLink "Triton User Manual"
#elif Edition == "IBE"
  #define MyAppName "Triton IBE"
  #define MyAppDir "Triton IBE"
  #define MyAppExeName "Triton_IBE.exe"
  #define DistDir "dist\Triton_IBE"
  #define ProgId "Triton.Projeto.IBE"
  #define AppGuid "{{D8490C72-38B2-5531-8669-4234542A0979}"
  #define SetupName "Triton_IBE_Setup_"
  #define CoreDesc "Aplicação Triton (Edição Ibérica: português de Portugal, valores em euros), manual, casos e exemplos"
  #define AssocFlags "; Flags: unchecked"
  #define ExcluirBases "*\climbra.db,*\climbra_*.db,*\climbra_partes.json"
  #define ExcluirIcones "CLIMBra.*"
  #define ManualPdf "_internal\manual\Manual-Triton.pdf"
  #define ManualLink "Manual do Triton"
#else
  #define MyAppName "Triton BRL"
  #define MyAppDir "Triton"
  #define MyAppExeName "Triton.exe"
  #define DistDir "dist\Triton"
  #define ProgId "Triton.Projeto"
  #define AppGuid "{{C0A59FB1-586B-5908-90B3-D89CC602E76B}"
  #define SetupName "Triton_Setup_"
  #define CoreDesc "Aplicativo Triton, base climática nacional CLIMBra (652 cidades, embutida), manual, casos e exemplos"
  #define AssocFlags ""
  #define ExcluirBases "*\climbra.db,*\portugal_eobs.db"
  #define ExcluirIcones ""
  #define ManualPdf "_internal\manual\Manual-Triton.pdf"
  #define ManualLink "Manual do Triton"
#endif
#ifndef MyAppVersion
  #define MyAppVersion "0.1.0"
#endif
#define MyAppPublisher "Grupo de Pesquisa em Ambientes Sustentáveis (UFSC)"
#define MyAppURL "https://sustainability.ufsc.br/"
#define MyAppIcon "icons\triton.ico"

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

; Pasta padrão: C:\Program Files\Triton, ou a pasta do usuário quando a
; instalação é feita sem privilégio de administrador.
DefaultDirName={autopf}\{#MyAppDir}
DefaultGroupName={#MyAppDir}
DisableProgramGroupPage=yes
UninstallDisplayIcon={app}\icons\triton.ico
UninstallDisplayName={#MyAppName} {#MyAppVersion}
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog commandline
ChangesAssociations=yes
MinVersion=10.0

; 64 bits nativo
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

; Licença (código-fonte acadêmico) e avisos antes e depois da instalação
LicenseFile=LICENSE.md
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
; Na Internacional, a associação vem desmarcada para não tomar os .triton da Brasil.
Name: "assoctriton"; Description: "Abrir arquivos .triton com o {#MyAppName}"; GroupDescription: "Associação de arquivos:"{#AssocFlags}

[Files]
; Programa compilado pelo PyInstaller. Os pacotes de idioma opcionais saem
; daqui e entram pelos componentes abaixo.
Source: "{#DistDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs; \
  Excludes: "simulation_outputs\*,\simulation_outputs,Dados.txt,\_internal\data\languages\es.json,\_internal\data\languages\zh.json,exemplos\triton-cli-template.triton,avisos_qt.log,*TARIFAS-DE-AGUA-E-ESGOTO*,brazilSHP\*,*\brazilSHP\*,manual\site\pdf\*,*\manual\site\pdf\*,tarifas\fontes\*,*\tarifas\fontes\*,tarifas\entrada\*,*\tarifas\entrada\*,*\tarifas_fontes.db,*\tarifas_portugal_fontes.db,{#ExcluirBases}"

Source: "{#DistDir}\_internal\data\languages\es.json"; DestDir: "{app}\_internal\data\languages"; Components: lang_es; Flags: ignoreversion
Source: "{#DistDir}\_internal\data\languages\zh.json"; DestDir: "{app}\_internal\data\languages"; Components: lang_zh; Flags: ignoreversion

; A licença acompanha o programa instalado, e não só a página do instalador.
Source: "LICENSE.md"; DestDir: "{app}"; Flags: ignoreversion
; Licenças do Python, do Qt (LGPL) e das bibliotecas empacotadas, geradas no build.
Source: "infos_licenses\AVISOS_DE_TERCEIROS.txt"; DestDir: "{app}"; Flags: ignoreversion

; Ícones para os atalhos e sistema
; O logotipo da CLIMBra acompanha só a Edição Brasil, que traz a base.
Source: "icons\*"; DestDir: "{app}\icons"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: "{#ExcluirIcones}"

[Registry]
; Associação dos arquivos .triton. HKA grava em HKLM numa instalação para todos
; os usuários e em HKCU numa instalação só para o usuário atual.
Root: HKA; Subkey: "Software\Classes\.triton"; ValueType: string; ValueName: ""; ValueData: "{#ProgId}"; Flags: uninsdeletevalue; Tasks: assoctriton
Root: HKA; Subkey: "Software\Classes\.triton\OpenWithProgids"; ValueType: string; ValueName: "{#ProgId}"; ValueData: ""; Flags: uninsdeletevalue; Tasks: assoctriton
Root: HKA; Subkey: "Software\Classes\{#ProgId}"; ValueType: string; ValueName: ""; ValueData: "Projeto do Triton"; Flags: uninsdeletekey; Tasks: assoctriton
Root: HKA; Subkey: "Software\Classes\{#ProgId}\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\icons\triton.ico,0"; Tasks: assoctriton
Root: HKA; Subkey: "Software\Classes\{#ProgId}\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""; Tasks: assoctriton
Root: HKA; Subkey: "Software\Classes\Applications\{#MyAppExeName}\SupportedTypes"; ValueType: string; ValueName: ".triton"; ValueData: ""; Tasks: assoctriton

[Icons]
; A pasta de trabalho é a do programa.
Name: "{autoprograms}\{#MyAppName} {#MyAppVersion}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; AppUserModelID: "{#MyAppUserModelID}"; IconFilename: "{app}\icons\triton.ico"
Name: "{autoprograms}\{#ManualLink}"; Filename: "{app}\{#ManualPdf}"; Check: FileExists(ExpandConstant('{app}\{#ManualPdf}')); IconFilename: "{app}\icons\triton.ico"
Name: "{autodesktop}\{#MyAppName} {#MyAppVersion}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; AppUserModelID: "{#MyAppUserModelID}"; Tasks: desktopicon; IconFilename: "{app}\icons\triton.ico"

[Run]
Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[InstallDelete]
; Atalhos com os nomes antigos desta edição (agora «Triton <ED> <versão>»)
Type: files; Name: "{autoprograms}\Triton IBE — Edição Ibérica.lnk"
Type: files; Name: "{autodesktop}\Triton IBE — Edição Ibérica.lnk"
Type: files; Name: "{autoprograms}\Triton IBE - Edição Ibérica.lnk"
Type: files; Name: "{autodesktop}\Triton IBE - Edição Ibérica.lnk"
Type: files; Name: "{autoprograms}\Triton — Edição Portugal.lnk"
Type: files; Name: "{autodesktop}\Triton — Edição Portugal.lnk"
Type: files; Name: "{autoprograms}\Triton - Edição Portugal.lnk"
Type: files; Name: "{autodesktop}\Triton - Edição Portugal.lnk"

[UninstallDelete]
; Arquivos que o próprio programa cria na pasta de instalação
Type: files; Name: "{app}\avisos_qt.log"
