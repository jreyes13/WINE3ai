# Scripts Guide and Operational Manual — WINE³ai

> **Versión en español disponible:** [README.md](file:///Users/jreyes13/GitHub/wine3ai/scripts/README.md)  
> **Directory:** `/scripts/`  
> **System Philosophy:** 100% Local, Absolute Privacy, **0 External Tokens** (Inference exclusively handled by local LM Studio at `http://127.0.0.1:1234/v1`).

---

## 1. Scripts Catalog and Overview

| Script | Language | Primary Purpose | When to Use |
| :--- | :--- | :--- | :--- |
| [`audit_manager.sh`](file:///Users/jreyes13/GitHub/wine3ai/scripts/audit_manager.sh) | Bash | Background daemon controller (start / stop / status / logs / quick). | **Recommended for daily use**: start and stop unattended audits during laptop idle time. |
| [`lm_studio_auditor.py`](file:///Users/jreyes13/GitHub/wine3ai/scripts/lm_studio_auditor.py) | Python 3 | Core analysis engine for wine regions, official specification pliegos, and geometries. | Direct interactive terminal runs, country filtering, or specialized audits (e.g., MAPA Spain). |
| [`overnight_worker.py`](file:///Users/jreyes13/GitHub/wine3ai/scripts/overnight_worker.py) | Python 3 | Autonomous overnight generator for sommelier flashcards (WSET3, CMS) and Winepedia articles. | Long unattended night runs scheduled by time or fixed duration. |
| [`compile_generated_data.py`](file:///Users/jreyes13/GitHub/wine3ai/scripts/compile_generated_data.py) | Python 3 | Atomic compiler using macOS `jsc` (JavaScriptCore) merging JSON checkpoints into production. | After generating articles/cards to safely consolidate into `data/` and `web/data/`. |
| [`lm_studio.py`](file:///Users/jreyes13/GitHub/wine3ai/scripts/lm_studio.py) | Python 3 | Reusable HTTP API client module connecting to LM Studio. | Programmatic helper library in scripts or quick terminal testing. |

---

## 2. Decision Matrix: "What to Run and When"

```
                 What task do you want to run?
                               │
       ┌───────────────────────┴───────────────────────┐
       ▼                                               ▼
[ AUDIT MAPS & PLIEGOS ]                     [ GENERATE EDUCATIONAL CONTENT ]
       │                                               │
       ├─ Laptop idle time (background)                ├─ Night session (default: 3h)
       │  └─> ./scripts/audit_manager.sh start         │  └─> python3 scripts/overnight_worker.py
       │                                               │
       ├─ I have 2 minutes (pliego file check only)   ├─ Run until 07:00 AM
       │  └─> ./scripts/audit_manager.sh quick         │  └─> python3 scripts/overnight_worker.py --end 07:00
       │                                               │
       ├─ Audit a specific country                     └─ Compile to web production:
       │  └─> python3 scripts/lm_studio_auditor.py --country Spain --mode spain_mapa
       │                                                  └─> python3 scripts/compile_generated_data.py
       └─ Stop and save state safely
          └─> ./scripts/audit_manager.sh stop
```

### Scenario A: Laptop Idle Time (Lunch, coffee breaks, or walking away)
Use the background manager script. It runs unattended, pauses briefly between regions to keep laptop temperatures cool, and is 100% safe to pause:
```bash
# Start background audit
./scripts/audit_manager.sh start

# Check current progress and metrics
./scripts/audit_manager.sh status

# Follow live LM Studio reasoning in real time (Ctrl+C exits viewer, process continues)
./scripts/audit_manager.sh logs

# Stop safely whenever you need the computer (auto-saves checkpoint)
./scripts/audit_manager.sh stop
```

### Scenario B: Instant Physical Pliego and Geometry Check (2 seconds)
Validates all 894 global wine regions on disk, reporting missing pliego PDFs, stub placeholders (<8KB), and rough/simplified polygons:
```bash
./scripts/audit_manager.sh quick
# or directly:
python3 scripts/lm_studio_auditor.py --mode pliegos
```

### Scenario C: Spain Deep Audit (Cross-referencing Official MAPA Registry)
Cross-references GeoJSON boundaries against the official Spanish Ministry of Agriculture document (`DOWNs/SPAIN/02_vinos.2026-07-03-13-01-22.pdf`), auditing municipalities against provincial borders and grape varieties:
```bash
python3 scripts/lm_studio_auditor.py --country Spain --mode spain_mapa
```

### Scenario D: Auditing a Specific Country (Czechia, Argentina, France...)
```bash
# Audit Czech Republic (detects placeholder pliegos and simplified geometries)
python3 scripts/lm_studio_auditor.py --country Czechia --mode full

# Audit all 26 Argentine IGs/DOCs recently restructured
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

## 3. Detailed Component Documentation

### 3.1. `audit_manager.sh` (Background Process Controller)
Manages the background execution lifecycle without requiring manual PID handling or keeping terminal sessions open.

*   `./scripts/audit_manager.sh start [options]`
    *   Launches `lm_studio_auditor.py` in the background with `nohup`.
    *   Passes through any custom arguments (e.g., `./scripts/audit_manager.sh start --country France`).
    *   Saves the process ID in `reports/auditor.pid`.
*   `./scripts/audit_manager.sh stop`
    *   Sends a `SIGTERM` signal. The auditor traps the signal, finishes the in-flight region, updates `reports/audit_state.json`, and terminates cleanly.
*   `./scripts/audit_manager.sh status`
    *   Reports whether the daemon is running or idle, and prints the updated dashboard summary.
*   `./scripts/audit_manager.sh logs`
    *   Runs `tail -f reports/auditor.log` to stream LM Studio queries and reasoning logs live.
*   `./scripts/audit_manager.sh quick`
    *   Runs the fast file-system and geometry check in 2 seconds.

---

### 3.2. `lm_studio_auditor.py` (Wine Intelligence Audit Engine)
An analytical tool evaluating consistency between the canonical map (`data/wine_regions.geojson`), official specification documents (`DOWNs/DOCs/`), and official registries (MAPA, eAmbrosia).

#### CLI Arguments:
```
python3 scripts/lm_studio_auditor.py [options]

  --country COUNTRY     Country to audit (e.g. Spain, France, Czechia, Argentina or all)
  --mode MODE           Audit mode:
                        - full: Complete audit (physical pliego check + LM Studio query)
                        - spain_mapa: Specific cross-check against MAPA official registry PDF
                        - pliegos: Ultra-fast physical disk check without LLM calls
  --limit N             Maximum number of regions to process in this run (ideal for short breaks)
  --delay S             Cooldown seconds between LLM calls to prevent thermal throttling (default: 1.5s)
  --status              Print current state metrics summary and exit
  --reset               Reset state checkpoint file to start from scratch
  --force               Re-audit regions previously marked as completed
```

#### Output Artifacts:
1.  [`reports/AUDIT_WINE_REGIONS_LMSTUDIO.md`](file:///Users/jreyes13/GitHub/wine3ai/reports/AUDIT_WINE_REGIONS_LMSTUDIO.md): Human-readable Markdown summary with breakdown tables by country and MAPA comparison.
2.  [`reports/audit_findings.json`](file:///Users/jreyes13/GitHub/wine3ai/reports/audit_findings.json): Structured JSON file containing all flagged issues, formatted for downstream AI analysis (e.g., Gemini).
3.  [`reports/audit_state.json`](file:///Users/jreyes13/GitHub/wine3ai/reports/audit_state.json): Resumable state tracker preventing redundant LLM queries across runs.

---

### 3.3. `overnight_worker.py` (Educational Content Generator)
Processes an internal catalog of 370 sommelier study units (WSET Level 3, CMS, ASI) and technical encyclopedia entries.

*   **CLI Options:**
    *   `--start HH:MM`: Scheduled start time (e.g., `23:30`).
    *   `--end HH:MM`: End cutoff time (e.g., `06:30`).
    *   `--hours N`: Fixed run duration in hours (e.g., `4.5`).
    *   `--now`: Start immediately without waiting.
*   **Workflow:**
    *   Saves batch checkpoints into `data/generated/`.
    *   Upon reaching time limits, automatically triggers `compile_generated_data.py` and produces `OVERNIGHT_REPORT.md`.

---

### 3.4. `compile_generated_data.py` (Production Atomic Compiler)
Safely compiles JSON checkpoints into production JavaScript and JSON files loaded by the web app:
*   Invokes `/System/Library/Frameworks/JavaScriptCore.framework/Versions/Current/Helpers/jsc` to evaluate and merge existing structures safely without AST syntax errors.
*   Synchronized production targets:
    *   `data/winepedia_articles.js` & `web/data/winepedia_articles.js`
    *   `data/study_cards.js` & `web/data/study_cards.js`
    *   `data/grape_varieties.json` & `web/data/grape_varieties.json`

---

### 3.5. `lm_studio.py` (Local Client Library)
Lightweight connector for programmatic queries to LM Studio (`http://127.0.0.1:1234/v1`).

```python
from scripts.lm_studio import query_lm

# Basic prompt
response = query_lm("Explain the terroir of Paraje Altamira in Mendoza.")

# Prompt with detailed reasoning token breakdown
response, stats = query_lm(
    prompt="Compare DOC Luján de Cuyo vs DOC San Rafael",
    model="qwen/qwen3.5-9b",
    return_usage=True
)
print(f"Generated tokens: {stats['completion_tokens']}, Reasoning: {stats.get('reasoning_tokens', 0)}")
```

---

## 4. LM Studio Requirements and Recommendations

1.  **LM Studio Server:** Must be running locally on `http://127.0.0.1:1234`.
2.  **Active Model:** Recommended model is `qwen/qwen3.5-9b` (or any model with context window >= 8192 tokens).
3.  **Token Budget:** When using reasoning models (Chain-of-Thought), configure `max_tokens` between 1200 and 2500 so the model has enough room to finish its thinking before generating the output conclusion.
4.  **Zero Cost:** All computation runs exclusively on local hardware (Mac Unified Memory / GPU). No external APIs are called.
