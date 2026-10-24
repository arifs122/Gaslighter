#!/usr/bin/env python3
"""Tool-evasion variants (attack surface #4): packing and API hiding.

Variants:
  pack_base      : plain sample (control, copied from mut_base)
  pack_upx       : UPX-packed sample
  pack_unpacked  : UPX-packed then `upx -d` (control for the unpack step)
  dynapi         : socket/inet_addr/htons resolved via dlsym; API names and the
                   C2 strings are XOR-encoded

Payload is harmless: TEST-NET-1 (192.0.2.1), no connect, nothing executed.

Usage:
    python3 attacker/packing.py
"""
from __future__ import annotations

import os
import shutil
import subprocess

IP = "192.0.2.1"
URL = "http://192.0.2.1:4444/gate.php"
KEY = 0x5A
API = ["socket", "inet_addr", "htons"]

DYN = """\
#include <stdio.h>
#include <string.h>
#include <dlfcn.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

static void dec(char *out, const unsigned char *in, int n) {
    int i;
    for (i = 0; i < n; i++) out[i] = (char)(in[i] ^ %(key)s);
    out[n] = 0;
}

int main(void) {
    unsigned char e_socket[] = { %(e_socket)s };
    unsigned char e_inet[] = { %(e_inet)s };
    unsigned char e_htons[] = { %(e_htons)s };
    unsigned char e_ip[] = { %(e_ip)s };
    unsigned char e_url[] = { %(e_url)s };
    char s_socket[16], s_inet[16], s_htons[16], ip[32], url[96];

    dec(s_socket, e_socket, %(n_socket)d);
    dec(s_inet, e_inet, %(n_inet)d);
    dec(s_htons, e_htons, %(n_htons)d);
    dec(ip, e_ip, %(n_ip)d);
    dec(url, e_url, %(n_url)d);

    int (*p_socket)(int, int, int) =
        (int (*)(int, int, int))dlsym(RTLD_DEFAULT, s_socket);
    unsigned int (*p_inet)(const char *) =
        (unsigned int (*)(const char *))dlsym(RTLD_DEFAULT, s_inet);
    unsigned short (*p_htons)(unsigned short) =
        (unsigned short (*)(unsigned short))dlsym(RTLD_DEFAULT, s_htons);

    int s = p_socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in a;
    memset(&a, 0, sizeof(a));
    a.sin_family = AF_INET;
    a.sin_port = p_htons(4444);
    a.sin_addr.s_addr = p_inet(ip);
    printf("connecting to %%s\\n", url);
    (void)s;
    return 0;
}
"""


def arr(text: str) -> str:
    return ", ".join(str(b ^ KEY) for b in text.encode())


def main() -> None:
    outdir = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                           "..", "samples"))
    os.makedirs(outdir, exist_ok=True)

    base = os.path.join(outdir, "bin_mut_base")
    if not os.path.isfile(base):
        raise SystemExit("run `python3 attacker/mutate.py` first (bin_mut_base missing)")

    # 1) UPX packing
    pack_base = os.path.join(outdir, "bin_pack_base")
    shutil.copy2(base, pack_base)
    upx = os.path.join(outdir, "bin_pack_upx")
    proc = subprocess.run(["upx", "-9", "-o", upx, pack_base],
                          capture_output=True, text=True)
    print(f"  pack_upx       {'OK' if proc.returncode == 0 else proc.stderr.strip()[:80]}")
    unpacked = os.path.join(outdir, "bin_pack_unpacked")
    proc = subprocess.run(["upx", "-d", "-o", unpacked, upx],
                          capture_output=True, text=True)
    print(f"  pack_unpacked  {'OK' if proc.returncode == 0 else proc.stderr.strip()[:80]}")

    # 2) dynamic API resolution + encoded strings
    src = os.path.join(outdir, "sample_dynapi.c")
    code = DYN % {
        "key": hex(KEY),
        "e_socket": arr(API[0]), "n_socket": len(API[0]),
        "e_inet": arr(API[1]), "n_inet": len(API[1]),
        "e_htons": arr(API[2]), "n_htons": len(API[2]),
        "e_ip": arr(IP), "n_ip": len(IP),
        "e_url": arr(URL), "n_url": len(URL),
    }
    with open(src, "w", encoding="utf-8") as fh:
        fh.write(code)
    dyn = os.path.join(outdir, "bin_dynapi")
    proc = subprocess.run(["gcc", "-O0", "-w", "-o", dyn, src, "-ldl"],
                          capture_output=True, text=True)
    print(f"  dynapi         {'OK' if proc.returncode == 0 else proc.stderr.strip()[:80]}")


if __name__ == "__main__":
    main()
