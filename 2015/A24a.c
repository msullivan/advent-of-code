//meh

#include <stdio.h>

int checkrest(long *rest, int count, long tgt) {
	for (int mask = 0; mask < 1 << count; mask++) {
		long sum = 0;
		for (int i = 0, j = 0; i < count; i++) {
			if (mask & (1 << i)) {
				sum += rest[i];
			}
		}
		if (sum != total) continue;


}

void solve(long *nums, int count) {
	long total = 0;
	for (int i = 0; i < count; i++) {
		total += nums[i];
	}
	total /= 3;

	long min_count = 10000000000;
	long min_q = 1 << 63;

	for (int mask = 0; mask < 1 << count; mask++) {
		int pop = __builtin_popcount(mask);
		if (pop > min_count) continue;

		long sum = 0;
		long rest[50];
		for (int i = 0, j = 0; i < count; i++) {
			if (mask & (1 << i)) {
				sum += nums[i];
			} else {
				rest[j++] = nums[i];
			}
		}
		if (sum != total) continue;

int main() {
	char buf[1000];
	long nums[50];
	int i = 0;
	while (fgets(buf, sizeof(buf), stdin)) {
		nums[i++] = strtol(buf, NULL, 0);
	}
	solve(nums, i);
}
