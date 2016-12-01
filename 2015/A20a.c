#include <stdio.h>

#define N 5000000
int nus[N];

int main() {
	for (int i = 1; i < N; i++) {
		for (int j = i; j < N; j += i) {
			nus[j] += i*10;
		}
	}
	for (int i = 1; i < N; i++) {
		if (nus[i] >= 29000000) {
			printf("%d %d\n", i, nus[i]);
		}
	}
	return 0;
}
