# Guía y Manual Operativo de Scripts — WINE³ai

> **English version available:** [README.en.md](file:///Users/jreyes13/GitHub/wine3ai/scripts/README.en.md)  
> **Directorio:** `/scripts/`  
> **Filosofía del Sistema:** 100% Local, Privacidad Total, **0 Tokens Externos** (Inferencia exclusiva mediante LM Studio local en `http://127.0.0.1:1234/v1`).

---

## 1. Mapa de Scripts y Componentes

| Script | Lenguaje | Propósito Principal | Cuándo Utilizarlo |
| :--- | :--- | :--- | :--- |
| [`start_panel.sh`](file:///Users/jreyes13/GitHub/wine3ai/scripts/start_panel.sh) | Bash | Lanza el **Panel de Control Web** en segundo plano desacoplado en el puerto 5050. | **Recomendado para uso visual**: control total desde el navegador en `http://localhost:5050`. |
| [`stop_panel.sh`](file:///Users/jreyes13/GitHub/wine3ai/scripts/stop_panel.sh) | Bash | Detiene el Panel de Control Web liberando el puerto 5050. | Cuando desees apagar el panel administrativo web. |
| [`control_panel.py`](file:///Users/jreyes13/GitHub/wine3ai/scripts/control_panel.py) | Python 3 | Servidor HTTP del Panel de Control (cero dependencias externas, estándar library). | Invocado automáticamente por `start_panel.sh`. |
| [`audit_manager.sh`](file:///Users/jreyes13/GitHub/wine3ai/scripts/audit_manager.sh) | Bash | Gestor de control de auditoría por terminal (start / stop / status / logs / quick). | Para arrancar y parar auditorías desatendidas desde terminal sin abrir el navegador. |
| [`lm_studio_auditor.py`](file:///Users/jreyes13/GitHub/wine3ai/scripts/lm_studio_auditor.py) | Python 3 | Motor analítico de regiones vitivinícolas, pliegos oficiales y geometrías. | Ejecución interactiva por consola, filtros por país o auditorías específicas (ej. MAPA España). |
| [`overnight_worker.py`](file:///Users/jreyes13/GitHub/wine3ai/scripts/overnight_worker.py) | Python 3 | Generador nocturno autónomo de fichas de estudio (WSET3, CMS) y artículos Winepedia. | Sesiones largas nocturnas programadas por horario o duración. |
| [`compile_generated_data.py`](file:///Users/jreyes13/GitHub/wine3ai/scripts/compile_generated_data.py) | Python 3 | Compilador atómico mediante `jsc` (JavaScriptCore) de checkpoints JSON a producción. | Tras generar artículos/tarjetas para consolidar en `data/` y `web/data/`. |
| [`lm_studio.py`](file:///Users/jreyes13/GitHub/wine3ai/scripts/lm_studio.py) | Python 3 | Módulo conector / cliente HTTP hacia la API de LM Studio. | Como librería reutilizable en otros scripts o pruebas rápidas por consola. |

---

## 2. Matriz de Decisión: "¿Qué ejecutar y cuándo?"

```
                         ¿Qué prefieres utilizar?
                                     │
           ┌─────────────────────────┴─────────────────────────┐
           ▼                                                   ▼
[ INTERFAZ GRÁFICA WEB ]                               [ LÍNEA DE COMANDOS ]
           │                                                   │
  1. ./scripts/start_panel.sh                                  ├─ Gestor en 2º plano (auditoría):
  2. Abrir http://localhost:5050                               │  └─> ./scripts/audit_manager.sh start
     - Ver estado LM Studio y modelo activo                    │
     - Lanzar/parar generador de fichas                        ├─ Escaneo instantáneo pliegos (2s):
     - Lanzar/parar auditor de mapas                           │  └─> ./scripts/audit_manager.sh quick
     - Ver logs en vivo en pantalla dividida                   │
     - Sincronización Total (Compilar + Git + VPS IONOS)       ├─ Auditoría MAPA España:
                                                               │  └─> python3 scripts/lm_studio_auditor.py --country Spain --mode spain_mapa
                                                               │
                                                               ├─ Generador nocturno:
                                                               │  └─> python3 scripts/overnight_worker.py --end 06:45
                                                               │
                                                               └─ Detener panel web:
                                                                  └─> ./scripts/stop_panel.sh
```

---

## 3. El Panel de Control Web (`control_panel.py` / `start_panel.sh`)

El **Panel de Control WINE³ai** es un cuadro de mando integral que unifica toda la administración del sistema en una interfaz web limpia, moderna y sin dependencias externas (usa la librería estándar `http.server` de Python).

### 3.1. Cómo iniciarlo y detenerlo
```bash
# Iniciar el panel en segundo plano
./scripts/start_panel.sh

# Detener el panel
./scripts/stop_panel.sh
```
Una vez iniciado, abre en tu navegador:  
👉 **`http://localhost:5050`**

### 3.2. Capacidades del Panel Web
1. **Estado en tiempo real de LM Studio:** Comprueba automáticamente la conectividad con `http://127.0.0.1:1234/v1` e identifica el modelo activo cargado en memoria (ej. `qwen/qwen3.5-9b`).
2. **Control del Generador de Fichas (`overnight_worker.py`):**
   - Presets directos con un clic: *Hasta las 16:15*, *Hasta las 06:45*, *Indefinido*, o por bloques de *1h*, *3h*, *5h*, *8h* o *Hora personalizada*.
   - Botón de parada segura (guarda checkpoints y compila automáticamente).
3. **Control del Auditor de Mapas y Pliegos (`lm_studio_auditor.py`):**
   - Selección de modo: *Cruce Oficial MAPA España*, *Auditoría Completa con IA*, o *Comprobación Física de Pliegos*.
   - Filtro por país (España, Francia, Chequia, Argentina, Todos...) y límite de regiones por sesión.
4. **Sincronización Total ("Sync All"):**
   - **Compilación local atómica:** Ejecuta `compile_generated_data.py`.
   - **Git Commit automático:** Registra los cambios generados con marca de tiempo.
   - **Despliegue a Producción (VPS IONOS):** Ejecuta `rsync` hacia `root@jreyes13.net:/var/www/vhosts/jreyes13.net/wine3ai/` y reajusta permisos a `jreyes169:psaserv`.
5. **Doble Consola de Logs en Vivo:** Visualiza en streaming tanto el log de generación de fichas como el log del auditor sin tocar la terminal.
6. **Visor de Informe Markdown en Vivo:** Renderiza directamente el archivo [`reports/AUDIT_WINE_REGIONS_LMSTUDIO.md`](file:///Users/jreyes13/GitHub/wine3ai/reports/AUDIT_WINE_REGIONS_LMSTUDIO.md) en pantalla.

---

## 4. Flujos Alternativos por Consola

Si prefieres la terminal o estás conectado por SSH sin navegador:

### Escenario A: Ratos muertos del portátil (Almuerzo o pausas)
```bash
# Iniciar auditoría en segundo plano
./scripts/audit_manager.sh start

# Ver progreso actual
./scripts/audit_manager.sh status

# Ver razonamiento de LM Studio en vivo
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

## 5. Guía Detallada de Scripts de Soporte

### 5.1. `audit_manager.sh` (Gestor CLI en Segundo Plano)
*   `./scripts/audit_manager.sh start [opciones]`: Arranca `lm_studio_auditor.py` con `nohup`.
*   `./scripts/audit_manager.sh stop`: Envía señal `SIGTERM`, guarda el estado y sale limpiamente.
*   `./scripts/audit_manager.sh status`: Muestra métricas globales y estado del proceso.
*   `./scripts/audit_manager.sh logs`: Streaming en tiempo real del archivo de log.
*   `./scripts/audit_manager.sh quick`: Comprobación física de pliegos en 2 segundos.

---

### 5.2. `lm_studio_auditor.py` (Motor de Auditoría Enológica)
Motor que audita la coherencia entre el mapa canónico (`data/wine_regions.geojson`), los documentos de pliego de condiciones (`DOWNs/DOCs/`) y los registros oficiales (MAPA, eAmbrosia).

#### Opciones CLI:
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
1.  [`reports/AUDIT_WINE_REGIONS_LMSTUDIO.md`](file:///Users/jreyes13/GitHub/wine3ai/reports/AUDIT_WINE_REGIONS_LMSTUDIO.md): Informe en Markdown con tablas de estado por país y comparativa oficial de España.
2.  [`reports/audit_findings.json`](file:///Users/jreyes13/GitHub/wine3ai/reports/audit_findings.json): Estructura JSON con todas las anomalías detectadas para consumo por Gemini u otras IAs.
3.  [`reports/audit_state.json`](file:///Users/jreyes13/GitHub/wine3ai/reports/audit_state.json): Registro de progreso para reanudar sin repetir trabajo.

---

### 5.3. `overnight_worker.py` (Generador de Contenido)
Orquestador que procesa el catálogo de 370 fichas de estudio para sumilleres (WSET3, CMS, ASI) y artículos enciclopédicos.
*   Genera checkpoints en `data/generated/`.
*   Al finalizar, invoca automáticamente a `compile_generated_data.py` y redacta `OVERNIGHT_REPORT.md`.

---

### 5.4. `compile_generated_data.py` (Compilador de Producción)
Consolida con seguridad atómica los datos JSON generados hacia los archivos de producción leídos por la interfaz web de WINE³ai:
*   Utiliza `/System/Library/Frameworks/JavaScriptCore.framework/Versions/Current/Helpers/jsc` para evaluar y fusionar los arrays JavaScript sin corromper el árbol de sintaxis.
*   Destinos sincronizados:
    *   `data/winepedia_articles.js` y `web/data/winepedia_articles.js`
    *   `data/study_cards.js` y `web/data/study_cards.js`
    *   `data/grape_varieties.json` y `web/data/grape_varieties.json`

---

### 5.5. `lm_studio.py` (Librería Conectora Local)
Módulo ligero para interactuar programáticamente con la API local de LM Studio (`http://127.0.0.1:1234/v1`).

---

## 6. Requisitos y Configuración de LM Studio

Para garantizar la ejecución sin errores:
1.  **LM Studio abierto:** Servidor local activo en `http://127.0.0.1:1234`.
2.  **Modelo cargado:** Modelo recomendado `qwen/qwen3.5-9b` (o compatible con ventana de contexto >= 8192 tokens).
3.  **Configuración de tokens:** En modelos con modo "Thinking" (cadena de razonamiento CoT), asegúrate de que el límite de tokens (`max_tokens`) sea de al menos 1200 a 2500 para evitar que la respuesta se corte antes de volcar la conclusión.
4.  **Cero costes:** Toda la inferencia transcurre exclusivamente en la memoria unificada / GPU del Mac.
