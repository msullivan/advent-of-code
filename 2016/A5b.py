#!/usr/bin/env python3

import sys
import hashlib

sekrit='reyedfim'
#sekrit='abc'


def main(args):
    pas = ["*"]*8
    for i in range(1000000000):
        s=hashlib.md5((sekrit+str(i)).encode())
        ss = s.hexdigest()
        if ss.startswith("00000"):
            i = int(ss[5], 16)
            if i < 8 and pas[i] == "*": pas[int(ss[5])] = ss[6]
#            pas += ss[5]
            print(len(pas), i, "".join(str(i) for i in pas), ss)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
