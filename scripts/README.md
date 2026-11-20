# Guía y Manual Operativo de Scripts — WINE³ai

> **English version available:** [README.en.md](file:///Users/jreyes13/GitHub/wine3ai/scripts/README.en.md)  
> **Directorio:** `/scripts/`  
> **Filosofía del Sistema:** 100% Local, Privacidad Total, **0 Tokens Externos** (Inferencia exclusiva mediante LM Studio local en `http://127.0.0.1:1234/v1`).

---

## 1. Mapa de Scripts y Componentes

| Script | Lenguaje | Propósito Principal | Cuándo Utilizarlo |
| :--- | :--- | :--- | :--- |
| [`audit_manager.sh`](file:///Users/jreyes13/GitHub/wine3ai/scripts/audit_manager.sh) | Bash | Gestor de control en segundo plano (start / stop / status / logs / quick). | **Recomendado para el día a día**: arrancar y parar auditorías desatendidas en ratos muertos del portátil. |
| [`lm_studio_auditor.py`](file:///Users/jreyes13/GitHub/wine3ai/scripts/lm_studio_auditor.py) | Python 3 | Motor analítico de regiones vitivinícolas, pliegos oficiales y geometrías. | Ejecución interactiva por consola, filtros por país o auditorías específicas (ej. MAPA España). |
| [`overnight_worker.py`](file:///Users/jreyes13/GitHub/wine3ai/scripts/overnight_worker.py) | Python 3 | Generador nocturno autónomo de fichas de estudio (WSET3, CMS) y artículos Winepedia. | Sesiones largas nocturnas programadas por horario o duración. |
| [`compile_generated_data.py`](file:///Users/jreyes13/GitHub/wine3ai/scripts/compile_generated_data.py) | Python 3 | Compilador atómico mediante `jsc` (JavaScriptCore) de checkpoints JSON a producción. | Tras generar artículos/tarjetas para consolidar en `data/` y `web/data/`. |
| [`lm_studio.py`](file:///Users/jreyes13/GitHub/wine3ai/scripts/lm_studio.py) | Python 3 | Módulo conector / cliente HTTP hacia la API de LM Studio. | Como librería reutilizable en otros scripts o pruebas rápidas por consola. |

---

## 2. Matriz de Decisión: "¿Qué ejecutar y cuándo?"

```
               ¿Qué tarea deseas realizar?
                            │
       ┌────────────────────┴────────────────────┐
       ▼                                         ▼
[ AUDITAR MAPAS Y PLIEGOS ]            [ GENERAR CONTENIDO EDUCATIVO ]
       │                                         │
       ├─ Tengo ratos muertos (2º plano)         ├─ Sesión nocturna (3h por defecto)
       │  └─> ./scripts/audit_manager.sh start   │  └─> python3 scripts/overnight_worker.py
       │                                         │
       ├─ Tengo 2 minutos (sólo pliegos)         ├─ Programar hasta las 07:00 AM
       │  └─> ./scripts/audit_manager.sh quick   │  └─> python3 scripts/overnight_worker.py --end 07:00
       │                                         │
       ├─ Quiero auditar un país concreto        └─ Tras generar, compilar a producción:
       │  └─> python3 scripts/lm_studio_auditor.py --country Spain --mode spain_mapa
       │                                            └─> python3 scripts/compile_generated_data.py
       └─ Quiero parar y guardar estado
          └─> ./scripts/audit_manager.sh stop
```

### Escenario A: Ratos muertos del portátil (Almuerzo, pausas o cuando no lo uses)
Utiliza el gestor en segundo plano. Corre desatendido, respeta el procesador con pausas entre regiones y es 100% seguro de pausar:
```bash
# Iniciar auditoría en segundo plano
./scripts/audit_manager.sh start

# Ver progreso actual
./scripts/audit_manager.sh status

# Ver razonamiento de LM Studio en vivo (Ctrl+C para salir, el proceso continúa)
./scripts/audit_manager.sh logs

# Detener de forma segura (guarda checkpoint automáticamente)
./scripts/audit_manager.sh stop
```

### Escenario B: Escaneo instantáneo de pliegos y geometrías (2 segundos)
Comprueba las 894 regiones del mapa en disco, reportando qué pliegos faltan o están vacíos y qué polígonos son toscos:
```bash
./scripts/audit_manager.sh quick
# o directamente:
python3 scripts/lm_studio_auditor.py --mode pliegos
```

### Escenario C: Auditoría específica de España (Cruce con Registro Oficial MAPA)
Cruza el GeoJSON contra el documento oficial del Ministerio de Agricultura (`DOWNs/SPAIN/02_vinos.2026-07-03-13-01-22.pdf`), auditando municipios por provincia y variedades de uva:
```bash
python3 scripts/lm_studio_auditor.py --country Spain --mode spain_mapa
```

### Escenario D: Auditoría de un país concreto (Chequia, Argentina, Francia...)
```bash
# Auditar regiones de Chequia (detecta pliegos débiles y geometrías simplificadas)
python3 scripts/lm_studio_auditor.py --country Czechia --mode full

# Auditar las 26 IGs/DOCs de Argentina recién actualizadas
python3 scripts/lm_studio_auditor.py --country Argentina --mode full
```

### Escenario E: Sesión nocturna de generación de fichas y artículos
```bash
# Arranca de inmediato y corre 3 horas:
python3 scripts/overnight_worker.py

# Dejar corriendo toda la noche hasta una hora fija:
python3 scripts/overnight_worker.py --end 07:00
```

---

## 3. Guía Detallada de Cada Script

### 3.1. `audit_manager.sh` (Gestor de Proceso en Segundo Plano)
Controla el ciclo de vida del auditor sin necesidad de recordar PIDs ni mantener terminales abiertas.

*   `./scripts/audit_manager.sh start [opciones]`
    *   Arranca `lm_studio_auditor.py` con `nohup` en segundo plano.
    *   Acepta argumentos adicionales (ej: `./scripts/audit_manager.sh start --country France`).
    *   Registra el PID en `reports/auditor.pid`.
*   `./scripts/audit_manager.sh stop`
    *   Envía la señal `SIGTERM` al proceso. El script atrapa la señal, termina de procesar la región actual, guarda el estado en `reports/audit_state.json` y sale limpiamente.
*   `./scripts/audit_manager.sh status`
    *   Informa si el proceso está activo o detenido y muestra el cuadro de mando actualizado con métricas globales.
*   `./scripts/audit_manager.sh logs`
    *   Ejecuta `tail -f reports/auditor.log` para monitorear el flujo de análisis en tiempo real.
*   `./scripts/audit_manager.sh quick`
    *   Lanza la comprobación física de pliegos y geometrías en 2 segundos.

---

### 3.2. `lm_studio_auditor.py` (Motor de Auditoría Enológica)
Motor inteligente que audita la coherencia entre el mapa canónico (`data/wine_regions.geojson`), los documentos de pliego de condiciones (`DOWNs/DOCs/`) y los registros oficiales (MAPA, eAmbrosia).

#### Opciones de línea de comandos:
```
python3 scripts/lm_studio_auditor.py [argumentos]

  --country COUNTRY     País a auditar (ej. Spain, France, Czechia, Argentina o all)
  --mode MODO           Modo de trabajo:
                        - full: Auditoría completa (física + consulta a LM Studio)
                        - spain_mapa: Cruce específico contra el PDF oficial del MAPA
                        - pliegos: Comprobación física ultrarrápida sin LLM
  --limit N             Procesar como máximo N regiones en esta tanda (ideal para pausas cortas)
  --delay S             Segundos de enfriamiento entre llamadas (por defecto 1.5s)
  --status              Muestra el resumen de métricas y sale
  --reset               Reinicia el archivo de estado para comenzar de cero
  --force               Vuelve a auditar regiones previamente marcadas como completadas
```

#### Salidas generadas:
1.  [`reports/AUDIT_WINE_REGIONS_LMSTUDIO.md`](file:///Users/jreyes13/GitHub/wine3ai/reports/AUDIT_WINE_REGIONS_LMSTUDIO.md): Informe legible en Markdown con tablas de estado por país y comparativa oficial de España.
2.  [`reports/audit_findings.json`](file:///Users/jreyes13/GitHub/wine3ai/reports/audit_findings.json): Estructura JSON con todas las anomalías detectadas, optimizada para consumo por Gemini u otras IAs.
3.  [`reports/audit_state.json`](file:///Users/jreyes13/GitHub/wine3ai/reports/audit_state.json): Registro de progreso que permite pausar y reanudar sin repetir trabajo.

---

### 3.3. `overnight_worker.py` (Generador de Contenido)
Orquestador que procesa el catálogo de 370 fichas de estudio para sumilleres (WSET3, CMS, ASI) y artículos enciclopédicos.

*   **Argumentos:**
    *   `--start HH:MM`: Hora de inicio programada (ej. `23:30`).
    *   `--end HH:MM`: Hora límite de parada (ej. `06:30`).
    *   `--hours N`: Duración fija en horas (ej. `4.5`).
    *   `--now`: Iniciar inmediatamente omitiendo el temporizador.
*   **Resultados:**
    *   Genera checkpoints en `data/generated/`.
    *   Al finalizar, invoca automáticamente a `compile_generated_data.py` y redacta `OVERNIGHT_REPORT.md`.

---

### 3.4. `compile_generated_data.py` (Compilador de Producción)
Consolida con seguridad atómica los datos JSON generados hacia los archivos de producción leídos por la interfaz web de WINE³ai:
*   Utiliza `/System/Library/Frameworks/JavaScriptCore.framework/Versions/Current/Helpers/jsc` para evaluar y fusionar los arrays JavaScript sin corromper el árbol de sintaxis.
*   Destinos sincronizados:
    *   `data/winepedia_articles.js` y `web/data/winepedia_articles.js`
    *   `data/study_cards.js` y `web/data/study_cards.js`
    *   `data/grape_varieties.json` y `web/data/grape_varieties.json`

---

### 3.5. `lm_studio.py` (Librería Conectora Local)
Módulo ligero para interactuar con la API local de LM Studio (`http://127.0.0.1:1234/v1`).

```python
from scripts.lm_studio import query_lm

# Consulta básica
respuesta = query_lm("Explica el terroir de Paraje Altamira en Mendoza.")

# Consulta con desglose de tokens de razonamiento
respuesta, stats = query_lm(
    prompt="Diferencias entre DOC Luján de Cuyo y DOC San Rafael",
    model="qwen/qwen3.5-9b",
    return_usage=True
)
print(f"Tokens generados: {stats['completion_tokens']}, Razonamiento: {stats.get('reasoning_tokens', 0)}")
```

---

## 4. Requisitos y Configuración de LM Studio

Para garantizar la ejecución sin errores:
1.  **LM Studio abierto:** El servidor local debe estar activo en `http://127.0.0.1:1234`.
2.  **Modelo cargado:** Modelo recomendado `qwen/qwen3.5-9b` (o compatible con ventana de contexto >= 8192 tokens).
3.  **Configuración de tokens:** En modelos con modo "Thinking" (cadena de razonamiento CoT), asegúrate de que el límite de tokens (`max_tokens`) sea de al menos 1200 a 2500 para evitar que la respuesta se corte antes de volcar la conclusión.
4.  **Cero costes:** Toda la inferencia transcurre exclusivamente en la memoria unificada / GPU del Mac.
