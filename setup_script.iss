; Script de Instalação do Netuno 5 com Inno Setup
; Grupo de Pesquisa Gestão Espaço Sustentável (UFSC)

#define MyAppName "Netuno 5"
#define MyAppVersion "5.0.8"
#define MyAppPublisher "Grupo de Pesquisa Gestão Espaço Sustentável (UFSC)"
#define MyAppURL "https://sustainability.ufsc.br/"
#define MyAppExeName "Netuno.exe"
#define MyAppIcon "icons\icon.ico"

[Setup]
; ID Único para evitar conflito com versões anteriores do Netuno
AppId={{D69F06B0-943D-4E4D-AAB2-350D616A06F5}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

; Diretório Padrão de Instalação: C:\Program Files\Netuno 5
DefaultDirName={autopf}\{#MyAppName}
UninstallDisplayIcon={app}\{#MyAppExeName}

; Configurações de Arquitetura (64-bit nativo)
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
DisableProgramGroupPage=yes

; Arquivos de Licença e Avisos Pré/Pós Instalação
LicenseFile=infos_licenses\license.txt
InfoBeforeFile=infos_licenses\info_before.txt
InfoAfterFile=infos_licenses\info_after.txt

; Configurações de Compilação e Visual
OutputDir=dist
OutputBaseFilename=Netuno_Setup_5_0_8
SetupIconFile={#MyAppIcon}
SolidCompression=yes
Compression=lzma2/ultra64
WizardStyle=modern dynamic windows11

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"
Name: "english"; MessagesFile: "compiler:Languages\English.isl"
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Types]
Name: "standard"; Description: "Instalação padrão (Português e English)"
Name: "custom"; Description: "Instalação personalizada"

[Components]
Name: "core"; Description: "Aplicativo Netuno + Português e English"; Types: standard custom; Flags: fixed
Name: "lang_es"; Description: "Pacote de idioma: Español"; Types: custom
Name: "lang_zh"; Description: "Pacote de idioma: 中文（简体）"; Types: custom

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Copia a pasta dist\Netuno ignorando saídas de simulação e arquivos temporários
Source: "dist\Netuno\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: "simulation_outputs\*,\simulation_outputs,Dados.txt,*es.json,*zh.json,exemplos\netuno-cli-template.netuno"
Source: "dist\Netuno\_internal\data\languages\es.json"; DestDir: "{app}\_internal\data\languages"; Components: lang_es; Flags: ignoreversion
Source: "dist\Netuno\_internal\data\languages\zh.json"; DestDir: "{app}\_internal\data\languages"; Components: lang_zh; Flags: ignoreversion

; Copia o ícone para o diretório da aplicação para vincular aos atalhos
Source: "icons\icon.ico"; DestDir: "{app}\icons"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\icons\icon.ico"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; IconFilename: "{app}\icons\icon.ico"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
