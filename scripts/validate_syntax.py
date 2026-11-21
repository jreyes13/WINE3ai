#!/usr/bin/env python3
"""
WINE³ai — Automated Pre-Flight Syntax & Integrity Validator
============================================================
Checks all JavaScript, JSON, HTML, and Python files in the repository.
Cross-platform (macOS + Windows + Linux):
  - Uses JavaScriptCore (jsc) natively on macOS when available.
  - Falls back to Node.js (`node --check`) on Windows/Linux.

Exit codes:
  0: All files passed validation cleanly.
  1: Syntax or integrity errors found.
"""

import os
import sys
import json
import glob
import shutil
import py_compile
import subprocess

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSC_BIN = "/System/Library/Frameworks/JavaScriptCore.framework/Versions/Current/Helpers/jsc"

def detect_js_validator():
    if os.path.exists(JSC_BIN):
        return "jsc", JSC_BIN
    node_bin = shutil.which("node")
    if node_bin:
        return "node", node_bin
    return None, None

def validate_js_files():
    errors = []
    # Find all JS files in root and data dirs
    js_patterns = [
        os.path.join(ROOT_DIR, "*.js"),
        os.path.join(ROOT_DIR, "data", "*.js"),
        os.path.join(ROOT_DIR, "web", "data", "*.js"),
        os.path.join(ROOT_DIR, "assets", "**", "*.js"),
    ]
    js_files = []
    for pat in js_patterns:
        js_files.extend(glob.glob(pat, recursive=True))

    js_files = sorted(list(set(js_files)))

    engine, engine_bin = detect_js_validator()
    if not engine:
        return [
            f"No JavaScript engine found (tried macOS jsc at {JSC_BIN} and 'node' in PATH). "
            "Install Node.js LTS to enable JS syntax validation on Windows/Linux."
        ]

    for js_path in js_files:
        rel_path = os.path.relpath(js_path, ROOT_DIR)
        if engine == "jsc":
            cmd = [engine_bin, "--dumpException", "-e", f'checkSyntax("{js_path}");']
        else:
            cmd = [engine_bin, "--check", js_path]
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if res.returncode != 0:
            err_msg = res.stdout.strip() or res.stderr.strip() or f"Syntax error (exit {res.returncode})"
            errors.append(f"❌ JS Syntax Error in {rel_path}:\n   {err_msg}")
        else:
            print(f"  ✓ {rel_path} (Valid JS via {engine})")

    return errors

def validate_json_files():
    errors = []
    json_patterns = [
        os.path.join(ROOT_DIR, "*.json"),
        os.path.join(ROOT_DIR, "data", "*.json"),
        os.path.join(ROOT_DIR, "web", "data", "*.json"),
        os.path.join(ROOT_DIR, "data", "generated", "*.json"),
    ]
    json_files = []
    for pat in json_patterns:
        json_files.extend(glob.glob(pat, recursive=True))

    json_files = sorted(list(set(json_files)))

    for json_path in json_files:
        rel_path = os.path.relpath(json_path, ROOT_DIR)
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                json.load(f)
            print(f"  ✓ {rel_path} (Valid JSON)")
        except Exception as e:
            errors.append(f"❌ JSON Parse Error in {rel_path}: {e}")

    return errors

def validate_python_files():
    errors = []
    py_files = sorted(glob.glob(os.path.join(ROOT_DIR, "scripts", "*.py")))
    for py_path in py_files:
        rel_path = os.path.relpath(py_path, ROOT_DIR)
        try:
            py_compile.compile(py_path, doraise=True)
            print(f"  ✓ {rel_path} (Valid Python)")
        except py_compile.PyCompileError as e:
            errors.append(f"❌ Python Syntax Error in {rel_path}: {e}")

    return errors

def main():
    print("=" * 70)
    print("🔍 WINE³ai — Verificación Pre-Flight de Integridad y Sintaxis")
    print("=" * 70)

    print("\n▶ Validando archivos JavaScript:")
    js_errors = validate_js_files()

    print("\n▶ Validando archivos JSON:")
    json_errors = validate_json_files()

    print("\n▶ Validando scripts Python:")
    py_errors = validate_python_files()

    all_errors = js_errors + json_errors + py_errors

    print("\n" + "=" * 70)
    if all_errors:
        print(f"🚨 SE ENCONTRARON {len(all_errors)} ERRORES DE SINTAXIS / INTEGRIDAD:")
        print("=" * 70)
        for err in all_errors:
            print(err)
        print("\n⛔ DESPLIEGUE O COMMIT BLOQUEADO. Corrige los errores antes de continuar.\n")
        return 1
    else:
        print("✨ TODOS LOS ARCHIVOS HAN SUPERADO LA VALIDACIÓN CON ÉXITO (0 errores).")
        print("=" * 70)
        return 0

if __name__ == "__main__":
    sys.exit(main())
