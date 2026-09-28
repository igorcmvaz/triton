; Script de instalação do Netuno 5 para o Inno Setup 6
; Grupo de Pesquisa em Ambientes Sustentáveis (UFSC)
;
; Como gerar o instalador: veja docs/instalador.md. Em resumo,
;   python build_exe.py --installer
; compila o programa com o PyInstaller em dist\Netuno e chama o ISCC com a
; versão lida de netuno/__init__.py. Para compilar à mão:
;   ISCC /DMyAppVersion=5.0.1 setup_script.iss
;
; Base climática compilada (CLIMBra / SQLite): incorporada diretamente no executável
; sob data/climbra.db (~1,1 GB), garantindo execução instantânea e portabilidade.
; Se a pasta original de arquivos CSV soltos "climbra_data" (ou "Netuno future files for 652 cities")
; estiver AO LADO do instalador no momento da instalação, o componente opcional
; «Base climática nacional (CSV brutos)» pode copiá-la para a pasta do programa.

#define MyAppName "Netuno 5"
#ifndef MyAppVersion
  #define MyAppVersion "5.0.1"
#endif
#define MyAppPublisher "Grupo de Pesquisa em Ambientes Sustentáveis (UFSC)"
#define MyAppURL "https://sustainability.ufsc.br/"
#define MyAppExeName "Netuno.exe"
#define MyAppIcon "icons\netuno5.ico"
#define ClimateFolder "climbra_data"
#define ClimateFolderLegacy "Netuno future files for 652 cities"
#define ProgId "Netuno.Projeto"

[Setup]
; ID único: mantém atualizações sobre a mesma instalação
AppId={{D69F06B0-943D-4E4D-AAB2-350D616A06F5}
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
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
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
OutputBaseFilename=Netuno_Setup_{#StringChange(MyAppVersion, '.', '_')}
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
Name: "full"; Description: "Instalação completa (todos os idiomas e a base climática, se disponível)"
Name: "custom"; Description: "Instalação personalizada"; Flags: iscustom

[Components]
Name: "core"; Description: "Aplicativo Netuno, base climática nacional compilada (CLIMBra), manual, casos e exemplos"; Types: standard full custom; Flags: fixed
Name: "lang_es"; Description: "Pacote de idioma: Español"; Types: standard full custom
Name: "lang_zh"; Description: "Pacote de idioma: 中文（简体）"; Types: standard full custom
Name: "clima"; Description: "Arquivos CSV brutos da base climática (opcional, cerca de 6,5 GB; copiada da pasta ao lado do instalador, se existir)"; Types: full; ExtraDiskSpaceRequired: 6979321856

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "assocnetuno"; Description: "Abrir arquivos .netuno com o {#MyAppName}"; GroupDescription: "Associação de arquivos:"

[Files]
; Programa compilado pelo PyInstaller. Os pacotes de idioma opcionais saem
; daqui e entram pelos componentes abaixo.
Source: "dist\Netuno\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs; \
  Excludes: "simulation_outputs\*,\simulation_outputs,Dados.txt,\_internal\data\languages\es.json,\_internal\data\languages\zh.json,exemplos\netuno-cli-template.netuno,avisos_qt.log"
Source: "dist\Netuno\_internal\data\languages\es.json"; DestDir: "{app}\_internal\data\languages"; Components: lang_es; Flags: ignoreversion
Source: "dist\Netuno\_internal\data\languages\zh.json"; DestDir: "{app}\_internal\data\languages"; Components: lang_zh; Flags: ignoreversion

; Ícones para os atalhos e sistema
Source: "icons\*"; DestDir: "{app}\icons"; Flags: ignoreversion recursesubdirs createallsubdirs

; Base climática: copiada de fora do instalador, de {src}, e ignorada se ausente.
; O programa a procura ao lado do executável (netuno/core/climate_database.py).
Source: "{src}\{#ClimateFolder}\*"; DestDir: "{app}\{#ClimateFolder}"; Components: clima; \
  Flags: external recursesubdirs createallsubdirs skipifsourcedoesntexist ignoreversion
Source: "{src}\{#ClimateFolderLegacy}\*"; DestDir: "{app}\{#ClimateFolderLegacy}"; Components: clima; \
  Flags: external recursesubdirs createallsubdirs skipifsourcedoesntexist ignoreversion

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
; A pasta de trabalho é a do programa, onde ele também procura a base climática.
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; IconFilename: "{app}\icons\netuno5.ico"
Name: "{autoprograms}\Manual do {#MyAppName}"; Filename: "{app}\_internal\manual\Manual-Netuno-5.pdf"; Check: FileExists(ExpandConstant('{app}\_internal\manual\Manual-Netuno-5.pdf')); IconFilename: "{app}\icons\netuno5.ico"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; Tasks: desktopicon; IconFilename: "{app}\icons\netuno5.ico"

[Run]
Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Arquivos que o próprio programa cria na pasta de instalação
Type: files; Name: "{app}\avisos_qt.log"

[Code]
// Avisa, na página de componentes, quando a base climática não está ao lado do
// instalador: o componente seria marcado e nada seria copiado.
function BaseClimaticaDisponivel(): Boolean;
begin
  Result := DirExists(ExpandConstant('{src}\{#ClimateFolder}'));
end;

procedure CurPageChanged(CurPageID: Integer);
begin
  if (CurPageID = wpSelectComponents) and (not BaseClimaticaDisponivel()) then
    WizardForm.ComponentsList.ItemCaption[3] :=
      'Base climática nacional CLIMBra: não encontrada ao lado do instalador (será ignorada)';
end;
