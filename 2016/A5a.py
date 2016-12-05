#!/usr/bin/env python3

import sys
import hashlib

sekrit='reyedfim'
#sekrit='abc'


def main(args):
    pas = ""
    for i in range(1000000000):
        s = hashlib.md5((sekrit+str(i)).encode())
        ss = s.hexdigest()
        if ss.startswith("00000"):
            pas += ss[5]
            print(len(pas), i, pas, ss)
            if len(pas) == 8: break
    print(pas)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
