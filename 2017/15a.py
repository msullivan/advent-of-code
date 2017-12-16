import sys

def main(args):
    a, b = 873, 583

    count = 0
    for i in range(40 * 1000000):
        a = (a * 16807) % 2147483647
        b = (b * 48271) % 2147483647
        if (a & 0xffff) == (b & 0xffff):
            count += 1

    print(count)

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
