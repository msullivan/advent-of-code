#!/usr/bin/env python3

# also b

import sys, json

def main(args):
    shit = [s.strip() for s in sys.stdin]
    # Hilariously, this was range(8) when I first did it
    # and it still passed part A.
    # Apparently none of the rect writes ever write to already lit
    # pixels, which means you could solve part A without implementing
    # rotate!
    # Then I spent a while being *super* confused in part B since
    # the things didn't look like fucking letters at all.
    pixels = [[0]*50 for i in range(6)]

    for line in shit:
        if "rect" in line:
            [_, a] = line.split(" ")
            [wid,h] = [int(x) for x in a.split("x")]
            for i in range(wid):
                for j in range(h):
                    pixels[j][i] = 1
        elif "rotate column" in line:
            [_, a] = line.split("=")
            [col,amt] = [int(x) for x in a.split(" by ")]
            pixels_2 = list(map(list, zip(*pixels)))
            pixels_2[col] = (pixels_2[col][-amt:] + pixels_2[col])[:len(pixels_2[col])]
            pixels = list(map(list, zip(*pixels_2)))
        elif "rotate row" in line:
            [_, a] = line.split("=")
            [col,amt] = [int(x) for x in a.split(" by ")]
            pixels_2 = pixels
            pixels_2[col] = (pixels_2[col][-amt:] + pixels_2[col])[:len(pixels_2[col])]
            pixels = pixels_2

        print("\n")
        print("\n".join("".join(" ."[i] for i in (x)) for x in (pixels)))

    cnt = sum(sum(x) for x in pixels)
    print(cnt)



if __name__ == '__main__':
    sys.exit(main(sys.argv))
