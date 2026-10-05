; Inno Setup Installation Script for Mass Certificate Generator
; Compatible with Inno Setup 6.x
; Configured for Windows 10 / 11 64-bit modern installer

#define MyAppName "Mass Certificate Generator"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Kazi Rifat Morshed"
#define MyAppURL "https://kazirifatmorshed.github.io/projects/MassCertificateGenerator.html"
#define MyAppExeName "MassCertificateGenerator.exe"

[Setup]
; Unique application GUID
AppId={{5E4B226D-7F9C-4E1B-9A31-D42CF8B05271}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} v{#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes

; 64-bit Windows architecture configuration
ArchitecturesInstallIn64BitMode=x64compatible
ArchitecturesAllowed=x64compatible

; Installer Output
OutputDir=dist\installer
OutputBaseFilename=MassCertificateGenerator-Setup-v{#MyAppVersion}
SetupIconFile=extra\MCG_logo.ico
UninstallDisplayIcon={app}\{#MyAppExeName}

; Compression settings
Compression=lzma2/ultra64
SolidCompression=yes

; Modern Windows UI style
WizardStyle=modern

; Flexible privilege handling: installs for current user or all users if elevated
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Standalone single-file executable (or folder contents if building onedir)
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "extra\MCG_logo.ico"; DestDir: "{app}\extra"; Flags: ignoreversion
Source: "extra\MCG_logo.png"; DestDir: "{app}\extra"; Flags: ignoreversion

; Sample templates and resources
Source: "input\template\*"; DestDir: "{app}\samples\template"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "input\data\*"; DestDir: "{app}\samples\data"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "input\fonts\*"; DestDir: "{app}\samples\fonts"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\extra\MCG_logo.ico"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\extra\MCG_logo.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
