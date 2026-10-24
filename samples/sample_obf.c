#include <stdio.h>
#include <string.h>



static unsigned char enc[] = { 50, 46, 46, 42, 96, 117, 117, 107, 99, 104, 116, 106, 116, 104, 116, 107, 96, 110, 110, 110, 110, 117, 61, 59, 46, 63, 116, 42, 50, 42 };
static const int enc_len = 30;

__attribute__((noinline)) static void bx(char *out) {
    int i;
    for (i = 0; i < enc_len; i++) out[i] = (char)(enc[i] ^ 0x5a);
    out[enc_len] = 0;
}

static void (*fp_build)(char *) = bx;

__attribute__((noinline)) static int opaque(int x) {
    return ((x * x + x) % 2) == 0;
}

int main(void) {
    char t[64];
    if (opaque(7)) { fp_build(t); }
    printf("connecting to %s\n", t);
    
    return 0;
}
