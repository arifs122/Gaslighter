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

static const char ev_0[] __attribute__((used)) = "https://cdn.example.com/asset_00.js\nhttps://cdn.example.com/asset_01.js\nhttps://cdn.example.com/asset_02.js\nhttps://cdn.example.com/asset_03.js\nhttps://cdn.example.com/asset_04.js\nhttps://cdn.example.com/asset_05.js\nhttps://cdn.example.com/asset_06.js\nhttps://cdn.example.com/asset_07.js\nhttps://cdn.example.com/asset_08.js\nhttps://cdn.example.com/asset_09.js\nhttps://cdn.example.com/asset_10.js\nhttps://cdn.example.com/asset_11.js\nhttps://cdn.example.com/asset_12.js\nhttps://cdn.example.com/asset_13.js\nhttps://cdn.example.com/asset_14.js\nhttps://cdn.example.com/asset_15.js\nhttps://cdn.example.com/asset_16.js\nhttps://cdn.example.com/asset_17.js\nhttps://cdn.example.com/asset_18.js\nhttps://cdn.example.com/asset_19.js\nhttps://cdn.example.com/asset_20.js\nhttps://cdn.example.com/asset_21.js\nhttps://cdn.example.com/asset_22.js\nhttps://cdn.example.com/asset_23.js\nhttps://cdn.example.com/asset_24.js\nhttps://cdn.example.com/asset_25.js\nhttps://cdn.example.com/asset_26.js\nhttps://cdn.example.com/asset_27.js\nhttps://cdn.example.com/asset_28.js\nhttps://cdn.example.com/asset_29.js\nhttps://cdn.example.com/asset_30.js\nhttps://cdn.example.com/asset_31.js\nhttps://cdn.example.com/asset_32.js\nhttps://cdn.example.com/asset_33.js\nhttps://cdn.example.com/asset_34.js\nhttps://cdn.example.com/asset_35.js\nhttps://cdn.example.com/asset_36.js\nhttps://cdn.example.com/asset_37.js\nhttps://cdn.example.com/asset_38.js\nhttps://cdn.example.com/asset_39.js\nhttps://cdn.example.com/asset_40.js\nhttps://cdn.example.com/asset_41.js\nhttps://cdn.example.com/asset_42.js\nhttps://cdn.example.com/asset_43.js\nhttps://cdn.example.com/asset_44.js\nhttps://cdn.example.com/asset_45.js\nhttps://cdn.example.com/asset_46.js\nhttps://cdn.example.com/asset_47.js\nhttps://cdn.example.com/asset_48.js\nhttps://cdn.example.com/asset_49.js\nhttps://cdn.example.com/asset_50.js\nhttps://cdn.example.com/asset_51.js\nhttps://cdn.example.com/asset_52.js\nhttps://cdn.example.com/asset_53.js\nhttps://cdn.example.com/asset_54.js\nhttps://cdn.example.com/asset_55.js\nhttps://cdn.example.com/asset_56.js\nhttps://cdn.example.com/asset_57.js\nhttps://cdn.example.com/asset_58.js\nhttps://cdn.example.com/asset_59.js";
int main(void) {
    beacon();
    return 0;
}
