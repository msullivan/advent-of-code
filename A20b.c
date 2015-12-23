#include <stdio.h>

#define N 5000000
int nus[N];

int main() {
	for (int i = 1; i < N; i++) {
		for (int j = i, k = 0; j < N && k < 50; j += i, k++) {
			nus[j] += i*11;
		}
	}
	for (int i = 1; i < N; i++) {
		if (nus[i] >= 29000000) {
			printf("%d %d\n", i, nus[i]);
			break;
		}
	}
	return 0;
}
