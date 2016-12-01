#!/usr/bin/env python3

import hashlib

sekrit='bgvyzdsv'

for i in range(1000000000):
    s=hashlib.md5((sekrit+str(i)).encode())
    if s.hexdigest().startswith("000000"):
        print(i)
        break
