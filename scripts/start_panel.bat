@echo off
setlocal
REM ==============================================================================
REM WINE3ai - Lanzador del Panel de Control en Windows (http://localhost:5050)
REM ==============================================================================

for %%I in ("%~dp0..") do set "ROOT_DIR=%%~fI"
cd /d "%ROOT_DIR%" || exit /b 1

if not exist "%ROOT_DIR%\logs" mkdir "%ROOT_DIR%\logs"

for /f "usebackq delims=" %%P in (`powershell -NoProfile -Command "(Get-NetTCPConnection -LocalPort 5050 -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty OwningProcess)"`) do set "EXISTING_PID=%%P"

if defined EXISTING_PID (
    echo [AVISO] El Panel de Control ya esta corriendo en http://localhost:5050 - PID: %EXISTING_PID%
    echo         Para detenerlo: scripts\stop_panel.bat
    exit /b 0
)

set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"

powershell -NoProfile -Command "Start-Process -FilePath 'python' -ArgumentList 'scripts/control_panel.py' -WorkingDirectory '%ROOT_DIR%' -WindowStyle Hidden -RedirectStandardOutput '%ROOT_DIR%\logs\control_panel.log' -RedirectStandardError '%ROOT_DIR%\logs\control_panel.err.log'"

powershell -NoProfile -Command "Start-Sleep -Seconds 2"

for /f "usebackq delims=" %%P in (`powershell -NoProfile -Command "(Get-NetTCPConnection -LocalPort 5050 -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty OwningProcess)"`) do set "NEW_PID=%%P"

if defined NEW_PID (
    echo =================================================================
    echo WINE3ai - Panel de Control iniciado con exito
    echo =================================================================
    echo    URL: http://localhost:5050
    echo    PID: %NEW_PID%
    echo    Log: %ROOT_DIR%\logs\control_panel.log
    echo    Para detener: scripts\stop_panel.bat
    echo =================================================================
) else (
    echo [ERROR] No se pudo iniciar el Panel de Control. Revisa logs\control_panel.log y logs\control_panel.err.log
    exit /b 1
)
