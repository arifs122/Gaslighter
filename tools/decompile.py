#!/usr/bin/env python3
"""Ghidra headless ile ikilileri decompile edip metin uretir (GPU'suz).

Kullanim:
    python3 tools/decompile.py            # samples/bin_* -> samples/decomp_*.c

Ortam:
    GHIDRA_INSTALL_DIR   (varsayilan: ~/Desktop/ghidra_12.1.4_PUBLIC)
    JAVA_HOME            (varsayilan: /usr/lib/jvm/jdk-27-oracle-x64)
"""
from __future__ import annotations

import glob
import json
import os
import subprocess
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
SAMPLES = os.path.join(ROOT, "samples")
SCRIPTS = os.path.join(HERE, "ghidra_scripts")
SCRIPT = "ExportC.java"

GHIDRA = os.environ.get("GHIDRA_INSTALL_DIR", os.path.expanduser("~/Desktop/ghidra_12.1.4_PUBLIC"))
JAVA_HOME = os.environ.get("JAVA_HOME", "/usr/lib/jvm/jdk-27-oracle-x64")
ANALYZE = os.path.join(GHIDRA, "support", "analyzeHeadless")
PROJECT_DIR = "/tmp/opencode/gaslighter_ghproj"


def decompile(binary: str) -> list[dict]:
    os.makedirs(PROJECT_DIR, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        out_json = os.path.join(tmp, "out.json")
        cmd = [
            ANALYZE, PROJECT_DIR, "GaslighterProj",
            "-import", binary,
            "-scriptPath", SCRIPTS,
            "-postScript", SCRIPT, out_json,
            "-deleteProject",
        ]
        env = dict(os.environ, JAVA_HOME=JAVA_HOME)
        proc = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=600)
        if not os.path.isfile(out_json):
            tail = (proc.stderr or proc.stdout or "")[-300:]
            raise RuntimeError(f"Ghidra cikti uretmedi: {tail}")
        with open(out_json, encoding="utf-8") as fh:
            return json.load(fh)


def extract_strings(path: str, minlen: int = 5, cap: int = 250) -> list[str]:
    """Ikili icinden okunabilir ASCII stringleri cikarir (analist 'strings' gorunumu)."""
    import re
    data = open(path, "rb").read()
    seen, out = set(), []
    for m in re.finditer(rb"[ -~]{%d,}" % minlen, data):
        s = m.group().decode("ascii", "replace")
        if s not in seen:
            seen.add(s)
            out.append(s)
            if len(out) >= cap:
                break
    return out


def to_code(funcs: list[dict], strings: list[str] | None = None) -> str:
    parts = [f"/* {f['name']} @ {f['offset']} */\n{f['c_code']}" for f in funcs]
    code = "\n\n".join(parts)
    if strings:
        code += ("\n\n/* ===== STRINGS (analist gorunumu) ===== */\n"
                 + "\n".join(strings))
    return code


def main() -> None:
    bins = sorted(glob.glob(os.path.join(SAMPLES, "bin_*")))
    if not bins:
        print("once `python3 attacker/generate.py` calistir (bin_* yok)")
        return
    print(f"[decompile] Ghidra: {GHIDRA}")
    for b in bins:
        name = os.path.basename(b)[len("bin_"):]
        funcs = decompile(b)
        code = to_code(funcs, extract_strings(b))
        out = os.path.join(SAMPLES, f"decomp_{name}.c")
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(code)
        print(f"  {name:12} {len(funcs)} fonksiyon -> {os.path.relpath(out, ROOT)}")


if __name__ == "__main__":
    main()
