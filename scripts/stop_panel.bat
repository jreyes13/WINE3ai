@echo off
setlocal
REM ==============================================================================
REM WINE3ai - Detenedor del Panel de Control en Windows (puerto 5050)
REM ==============================================================================

for /f "usebackq delims=" %%P in (`powershell -NoProfile -Command "(Get-NetTCPConnection -LocalPort 5050 -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty OwningProcess)"`) do set "PANEL_PID=%%P"

if defined PANEL_PID (
    taskkill /PID %PANEL_PID% /T /F >nul 2>&1
    echo Panel de Control detenido - PID: %PANEL_PID%
) else (
    echo No hay ningun Panel de Control corriendo en el puerto 5050.
)
