@echo off
title Switch ES - The Goonies OS - Control Center
setlocal enabledelayedexpansion

:: CONFIGURACIÓN DE RUTAS ABSOLUTAS RESPECTO AL BAT
set "PY_ENGINE=%~dp0engine\python.exe"
set "PTH_FILE=%~dp0engine\python312._pth"
set "TEMP_SEL=%~dp0data\.selection.tmp"

:: VERIFICACIÓN DE MOTOR
if not exist "%PY_ENGINE%" (
    echo [ERROR] No se encuentra la carpeta 'engine'.
    pause
    exit /b
)

:: FORZAR RUTAS RELATIVAS (Soluciona el error en otros PCs)
(
    echo python312.zip
    echo .
    echo Lib\site-packages
    echo import site
) > "%PTH_FILE%"

:MAIN_MENU
cls
if exist "%TEMP_SEL%" del "%TEMP_SEL%"

:: LANZAR GESTOR
"%PY_ENGINE%" "%~dp0src\selector.py"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [!] El sistema detecto un problema.
    pause
    goto MAIN_MENU
)

if exist "%TEMP_SEL%" (
    set /p RAW_DATA=<"%TEMP_SEL%"
    goto PROCESS_DATA
) else (
    goto MAIN_MENU
)

:PROCESS_DATA
for /f "tokens=1-8 delims=|" %%a in ("!RAW_DATA!") do (
    set "SEL_ID=%%a"
    set "SEL_TOPIC=%%b"
    set "SEL_DB=%%c"
    set "SEL_HTML=%%d"
    set "SEL_TM=%%e"
    set "SEL_TS=%%f"
    set "SEL_AVATAR=%%g"
    set "SEL_NAME=%%h"
)

:ACTION_MENU
cls
echo ======================================================
echo           BIBLIOTECA: %SEL_NAME%
echo ======================================================
echo  ARCHIVO: %SEL_HTML%
echo  AVATAR:  %SEL_AVATAR%
if not "%SEL_TOPIC%"=="0" echo  SECCION (Topic): %SEL_TOPIC%
echo ======================================================
echo.
echo  1. ACTUALIZACION RAPIDA (Nuevos)
echo  2. ESCANEO HISTORICO (Fecha)
echo  3. REPARAR / OPTIMIZAR WEB
echo  4. VOLVER AL SELECTOR
echo  5. SALIR
echo.
echo ======================================================
set /p opt="Opcion [1-5]: "

if "%opt%"=="1" goto QUICK
if "%opt%"=="2" goto HISTORY
if "%opt%"=="3" goto RESCUE
if "%opt%"=="4" goto MAIN_MENU
if "%opt%"=="5" exit
goto ACTION_MENU

:QUICK
"%PY_ENGINE%" "%~dp0src\scraper.py" "%SEL_ID%" "%SEL_TOPIC%" "%SEL_DB%" "%SEL_HTML%" "%SEL_TM%" "%SEL_TS%" "%SEL_AVATAR%"
echo.
pause
goto ACTION_MENU

:HISTORY
set /p dte="Fecha [DD/MM/YYYY]: "
"%PY_ENGINE%" "%~dp0src\scraper.py" "%SEL_ID%" "%SEL_TOPIC%" "%SEL_DB%" "%SEL_HTML%" "%SEL_TM%" "%SEL_TS%" "%SEL_AVATAR%" "%dte%"
echo.
pause
goto ACTION_MENU

:RESCUE
"%PY_ENGINE%" "%~dp0src\rescue_db.py" "%SEL_DB%" "%SEL_HTML%" "%SEL_TM%" "%SEL_TS%" "%SEL_AVATAR%"
echo.
pause
goto ACTION_MENU
