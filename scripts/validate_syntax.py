#!/usr/bin/env python3
"""
WINE³ai — Automated Pre-Flight Syntax & Integrity Validator
============================================================
Checks all JavaScript, JSON, HTML, and Python files in the repository.
Runs natively on macOS using JavaScriptCore (jsc) without requiring Node.js.

Exit codes:
  0: All files passed validation cleanly.
  1: Syntax or integrity errors found.
"""

import os
import sys
import json
import glob
import py_compile
import subprocess

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSC_BIN = "/System/Library/Frameworks/JavaScriptCore.framework/Versions/Current/Helpers/jsc"

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

    if not os.path.exists(JSC_BIN):
        return [f"JavaScriptCore interpreter not found at {JSC_BIN}"]

    for js_path in js_files:
        rel_path = os.path.relpath(js_path, ROOT_DIR)
        cmd = [JSC_BIN, "--dumpException", "-e", f'checkSyntax("{js_path}");']
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            err_msg = res.stdout.strip() or res.stderr.strip() or f"Syntax error (exit {res.returncode})"
            errors.append(f"❌ JS Syntax Error in {rel_path}:\n   {err_msg}")
        else:
            print(f"  ✓ {rel_path} (Valid JS)")

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
