#!/usr/bin/env python3
"""CrowbarAF'in deterministik (model-oncesi) katmani L0-L4 uzerinde ne goruyor?

Amac: 'LLM'e hic gitmeden' ne tespit edilebiliyor? Obfuscation'i *isaretleyebiliyor*
mu, yoksa o da mi korlesiyor?

Kullanilan CrowbarAF mantigi:
  * filter_iocs  (nodes.py)  -> IP/URL/dosya/registry regex'leri
  * obfuscation gostergeleri -> string-array/base64/hex/parseInt/CFF izleri
  * supheli API izleri       -> eval/Function/child_process/net/fs/crypto
"""
from __future__ import annotations

import glob
import os
import re

LAB = os.path.expanduser("~/Desktop/rea-obfuscation-lab")

# --- CrowbarAF nodes.py'den birebir (IoC filtresi) ---
_IPV4_RE = re.compile(
    r"(?<![\d.])(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?!\d|\.\d)")
_URL_RE = re.compile(r"\b(?:https?|tcp)://[^\s'\"<>]+", re.IGNORECASE)
_FILE_EXT_RE = re.compile(
    r"[\w\-\\/:.$%]+\.(?:exe|dll|sys|bat|ps1|vbs|scr|lnk)(?![A-Za-z0-9])", re.IGNORECASE)
_REGISTRY_RE = re.compile(
    r"(?:\b(?:HKLM|HKCU|HKCR|HKU|HKCC|HKEY_[A-Z_]+)\\|Software\\Microsoft|SYSTEM\\CurrentControlSet)",
    re.IGNORECASE)
_IOC_PATTERNS = (_IPV4_RE, _URL_RE, _FILE_EXT_RE, _REGISTRY_RE)


def filter_iocs(texts: list[str]) -> list[str]:
    kept = [s for s in texts if isinstance(s, str) and s.strip()
            and any(p.search(s) for p in _IOC_PATTERNS)]
    return list(dict.fromkeys(kept))


# --- deterministik "obfuscation var mi?" gostergeleri ---
OBF_SIGNALS = {
    "hex_escape":      re.compile(r"(?:\\x[0-9a-fA-F]{2}){4,}"),
    "string_array":    re.compile(r"_0x[0-9a-f]{4,}\s*\("),
    "array_indexing":  re.compile(r"\[[^\]]*_0x[0-9a-f]{4,}[^\]]*\]"),
    "parseInt_noise":  re.compile(r"parseInt\s*\(\s*_0x"),
    "b64_decoder":     re.compile(r"decodeURIComponent|atob|base64", re.IGNORECASE),
    "num_expression":  re.compile(r"[-+]\s*\d+\s*\*\s*[-]?\d+\s*[-+]"),
    "hex_idents":      re.compile(r"\b_0x[0-9a-f]{4,}\b"),
}

SUSPICIOUS_API = {
    "eval":            re.compile(r"\beval\s*\("),
    "Function_ctor":   re.compile(r"new\s+Function\s*\("),
    "child_process":   re.compile(r"child_process|execSync|spawnSync"),
    "network":         re.compile(r"require\(\s*['\"](?:net|http|https|dns)['\"]"),
    "fs":              re.compile(r"require\(\s*['\"]fs['\"]"),
    "crypto":          re.compile(r"require\(\s*['\"]crypto['\"]"),
}


def read_level(level: str) -> str:
    if level == "L0":
        files = sorted(glob.glob(os.path.join(LAB, "targets", "js", "src", "*.js")))
        return "\n".join(open(f, encoding="utf-8").read() for f in files)
    md = os.path.join(LAB, "output", f"recovered-{level}", "modules")
    files = sorted(f for f in glob.glob(os.path.join(md, "*.js")) if not f.endswith(".map"))
    return "\n".join(open(f, encoding="utf-8").read() for f in files)


def strings_of(code: str) -> list[str]:
    """Kaba string literal cikarimi (IoC filtresine vermek icin)."""
    out = []
    for m in re.finditer(r"'([^'\\\n]{4,})'|\"([^\"\\\n]{4,})\"", code):
        out.append(m.group(1) or m.group(2))
    return out


def main() -> None:
    print(f"{'seviye':<7}{'boyut':>8}{'IoC':>6}{'API':>5}{'OBF sinyali':>13}  sinyaller")
    print("-" * 78)
    for lvl in ["L0", "L1", "L2", "L3", "L4"]:
        code = read_level(lvl)
        iocs = filter_iocs(strings_of(code))
        api = [k for k, rx in SUSPICIOUS_API.items() if rx.search(code)]
        obf = [k for k, rx in OBF_SIGNALS.items() if rx.search(code)]
        print(f"{lvl:<7}{len(code):>8}{len(iocs):>6}{len(api):>5}{len(obf):>13}  "
              f"obf={obf} api={api}")


if __name__ == "__main__":
    main()
