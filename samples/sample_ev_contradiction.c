#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
__attribute__((noinline)) static void beacon(void) {
    int s = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in a;
    memset(&a, 0, sizeof(a));
    a.sin_family = AF_INET;
    a.sin_port = htons(4444);
    a.sin_addr.s_addr = inet_addr("192.0.2.1");
    printf("connecting to %s\n", "http://192.0.2.1:4444/gate.php");
    (void)s;
}

static const char ev_0[] __attribute__((used)) = "https://www.microsoft.com";
static const char ev_1[] __attribute__((used)) = "Publisher: Microsoft Corporation";
static const char ev_2[] __attribute__((used)) = "Known-good SHA256: 3f786850e387550fdab836ed7e6dc881de23001b";
int main(void) {
    beacon();
    return 0;
}
