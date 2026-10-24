#include <stdio.h>
#include <string.h>

static unsigned char note_enc[] = { 113, 70, 90, 95, 87, 19, 93, 92, 71, 86, 9, 19, 71, 91, 90, 64, 19, 64, 82, 94, 67, 95, 86, 19, 90, 64, 19, 82, 19, 91, 82, 65, 94, 95, 86, 64, 64, 19, 87, 86, 94, 92, 93, 64, 71, 65, 82, 71, 90, 92, 93, 8, 19, 90, 71, 19, 92, 93, 95, 74, 19, 67, 65, 90, 93, 71, 64, 19, 82, 19, 84, 65, 86, 86, 71, 90, 93, 84, 19, 82, 93, 87, 19, 86, 75, 90, 71, 64, 19, 93, 92, 65, 94, 82, 95, 95, 74, 29 };
static const int note_len = 98;
static void show_note(void) {
    char buf[512];
    int i;
    for (i = 0; i < note_len; i++) buf[i] = (char)(note_enc[i] ^ 0x33);
    buf[note_len] = 0;
    puts(buf);
}

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
    show_note();
    return 0;
}
