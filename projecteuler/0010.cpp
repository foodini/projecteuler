#include <stdio.h>
#include "primes.h"

int main()
{
	int i=0;
	long long sum=0LL;
	while (primes[i] < 2000000)
	{
		sum += primes[i];
		i++;
	}
	printf ("%lld\n", sum);
}
