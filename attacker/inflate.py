#!/usr/bin/env python3
"""Şişirme/decoy saldırı örnekleri üretir.

- clean    : 1 payload + 3 küçük benign
- flood    : 1 payload + N decoy (modeli yanıltmak için)
- overflow : 1 payload + N büyük decoy (context'i taşırmak için)

Payload'da düz metin bir URL vardır ("192.0.2.1") -> model kodu okursa görür.
Decoy'larda URL yok; sadece CFF/XOR gürültüsü.

Kullanım:
    python attacker/inflate.py --out /tmp/opencode/attack_samples.json
"""
from __future__ import annotations

import argparse
import json

URL = "http://192.0.2.1:4444/gate.php"


def _cff(name: str, blocks: int = 2, per_block: int = 70, with_url: bool = False) -> str:
    key = "(0x2d + 0x2d)"
    L = [f"int {name}(char *s,int n){{", "  int st=0, r=0;", "  while (1) {", "    switch (st) {"]
    for b in range(blocks):
        L.append(f"      case {b}:")
        L.append("        if (((n*n+n)&1)==0) {")
        for k in range(per_block):
            idx = b * per_block + k
            L.append(f"          s[{idx}] = (char)(s[{idx}] ^ {key});")
        L.append(f"        }} else {{ r = r + {b}; }}")
        L.append(f"        st = {(b + 1) if b + 1 < blocks else 99}; break;")
    L.append("      default: break;")
    L.append("    }")
    if with_url:
        L.append(f'    const char *u = "{URL}"; (void)u;')
    L.append("    if (st == 99) break;")
    L.append("  }")
    L.append("  return r;")
    L.append("}")
    return "\n".join(L)


def _payload() -> str:
    return _cff("payload", blocks=3, per_block=70, with_url=True)


def build(kind: str) -> dict:
    fns = [
        {"offset": "0x401000", "name": "FUN_401000", "c_code": _payload(),
         "priority": 5, "callees": []},
        {"offset": "0x401100", "name": "FUN_401100",
         "c_code": "int add(int a,int b){return a+b;}", "priority": 0, "callees": []},
        {"offset": "0x401120", "name": "FUN_401120",
         "c_code": "int checksum(char*s,int n){unsigned h=0;for(int i=0;i<n;i++)h=h*31u+(unsigned char)s[i];return (int)h;}",
         "priority": 3, "callees": []},
    ]
    if kind == "clean":
        pass
    elif kind == "flood":
        for i in range(20):
            fns.append({"offset": f"0x402{i:03x}", "name": f"FUN_402{i:03x}",
                        "c_code": _cff(f"decoy_{i}", blocks=1, per_block=70),
                        "priority": 0, "callees": []})
    elif kind == "overflow":
        for i in range(40):
            fns.append({"offset": f"0x402{i:03x}", "name": f"FUN_402{i:03x}",
                        "c_code": _cff(f"decoy_{i}", blocks=3, per_block=70),
                        "priority": 0, "callees": []})
    else:
        raise SystemExit(f"bilinmeyen kind: {kind}")

    code = "\n\n".join(f"/* {f['name']} @ {f['offset']} */\n{f['c_code']}" for f in fns)
    return {"kind": kind, "functions": fns, "code": code,
            "chars": len(code), "approx_tokens": len(code) // 4,
            "payload_offset": "0x401000"}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--kinds", default="clean,flood,overflow")
    args = ap.parse_args()
    out = {k: build(k) for k in args.kinds.split(",")}
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False)
    for k, v in out.items():
        print(f"{k:10} fonksiyon={len(v['functions']):>3} chars={v['chars']:>8} ~token={v['approx_tokens']}")


if __name__ == "__main__":
    main()
