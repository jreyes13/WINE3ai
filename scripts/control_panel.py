#!/usr/bin/env python3
"""
WINE³ai — Local Web Control Panel & Script Manager
Lightweight administrative dashboard running on http://localhost:5050.
Zero dependencies (uses standard library http.server).
Allows:
  - Monitoring local worker status (LM Studio inference progress, PID, tokens)
  - Starting and stopping generation workers with flexible schedules
  - One-click compilation and production deployment (IONOS VPS)
  - Running map and GeoJSON compilation tasks
  - Live console streaming of logs
"""

import os
import sys
import json
import time
import signal
import subprocess
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

PORT = 5050
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(ROOT_DIR, "logs", "overnight_generation.log")
PID_FILE = os.path.join(ROOT_DIR, "logs", "worker.pid")
GEN_DIR = os.path.join(ROOT_DIR, "data", "generated")

os.makedirs(os.path.join(ROOT_DIR, "logs"), exist_ok=True)
os.makedirs(GEN_DIR, exist_ok=True)

def is_worker_running():
    if not os.path.exists(PID_FILE):
        return False, None
    try:
        with open(PID_FILE, "r") as f:
            pid = int(f.read().strip())
        # Check if process is alive
        os.kill(pid, 0)
        return True, pid
    except (OSError, ValueError):
        # Process dead or invalid PID
        if os.path.exists(PID_FILE):
            try:
                os.remove(PID_FILE)
            except Exception:
                pass
        return False, None

def get_stats():
    articles_count = 0
    cards_count = 0
    grapes_count = 0

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

    return {
        "articles": articles_count,
        "cards": cards_count,
        "grapes": grapes_count
    }

def get_recent_logs(lines=50):
    if not os.path.exists(LOG_FILE):
        return "Sin registros en logs/overnight_generation.log."
    try:
        with open(LOG_FILE, "r", encoding="utf-8", errors="ignore") as f:
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
            running, pid = is_worker_running()
            self._send_json({
                "running": running,
                "pid": pid,
                "stats": get_stats(),
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        elif url.path == "/api/logs":
            self._send_json({
                "logs": get_recent_logs(60)
            })
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

        if url.path == "/api/start":
            running, pid = is_worker_running()
            if running:
                self._send_json({"ok": False, "msg": f"El worker ya está en ejecución (PID {pid})."})
                return

            args_mode = data.get("mode", "hours_3")
            worker_cmd = [sys.executable, "scripts/overnight_worker.py"]

            if args_mode == "hours_1":
                worker_cmd += ["--hours", "1"]
            elif args_mode == "hours_3":
                worker_cmd += ["--hours", "3"]
            elif args_mode == "hours_5":
                worker_cmd += ["--hours", "5"]
            elif args_mode == "hours_8":
                worker_cmd += ["--hours", "8"]
            elif args_mode == "end_1830":
                worker_cmd += ["--end", "18:30"]
            elif args_mode == "end_0645":
                worker_cmd += ["--end", "06:45"]
            elif args_mode == "custom" and data.get("custom_end"):
                worker_cmd += ["--end", data["custom_end"]]

            log_out = open(LOG_FILE, "a", encoding="utf-8")
            proc = subprocess.Popen(worker_cmd, cwd=ROOT_DIR, stdout=log_out, stderr=subprocess.STDOUT)
            with open(PID_FILE, "w") as f:
                f.write(str(proc.pid))

            self._send_json({"ok": True, "msg": f"Worker iniciado correctamente con PID {proc.pid}.", "pid": proc.pid})

        elif url.path == "/api/stop":
            running, pid = is_worker_running()
            if not running:
                self._send_json({"ok": False, "msg": "El worker no está en ejecución."})
                return

            try:
                os.kill(pid, signal.SIGTERM)
                time.sleep(1)
                if os.path.exists(PID_FILE):
                    os.remove(PID_FILE)
                self._send_json({"ok": True, "msg": f"Worker (PID {pid}) detenido correctamente."})
            except Exception as e:
                self._send_json({"ok": False, "msg": f"Error deteniendo PID {pid}: {e}"})

        elif url.path == "/api/deploy":
            try:
                # 1. Compile
                compile_res = subprocess.run([sys.executable, "scripts/compile_generated_data.py"], cwd=ROOT_DIR, capture_output=True, text=True)
                # 2. Rsync to IONOS
                rsync_cmd = "rsync -avz -e 'ssh -i ~/.ssh/id_ionos_vps -o StrictHostKeyChecking=no' winepedia.html OVERNIGHT_REPORT.md web/ data/ root@jreyes13.net:/var/www/vhosts/jreyes13.net/wine3ai/"
                deploy_res = subprocess.run(rsync_cmd, shell=True, cwd=ROOT_DIR, capture_output=True, text=True)
                # 3. Permissions
                perm_cmd = "ssh -i ~/.ssh/id_ionos_vps -o StrictHostKeyChecking=no root@jreyes13.net 'find /var/www/vhosts/jreyes13.net/wine3ai -type f -exec chmod 644 {} + && find /var/www/vhosts/jreyes13.net/wine3ai -type d -exec chmod 755 {} + && chown -R jreyes169:psaserv /var/www/vhosts/jreyes13.net/wine3ai/'"
                perm_res = subprocess.run(perm_cmd, shell=True, capture_output=True, text=True)

                self._send_json({
                    "ok": True,
                    "msg": "Compilación y despliegue a producción completados con éxito.",
                    "compile_output": compile_res.stdout,
                    "deploy_output": deploy_res.stdout
                })
            except Exception as e:
                self._send_json({"ok": False, "msg": f"Error en despliegue: {e}"})

        elif url.path == "/api/build_maps":
            try:
                map_script = os.path.join(ROOT_DIR, "scratch", "build_web_geojson.py")
                if not os.path.exists(map_script):
                    map_script = os.path.join(ROOT_DIR, "scratch", "build_world_web_geojson.py")

                if os.path.exists(map_script):
                    res = subprocess.run([sys.executable, map_script], cwd=ROOT_DIR, capture_output=True, text=True)
                    self._send_json({"ok": True, "msg": "Script de mapas ejecutado con éxito.", "output": res.stdout})
                else:
                    self._send_json({"ok": False, "msg": "No se encontró el script de mapas."})
            except Exception as e:
                self._send_json({"ok": False, "msg": f"Error compilando mapas: {e}"})
        else:
            self.send_error(404, "Not Found")

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="es" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>WINE³ai — Panel de Control Local</title>
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

  <div class="max-w-5xl w-full space-y-6">
    
    <!-- Header -->
    <header class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-6 rounded-3xl bg-[#12141c] border border-white/10 shadow-xl">
      <div class="flex items-center gap-4">
        <span class="text-3xl">🍷</span>
        <div>
          <h1 class="text-2xl font-bold font-serif-wine text-white tracking-wide">
            WINE<span class="text-amber-400">³</span>ai — Panel de Control
          </h1>
          <p class="text-xs text-slate-400 font-mono mt-0.5">
            Gestor de Procesos Locales · LM Studio (Apple Silicon) · Despliegue en 1 Clic
          </p>
        </div>
      </div>
      <div id="status-pill" class="flex items-center gap-2 px-4 py-2 rounded-2xl bg-white/5 border border-white/10 text-xs font-mono">
        <span class="w-2.5 h-2.5 rounded-full bg-slate-500 animate-pulse" id="status-dot"></span>
        <span id="status-text" class="text-slate-300">Consultando estado...</span>
      </div>
    </header>

    <!-- Stats Row -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 font-mono">
      <div class="p-5 rounded-2xl bg-[#12141c]/80 border border-white/10">
        <div class="text-xs text-slate-400 uppercase tracking-wider mb-1">📚 Artículos WINEp3dIA</div>
        <div class="text-3xl font-bold text-amber-300" id="stat-articles">--</div>
        <div class="text-[11px] text-slate-500 mt-1">Suelos, Enología, Bioquímica, CMS, ASI</div>
      </div>
      <div class="p-5 rounded-2xl bg-[#12141c]/80 border border-white/10">
        <div class="text-xs text-slate-400 uppercase tracking-wider mb-1">🎴 Flashcards de Examen</div>
        <div class="text-3xl font-bold text-purple-300" id="stat-cards">--</div>
        <div class="text-[11px] text-slate-500 mt-1">WSET 3, CMS Deductive y ASI Global</div>
      </div>
      <div class="p-5 rounded-2xl bg-[#12141c]/80 border border-white/10">
        <div class="text-xs text-slate-400 uppercase tracking-wider mb-1">🍇 Variedades de Uva</div>
        <div class="text-3xl font-bold text-rose-300" id="stat-grapes">--</div>
        <div class="text-[11px] text-slate-500 mt-1">Perfiles organolépticos y maridaje molecular</div>
      </div>
    </div>

    <!-- Main Controls Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      
      <!-- Worker Control Box -->
      <div class="p-6 rounded-3xl bg-[#12141c] border border-white/10 shadow-lg space-y-5">
        <div class="flex items-center justify-between border-b border-white/10 pb-3">
          <h2 class="text-lg font-bold font-serif-wine text-white flex items-center gap-2">
            <span>⚙️</span> Inferencia LM Studio
          </h2>
          <span class="text-xs font-mono text-emerald-400 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-800/40">0 Tokens Nube</span>
        </div>

        <div>
          <label class="block text-xs font-mono text-slate-400 mb-2">Duración programada:</label>
          <select id="worker-mode" class="w-full px-4 py-3 rounded-xl bg-black/40 border border-white/15 text-white font-mono text-xs focus:outline-none focus:border-amber-400">
            <option value="hours_1">⏱️ 1 Hora (Prueba rápida)</option>
            <option value="hours_3" selected>⏱️ 3 Horas (Sesión moderada)</option>
            <option value="hours_5">⏱️ 5 Horas (Sesión extendida)</option>
            <option value="hours_8">💼 8 Horas (Jornada laboral completa)</option>
            <option value="end_1830">🌇 Hasta las 18:30 (Salida de oficina)</option>
            <option value="end_0645">🌙 Toda la noche (Hasta las 06:45 AM)</option>
          </select>
        </div>

        <div class="flex items-center gap-3 pt-2">
          <button id="btn-start" onclick="startWorker()" class="flex-1 py-3.5 px-4 rounded-xl bg-amber-500 hover:bg-amber-400 text-black font-mono text-xs font-bold transition-all shadow-lg flex items-center justify-center gap-2 active:scale-95">
            <span>▶</span> Iniciar Generador
          </button>
          <button id="btn-stop" onclick="stopWorker()" class="py-3.5 px-5 rounded-xl bg-red-950 hover:bg-red-900 text-red-200 border border-red-800/50 font-mono text-xs font-semibold transition-all flex items-center justify-center gap-2 active:scale-95 disabled:opacity-40" disabled>
            <span>⏹</span> Detener
          </button>
        </div>

        <p class="text-[11px] text-slate-500 font-mono leading-relaxed">
          * Los artículos ya generados se saltan automáticamente. Al pulsar Iniciar, el proceso arranca en segundo plano y continúa de forma segura.
        </p>
      </div>

      <!-- Deployment & Tools Box -->
      <div class="p-6 rounded-3xl bg-[#12141c] border border-white/10 shadow-lg space-y-5">
        <div class="flex items-center justify-between border-b border-white/10 pb-3">
          <h2 class="text-lg font-bold font-serif-wine text-white flex items-center gap-2">
            <span>🚀</span> Publicación y Mapas
          </h2>
          <span class="text-xs font-mono text-blue-400 bg-blue-950/60 px-2 py-0.5 rounded border border-blue-800/40">IONOS VPS</span>
        </div>

        <div class="space-y-3">
          <button onclick="deployProduction()" id="btn-deploy" class="w-full py-3.5 px-4 rounded-xl bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-mono text-xs font-bold transition-all shadow-lg flex items-center justify-center gap-2 active:scale-95">
            <span>🚀</span> Compilar y Publicar en Producción (IONOS)
          </button>
          <p class="text-[11px] text-slate-400 font-mono">
            Fusiona los JSON locales con la base oficial y sincroniza con el servidor web vía SSH/Rsync.
          </p>
        </div>

        <div class="pt-3 border-t border-white/10">
          <button onclick="buildMaps()" id="btn-maps" class="w-full py-2.5 px-4 rounded-xl bg-white/5 hover:bg-white/10 text-slate-300 border border-white/10 font-mono text-xs font-semibold transition-all flex items-center justify-center gap-2 active:scale-95">
            <span>🗺️</span> Compilar Capas GeoJSON de Mapas
          </button>
        </div>

        <div id="action-feedback" class="hidden p-3 rounded-xl bg-white/5 border border-white/10 text-xs font-mono text-amber-300"></div>
      </div>
    </div>

    <!-- Live Console Log Viewer -->
    <div class="p-6 rounded-3xl bg-[#12141c] border border-white/10 shadow-lg space-y-3">
      <div class="flex items-center justify-between">
        <h3 class="text-sm font-bold font-mono text-slate-300 flex items-center gap-2">
          <span>📟</span> Consola de Registro en Vivo (overnight_generation.log)
        </h3>
        <button onclick="refreshLogs()" class="text-xs font-mono text-slate-400 hover:text-white px-2 py-1 rounded bg-white/5 border border-white/10">
          🔄 Actualizar
        </button>
      </div>
      <pre id="log-console" class="w-full p-4 rounded-2xl bg-black/60 border border-white/10 text-[11px] font-mono text-slate-400 overflow-x-auto max-h-64 overflow-y-auto leading-relaxed">Cargando registros...</pre>
    </div>

  </div>

  <script>
    async function fetchStatus() {
      try {
        const res = await fetch('/api/status');
        const data = await res.json();
        
        document.getElementById('stat-articles').textContent = data.stats.articles;
        document.getElementById('stat-cards').textContent = data.stats.cards;
        document.getElementById('stat-grapes').textContent = data.stats.grapes;

        const dot = document.getElementById('status-dot');
        const text = document.getElementById('status-text');
        const btnStart = document.getElementById('btn-start');
        const btnStop = document.getElementById('btn-stop');

        if (data.running) {
          dot.className = "w-2.5 h-2.5 rounded-full bg-emerald-400 shadow-[0_0_8px_#34d399]";
          text.textContent = `🟢 En Ejecución (PID ${data.pid})`;
          text.className = "text-emerald-400 font-bold";
          btnStart.disabled = true;
          btnStart.classList.add('opacity-40');
          btnStop.disabled = false;
        } else {
          dot.className = "w-2.5 h-2.5 rounded-full bg-slate-500";
          text.textContent = "⚪ Detenido (Inactivo)";
          text.className = "text-slate-400";
          btnStart.disabled = false;
          btnStart.classList.remove('opacity-40');
          btnStop.disabled = true;
        }
      } catch (err) {
        console.error('Error fetching status:', err);
      }
    }

    async function fetchLogs() {
      try {
        const res = await fetch('/api/logs');
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
      const mode = document.getElementById('worker-mode').value;
      const fb = document.getElementById('action-feedback');
      fb.classList.remove('hidden');
      fb.textContent = "Iniciando worker con LM Studio...";

      try {
        const res = await fetch('/api/start', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ mode })
        });
        const data = await res.json();
        fb.textContent = data.msg;
        fetchStatus();
        fetchLogs();
      } catch (e) {
        fb.textContent = "Error al iniciar: " + e;
      }
    }

    async function stopWorker() {
      const fb = document.getElementById('action-feedback');
      fb.classList.remove('hidden');
      fb.textContent = "Deteniendo worker...";

      try {
        const res = await fetch('/api/stop', { method: 'POST' });
        const data = await res.json();
        fb.textContent = data.msg;
        fetchStatus();
        fetchLogs();
      } catch (e) {
        fb.textContent = "Error al detener: " + e;
      }
    }

    async function deployProduction() {
      const fb = document.getElementById('action-feedback');
      const btn = document.getElementById('btn-deploy');
      fb.classList.remove('hidden');
      fb.textContent = "Compilando y desplegando a IONOS VPS... Espera unos segundos.";
      btn.disabled = true;
      btn.classList.add('opacity-50');

      try {
        const res = await fetch('/api/deploy', { method: 'POST' });
        const data = await res.json();
        fb.textContent = data.msg;
        fetchStatus();
      } catch (e) {
        fb.textContent = "Error en despliegue: " + e;
      } finally {
        btn.disabled = false;
        btn.classList.remove('opacity-50');
      }
    }

    async function buildMaps() {
      const fb = document.getElementById('action-feedback');
      fb.classList.remove('hidden');
      fb.textContent = "Ejecutando script de mapas GeoJSON...";
      try {
        const res = await fetch('/api/build_maps', { method: 'POST' });
        const data = await res.json();
        fb.textContent = data.msg;
      } catch (e) {
        fb.textContent = "Error en mapas: " + e;
      }
    }

    // Auto-refresh loops
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
    print(f"🍷 WINE³ai — Panel de Control Local Activo")
    print(f"👉 Abre en tu navegador: http://localhost:{PORT}")
    print(f"Presiona Ctrl+C para detener el panel.")
    print(f"==========================================================\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nPanel de control cerrado.")

if __name__ == "__main__":
    main()
