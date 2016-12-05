#!/usr/bin/env python3

import sys
import hashlib

sekrit='reyedfim'
#sekrit='abc'


def main(args):
    pas = ["*"]*8
    for i in range(1000000000):
        s = hashlib.md5((sekrit+str(i)).encode())
        ss = s.hexdigest()
        if ss.startswith("00000"):
            j = int(ss[5], 16)
            if j < 8 and pas[j] == "*": pas[int(ss[5])] = ss[6]
            print(i, "".join(pas), ss)
            if "*" not in pas: break
    print("".join(pas))

if __name__ == '__main__':
    sys.exit(main(sys.argv))
