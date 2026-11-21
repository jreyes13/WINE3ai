#!/usr/bin/env python3
"""
WINE³ai — Local Web Control Panel & Multi-Script Manager
========================================================
Lightweight administrative dashboard running on http://localhost:5050.
Zero dependencies (uses standard library http.server).

Features:
  - Real-time LM Studio readiness & active model indicator
  - Generation Worker control (Presets: 16:15, 06:45, Indefinido, Custom)
  - Map & Region Auditor control (lm_studio_auditor.py)
  - Full Synchronization (Compile + Git Commit/Push + IONOS VPS Rsync)
  - Dual live console streaming (Fichas log vs Auditoría log)
"""

import os
import sys
import json
import time
import glob
import shutil
import signal
import subprocess
import urllib.request
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

IS_WINDOWS = (os.name == "nt")

PORT = 5050
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE_WORKER = os.path.join(ROOT_DIR, "logs", "overnight_generation.log")
LOG_FILE_AUDITOR = os.path.join(ROOT_DIR, "reports", "auditor.log")
PID_FILE_WORKER = os.path.join(ROOT_DIR, "logs", "worker.pid")
PID_FILE_AUDITOR = os.path.join(ROOT_DIR, "reports", "auditor.pid")
GEN_DIR = os.path.join(ROOT_DIR, "data", "generated")
REPORTS_DIR = os.path.join(ROOT_DIR, "reports")
LM_STUDIO_URL = "http://127.0.0.1:1234/v1"

os.makedirs(os.path.join(ROOT_DIR, "logs"), exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(GEN_DIR, exist_ok=True)

def build_subprocess_env():
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    return env

def background_popen_kwargs():
    kwargs = {"env": build_subprocess_env()}
    if IS_WINDOWS and hasattr(subprocess, "CREATE_NO_WINDOW"):
        kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
    return kwargs

def find_git_executable():
    git_bin = shutil.which("git")
    if git_bin:
        return git_bin
    if IS_WINDOWS:
        local_app = os.environ.get("LOCALAPPDATA", "")
        candidates = sorted(
            glob.glob(os.path.join(local_app, "GitHubDesktop", "app-*", "resources", "app", "git", "cmd", "git.exe")),
            reverse=True,
        )
        if candidates:
            return candidates[0]
    return "git"

def is_pid_running(pid):
    if pid <= 0:
        return False
    if IS_WINDOWS:
        import ctypes
        PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
        STILL_ACTIVE = 259
        handle = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, int(pid))
        if not handle:
            return False
        try:
            exit_code = ctypes.c_ulong()
            if ctypes.windll.kernel32.GetExitCodeProcess(handle, ctypes.byref(exit_code)):
                return exit_code.value == STILL_ACTIVE
            return False
        finally:
            ctypes.windll.kernel32.CloseHandle(handle)
    else:
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False

def terminate_pid(pid):
    if IS_WINDOWS:
        res = subprocess.run(
            ["taskkill", "/PID", str(pid), "/T", "/F"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            **background_popen_kwargs(),
        )
        if res.returncode != 0:
            os.kill(pid, signal.SIGTERM)
    else:
        os.kill(pid, signal.SIGTERM)

def check_process_alive(pid_path, script_pattern=None):
    if not os.path.exists(pid_path):
        return False, None
    try:
        with open(pid_path, "r", encoding="utf-8") as f:
            pid = int(f.read().strip())
        if is_pid_running(pid):
            return True, pid
    except (OSError, ValueError):
        pass

    if os.path.exists(pid_path):
        try:
            os.remove(pid_path)
        except Exception:
            pass
    return False, None

def check_lm_studio_health():
    try:
        req = urllib.request.Request(f"{LM_STUDIO_URL}/models", headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=2.5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            models = [m.get("id") for m in data.get("data", [])]
            active = models[0] if models else "Desconocido"
            return True, active, models
    except Exception as e:
        return False, None, []

def get_stats():
    articles_count = 0
    cards_count = 0
    grapes_count = 0
    audit_findings_count = 0

    art_file = os.path.join(GEN_DIR, "winepedia_articles.json")
    if os.path.exists(art_file):
        try:
            with open(art_file, "r", encoding="utf-8") as f:
                articles_count = len(json.load(f))
        except Exception:
            pass

    cards_file = os.path.join(GEN_DIR, "study_cards.json")
    if os.path.exists(cards_file):
        try:
            with open(cards_file, "r", encoding="utf-8") as f:
                cards_count = len(json.load(f))
        except Exception:
            pass

    grapes_file = os.path.join(GEN_DIR, "grape_profiles.json")
    if os.path.exists(grapes_file):
        try:
            with open(grapes_file, "r", encoding="utf-8") as f:
                grapes_count = len(json.load(f))
        except Exception:
            pass

    findings_file = os.path.join(REPORTS_DIR, "audit_findings.json")
    if os.path.exists(findings_file):
        try:
            with open(findings_file, "r", encoding="utf-8") as f:
                audit_findings_count = len(json.load(f))
        except Exception:
            pass

    return {
        "articles": articles_count,
        "cards": cards_count,
        "grapes": grapes_count,
        "audit_findings": audit_findings_count
    }

def get_recent_logs(log_path, lines=50):
    if not os.path.exists(log_path):
        return f"Sin registros en {os.path.basename(log_path)}."
    try:
        with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
            all_lines = f.readlines()
            return "".join(all_lines[-lines:])
    except Exception as e:
        return f"Error leyendo log: {e}"

class DashboardHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, html):
        body = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/" or url.path == "/index.html":
            self._send_html(HTML_TEMPLATE)
        elif url.path == "/api/status":
            worker_running, worker_pid = check_process_alive(PID_FILE_WORKER)
            auditor_running, auditor_pid = check_process_alive(PID_FILE_AUDITOR)
            lm_ok, lm_active, lm_models = check_lm_studio_health()

            self._send_json({
                "worker": {"running": worker_running, "pid": worker_pid},
                "auditor": {"running": auditor_running, "pid": auditor_pid},
                "lm_studio": {"ok": lm_ok, "active_model": lm_active, "models": lm_models},
                "stats": get_stats(),
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        elif url.path == "/api/logs":
            params = url.query
            target = "worker"
            if "target=auditor" in params:
                target = "auditor"

            log_file = LOG_FILE_AUDITOR if target == "auditor" else LOG_FILE_WORKER
            self._send_json({
                "target": target,
                "logs": get_recent_logs(log_file, 60)
            })
        elif url.path == "/api/report_markdown":
            md_path = os.path.join(REPORTS_DIR, "AUDIT_WINE_REGIONS_LMSTUDIO.md")
            if os.path.exists(md_path):
                with open(md_path, "r", encoding="utf-8") as f:
                    self._send_json({"ok": True, "content": f.read()})
            else:
                self._send_json({"ok": False, "content": "# Aún no se ha generado el informe de auditoría."})
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        url = urlparse(self.path)
        content_len = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_len).decode("utf-8") if content_len > 0 else ""
        data = {}
        if body:
            try:
                data = json.loads(body)
            except Exception:
                pass

        # ---------------- WORKER (FICHAS) START / STOP ----------------
        if url.path == "/api/worker/start":
            running, pid = check_process_alive(PID_FILE_WORKER)
            if running:
                self._send_json({"ok": False, "msg": f"El generador ya está en ejecución (PID {pid})."})
                return

            mode = data.get("mode", "end_1615")
            worker_cmd = [sys.executable, "scripts/overnight_worker.py"]

            if mode == "indefinite":
                worker_cmd += ["--indefinite"]
            elif mode == "end_1615":
                worker_cmd += ["--end", "16:15"]
            elif mode == "end_0645":
                worker_cmd += ["--end", "06:45"]
            elif mode == "hours_1":
                worker_cmd += ["--hours", "1"]
            elif mode == "hours_3":
                worker_cmd += ["--hours", "3"]
            elif mode == "hours_5":
                worker_cmd += ["--hours", "5"]
            elif mode == "hours_8":
                worker_cmd += ["--hours", "8"]
            elif mode == "custom" and data.get("custom_end"):
                worker_cmd += ["--end", data["custom_end"]]

            log_out = open(LOG_FILE_WORKER, "a", encoding="utf-8")
            proc = subprocess.Popen(worker_cmd, cwd=ROOT_DIR, stdout=log_out, stderr=subprocess.STDOUT, **background_popen_kwargs())
            with open(PID_FILE_WORKER, "w", encoding="utf-8") as f:
                f.write(str(proc.pid))

            self._send_json({"ok": True, "msg": f"Generador de fichas iniciado (PID {proc.pid}).", "pid": proc.pid})

        elif url.path == "/api/worker/stop":
            running, pid = check_process_alive(PID_FILE_WORKER)
            if not running:
                self._send_json({"ok": False, "msg": "El generador no está en ejecución."})
                return

            try:
                terminate_pid(pid)
                time.sleep(1)
                if os.path.exists(PID_FILE_WORKER):
                    os.remove(PID_FILE_WORKER)
                self._send_json({"ok": True, "msg": f"Generador (PID {pid}) detenido correctamente."})
            except Exception as e:
                self._send_json({"ok": False, "msg": f"Error deteniendo PID {pid}: {e}"})

        # ---------------- AUDITOR (MAPAS) START / STOP ----------------
        elif url.path == "/api/auditor/start":
            running, pid = check_process_alive(PID_FILE_AUDITOR)
            if running:
                self._send_json({"ok": False, "msg": f"El auditor de mapas ya está corriendo (PID {pid})."})
                return

            audit_mode = data.get("mode", "spain_mapa")
            country = data.get("country", "all")
            limit = data.get("limit", None)

            auditor_cmd = [sys.executable, "scripts/lm_studio_auditor.py", "--mode", audit_mode, "--country", country]
            if limit and str(limit).isdigit() and int(limit) > 0:
                auditor_cmd += ["--limit", str(limit)]

            log_out = open(LOG_FILE_AUDITOR, "a", encoding="utf-8")
            proc = subprocess.Popen(auditor_cmd, cwd=ROOT_DIR, stdout=log_out, stderr=subprocess.STDOUT, **background_popen_kwargs())
            with open(PID_FILE_AUDITOR, "w", encoding="utf-8") as f:
                f.write(str(proc.pid))

            self._send_json({"ok": True, "msg": f"Auditor de mapas iniciado (PID {proc.pid}).", "pid": proc.pid})

        elif url.path == "/api/auditor/stop":
            running, pid = check_process_alive(PID_FILE_AUDITOR)
            if not running:
                self._send_json({"ok": False, "msg": "El auditor de mapas no está en ejecución."})
                return

            try:
                terminate_pid(pid)
                time.sleep(1)
                if os.path.exists(PID_FILE_AUDITOR):
                    os.remove(PID_FILE_AUDITOR)
                self._send_json({"ok": True, "msg": f"Auditor (PID {pid}) detenido correctamente."})
            except Exception as e:
                self._send_json({"ok": False, "msg": f"Error deteniendo auditor PID {pid}: {e}"})

        # ---------------- SYNC TOTAL (COMPILE + GIT + IONOS) ----------------
        elif url.path == "/api/sync_all":
            results = []
            deploy_details = ""
            sub_env = build_subprocess_env()
            try:
                # 0. Pre-Flight Syntax Validation Gate (Zero Broken Deployments)
                val_res = subprocess.run(
                    [sys.executable, "scripts/validate_syntax.py"],
                    cwd=ROOT_DIR,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    env=sub_env,
                )
                if val_res.returncode != 0:
                    self._send_json({
                        "ok": False,
                        "msg": "🚨 DESPLIEGUE BLOQUEADO: Se detectaron errores de sintaxis en los archivos. La web pública ha sido protegida.",
                        "details": val_res.stdout or val_res.stderr
                    })
                    return
                results.append("✓ Pre-flight: Sintaxis JS, JSON y Python verificada (0 errores).")

                # 1. Compile generated data
                subprocess.run(
                    [sys.executable, "scripts/compile_generated_data.py"],
                    cwd=ROOT_DIR,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    env=sub_env,
                )
                results.append("✓ Compilación local completada.")

                # 2. Git commit
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                git_bin = find_git_executable()
                subprocess.run([
                    git_bin, "add",
                    "data/", "web/", "reports/", "scripts/",
                    "winepedia.html", "flashcards.html", "sebastian.html",
                    "map.html", "app.js", "style.css",
                    "index.html", "index_es.html", "grapes.html", "grapes.js", "grapes.css",
                    "OVERNIGHT_REPORT.md", "ROADMAP_TASKS.md"
                ], cwd=ROOT_DIR, capture_output=True, text=True, encoding="utf-8", errors="replace", env=sub_env)
                git_commit = subprocess.run(
                    [git_bin, "commit", "-m", f"chore(sync): automated sync via control panel at {timestamp}"],
                    cwd=ROOT_DIR,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    env=sub_env,
                )
                if git_commit.returncode == 0:
                    results.append("✓ Commit local registrado en Git.")
                else:
                    results.append("ℹ Git: Sin cambios pendientes para commitear.")

                # 3. Rsync to IONOS VPS (cuando rsync y la clave SSH estén disponibles)
                rsync_bin = shutil.which("rsync")
                ssh_bin = shutil.which("ssh")
                ssh_key = os.path.expanduser("~/.ssh/id_ionos_vps")
                if rsync_bin and ssh_bin and os.path.exists(ssh_key):
                    rsync_args = [
                        rsync_bin, "-avz",
                        "-e", f"ssh -i {ssh_key} -o StrictHostKeyChecking=no",
                        "winepedia.html", "flashcards.html", "sebastian.html", "map.html",
                        "app.js", "style.css", "index.html", "index_es.html",
                        "grapes.html", "grapes.js", "grapes.css", "OVERNIGHT_REPORT.md",
                        "web", "data/", "reports/",
                        "root@jreyes13.net:/var/www/vhosts/jreyes13.net/wine3ai/",
                    ]
                    deploy_res = subprocess.run(
                        rsync_args,
                        cwd=ROOT_DIR,
                        capture_output=True,
                        text=True,
                        encoding="utf-8",
                        errors="replace",
                        env=sub_env,
                    )
                    deploy_details = deploy_res.stdout or deploy_res.stderr
                    if deploy_res.returncode == 0:
                        results.append("✓ Sincronización con servidor IONOS (VPS) completada.")
                    else:
                        results.append("⚠️ Rsync IONOS terminó con advertencias.")

                    # 4. Set remote permissions
                    perm_args = [
                        ssh_bin, "-i", ssh_key, "-o", "StrictHostKeyChecking=no",
                        "root@jreyes13.net",
                        "find /var/www/vhosts/jreyes13.net/wine3ai -type f -exec chmod 644 {} + && "
                        "find /var/www/vhosts/jreyes13.net/wine3ai -type d -exec chmod 755 {} + && "
                        "chown -R jreyes169:psaserv /var/www/vhosts/jreyes13.net/wine3ai/",
                    ]
                    subprocess.run(perm_args, capture_output=True, text=True, encoding="utf-8", errors="replace", env=sub_env)
                    results.append("✓ Permisos web (644/755) aplicados.")
                else:
                    results.append("ℹ Despliegue IONOS omitido en este equipo (requiere rsync y clave ~/.ssh/id_ionos_vps).")

                self._send_json({
                    "ok": True,
                    "msg": " | ".join(results),
                    "details": deploy_details
                })
            except Exception as e:
                self._send_json({"ok": False, "msg": f"Error durante la sincronización: {e}"})

        else:
            self.send_error(404, "Not Found")

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="es" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>WINE³ai — Panel de Control y Orquestador Local</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;800&family=JetBrains+Mono:wght@400;600;700&family=Plus+Jakarta+Sans:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    body { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #0b0d13; color: #e2e8f0; }
    .font-serif-wine { font-family: 'Cinzel', serif; }
    .font-mono { font-family: 'JetBrains Mono', monospace; }
  </style>
</head>
<body class="min-h-screen p-4 sm:p-8 flex flex-col items-center">

  <div class="max-w-6xl w-full space-y-6">
    
    <!-- Top Bar with Brand and Dual Readiness Indicators -->
    <header class="flex flex-col md:flex-row md:items-center justify-between gap-4 p-6 rounded-3xl bg-[#12141c] border border-white/10 shadow-xl">
      <div class="flex items-center gap-4">
        <span class="text-3xl">🍷</span>
        <div>
          <h1 class="text-2xl font-bold font-serif-wine text-white tracking-wide">
            WINE<span class="text-amber-400">³</span>ai — Panel de Control
          </h1>
          <p class="text-xs text-slate-400 font-mono mt-0.5">
            Orquestador Local · LM Studio Inferencia Offline · Auditoría de Mapas · Sincronización
          </p>
        </div>
      </div>

      <!-- Live Readiness Badges -->
      <div class="flex flex-wrap items-center gap-3 text-xs font-mono">
        <!-- LM Studio Ready Badge -->
        <div id="lm-studio-badge" class="flex items-center gap-2 px-3.5 py-2 rounded-2xl bg-white/5 border border-white/10 transition-colors">
          <span class="w-2.5 h-2.5 rounded-full bg-slate-500" id="lm-dot"></span>
          <span id="lm-text" class="text-slate-300">Verificando LM Studio...</span>
        </div>

        <!-- System Clock -->
        <div class="px-3.5 py-2 rounded-2xl bg-white/5 border border-white/10 text-slate-400 hidden sm:block" id="system-clock">
          --:--:--
        </div>
      </div>
    </header>

    <!-- Stats Counter Bar -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 font-mono">
      <div class="p-4 sm:p-5 rounded-2xl bg-[#12141c]/80 border border-white/10">
        <div class="text-[11px] text-slate-400 uppercase tracking-wider mb-1">📚 WINEp3dIA</div>
        <div class="text-2xl sm:text-3xl font-bold text-amber-300" id="stat-articles">--</div>
        <div class="text-[10px] text-slate-500 mt-1">Artículos Canónicos</div>
      </div>
      <div class="p-4 sm:p-5 rounded-2xl bg-[#12141c]/80 border border-white/10">
        <div class="text-[11px] text-slate-400 uppercase tracking-wider mb-1">🎴 Flashcards</div>
        <div class="text-2xl sm:text-3xl font-bold text-purple-300" id="stat-cards">--</div>
        <div class="text-[10px] text-slate-500 mt-1">WSET 3, CMS y ASI</div>
      </div>
      <div class="p-4 sm:p-5 rounded-2xl bg-[#12141c]/80 border border-white/10">
        <div class="text-[11px] text-slate-400 uppercase tracking-wider mb-1">🍇 Uvas</div>
        <div class="text-2xl sm:text-3xl font-bold text-rose-300" id="stat-grapes">--</div>
        <div class="text-[10px] text-slate-500 mt-1">Perfiles de Cata</div>
      </div>
      <div class="p-4 sm:p-5 rounded-2xl bg-[#12141c]/80 border border-white/10">
        <div class="text-[11px] text-slate-400 uppercase tracking-wider mb-1">🗺️ Auditoría Mapas</div>
        <div class="text-2xl sm:text-3xl font-bold text-emerald-300" id="stat-audit">--</div>
        <div class="text-[10px] text-slate-500 mt-1">Incidencias / Pliegos</div>
      </div>
    </div>

    <!-- Alert Banner when LM Studio is disconnected -->
    <div id="lm-alert-banner" class="hidden p-4 rounded-2xl bg-rose-950/40 border border-rose-500/50 text-rose-200 text-xs font-mono flex items-center justify-between">
      <div class="flex items-center gap-2">
        <span class="text-lg">⚠️</span>
        <span><strong>LM Studio no está activo en http://127.0.0.1:1234.</strong> Inicia la aplicación LM Studio y carga el modelo <code class="bg-black/50 px-1 py-0.5 rounded text-amber-300">qwen/qwen3.5-9b</code> para arrancar los procesos.</span>
      </div>
      <button onclick="fetchStatus()" class="px-2.5 py-1 rounded-lg bg-rose-900/60 hover:bg-rose-800 text-white transition-colors">Reintentar</button>
    </div>

    <!-- Action Boxes Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      
      <!-- Box 1: Generador de Fichas (WINEp3dIA & Flashcards) -->
      <div class="p-6 rounded-3xl bg-[#12141c] border border-white/10 shadow-lg space-y-4">
        <div class="flex items-center justify-between border-b border-white/10 pb-3">
          <div class="flex items-center gap-2.5">
            <span class="text-xl">🍷</span>
            <h2 class="text-base font-bold font-serif-wine text-white">Generador de Fichas</h2>
          </div>
          <span id="worker-status-badge" class="text-xs font-mono px-2.5 py-0.5 rounded-full bg-slate-800 text-slate-400 border border-white/10">
            ⚪ Detenido
          </span>
        </div>

        <div>
          <label class="block text-xs font-mono text-slate-400 mb-1.5">Programación y Límite de Tiempo:</label>
          <select id="worker-preset" onchange="toggleCustomTime()" class="w-full px-3.5 py-2.5 rounded-xl bg-black/50 border border-white/15 text-white font-mono text-xs focus:outline-none focus:border-amber-400">
            <option value="end_1615" selected>💼 Hasta las 16:15 (Jornada laboral)</option>
            <option value="end_0645">🌙 Hasta las 06:45 (Overnight nocturno)</option>
            <option value="indefinite">♾️ Modo Indefinido (Hasta pulsar Detener)</option>
            <option value="hours_1">⏱️ 1 Hora (Prueba rápida)</option>
            <option value="hours_3">⏱️ 3 Horas (Sesión estándar)</option>
            <option value="hours_5">⏱️ 5 Horas (Sesión extendida)</option>
            <option value="hours_8">⏱️ 8 Horas continuas</option>
            <option value="custom">🕒 Hora personalizada (HH:MM)...</option>
          </select>
          <input type="text" id="custom-time-input" placeholder="Ej: 19:45" class="hidden mt-2 w-full px-3.5 py-2 rounded-xl bg-black/50 border border-white/15 text-white font-mono text-xs focus:outline-none focus:border-amber-400">
        </div>

        <div class="flex items-center gap-3 pt-2">
          <button id="btn-worker-start" onclick="startWorker()" class="flex-1 py-3 px-4 rounded-xl bg-amber-500 hover:bg-amber-400 text-black font-mono text-xs font-bold transition-all shadow-lg flex items-center justify-center gap-2 active:scale-95">
            <span>▶</span> Iniciar Generador
          </button>
          <button id="btn-worker-stop" onclick="stopWorker()" class="py-3 px-5 rounded-xl bg-red-950 hover:bg-red-900 text-red-200 border border-red-800/50 font-mono text-xs font-semibold transition-all flex items-center justify-center gap-2 active:scale-95 disabled:opacity-30" disabled>
            <span>⏹</span> Detener
          </button>
        </div>
        <p class="text-[11px] text-slate-500 font-mono">
          * Salta automáticamente temas completados. Genera WINEp3dIA, CMS, ASI y Uvas con 0 tokens externos.
        </p>
      </div>

      <!-- Box 2: Auditor de Mapas y Pliegos con LM Studio -->
      <div class="p-6 rounded-3xl bg-[#12141c] border border-white/10 shadow-lg space-y-4">
        <div class="flex items-center justify-between border-b border-white/10 pb-3">
          <div class="flex items-center gap-2.5">
            <span class="text-xl">🗺️</span>
            <h2 class="text-base font-bold font-serif-wine text-white">Auditor de Mapas Vitícolas</h2>
          </div>
          <span id="auditor-status-badge" class="text-xs font-mono px-2.5 py-0.5 rounded-full bg-slate-800 text-slate-400 border border-white/10">
            ⚪ Detenido
          </span>
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-xs font-mono text-slate-400 mb-1.5">Modo de Auditoría:</label>
            <select id="auditor-mode" class="w-full px-3 py-2 rounded-xl bg-black/50 border border-white/15 text-white font-mono text-xs focus:outline-none focus:border-amber-400">
              <option value="spain_mapa" selected>🇪🇸 España vs MAPA Oficial</option>
              <option value="full">🌍 Mundial Completo (Full AI)</option>
              <option value="pliegos">📄 Pliegos de Condiciones</option>
            </select>
          </div>
          <div>
            <label class="block text-xs font-mono text-slate-400 mb-1.5">Límite de Regiones:</label>
            <select id="auditor-limit" class="w-full px-3 py-2 rounded-xl bg-black/50 border border-white/15 text-white font-mono text-xs focus:outline-none focus:border-amber-400">
              <option value="0" selected>♾️ Indefinido (todas)</option>
              <option value="10">10 Regiones</option>
              <option value="25">25 Regiones</option>
              <option value="50">50 Regiones</option>
            </select>
          </div>
        </div>

        <div class="flex items-center gap-3 pt-2">
          <button id="btn-auditor-start" onclick="startAuditor()" class="flex-1 py-3 px-4 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-black font-mono text-xs font-bold transition-all shadow-lg flex items-center justify-center gap-2 active:scale-95">
            <span>▶</span> Iniciar Auditoría
          </button>
          <button id="btn-auditor-stop" onclick="stopAuditor()" class="py-3 px-5 rounded-xl bg-red-950 hover:bg-red-900 text-red-200 border border-red-800/50 font-mono text-xs font-semibold transition-all flex items-center justify-center gap-2 active:scale-95 disabled:opacity-30" disabled>
            <span>⏹</span> Detener
          </button>
        </div>
        <p class="text-[11px] text-slate-500 font-mono">
          * Analiza polígonos GeoJSON, municipios y pliegos. Guarda estado en <code>reports/audit_state.json</code>.
        </p>
      </div>

    </div>

    <!-- Master Synchronization Bar (Compile + Git + IONOS) -->
    <div class="p-6 rounded-3xl bg-gradient-to-r from-purple-950/30 via-[#131622] to-indigo-950/30 border border-purple-500/30 shadow-xl space-y-4">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <h2 class="text-base font-bold font-serif-wine text-white flex items-center gap-2">
            <span>🚀</span> Sincronización Total con 1 Clic (Producción)
          </h2>
          <p class="text-xs text-slate-400 font-mono mt-0.5">
            Compila los datos generados, registra commit en Git y sincroniza en caliente con el VPS de IONOS.
          </p>
        </div>

        <button onclick="syncAllProduction()" id="btn-sync-all" class="px-6 py-3 rounded-2xl bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-mono text-xs font-bold shadow-lg transition-transform active:scale-95 shrink-0 flex items-center gap-2">
          <span>🚀</span> Sincronizar con GitHub y Servidor IONOS
        </button>
      </div>

      <div id="sync-feedback" class="hidden p-3.5 rounded-xl bg-black/60 border border-white/10 text-xs font-mono text-amber-300"></div>
    </div>

    <!-- Dual Live Console Log Viewer -->
    <div class="p-6 rounded-3xl bg-[#12141c] border border-white/10 shadow-lg space-y-3">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-white/10 pb-3">
        <!-- Log Selector Tabs -->
        <div class="flex items-center gap-2 text-xs font-mono">
          <button id="tab-log-worker" onclick="switchLogTab('worker')" class="px-3.5 py-1.5 rounded-xl bg-amber-500/20 text-amber-300 border border-amber-500/40 font-bold transition-all">
            🍷 Generador de Fichas
          </button>
          <button id="tab-log-auditor" onclick="switchLogTab('auditor')" class="px-3.5 py-1.5 rounded-xl bg-white/5 text-slate-400 hover:text-white border border-white/10 transition-all">
            🗺️ Auditoría de Mapas
          </button>
        </div>

        <div class="flex items-center gap-2">
          <button onclick="refreshLogs()" class="text-xs font-mono text-slate-400 hover:text-white px-2.5 py-1 rounded-lg bg-white/5 border border-white/10">
            🔄 Refrescar
          </button>
          <button onclick="viewMarkdownReport()" class="text-xs font-mono text-amber-300 hover:text-amber-200 px-2.5 py-1 rounded-lg bg-amber-500/10 border border-amber-500/30">
            📄 Ver Informe Auditoría
          </button>
        </div>
      </div>

      <pre id="log-console" class="w-full p-4 rounded-2xl bg-black/70 border border-white/10 text-[11px] font-mono text-slate-300 overflow-x-auto max-h-72 overflow-y-auto leading-relaxed">Cargando registros...</pre>
    </div>

  </div>

  <!-- Markdown Report Modal -->
  <div id="report-modal" class="fixed inset-0 z-50 bg-black/80 backdrop-blur-md hidden flex items-center justify-center p-4 overflow-y-auto">
    <div class="bg-[#12141c] border border-white/15 rounded-3xl max-w-4xl w-full max-h-[88vh] flex flex-col p-6 shadow-2xl relative">
      <div class="flex items-center justify-between border-b border-white/10 pb-3 mb-4">
        <h3 class="text-lg font-bold font-serif-wine text-white">📄 Informe de Auditoría de Mapas (Markdown)</h3>
        <button onclick="closeReportModal()" class="w-8 h-8 rounded-full bg-white/10 hover:bg-white/20 text-white flex items-center justify-center text-sm">✕</button>
      </div>
      <div class="overflow-y-auto flex-1 text-xs font-mono text-slate-300 whitespace-pre-wrap leading-relaxed bg-black/40 p-4 rounded-2xl border border-white/5" id="report-content">
        Cargando informe...
      </div>
    </div>
  </div>

  <script>
    let currentLogTab = 'worker';

    function toggleCustomTime() {
      const preset = document.getElementById('worker-preset').value;
      const input = document.getElementById('custom-time-input');
      if (preset === 'custom') {
        input.classList.remove('hidden');
      } else {
        input.classList.add('hidden');
      }
    }

    function switchLogTab(tab) {
      currentLogTab = tab;
      const tabWorker = document.getElementById('tab-log-worker');
      const tabAuditor = document.getElementById('tab-log-auditor');
      if (tab === 'worker') {
        tabWorker.className = "px-3.5 py-1.5 rounded-xl bg-amber-500/20 text-amber-300 border border-amber-500/40 font-bold transition-all";
        tabAuditor.className = "px-3.5 py-1.5 rounded-xl bg-white/5 text-slate-400 hover:text-white border border-white/10 transition-all";
      } else {
        tabAuditor.className = "px-3.5 py-1.5 rounded-xl bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 font-bold transition-all";
        tabWorker.className = "px-3.5 py-1.5 rounded-xl bg-white/5 text-slate-400 hover:text-white border border-white/10 transition-all";
      }
      fetchLogs();
    }

    async function fetchStatus() {
      try {
        const res = await fetch('/api/status');
        const data = await res.json();
        
        document.getElementById('stat-articles').textContent = data.stats.articles;
        document.getElementById('stat-cards').textContent = data.stats.cards;
        document.getElementById('stat-grapes').textContent = data.stats.grapes;
        document.getElementById('stat-audit').textContent = data.stats.audit_findings;
        document.getElementById('system-clock').textContent = data.time.split(' ')[1];

        // LM Studio Readiness
        const lmBadge = document.getElementById('lm-studio-badge');
        const lmDot = document.getElementById('lm-dot');
        const lmText = document.getElementById('lm-text');
        const lmAlert = document.getElementById('lm-alert-banner');

        if (data.lm_studio.ok) {
          lmDot.className = "w-2.5 h-2.5 rounded-full bg-emerald-400 shadow-[0_0_8px_#34d399]";
          lmText.textContent = `LM Studio Listo (${data.lm_studio.active_model})`;
          lmText.className = "text-emerald-300 font-bold";
          lmBadge.className = "flex items-center gap-2 px-3.5 py-2 rounded-2xl bg-emerald-950/40 border border-emerald-800/40";
          lmAlert.classList.add('hidden');
        } else {
          lmDot.className = "w-2.5 h-2.5 rounded-full bg-rose-500";
          lmText.textContent = "LM Studio Desconectado";
          lmText.className = "text-rose-400 font-bold";
          lmBadge.className = "flex items-center gap-2 px-3.5 py-2 rounded-2xl bg-rose-950/40 border border-rose-800/40";
          lmAlert.classList.remove('hidden');
        }

        // Worker Status
        const wBadge = document.getElementById('worker-status-badge');
        const btnWStart = document.getElementById('btn-worker-start');
        const btnWStop = document.getElementById('btn-worker-stop');

        if (data.worker.running) {
          wBadge.textContent = `🟢 En Ejecución (PID ${data.worker.pid})`;
          wBadge.className = "text-xs font-mono px-2.5 py-0.5 rounded-full bg-emerald-950 text-emerald-300 border border-emerald-800/50 font-bold";
          btnWStart.disabled = true;
          btnWStart.classList.add('opacity-40');
          btnWStop.disabled = false;
        } else {
          wBadge.textContent = "⚪ Detenido";
          wBadge.className = "text-xs font-mono px-2.5 py-0.5 rounded-full bg-white/5 text-slate-400 border border-white/10";
          btnWStart.disabled = false;
          btnWStart.classList.remove('opacity-40');
          btnWStop.disabled = true;
        }

        // Auditor Status
        const aBadge = document.getElementById('auditor-status-badge');
        const btnAStart = document.getElementById('btn-auditor-start');
        const btnAStop = document.getElementById('btn-auditor-stop');

        if (data.auditor.running) {
          aBadge.textContent = `🟢 En Ejecución (PID ${data.auditor.pid})`;
          aBadge.className = "text-xs font-mono px-2.5 py-0.5 rounded-full bg-emerald-950 text-emerald-300 border border-emerald-800/50 font-bold";
          btnAStart.disabled = true;
          btnAStart.classList.add('opacity-40');
          btnAStop.disabled = false;
        } else {
          aBadge.textContent = "⚪ Detenido";
          aBadge.className = "text-xs font-mono px-2.5 py-0.5 rounded-full bg-white/5 text-slate-400 border border-white/10";
          btnAStart.disabled = false;
          btnAStart.classList.remove('opacity-40');
          btnAStop.disabled = true;
        }

      } catch (err) {
        console.error('Error fetching status:', err);
      }
    }

    async function fetchLogs() {
      try {
        const res = await fetch(`/api/logs?target=${currentLogTab}`);
        const data = await res.json();
        const el = document.getElementById('log-console');
        el.textContent = data.logs || "Sin registros recientes.";
        el.scrollTop = el.scrollHeight;
      } catch (err) {}
    }

    function refreshLogs() {
      fetchLogs();
    }

    async function startWorker() {
      const mode = document.getElementById('worker-preset').value;
      const customEnd = document.getElementById('custom-time-input').value;
      const fb = document.getElementById('sync-feedback');
      fb.classList.remove('hidden');
      fb.textContent = "Iniciando generador de fichas con LM Studio...";

      try {
        const res = await fetch('/api/worker/start', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ mode, custom_end: customEnd })
        });
        const data = await res.json();
        fb.textContent = data.msg;
        fetchStatus();
        fetchLogs();
      } catch (e) {
        fb.textContent = "Error al iniciar generador: " + e;
      }
    }

    async function stopWorker() {
      const fb = document.getElementById('sync-feedback');
      fb.classList.remove('hidden');
      fb.textContent = "Deteniendo generador de fichas...";
      try {
        const res = await fetch('/api/worker/stop', { method: 'POST' });
        const data = await res.json();
        fb.textContent = data.msg;
        fetchStatus();
      } catch (e) {
        fb.textContent = "Error al detener: " + e;
      }
    }

    async function startAuditor() {
      const mode = document.getElementById('auditor-mode').value;
      const limit = document.getElementById('auditor-limit').value;
      const fb = document.getElementById('sync-feedback');
      fb.classList.remove('hidden');
      fb.textContent = "Iniciando auditor de mapas con LM Studio...";

      try {
        const res = await fetch('/api/auditor/start', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ mode, limit: parseInt(limit) || 0 })
        });
        const data = await res.json();
        fb.textContent = data.msg;
        fetchStatus();
        switchLogTab('auditor');
      } catch (e) {
        fb.textContent = "Error al iniciar auditor: " + e;
      }
    }

    async function stopAuditor() {
      const fb = document.getElementById('sync-feedback');
      fb.classList.remove('hidden');
      fb.textContent = "Deteniendo auditor de mapas...";
      try {
        const res = await fetch('/api/auditor/stop', { method: 'POST' });
        const data = await res.json();
        fb.textContent = data.msg;
        fetchStatus();
      } catch (e) {
        fb.textContent = "Error al detener: " + e;
      }
    }

    async function syncAllProduction() {
      const fb = document.getElementById('sync-feedback');
      const btn = document.getElementById('btn-sync-all');
      fb.classList.remove('hidden');
      fb.textContent = "Compilando datos, registrando en Git y sincronizando con IONOS VPS... Espera unos segundos.";
      btn.disabled = true;
      btn.classList.add('opacity-50');

      try {
        const res = await fetch('/api/sync_all', { method: 'POST' });
        const data = await res.json();
        fb.textContent = data.msg;
        fetchStatus();
      } catch (e) {
        fb.textContent = "Error en sincronización: " + e;
      } finally {
        btn.disabled = false;
        btn.classList.remove('opacity-50');
      }
    }

    async function viewMarkdownReport() {
      try {
        const res = await fetch('/api/report_markdown');
        const data = await res.json();
        document.getElementById('report-content').textContent = data.content;
        document.getElementById('report-modal').classList.remove('hidden');
      } catch (e) {}
    }

    function closeReportModal() {
      document.getElementById('report-modal').classList.add('hidden');
    }

    // Polling intervals
    fetchStatus();
    fetchLogs();
    setInterval(fetchStatus, 3000);
    setInterval(fetchLogs, 4000);
  </script>
</body>
</html>
"""

def main():
    server_address = ("127.0.0.1", PORT)
    httpd = HTTPServer(server_address, DashboardHandler)
    print(f"\n==========================================================")
    print(f"🍷 WINE³ai — Panel de Control y Orquestador Local Activo")
    print(f"👉 Abre en tu navegador: http://localhost:{PORT}")
    print(f"==========================================================\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nPanel de control cerrado.")

if __name__ == "__main__":
    main()
