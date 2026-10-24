#include <stdio.h>
#include <string.h>



__attribute__((noinline)) static void build_target(char *o) {
    o[0]='h';o[1]='t';o[2]='t';o[3]='p';o[4]=':';o[5]='/';o[6]='/';
    o[7]='1';o[8]='9';o[9]='2';o[10]='.';o[11]='0';o[12]='.';o[13]='2';
    o[14]='.';o[15]='1';o[16]=':';o[17]='4';o[18]='4';o[19]='4';o[20]='4';
    o[21]='/';o[22]='g';o[23]='a';o[24]='t';o[25]='e';o[26]='.';o[27]='p';
    o[28]='h';o[29]='p';o[30]='\0';
}

int main(void) {
    char t[64];
    build_target(t);
    printf("connecting to %s\n", t);
    
    return 0;
}
