#include <stdio.h>

int main(int argc, char *argv[])
{
  int pos, x=235, y=93;
  printf("%d  %n %d\n", x, &pos, y);
  printf("The offset was %d\n", pos);
}
