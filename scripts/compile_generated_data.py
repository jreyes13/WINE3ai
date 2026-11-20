#!/usr/bin/env python3
"""
Compile generated JSON checkpoints into production JavaScript/JSON assets.
Safely merges:
  - data/generated/winepedia_articles.json -> data/winepedia_articles.js & web/data/winepedia_articles.js
  - data/generated/study_cards.json       -> data/study_cards.js & web/data/study_cards.js
  - data/generated/grape_profiles.json    -> data/grape_varieties.json & web/data/grape_varieties.json
"""

import os
import json
import subprocess
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN_DIR = os.path.join(ROOT, "data", "generated")
JSC_BIN = "/System/Library/Frameworks/JavaScriptCore.framework/Versions/Current/Helpers/jsc"

def load_js_via_jsc(rel_path, var_name):
    cmd = [JSC_BIN, "-e", f'var window={{}}; load("{rel_path}"); print(JSON.stringify(window.{var_name}));']
    res = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if res.returncode == 0 and res.stdout.strip():
        try:
            return json.loads(res.stdout)
        except Exception:
            pass
    return []

def merge_winepedia():
    gen_file = os.path.join(GEN_DIR, "winepedia_articles.json")
    if not os.path.exists(gen_file):
        print("No new winepedia articles found.")
        return 0

    with open(gen_file, "r", encoding="utf-8") as f:
        new_articles = json.load(f)

    existing_articles = load_js_via_jsc("data/winepedia_articles.js", "WINEPEDIA_ARTICLES")
    if not existing_articles:
        print("Warning: could not load existing articles via JSC; aborting to prevent overwrite.")
        return 0

    existing_ids = set(a.get("id") for a in existing_articles)
    added = 0
    for a in new_articles:
        if a.get("id") not in existing_ids:
            existing_articles.append(a)
            existing_ids.add(a.get("id"))
            added += 1

    js_code = """// WINE³ai — WINEp3dIA: Base de Datos Enciclopédica y Artículos de Referencia
// Fuentes analíticas: WSET Nivel 3, Court of Master Sommeliers (CMS), ASI
// Canon unificado con referencias canónicas (Robinson & Johnson, VIVC, Lepeltier, Goode)

(function(root) {
  'use strict';

  var WINEPEDIA_ARTICLES = """ + json.dumps(existing_articles, ensure_ascii=False, indent=2) + """;

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = WINEPEDIA_ARTICLES;
  } else {
    root.WINEPEDIA_ARTICLES = WINEPEDIA_ARTICLES;
  }
})(typeof window !== 'undefined' ? window : globalThis);
"""

    dest_file = os.path.join(ROOT, "data", "winepedia_articles.js")
    with open(dest_file, "w", encoding="utf-8") as f:
        f.write(js_code)

    web_dest = os.path.join(ROOT, "web", "data", "winepedia_articles.js")
    if os.path.exists(os.path.dirname(web_dest)):
        with open(web_dest, "w", encoding="utf-8") as f:
            f.write(js_code)

    print(f"Winepedia: Merged {added} new articles (Total: {len(existing_articles)}).")
    return added

def merge_cards():
    gen_file = os.path.join(GEN_DIR, "study_cards.json")
    if not os.path.exists(gen_file):
        print("No new study cards found.")
        return 0

    with open(gen_file, "r", encoding="utf-8") as f:
        new_cards = json.load(f)

    existing_cards = load_js_via_jsc("data/study_cards.js", "STUDY_CARDS")
    if not existing_cards:
        print("Warning: could not load existing cards via JSC; aborting to prevent overwrite.")
        return 0

    existing_ids = set(c.get("id") for c in existing_cards)
    added = 0
    for c in new_cards:
        if c.get("id") not in existing_ids:
            existing_cards.append(c)
            existing_ids.add(c.get("id"))
            added += 1

    js_code = """// WINE³ai — Banco Canónico de Fichas de Examen & Cata Deductiva
// Estructurado estrictamente bajo los 3 grandes cánones internacionales:
// 1. WSET 3 (Wine & Spirit Education Trust)
// 2. CMS (Court of Master Sommeliers)
// 3. ASI (Association de la Sommellerie Internationale)
// Fuentes y Bibliografía: Jamie Goode, Pascaline Lepeltier, Hugh Johnson & Jancis Robinson, VIVC

window.STUDY_CARDS = """ + json.dumps(existing_cards, ensure_ascii=False, indent=2) + """;
"""

    dest_file = os.path.join(ROOT, "data", "study_cards.js")
    with open(dest_file, "w", encoding="utf-8") as f:
        f.write(js_code)

    web_dest = os.path.join(ROOT, "web", "data", "study_cards.js")
    if os.path.exists(os.path.dirname(web_dest)):
        with open(web_dest, "w", encoding="utf-8") as f:
            f.write(js_code)

    print(f"Study Cards: Merged {added} new cards (Total: {len(existing_cards)}).")
    return added

def merge_grapes():
    gen_file = os.path.join(GEN_DIR, "grape_profiles.json")
    if not os.path.exists(gen_file):
        return 0

    with open(gen_file, "r", encoding="utf-8") as f:
        new_profiles = json.load(f)

    dest_file = os.path.join(ROOT, "data", "grape_varieties.json")
    if not os.path.exists(dest_file):
        return 0

    with open(dest_file, "r", encoding="utf-8") as f:
        varieties = json.load(f)

    profile_map = {p["grape"].lower(): p for p in new_profiles if "grape" in p}
    updated = 0
    for v in varieties:
        name_lower = v.get("name", "").lower()
        if name_lower in profile_map:
            p = profile_map[name_lower]
            v["organoleptic_profile"] = p.get("profile")
            if "sommelier_note_es" in p:
                v["sommelier_note_es"] = p["sommelier_note_es"]
            if "sommelier_note_en" in p:
                v["sommelier_note_en"] = p["sommelier_note_en"]
            updated += 1

    with open(dest_file, "w", encoding="utf-8") as f:
        json.dump(varieties, f, ensure_ascii=False, indent=2)

    web_dest = os.path.join(ROOT, "web", "data", "grape_varieties.json")
    if os.path.exists(os.path.dirname(web_dest)):
        with open(web_dest, "w", encoding="utf-8") as f:
            json.dump(varieties, f, ensure_ascii=False, indent=2)

    # Also synchronize production JS bundle for zero-latency offline loading
    js_content = "window.GRAPE_VARIETIES_DATA = " + json.dumps(varieties, ensure_ascii=False) + ";\n"
    js_dest = os.path.join(ROOT, "data", "grape_varieties.js")
    with open(js_dest, "w", encoding="utf-8") as f:
        f.write(js_content)

    web_js_dest = os.path.join(ROOT, "web", "data", "grape_varieties.js")
    if os.path.exists(os.path.dirname(web_js_dest)):
        with open(web_js_dest, "w", encoding="utf-8") as f:
            f.write(js_content)

    print(f"Grape Varieties: Enriched {updated} varieties.")
    return updated

def main():
    print("Compiling overnight generated content into production files safely...")
    merge_winepedia()
    merge_cards()
    merge_grapes()
    print("Done!")

if __name__ == "__main__":
    main()
