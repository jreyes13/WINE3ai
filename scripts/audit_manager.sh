#!/usr/bin/env bash
# ==============================================================================
# WINE³ai — GESTOR DE AUDITORÍA EN SEGUNDO PLANO CON LM STUDIO
# ==============================================================================
# Permite arrancar, parar, monitorear y consultar la auditoría local
# sin consumir tokens externos y con reanudación automática.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PID_FILE="$BASE_DIR/reports/auditor.pid"
LOG_FILE="$BASE_DIR/reports/auditor.log"
PYTHON_SCRIPT="$SCRIPT_DIR/lm_studio_auditor.py"

cd "$BASE_DIR" || exit 1
mkdir -p "$BASE_DIR/reports"

is_running() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            return 0
        fi
    fi
    # Comprobar también por nombre por si quedó huérfano
    pgrep -f "lm_studio_auditor.py" > /dev/null 2>&1
    return $?
}

get_pid() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            echo "$PID"
            return
        fi
    fi
    pgrep -f "lm_studio_auditor.py" | head -n 1
}

case "$1" in
    start)
        if is_running; then
            PID=$(get_pid)
            echo "⚠️  El auditor ya está en ejecución (PID: $PID)."
            echo "   Puedes ver el avance con: $0 logs"
            exit 0
        fi
        
        # Opciones opcionales pasadas al script (ej: ./audit_manager.sh start --country Spain)
        shift
        EXTRA_ARGS="$*"
        if [ -z "$EXTRA_ARGS" ]; then
            EXTRA_ARGS="--mode full --delay 2.0"
        fi
        
        echo "🚀 Iniciando auditoría en segundo plano con LM Studio..."
        echo "   Argumentos: $EXTRA_ARGS"
        echo "   Registro de actividad: $LOG_FILE"
        
        nohup python3 "$PYTHON_SCRIPT" $EXTRA_ARGS > "$LOG_FILE" 2>&1 &
        AUDIT_PID=$!
        echo "$AUDIT_PID" > "$PID_FILE"
        sleep 1
        
        if ps -p "$AUDIT_PID" > /dev/null 2>&1; then
            echo "✅ Auditor arrancado correctamente (PID: $AUDIT_PID)."
            echo "   Comandos útiles:"
            echo "     $0 status  -> Ver progreso actual"
            echo "     $0 logs    -> Ver log en vivo"
            echo "     $0 stop    -> Detener de forma segura"
        else
            echo "❌ Error al iniciar. Revisa el log con: cat $LOG_FILE"
        fi
        ;;

    stop)
        if ! is_running; then
            echo "ℹ️  No hay ningún auditor ejecutándose en este momento."
            [ -f "$PID_FILE" ] && rm -f "$PID_FILE"
            exit 0
        fi
        PID=$(get_pid)
        echo "🛑 Deteniendo auditor (PID: $PID)..."
        kill -TERM "$PID" 2>/dev/null
        # Esperar hasta 5 segundos a que guarde el estado
        for i in {1..5}; do
            if ! ps -p "$PID" > /dev/null 2>&1; then
                break
            fi
            sleep 1
        done
        if ps -p "$PID" > /dev/null 2>&1; then
            echo "   Forzando parada..."
            kill -KILL "$PID" 2>/dev/null
        fi
        rm -f "$PID_FILE"
        echo "✅ Auditor detenido de forma segura. El progreso quedó guardado para reanudar cuando quieras."
        ;;

    status)
        if is_running; then
            PID=$(get_pid)
            echo "🟢 ESTADO DEL PROCESO: EN EJECUCIÓN (PID: $PID)"
        else
            echo "⚪ ESTADO DEL PROCESO: DETENIDO"
        fi
        echo ""
        python3 "$PYTHON_SCRIPT" --status
        ;;

    logs)
        if [ ! -f "$LOG_FILE" ]; then
            echo "ℹ️  Aún no hay archivo de registro ($LOG_FILE)."
            exit 0
        fi
        echo "📋 Mostrando registro en vivo (Ctrl+C para salir)..."
        tail -f "$LOG_FILE"
        ;;

    quick)
        echo "⚡ Ejecutando escaneo rápido de pliegos y geometrías en disco (sin LLM)..."
        python3 "$PYTHON_SCRIPT" --mode pliegos
        ;;

    *)
        echo "Uso: $0 {start|stop|status|logs|quick}"
        echo ""
        echo "Comandos:"
        echo "  start [opciones]  Lanzar en segundo plano (ej: $0 start o $0 start --country Spain)"
        echo "  stop              Detener de forma segura guardando el estado"
        echo "  status            Ver estado del proceso y resumen de regiones auditadas"
        echo "  logs              Seguir el log en tiempo real (Ctrl+C para salir)"
        echo "  quick             Escaneo ultra-rápido de pliegos físicos (tarda 2s)"
        echo ""
        ;;
esac
