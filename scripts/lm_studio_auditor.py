#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WINE³ai — Local LM Studio Wine Region & Specification Auditor
=============================================================
Auditoría inteligente de mapas vitivinícolas, municipios y pliegos de condiciones
utilizando exclusivamente modelos locales en LM Studio (0 tokens externos).

Diseñado para ejecutarse en ratos muertos o en segundo plano, con guardado de
estado continuo y reanudación automática.

Uso:
  python3 scripts/lm_studio_auditor.py --mode spain_mapa
  python3 scripts/lm_studio_auditor.py --mode pliegos
  python3 scripts/lm_studio_auditor.py --country Spain --limit 10
  python3 scripts/lm_studio_auditor.py --status
  python3 scripts/lm_studio_auditor.py --help
"""

import os
import sys
import json
import time
import signal
import argparse
import urllib.request
import urllib.error
from datetime import datetime

# Rutas base relativas al proyecto WINE³ai
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
GEOJSON_PATH = os.path.join(BASE_DIR, "data", "wine_regions.geojson")
MAPA_PDF_PATH = os.path.join(BASE_DIR, "DOWNs", "SPAIN", "02_vinos.2026-07-03-13-01-22.pdf")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
STATE_FILE = os.path.join(REPORTS_DIR, "audit_state.json")
FINDINGS_FILE = os.path.join(REPORTS_DIR, "audit_findings.json")
MARKDOWN_REPORT_FILE = os.path.join(REPORTS_DIR, "AUDIT_WINE_REGIONS_LMSTUDIO.md")

LM_STUDIO_URL = "http://127.0.0.1:1234/v1"

COUNTRY_ALIASES = {
    "spain": ["españa", "spain", "es"],
    "españa": ["españa", "spain", "es"],
    "es": ["españa", "spain", "es"],
    "czechia": ["chequia", "czech republic", "czechia", "república checa", "cz"],
    "chequia": ["chequia", "czech republic", "czechia", "república checa", "cz"],
    "cz": ["chequia", "czech republic", "czechia", "república checa", "cz"],
    "france": ["francia", "france", "fr"],
    "francia": ["francia", "france", "fr"],
    "italy": ["italia", "italy", "it"],
    "italia": ["italia", "italy", "it"],
    "argentina": ["argentina", "ar"],
    "portugal": ["portugal", "pt"],
}

def match_country(candidate_str, feat_country, feat_code):
    cand = candidate_str.lower().strip()
    c_name = (feat_country or "").lower().strip()
    c_code = (feat_code or "").lower().strip()
    if cand == "all":
        return True
    if cand in COUNTRY_ALIASES:
        aliases = COUNTRY_ALIASES[cand]
        return any(a in c_name or a == c_code for a in aliases)
    return cand in c_name or cand == c_code
STOP_REQUESTED = False

def handle_sigint(signum, frame):
    global STOP_REQUESTED
    print("\n[!] Solicitud de interrupción detectada. Guardando estado y saliendo de forma limpia...")
    STOP_REQUESTED = True

signal.signal(signal.SIGINT, handle_sigint)
signal.signal(signal.SIGTERM, handle_sigint)


# ==============================================================================
# 1. CLIENTE Y COMUNICACIÓN CON LM STUDIO (LOCAL)
# ==============================================================================

def check_lm_studio():
    """Verifica si LM Studio está activo y devuelve el modelo cargado."""
    try:
        req = urllib.request.Request(f"{LM_STUDIO_URL}/models", headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            models = [m.get("id") for m in data.get("data", [])]
            return True, models
    except Exception as e:
        return False, str(e)


def query_lm_studio(prompt, system_prompt=None, model="qwen/qwen3.5-9b", max_tokens=1500, timeout=120):
    """Realiza una consulta a LM Studio y extrae la respuesta."""
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.1
    }

    req = urllib.request.Request(
        f"{LM_STUDIO_URL}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            choice = data["choices"][0]
            content = choice["message"].get("content", "").strip()
            reasoning = choice["message"].get("reasoning_content", "").strip()
            usage = data.get("usage", {})
            return content, reasoning, usage
    except Exception as e:
        return None, None, {"error": str(e)}


# ==============================================================================
# 2. GESTIÓN DE ESTADO Y PERSISTENCIA (RESUME CAPABILITY)
# ==============================================================================

def load_state():
    """Carga el estado de auditorías previas."""
    os.makedirs(REPORTS_DIR, exist_ok=True)
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "created_at": datetime.now().isoformat(),
        "last_updated": None,
        "total_regions": 0,
        "audited_count": 0,
        "issues_count": 0,
        "regions_state": {}
    }


def save_state(state):
    """Guarda el estado actual en disco."""
    os.makedirs(REPORTS_DIR, exist_ok=True)
    state["last_updated"] = datetime.now().isoformat()
    # Recalcular métricas
    regions = state.get("regions_state", {})
    state["audited_count"] = sum(1 for r in regions.values() if r.get("status") == "completed")
    state["issues_count"] = sum(len(r.get("issues", [])) for r in regions.values())
    
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def save_findings_and_markdown(state, all_features, mapa_entries=None):
    """Genera los reportes JSON y Markdown estructurados."""
    findings = {
        "generated_at": datetime.now().isoformat(),
        "summary": {
            "total_regions_in_map": len(all_features),
            "audited_regions": state.get("audited_count", 0),
            "total_issues": state.get("issues_count", 0)
        },
        "issues_by_region": {}
    }

    # Recoger hallazgos
    for reg_id, reg_data in state.get("regions_state", {}).items():
        if reg_data.get("issues"):
            findings["issues_by_region"][reg_id] = {
                "name": reg_data.get("name"),
                "country": reg_data.get("country"),
                "issues": reg_data.get("issues"),
                "pliego_status": reg_data.get("pliego_status"),
                "pliego_path": reg_data.get("pliego_path"),
                "geometry_precision": reg_data.get("geometry_precision"),
                "last_audited": reg_data.get("last_audited")
            }

    with open(FINDINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(findings, f, indent=2, ensure_ascii=False)

    # Generar Markdown Report legible
    lines = [
        "# Informe de Auditoría Cartográfica y Pliegos — WINE³ai",
        f"**Generado:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ",
        "**Motor de Auditoría:** LM Studio (Local / 0 Tokens Externos)  ",
        "**Documento Oficial de Referencia España:** MAPA `02_vinos.2026-07-03-13-01-22.pdf`  ",
        "",
        "---",
        "",
        "## 1. Resumen Ejecutivo de la Auditoría",
        "",
        f"- **Regiones en GeoJSON:** {len(all_features)}",
        f"- **Regiones Auditadas:** {state.get('audited_count', 0)} ({state.get('audited_count', 0)*100.0/max(1, len(all_features)):.1f}%)",
        f"- **Incidencias / Mejoras Registradas:** {state.get('issues_count', 0)}",
        "",
        "---",
        "",
        "## 2. Estado de Denominaciones de España (Comparativa con MAPA Oficial)",
        "",
        "| Denominación Oficial | Categoría Oficial | En Mapa GeoJSON | Pliego Oficial | Estado Auditoría | Observaciones |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |"
    ]

    spain_regs = {k: v for k, v in state.get("regions_state", {}).items() if v.get("country_code") == "ES"}
    for reg_id, data in sorted(spain_regs.items(), key=lambda x: x[1].get("name", "")):
        pliego_badge = "🟢 OK" if data.get("pliego_status") == "ok" else ("🟡 Placeholder" if data.get("pliego_status") == "small" else "🔴 Faltante")
        issues_str = "; ".join(data.get("issues", [])) if data.get("issues") else "Validada sin objeciones"
        lines.append(f"| **{data.get('name')}** | {data.get('category')} | 🟢 Sí (`{reg_id}`) | {pliego_badge} | {data.get('status')} | {issues_str} |")

    lines.extend([
        "",
        "---",
        "",
        "## 3. Resumen Internacional: Pliegos Faltantes o Débiles por País",
        "",
        "| País | Regiones en Mapa | Pliegos OK | Pliegos Débiles (<10KB) | Pliegos Ausentes | Diagnóstico |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |"
    ])

    # Agrupar por país
    country_groups = {}
    for r in state.get("regions_state", {}).values():
        c = r.get("country", "Desconocido")
        if c not in country_groups:
            country_groups[c] = {"total": 0, "ok": 0, "small": 0, "missing": 0}
        country_groups[c]["total"] += 1
        st = r.get("pliego_status", "missing")
        if st == "ok":
            country_groups[c]["ok"] += 1
        elif st == "small":
            country_groups[c]["small"] += 1
        else:
            country_groups[c]["missing"] += 1

    for c, stats in sorted(country_groups.items(), key=lambda x: -x[1]["total"]):
        if stats["missing"] == 0 and stats["small"] == 0:
            diag = "🟢 Completo"
        elif stats["missing"] > 0:
            diag = f"🔴 Faltan {stats['missing']} pliegos"
        else:
            diag = f"🟡 {stats['small']} pliegos placeholder"
        lines.append(f"| **{c}** | {stats['total']} | {stats['ok']} | {stats['small']} | {stats['missing']} | {diag} |")

    with open(MARKDOWN_REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


# ==============================================================================
# 3. EXTRACCIÓN DEL REGISTRO OFICIAL MAPA ESPAÑA (02_vinos PDF)
# ==============================================================================

def parse_spain_mapa_pdf():
    """Lee el PDF de 02_vinos del MAPA y extrae todas las DOPs e IGPs registradas."""
    if not os.path.exists(MAPA_PDF_PATH):
        print(f"[!] No se encontró el PDF oficial de España en: {MAPA_PDF_PATH}")
        return []

    try:
        from pypdf import PdfReader
    except ImportError:
        print("[!] Requiere librería 'pypdf'. Instalar con: pip install pypdf")
        return []

    reader = PdfReader(MAPA_PDF_PATH)
    full_text = "\n".join([page.extract_text() for page in reader.pages])
    
    entries = []
    current_ccaa = "Supraautonómico"

    lines = full_text.split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Detección de Comunidad Autónoma
        if " Total:" in line and not line.startswith("Total"):
            current_ccaa = line.split(" Total:")[0].strip()
            continue

        # Detección de denominaciones DOP / IGP
        if line.startswith("DOP ") or line.startswith("IGP "):
            parts = line.split()
            tipo = parts[0] # DOP o IGP
            
            # Buscar expediente UE tipo PDO-ES-... o PGI-ES-...
            ue_code = ""
            trad_term = ""
            name_parts = []
            
            for part in parts[1:]:
                if "PDO-ES-" in part or "PGI-ES-" in part:
                    ue_code = part
                elif part in ["DO", "DOCa", "VP", "VC", "VT"]:
                    trad_term = part
                elif part != "Total":
                    name_parts.append(part)
            
            name = " ".join(name_parts).strip()
            if name:
                entries.append({
                    "type": tipo,
                    "name": name,
                    "trad_term": trad_term or ("DO" if tipo == "DOP" else "VT"),
                    "ue_code": ue_code,
                    "ccaa": current_ccaa
                })

    return entries


# ==============================================================================
# 4. AUDITORÍA DE REGIONES CON LM STUDIO
# ==============================================================================

def check_pliego_physical(pliego_rel_path):
    """Comprueba si el pliego existe en disco y su salud."""
    if not pliego_rel_path:
        return "missing", 0
    full_path = os.path.join(BASE_DIR, pliego_rel_path)
    if not os.path.exists(full_path):
        return "missing", 0
    size = os.path.getsize(full_path)
    if size < 8000: # Menor a 8 KB suele ser un archivo de texto o plantilla vacía
        return "small", size
    return "ok", size


def audit_region_with_lm_studio(feature, model="qwen/qwen3.5-9b"):
    """Consulta a LM Studio para auditar inconsistencias toponímicas y varietales."""
    props = feature.get("properties", {})
    name = props.get("name")
    country = props.get("country")
    category = props.get("category")
    region_zone = props.get("region")
    munis = props.get("munis", [])
    grapes_red = props.get("grapes_red", "")
    grapes_white = props.get("grapes_white", "")

    # Prompt enfocado, directo y conciso para no saturar al modelo local
    prompt = f"""Audita brevemente esta denominación vitivinícola:
- Denominación: {name} ({category})
- País: {country} | Región/Zona: {region_zone}
- Municipios registrados ({len(munis)}): {', '.join(munis[:15])}{'...' if len(munis)>15 else ''}
- Uvas tintas declaradas: {grapes_red}
- Uvas blancas declaradas: {grapes_white}

En 2 o 3 frases directas:
1. ¿Son correctos los municipios para esta denominación y provincia? ¿Hay municipios claramente erróneos?
2. ¿Falta alguna variedad principal o hay alguna incongruencia en la clasificación?
Responde en español de forma escueta."""

    content, reasoning, usage = query_lm_studio(
        prompt,
        system_prompt="Eres un sommelier y experto en geografía vitivinícola y normativa europea (DOP/IGP).",
        model=model,
        max_tokens=1200
    )

    findings = []
    # Usar prioritariamente content, y solo si viene vacío acudir a reasoning limpio
    text_to_analyze = content.strip() if content else ""
    if not text_to_analyze and reasoning:
        # Si extraemos del reasoning, buscar la conclusión final
        clean_r = reasoning
        if "Thinking Process:" in clean_r:
            parts = clean_r.split("Thinking Process:")
            clean_r = parts[-1]
        text_to_analyze = clean_r.strip()

    lower = text_to_analyze.lower()
    # Buscar observaciones críticas reales
    if any(k in lower for k in ["incongruen", "no corresponde", "municipio erróneo", "provincia incorrecta", "falta variedad", "clasificación errónea"]):
        # Extraer extracto relevante limpio
        snippet = text_to_analyze[:300].replace("\n", " ").strip()
        findings.append(f"Obs. LM Studio: {snippet}")

    return findings, text_to_analyze


# ==============================================================================
# 5. BUCLE PRINCIPAL DE AUDITORÍA
# ==============================================================================

def run_auditor(args):
    global STOP_REQUESTED
    
    print("=" * 70)
    print("  WINE³ai — AUDITOR LOCAL DE MAPAS Y PLIEGOS (LM STUDIO)")
    print("=" * 70)

    # 1. Verificar conexión LM Studio
    lm_ok, models = check_lm_studio()
    if not lm_ok:
        print("\n[!] AVISO: LM Studio no está respondiendo en http://127.0.0.1:1234/v1")
        print(f"    Detalle del error: {models}")
        print("    Asegúrate de tener LM Studio abierto con el servidor local activo.")
        if args.mode not in ["pliegos", "status"]:
            print("    Para ejecutar auditoría de pliegos sin IA, usa: --mode pliegos\n")
            return
    else:
        active_model = models[0] if models else "qwen/qwen3.5-9b"
        print(f"[✓] LM Studio Conectado. Modelo activo: {active_model}")

    # 2. Cargar GeoJSON
    if not os.path.exists(GEOJSON_PATH):
        print(f"[!] Archivo GeoJSON no encontrado en: {GEOJSON_PATH}")
        return

    with open(GEOJSON_PATH, "r", encoding="utf-8") as f:
        geojson_data = json.load(f)
    all_features = geojson_data.get("features", [])
    print(f"[✓] Capa canónica cargada: {len(all_features)} regiones vitivinícolas mundiales.")

    # 3. Cargar o inicializar estado
    state = load_state()
    state["total_regions"] = len(all_features)

    # Poblar registros nuevos en el estado si faltaban
    for f in all_features:
        fid = f.get("id") or f.get("properties", {}).get("id")
        if fid not in state["regions_state"]:
            state["regions_state"][fid] = {
                "id": fid,
                "name": f.get("properties", {}).get("name"),
                "country": f.get("properties", {}).get("country"),
                "country_code": f.get("properties", {}).get("country_code"),
                "category": f.get("properties", {}).get("category"),
                "pliego_path": f.get("properties", {}).get("pliego"),
                "pliego_status": "pending",
                "geometry_precision": "polygon" if len(f.get("geometry", {}).get("coordinates", [[]])[0]) > 6 else "rough_box",
                "status": "pending",
                "issues": [],
                "last_audited": None
            }

    # Mostrar dashboard si se pide solo --status
    if args.status:
        audited = sum(1 for r in state["regions_state"].values() if r["status"] == "completed")
        issues = sum(len(r["issues"]) for r in state["regions_state"].values())
        missing_pliegos = sum(1 for r in state["regions_state"].values() if r.get("pliego_status") == "missing")
        print("\n--- ESTADO DE AUDITORÍA ACTUAL ---")
        print(f"Total regiones registradas : {len(state['regions_state'])}")
        print(f"Auditadas con éxito        : {audited} ({audited*100.0/len(state['regions_state']):.1f}%)")
        print(f"Pendientes de auditar      : {len(state['regions_state']) - audited}")
        print(f"Pliegos ausentes en disco  : {missing_pliegos}")
        print(f"Incidencias registradas    : {issues}")
        print(f"Última actualización       : {state.get('last_updated')}")
        print(f"Reporte Markdown           : {MARKDOWN_REPORT_FILE}\n")
        return

    # 4. Modo específico España MAPA
    if args.mode == "spain_mapa":
        print("\n--- AUDITORÍA ESPECÍFICA ESPAÑA: MAPA 02_VINOS PDF vs GEOJSON ---")
        mapa_entries = parse_spain_mapa_pdf()
        print(f"[✓] Extraídas {len(mapa_entries)} denominaciones oficiales del MAPA (DOPs e IGPs).")
        
        spain_geo_names = {f["properties"].get("name", "").lower(): f for f in all_features if f.get("properties", {}).get("country_code") == "ES"}
        
        missing_in_geo = []
        for me in mapa_entries:
            m_name = me["name"].lower()
            # Búsqueda difusa simple
            matched = any(m_name in g_name or g_name in m_name for g_name in spain_geo_names.keys())
            if not matched:
                missing_in_geo.append(me)

        print(f"\n[!] Denominaciones oficiales del MAPA que NO están actualmente en el GeoJSON: {len(missing_in_geo)}")
        for m in missing_in_geo[:15]:
            print(f"    - {m['type']} {m['name']} ({m['trad_term']}) — CCAA: {m['ccaa']}")
        if len(missing_in_geo) > 15:
            print(f"    ... y {len(missing_in_geo) - 15} más (principalmente IGPs / Vinos de la Tierra).")

    # 5. Filtrar candidatos para procesar
    candidates = []
    for f in all_features:
        fid = f.get("id") or f.get("properties", {}).get("id")
        reg_state = state["regions_state"][fid]
        
        # Filtro de país
        if args.country and not match_country(args.country, f.get("properties", {}).get("country"), f.get("properties", {}).get("country_code")):
            continue

        # Si ya está completada y no forzamos re-análisis, saltar
        if reg_state["status"] == "completed" and not args.force:
            continue
            
        candidates.append(f)

    print(f"\n[i] Candidatos a procesar en esta ejecución: {len(candidates)}")
    if args.limit:
        candidates = candidates[:args.limit]
        print(f"[i] Límite por sesión aplicado: {len(candidates)} regiones.")

    # 6. Procesamiento por lotes
    processed = 0
    model_name = models[0] if (lm_ok and models) else "qwen/qwen3.5-9b"

    # Si el modo es solo pliegos, usar delay 0 por defecto para velocidad instantánea
    effective_delay = 0.0 if args.mode == "pliegos" and args.delay == 1.5 else args.delay

    for idx, feature in enumerate(candidates):
        if STOP_REQUESTED:
            break

        fid = feature.get("id") or feature.get("properties", {}).get("id")
        props = feature.get("properties", {})
        name = props.get("name", fid)
        country = props.get("country", "")
        pliego_path = props.get("pliego")

        print(f"\n[{idx+1}/{len(candidates)}] {country} -> {name} ({props.get('category')})...", end="", flush=True)

        # Paso A: Comprobación física de pliego
        pliego_status, psize = check_pliego_physical(pliego_path)
        issues = []
        if pliego_status == "missing":
            issues.append(f"Pliego ausente en disco: {pliego_path or 'No especificado'}")
        elif pliego_status == "small":
            issues.append(f"Pliego sospechoso (menor a 8KB, tamaño: {psize} bytes)")

        # Paso B: Comprobación de polígono
        geom_pts = len(feature.get("geometry", {}).get("coordinates", [[]])[0])
        if geom_pts <= 6:
            issues.append(f"Geometría tosca (caja simplificada de {geom_pts} vértices)")

        # Paso C: Auditoría inteligente con LM Studio (si no estamos en modo pliegos y LM Studio está activo)
        if args.mode != "pliegos" and lm_ok:
            lm_issues, lm_text = audit_region_with_lm_studio(feature, model=model_name)
            if lm_issues:
                issues.extend(lm_issues)
            print(" [LM Studio ✓]", end="", flush=True)
        else:
            print(" [Pliego ✓]", end="", flush=True)

        # Actualizar estado
        state["regions_state"][fid].update({
            "pliego_status": pliego_status,
            "status": "completed",
            "issues": issues,
            "last_audited": datetime.now().isoformat()
        })

        if issues:
            print(f" -> {len(issues)} incidencias")
        else:
            print(" -> Limpia")

        processed += 1

        # Guardado continuo tras cada región
        save_state(state)
        save_findings_and_markdown(state, all_features)

        # Pausa suave para mantener frío el portátil
        if effective_delay > 0 and not STOP_REQUESTED:
            time.sleep(effective_delay)

    print("\n" + "=" * 70)
    print(f"  SESIÓN FINALIZADA. Regiones procesadas: {processed}")
    print(f"  Estado guardado en : {STATE_FILE}")
    print(f"  Hallazgos JSON     : {FINDINGS_FILE}")
    print(f"  Informe Markdown   : {MARKDOWN_REPORT_FILE}")
    print("=" * 70)


# ==============================================================================
# ENTRADA PRINCIPAL
# ==============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Auditor local de regiones y pliegos con LM Studio.")
    parser.add_argument("--country", type=str, default="all", help="País a auditar (ej. Spain, France, Czechia, all)")
    parser.add_argument("--mode", type=str, choices=["full", "spain_mapa", "pliegos"], default="full", help="Modo de auditoría")
    parser.add_argument("--limit", type=int, default=None, help="Límite máximo de regiones en esta sesión")
    parser.add_argument("--delay", type=float, default=1.5, help="Segundos de pausa entre consultas (por defecto 1.5s)")
    parser.add_argument("--force", action="store_true", help="Re-analizar regiones ya marcadas como completadas")
    parser.add_argument("--status", action="store_true", help="Mostrar resumen de estado sin ejecutar análisis")
    parser.add_argument("--reset", action="store_true", help="Reiniciar estado de auditoría desde cero")

    args = parser.parse_args()

    if args.reset:
        if os.path.exists(STATE_FILE):
            os.remove(STATE_FILE)
            print("[✓] Estado anterior reiniciado con éxito.")

    run_auditor(args)
