# Installs the research skills into %USERPROFILE%\.claude\skills and records where this template lives.
# Run again after every `git pull` to update the skills. Windows PowerShell:
#   powershell -ExecutionPolicy Bypass -File kur.ps1 [-Kisisel <personal folder>]
# Default personal folder: the saved path, else _arastirma-kisisel next to this template.
param([string]$Kisisel = "")
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
# Personal folder: this researcher's own kaynak.json, kapali_kapilar.json and gecmis.md. Never overwrite a file.
$kTxt = Join-Path $ara "kisisel_yolu.txt"
if ($Kisisel -ne "") { $k = $Kisisel }
elseif (Test-Path $kTxt) { $k = ([System.IO.File]::ReadAllText($kTxt)).Trim() }
else { $k = Join-Path (Split-Path -Parent $here) "_arastirma-kisisel" }
New-Item -ItemType Directory -Force -Path $k | Out-Null
$k = (Resolve-Path $k).Path
Get-ChildItem -File (Join-Path $here "kisisel-ornek") | ForEach-Object {
    $d = Join-Path $k $_.Name
    if (-not (Test-Path $d)) { Copy-Item $_.FullName $d; Write-Output "kisisel dosya olusturuldu: $d" }
}
[System.IO.File]::WriteAllText($kTxt, $k, $utf8)
Write-Output "kisisel klasor: $k"
