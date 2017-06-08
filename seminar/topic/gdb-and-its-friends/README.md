footer: GDB & its Friends © 2O2L2H Seminar, 2017
slidenumbers: true

# [fit] GDB & its Friends

---
# gdb

- Initial break point 가장 불편 ?

- `b*main`
- `r`


---
# gef

- `gef help` : Menu listup
- `entry-break` : Auto initial breakpoint
- `ctx` : context
- pros
  - `entry-break`
  - stack에서 `$esp`, `$ebp` 표
- cons



---
#  peda

- `peda` : Menu listup
- `context` : context menu
- `pdisas` : colorful display
- `elfsymbol`
- `find`
    `find /bin/sh libc`
- `ropgadget`
```
ret = 0x5555555544c0
popret = 0x555555554aab
pop2ret = 0x555555554eb1
addesp_8 = 0x555555554956
addesp_1064 = 0x555555554ea3
```

---
#  pwndbg

- `pwndbg` : menu print
- `entry` : Initial break point
- `ropper` : only print offset
- `plt`

---
#  [fit] Comparison : Screen, Easy to debug

- [O] gef : Best
- [] pwndbg : too small.
- [] peda

---
##  Comparison : Initial break

- [O] gef : `entry-break` - auto break on `__libc_start_main` 
- [0] peda : `break`
- [] pwndbg

---
## Comparison : stack canary : gef

- parent의 canary가 정해지면, 하위 child의 canary는 parent의 canary와 모두 동일하다.
- [0] gef

```
gef)  canary
[+] Found AT_RANDOM at 0xffffd0ab, reading 4 bytes
[+] The canary of process 1448 is 0x7f4c1300
```

- [0] pwndbg

```
pwndbg> canary
AT_RANDOM=0xffffd0a
```

- [x] peda


---
#  Comparison : string find

- [O] peda
- [] gef
- [] pwndbg

- Network 형태가 아니라 서버에 접속해서 풀 수 있는 문제라면 직접 주소 구하기 쉽다. 특히 libc 안에...


---
# [fit] Tool

---
# rpi++

- `libc` 와 같은 경우  standalone 으로 gadget offset 찾아야 할 필요 있음.
- gdb 에서 libc gadget print 하면 화면 너무 많이 넘어가 찾을 수 없음.
- [Downloads · 0vercl0k/rp](https://github.com/0vercl0k/rp/downloads)

```bash
$  rp-lin-x64
DESCRIPTION:
rp++ allows you to find ROP gadgets in pe/elf/mach-o x86/x64 binaries.
NB: The original idea comes from (@jonathansalwan) and its 'ROPGadget' tool.

USAGE:
./rp++ [-hv] [-f <binary path>] [-i <1,2,3>] [-r <positive int>] [--raw=<archi>] [--atsyntax] [--unique] [--search-hexa=<\x90A\x90>] [--search-int=<int in hex>]

OPTIONS:
  -f, --file=<binary path>  give binary path
  -i, --info=<1,2,3>        display information about the binary header
  -r, --rop=<positive int>  find useful gadget for your future exploits, arg is the gadget maximum size in instructions
  --raw=<archi>             find gadgets in a raw file, 'archi' must be in the following list: x86, x64
  --atsyntax                enable the at&t syntax
  --unique                  display only unique gadget
  --search-hexa=<\x90A\x90> try to find hex values
  --search-int=<int in hex> try to find a pointer on a specific integer value
  -h, --help                print this help and exit
  -v, --version             print version information and exit

$ rp-lin-x64 -f libc.so.6 -r 4
```





