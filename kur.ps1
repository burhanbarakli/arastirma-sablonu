# Installs the research skills into %USERPROFILE%\.claude\skills and records where this template lives.
# Run again after every `git pull` to update the skills. Windows PowerShell:
#   powershell -ExecutionPolicy Bypass -File kur.ps1
$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$claude = Join-Path $env:USERPROFILE ".claude"
$skills = Join-Path $claude "skills"
$ara = Join-Path $claude "arastirma"
New-Item -ItemType Directory -Force -Path $skills, $ara | Out-Null
Get-ChildItem -Directory (Join-Path $here "skills") | ForEach-Object {
    $dest = Join-Path $skills $_.Name
    if (Test-Path $dest) { Remove-Item -Recurse -Force $dest }
    Copy-Item -Recurse $_.FullName $dest
    Write-Output "skill kuruldu: $($_.Name)"
}
# Windows PowerShell 5.1's "Set-Content -Encoding UTF8" adds a BOM, which breaks JSON readers; write plain UTF-8.
$utf8 = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText((Join-Path $ara "sablon_yolu.txt"), $here, $utf8)
$reg = Join-Path $ara "projeler.json"
if (-not (Test-Path $reg)) { [System.IO.File]::WriteAllText($reg, "[]", $utf8) }
# Messages stay ASCII: PowerShell 5.1 reads a BOM-less script in the ANSI code page and garbles Turkish letters.
Write-Output "sablon yolu: $here"
