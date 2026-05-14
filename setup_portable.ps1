# setup_portable.ps1 (Version Ultra-Portable)
$ErrorActionPreference = "Stop"
$PythonVersion = "3.12.3"
$Url = "https://www.python.org/ftp/python/$PythonVersion/python-$PythonVersion-embed-amd64.zip"
$EngineDir = Join-Path (Get-Location) "engine"
$ZipFile = Join-Path $EngineDir "python_portable.zip"

if (!(Test-Path $EngineDir)) { New-Item -ItemType Directory -Path $EngineDir }

Write-Host "--- 1. Descargando Nucleo de Python ---" -ForegroundColor Cyan
if (!(Test-Path (Join-Path $EngineDir "python.exe"))) {
    Invoke-WebRequest -Uri $Url -OutFile $ZipFile
    Expand-Archive -Path $ZipFile -DestinationPath $EngineDir -Force
    Remove-Item $ZipFile
}

Write-Host "--- 2. Configurando Rutas Maestras ---" -ForegroundColor Cyan
$PthFile = Get-ChildItem -Path $EngineDir -Filter "*._pth" | Select-Object -First 1
if ($PthFile) {
    # Forzar a Python a que use carpetas locales de librerias
    $PthContent = @(
        "python312.zip",
        ".",
        "Lib\site-packages",
        "import site"
    )
    $PthContent | Set-Content $PthFile.FullName -Encoding Ascii
}

Write-Host "--- 3. Instalando Gestor PIP ---" -ForegroundColor Cyan
$GetPipFile = Join-Path $EngineDir "get-pip.py"
Invoke-WebRequest -Uri "https://bootstrap.pypa.io/get-pip.py" -OutFile $GetPipFile
& "$EngineDir\python.exe" $GetPipFile --no-warn-script-location
Remove-Item $GetPipFile

Write-Host "--- 4. Instalando Librerias Criticas (Pillow, Hydrogram, etc) ---" -ForegroundColor Cyan
# Forzamos la instalacion dentro de la carpeta 'engine' para que sea 100% portable
& "$EngineDir\python.exe" -m pip install --upgrade Pillow hydrogram tgcrypto python-dotenv aiohttp typing_extensions --no-warn-script-location

Write-Host "-------------------------------------------" -ForegroundColor Green
Write-Host "EXITO: El motor ahora es 100% independiente."
Write-Host "Ya puedes ejecutar run.bat en este PC."
Write-Host "-------------------------------------------" -ForegroundColor Green
