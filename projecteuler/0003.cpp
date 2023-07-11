#include <stdio.h>
#include <math.h>

int main()
{
	long long victim = 600851475143LL;
	long long largest = 0;
	long long i;

	while (victim != 1LL)
	{
		for (i=2; i<=victim; i++)
		{
			if (victim%i == 0)
			{
				if (i>largest)
					largest = i;
				victim /= i;
				break;
			}
		}
	}
	printf ("%lld\n", largest);
}
