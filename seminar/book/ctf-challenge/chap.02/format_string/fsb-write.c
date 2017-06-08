#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[])
{
  char text[1024];
  static int test_val = -72;

  if(argc<2) {
    printf("사용법: %s <출력할 테스트>\n", argv[0]);
    exit(0);
  }

  strcpy(text, argv[1]);

  printf("[+] Good example:\n");
  printf("%s\n", text);

  printf("[-] Bad example:\n");
  printf(text);

  printf("\n[*] test_val @ %p = %d, %p\n", &test_val, test_val, test_val);

  return 0;
}
