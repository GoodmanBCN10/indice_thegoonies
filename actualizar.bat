@echo off
title Switch ES ¡NUEVO! - Actualizacion Automatica
setlocal enabledelayedexpansion

set "PY_ENGINE=%~dp0..\INDICE Switch ES - The Goonies OS\engine\python.exe"

if not exist "%PY_ENGINE%" (
    echo [ERROR] No se encuentra la carpeta 'engine' en el proyecto anterior. Ejecuta con tu propio Python.
    python generar_indice.py
) else (
    "%PY_ENGINE%" generar_indice.py
)

echo.
echo ======================================================
echo           PROCESO FINALIZADO
echo ======================================================
:: pause
