#!/usr/bin/env python3

import sys, json

def crawl(obj):
    if isinstance(obj, int) or isinstance(obj, float):
        return obj

    sum = 0
    if isinstance(obj, list):
        for a in obj:
            sum += crawl(a)
    if isinstance(obj, dict):
        for a in obj.values():
            if a == "red":
                return 0
            sum += crawl(a)
    return sum

def main(args):
    shit = "\n".join([s.strip() for s in sys.stdin])
    js = json.loads(shit)

    print(crawl(js))

if __name__ == '__main__':
    sys.exit(main(sys.argv))
