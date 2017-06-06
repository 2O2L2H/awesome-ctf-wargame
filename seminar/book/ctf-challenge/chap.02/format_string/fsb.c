#include <stdio.h>
int secret = 0x12345678;

int main(int argc, char *argv[])
{
  char str[128];
  fgets(str, 128, stdin);
  printf(str);
  printf("secret = 0x%x\n", secret);
  return 0;
}
