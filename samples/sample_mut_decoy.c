#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

__attribute__((noinline)) static int init_config(int x) { return x + 1; }
__attribute__((noinline)) static int read_config(int x) { return x * 2; }
__attribute__((noinline)) static int log_event(int x) { return x - 1; }
__attribute__((noinline)) static int checksum(int x) { return x ^ 0x55; }
__attribute__((noinline)) static int cleanup(int x) { return x | 1; }
__attribute__((noinline)) static int run_task(int x) { return x + 7; }

static void beacon(void) {
    int s = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in a;
    memset(&a, 0, sizeof(a));
    a.sin_family = AF_INET;
    a.sin_port = htons(4444);
    a.sin_addr.s_addr = inet_addr("192.0.2.1");
    printf("connecting to %s\n", "http://192.0.2.1:4444/gate.php");

    (void)s;
}

int main(void) {
    beacon();
    (void)init_config(1);
    (void)read_config(2);
    (void)log_event(3);
    (void)checksum(4);
    (void)cleanup(5);
    (void)run_task(6);
    return 0;
}
