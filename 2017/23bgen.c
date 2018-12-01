long mul_count;
long func(long a) {
    long b, c, d, e, f, g, h;
    b = c = d = e = f = g = h = 0;
    mul_count = 0;

    b = 99;
    c = b;
    if (a) goto L0;
    goto L1;

L0:
    b *= 100; mul_count++;
    b += 100000;
    c = b;
    c += 17000;

L1:
    f = 1;
    d = 2;

L2:
    e = 2;

L3:
    g = d;
    g *= e; mul_count++;
    g -= b;
    if (g) goto L4;
    f = 0;

L4:
    e += 1;
    g = e;
    g -= b;
    if (g) goto L3;
    d += 1;
    g = d;
    g -= b;
    if (g) goto L2;
    if (f) goto L5;
    h += 1;

L5:
    g = b;
    g -= c;
    if (g) goto L6;
    goto L7;

L6:
    b += 17;
    goto L1;

L7:
    return h;
}

