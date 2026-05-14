@echo off
title Preparar Secretos de GitHub
setlocal enabledelayedexpansion

set "PY_ENGINE=%~dp0engine\python.exe"
set "PTH_FILE=%~dp0engine\python312._pth"

if not exist "%PY_ENGINE%" (
    echo [ERROR] No se encuentra la carpeta 'engine'.
    pause
    exit /b
)

:: FORZAR RUTAS RELATIVAS
(
    echo python312.zip
    echo .
    echo Lib\site-packages
    echo import site
) > "%PTH_FILE%"

cls
"%PY_ENGINE%" "%~dp0preparar_secretos.py"
pause
