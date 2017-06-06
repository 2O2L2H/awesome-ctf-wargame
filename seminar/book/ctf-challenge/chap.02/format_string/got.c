#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[])
{
  char str[128];

  fgets(str, 128, stdin);
  printf(str);

  fgets(str, 128, stdin);
  printf("%d\n", strlen(str));

  return 0;
}
