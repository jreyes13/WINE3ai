# Scripts Guide and Operational Manual — WINE³ai

> **Versión en español disponible:** [README.md](file:///Users/jreyes13/GitHub/wine3ai/scripts/README.md)  
> **Directory:** `/scripts/`  
> **System Philosophy:** 100% Local, Absolute Privacy, **0 External Tokens** (Inference exclusively handled by local LM Studio at `http://127.0.0.1:1234/v1`).

---

## 1. Scripts Catalog and Overview

| Script | Language | Primary Purpose | When to Use |
| :--- | :--- | :--- | :--- |
| [`start_panel.sh`](file:///Users/jreyes13/GitHub/wine3ai/scripts/start_panel.sh) | Bash | Launches the **Web Control Panel** in the background on port 5050. | **Recommended for visual use**: full management via browser at `http://localhost:5050`. |
| [`stop_panel.sh`](file:///Users/jreyes13/GitHub/wine3ai/scripts/stop_panel.sh) | Bash | Stops the Web Control Panel and frees port 5050. | Whenever you want to turn off the administrative web interface. |
| [`control_panel.py`](file:///Users/jreyes13/GitHub/wine3ai/scripts/control_panel.py) | Python 3 | Lightweight HTTP server for the Control Panel (zero dependencies, Python standard library). | Invoked automatically by `start_panel.sh`. |
| [`audit_manager.sh`](file:///Users/jreyes13/GitHub/wine3ai/scripts/audit_manager.sh) | Bash | Terminal background process manager (start / stop / status / logs / quick). | For headless terminal control when you prefer not to open a browser. |
| [`lm_studio_auditor.py`](file:///Users/jreyes13/GitHub/wine3ai/scripts/lm_studio_auditor.py) | Python 3 | Core analysis engine for wine regions, specification pliegos, and geometries. | Direct interactive terminal runs, country filtering, or specialized audits (e.g., MAPA Spain). |
| [`overnight_worker.py`](file:///Users/jreyes13/GitHub/wine3ai/scripts/overnight_worker.py) | Python 3 | Autonomous overnight generator for sommelier flashcards (WSET3, CMS) and Winepedia articles. | Long unattended night runs scheduled by time or fixed duration. |
| [`compile_generated_data.py`](file:///Users/jreyes13/GitHub/wine3ai/scripts/compile_generated_data.py) | Python 3 | Atomic compiler using macOS `jsc` (JavaScriptCore) merging JSON checkpoints into production. | After generating articles/cards to safely consolidate into `data/` and `web/data/`. |
| [`lm_studio.py`](file:///Users/jreyes13/GitHub/wine3ai/scripts/lm_studio.py) | Python 3 | Reusable HTTP API client module connecting to LM Studio. | Programmatic helper library in scripts or quick terminal testing. |

---

## 2. Decision Matrix: "What to Run and When"

```
                         Which interface do you prefer?
                                       │
           ┌───────────────────────────┴───────────────────────────┐
           ▼                                                       ▼
[ GRAPHICAL WEB INTERFACE ]                                [ TERMINAL CLI ]
           │                                                       │
  1. ./scripts/start_panel.sh                                      ├─ Background audit manager:
  2. Open http://localhost:5050                                    │  └─> ./scripts/audit_manager.sh start
     - Check LM Studio health & active model                       │
     - Start/stop card generator (presets or custom)               ├─ Instant pliego check (2s):
     - Start/stop map & region auditor                             │  └─> ./scripts/audit_manager.sh quick
     - Live split-view streaming logs                              │
     - Full Synchronization (Compile + Git + IONOS VPS)            ├─ MAPA Spain deep audit:
                                                                   │  └─> python3 scripts/lm_studio_auditor.py --country Spain --mode spain_mapa
                                                                   │
                                                                   ├─ Overnight card generator:
                                                                   │  └─> python3 scripts/overnight_worker.py --end 06:45
                                                                   │
                                                                   └─ Stop web dashboard:
                                                                      └─> ./scripts/stop_panel.sh
```

---

## 3. The Web Control Panel (`control_panel.py` / `start_panel.sh`)

The **WINE³ai Control Panel** is an administrative dashboard providing full system control through a modern web UI with zero external dependencies (built on Python's built-in `http.server`).

### 3.1. Starting and Stopping
```bash
# Start the web dashboard in background
./scripts/start_panel.sh

# Stop the web dashboard
./scripts/stop_panel.sh
```
Once started, open your web browser at:  
👉 **`http://localhost:5050`**

### 3.2. Dashboard Capabilities
1. **Real-time LM Studio Health:** Auto-detects local server connectivity at `http://127.0.0.1:1234/v1` and identifies the active model in memory (e.g. `qwen/qwen3.5-9b`).
2. **Content Generation Manager (`overnight_worker.py`):**
   - One-click presets: *Until 16:15*, *Until 06:45*, *Indefinite*, or blocks of *1h*, *3h*, *5h*, *8h*, or *Custom time*.
   - Safe stop button (ensures checkpoints are flushed and compiled).
3. **Map & Region Auditor Manager (`lm_studio_auditor.py`):**
   - Mode selector: *Official MAPA Spain cross-check*, *Full AI Audit*, or *Physical Pliego Check*.
   - Country filter (Spain, France, Czechia, Argentina, All...) and per-session region limits.
4. **Full Synchronization ("Sync All"):**
   - **Atomic local compilation:** Runs `compile_generated_data.py`.
   - **Automated Git Commit:** Commits newly generated data and reports with timestamps.
   - **Production Deployment (IONOS VPS):** Syncs via `rsync` to `root@jreyes13.net:/var/www/vhosts/jreyes13.net/wine3ai/` and resets remote permissions to `jreyes169:psaserv`.
5. **Dual Live Web Consoles:** Streams both the content generation log and the map auditor log side by side without needing a terminal open.
6. **Live Markdown Report Viewer:** Renders [`reports/AUDIT_WINE_REGIONS_LMSTUDIO.md`](file:///Users/jreyes13/GitHub/wine3ai/reports/AUDIT_WINE_REGIONS_LMSTUDIO.md) directly in the browser.

---

## 4. Headless & CLI Workflows

If you are working over SSH or prefer running commands directly in your terminal:

### Scenario A: Laptop Idle Time (Lunch or short breaks)
```bash
# Start background audit
./scripts/audit_manager.sh start

# Check progress and metrics
./scripts/audit_manager.sh status

# Follow live LM Studio reasoning
./scripts/audit_manager.sh logs

# Stop safely whenever you return (auto-saves state)
./scripts/audit_manager.sh stop
```

### Scenario B: Instant Physical Pliego and Geometry Check (2 seconds)
```bash
./scripts/audit_manager.sh quick
# or directly:
python3 scripts/lm_studio_auditor.py --mode pliegos
```

### Scenario C: Spain Deep Audit (Cross-referencing Official MAPA Registry)
```bash
python3 scripts/lm_studio_auditor.py --country Spain --mode spain_mapa
```

### Scenario D: Auditing a Specific Country (Czechia, Argentina, France...)
```bash
# Audit Czech Republic
python3 scripts/lm_studio_auditor.py --country Czechia --mode full

# Audit all 26 Argentine IGs/DOCs recently updated
python3 scripts/lm_studio_auditor.py --country Argentina --mode full
```

### Scenario E: Overnight Content Generation Session
```bash
# Starts immediately and runs for 3 hours:
python3 scripts/overnight_worker.py

# Keep running all night until a specific time in the morning:
python3 scripts/overnight_worker.py --end 07:00
```

---

## 5. Detailed Component Documentation

### 5.1. `audit_manager.sh` (CLI Background Controller)
*   `./scripts/audit_manager.sh start [options]`: Launches `lm_studio_auditor.py` in the background with `nohup`.
*   `./scripts/audit_manager.sh stop`: Sends `SIGTERM`, saves state, and cleanly terminates.
*   `./scripts/audit_manager.sh status`: Displays summary metrics and process state.
*   `./scripts/audit_manager.sh logs`: Streams live output from the log file.
*   `./scripts/audit_manager.sh quick`: Fast physical file and geometry verification in 2 seconds.

---

### 5.2. `lm_studio_auditor.py` (Wine Intelligence Audit Engine)
An analytical tool evaluating consistency between the canonical map (`data/wine_regions.geojson`), official specification documents (`DOWNs/DOCs/`), and official registries (MAPA, eAmbrosia).

#### CLI Arguments:
```
python3 scripts/lm_studio_auditor.py [options]

  --country COUNTRY     Country to audit (e.g. Spain, France, Czechia, Argentina or all)
  --mode MODE           Audit mode:
                        - full: Complete audit (physical pliego check + LM Studio query)
                        - spain_mapa: Specific cross-check against MAPA official registry PDF
                        - pliegos: Ultra-fast physical disk check without LLM calls
  --limit N             Maximum number of regions to process in this run
  --delay S             Cooldown seconds between LLM calls to prevent thermal throttling (default: 1.5s)
  --status              Print current state metrics summary and exit
  --reset               Reset state checkpoint file to start from scratch
  --force               Re-audit regions previously marked as completed
```

#### Output Artifacts:
1.  [`reports/AUDIT_WINE_REGIONS_LMSTUDIO.md`](file:///Users/jreyes13/GitHub/wine3ai/reports/AUDIT_WINE_REGIONS_LMSTUDIO.md): Human-readable Markdown summary with breakdown tables.
2.  [`reports/audit_findings.json`](file:///Users/jreyes13/GitHub/wine3ai/reports/audit_findings.json): Structured JSON file containing all flagged issues.
3.  [`reports/audit_state.json`](file:///Users/jreyes13/GitHub/wine3ai/reports/audit_state.json): Resumable state tracker preventing redundant queries.

---

### 5.3. `overnight_worker.py` (Educational Content Generator)
Processes an internal catalog of 370 sommelier study units (WSET Level 3, CMS, ASI) and technical encyclopedia entries.
*   Saves batch checkpoints into `data/generated/`.
*   Automatically invokes `compile_generated_data.py` and creates `OVERNIGHT_REPORT.md` upon completion.

---

### 5.4. `compile_generated_data.py` (Production Atomic Compiler)
Safely compiles JSON checkpoints into production JavaScript and JSON files loaded by the web app using `/System/Library/Frameworks/JavaScriptCore.framework/Versions/Current/Helpers/jsc`.

---

### 5.5. `lm_studio.py` (Local Client Library)
Lightweight connector for programmatic queries to LM Studio (`http://127.0.0.1:1234/v1`).

---

## 6. LM Studio Requirements and Recommendations

1.  **LM Studio Server:** Must be running locally on `http://127.0.0.1:1234`.
2.  **Active Model:** Recommended model is `qwen/qwen3.5-9b` (or any model with context window >= 8192 tokens).
3.  **Token Budget:** Set `max_tokens` between 1200 and 2500 for reasoning models (CoT).
4.  **Zero Cost:** All computation runs exclusively on local hardware (Mac Unified Memory / GPU). No external APIs are called.
