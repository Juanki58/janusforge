# Crea acceso directo en el Escritorio: "Janusforge Visor"
# Apunta a lanzar_visor.bat en la raíz del repo.

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Resolve-Path (Join-Path $ScriptDir "..")).Path
$BatPath = Join-Path $RepoRoot "lanzar_visor.bat"

if (-not (Test-Path -LiteralPath $BatPath)) {
    Write-Error "No se encuentra lanzar_visor.bat en: $BatPath"
    exit 1
}

$Desktop = [Environment]::GetFolderPath("Desktop")
if (-not $Desktop -or -not (Test-Path -LiteralPath $Desktop)) {
    $Desktop = Join-Path $env:USERPROFILE "Desktop"
}
$ShortcutPath = Join-Path $Desktop "Janusforge Visor.lnk"

$Wsh = New-Object -ComObject WScript.Shell
$Sc = $Wsh.CreateShortcut($ShortcutPath)
$Sc.TargetPath = $BatPath
$Sc.WorkingDirectory = $RepoRoot
$Sc.WindowStyle = 1
$Sc.Description = "Janusforge Visor Molecular (local FastAPI + 3Dmol)"
# Icono: molécula/aplicación de shell32 (índice 13 suele ser un chip/red; 21 carpeta; usamos 13)
$Sc.IconLocation = "$env:SystemRoot\System32\shell32.dll,13"
$Sc.Save()

Write-Host "OK: acceso directo creado:"
Write-Host "  $ShortcutPath"
Write-Host "Destino:"
Write-Host "  $BatPath"
exit 0
