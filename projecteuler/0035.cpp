#include <stdio.h>
#include <stdlib.h>
#include "primes.h"

int rotate(int i)
{
	//note the bug:  values with zeros in them rotate incorrectly, but
	//none are circular anyway, so I ignored the issue.
	if (i>99999)
		return i/10 + (i%10) * 100000;
	if (i>9999)
		return i/10 + (i%10) * 10000;
	if (i>999)
		return i/10 + (i%10) * 1000;
	if (i>99)
		return i/10 + (i%10) * 100;
	if (i>9)
		return i/10 + (i%10) * 10;
	return i;
}

int main()
{
	int count = 0;
	for (int i=1; i<1000000; i++)
	{
		bool all_prime = true;
		int k=i;
		for (int j=0; j<6; j++)
		{
			if (is_prime(k) != true)
				all_prime=false;
			k=rotate(k);
		}
		if (all_prime)
			count++;
	}
	printf ("%d\n", count);
}
