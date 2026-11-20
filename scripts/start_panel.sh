#!/usr/bin/env bash
# ==============================================================================
# WINE³ai — Lanzador Autónomo del Panel de Control (Independiente de Antigravity)
# ==============================================================================

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR" || exit 1

mkdir -p "$ROOT_DIR/logs"

# Comprobar si ya está corriendo en el puerto 5050
PID=$(lsof -ti :5050 2>/dev/null)
if [ -n "$PID" ]; then
    echo "⚠️  El Panel de Control ya está corriendo en http://localhost:5050 (PID: $PID)"
    echo "   Para detenerlo: kill $PID"
    exit 0
fi

# Iniciar en segundo plano desacoplado
nohup python3 "$ROOT_DIR/scripts/control_panel.py" > "$ROOT_DIR/logs/control_panel.log" 2>&1 &
NEW_PID=$!

sleep 1

if ps -p "$NEW_PID" > /dev/null; then
    echo "================================================================="
    echo "🍷 WINE³ai — Panel de Control iniciado con éxito"
    echo "================================================================="
    echo "   🌐 URL: http://localhost:5050"
    echo "   📋 PID: $NEW_PID"
    echo "   📄 Log: $ROOT_DIR/logs/control_panel.log"
    echo "   🛑 Para detener: ./scripts/stop_panel.sh (o kill $NEW_PID)"
    echo "================================================================="
else
    echo "❌ Error al iniciar el Panel de Control. Revisa logs/control_panel.log"
    exit 1
fi
