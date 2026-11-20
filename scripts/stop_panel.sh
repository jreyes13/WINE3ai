#!/usr/bin/env bash
# ==============================================================================
# WINE³ai — Detenedor del Panel de Control
# ==============================================================================

PID=$(lsof -ti :5050 2>/dev/null)
if [ -n "$PID" ]; then
    kill "$PID"
    echo "🛑 Panel de Control (PID $PID) detenido."
else
    echo "ℹ️  No hay ningún Panel de Control corriendo en el puerto 5050."
fi
