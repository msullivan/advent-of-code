#include <stdio.h>

/*
      1	set b 99
     2	set c b
     b = 99
     c = b
     if part2: goto 5
     3	jnz a !5
     4	jnz 1 !9
     5	mul b 100
     6	sub b -100000
     b = 99*100 + 100000 = 109900
     7	set c b
     8	sub c -17000
     c = 126900,

TOP:
     9	set f 1
    10	set d 2
OUTER:
    11	set e 2
INNER:
    12	set g d
    13	mul g e
    14	sub g b
if d*e == b:
   f = 0
    15	jnz g !17
    16	set f 0
e += 1
    17	sub e -1
g = e - b
    18	set g e
    19	sub g b
if e != b goto INNER
    20	jnz g !INNER
d += 1
    21	sub d -1
if d != b: goto OUTER
    22	set g d
    23	sub g b
    24	jnz g OUTER
if f == 0:
    h += 1
    25	jnz f !27
    26	sub h -1
if b == c:
    EXIT
    27	set g b
    28	sub g c
    29	jnz g !31
    30	jnz 1 EXIT
b += 17
goto TOP
    31	sub b -17
    32	jnz 1 TOP
*/


void func(long a) {
	long b, c, d, e, f, g, h;
	b = c = d = e = f = g = h = 0;

	long cnt = 0;

	b = 99;
	c = b;
	if (a) {
		cnt++;
		b = b*100 + 100000; /* 109900 */
		c = b + 17000; /* 126900 */
	}

	for (;;) {
		f = 1;
		d = 2;

		do {
			cnt += (b - 2);
			if (b % d == 0) f = 0;
			e = b;

			d++;
		} while (d != b);
		if (f == 0) {
			h++;
		}
		if (b == c) {
			printf("cnt: %ld\n", cnt);
			printf("h: %ld\n", h);
			return ;
		}
		b += 17;
	}

}

int main() {
	func(0);
	func(1);
}
