#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#define SCALE 10000
#define MAX_INPUT 1000
#define MAX_BUF (MAX_INPUT*SCALE)

#define ITERS 10


#define min(x, y) ((x) < (y) ? (x) : (y))

uint8_t go(int n, int *partials, int end) {
    int step = n * 2;
    int mode = 1;

    int lo = n - 1;
    int hi = lo + n;
    int rhi = hi + n;

    int res = 0;
    int res2 = 0;

    while (rhi < end) {
        int val = partials[hi] - partials[lo];
        int val2 = partials[rhi] - partials[hi];
        //res += mode * val;
        res += val;
        res2 -= val2;
//        res += mode == 1 ? val : -val;
        //mode = -mode;
        lo += step;
        hi += step;
        rhi += step;
    }
    res += res2;

    while (lo < end) {
        hi = min(lo + n, end);
        res += mode * (partials[hi] - partials[lo]);
        mode = -mode;
        lo += step;
    }

    return abs(res) % 10;
}

int partials[MAX_BUF+1];
void fft(uint8_t *signal, int len) {
    partials[0] = 0;

    int sum = 0;
    for (int i = 0; i < len; i++) {
        sum += signal[i];
        partials[i+1] = sum;
    }

    for (int i = 0; i < len; i++) {
        signal[i] = go(i+1, partials, len);
    }
}


void print(uint8_t *signal, int offset, int n) {
    for (int i = 0; i < n; i++) {
        putchar('0' + signal[offset+i]);
    }
}

uint8_t signal[MAX_BUF];
int main(int *argc, char **argv) {
    char input[MAX_INPUT];

    if (!fgets(input, MAX_INPUT, stdin)) return 2;
    int len = strlen(input) - 1;

    if (len < 8) return 2;

    for (int i = 0; i < SCALE; i++) {
        for (int j = 0; j < len; j++) {
            signal[i*len + j] = input[j] - '0';
        }
    }
    input[7] = '\0';
    int offset = atoi(input);
    printf("offset: %d\n", offset);

    for (int i = 0; i < ITERS; i++) {
        printf("%d ", i);
        print(signal, 0, 8);
        printf(" ");
        print(signal, offset, 8);
        printf("\n");
        fft(signal, len*SCALE);
    }

    print(signal, offset, 8);
    printf("\n");

    return 0;
}
