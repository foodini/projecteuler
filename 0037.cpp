#include <stdio.h>
#include "primes.h"
#include <stdlib.h>

char buf[100];
int lop_off_top(int test)
{
	sprintf (buf, "%d", test);
	return atoi(buf+1);
}

int main()
{
	int sum=0;

	//the fifth prime is the first multi-digit prime
	for (int i=4; i<num_primes; i++)
	{
		int test = primes[i];
		//test is known to be prime...
		
		bool truncatable=true;
		while (test >= 10)
		{
			test /= 10;
			if (!is_prime(test))
				truncatable=false;
		}
		
		if (truncatable)
		{
			test = primes[i];
			while (test >= 10)
			{
				test = lop_off_top(test);
				if (!is_prime(test))
					truncatable=false;
			}
		}
		if (truncatable)
			sum+=primes[i];
	}
	printf ("%d\n", sum);
}
