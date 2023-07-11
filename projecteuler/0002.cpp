#include <stdio.h>

int main()
{
	int a=1;
	int b=2;
	int sum=0;
	while (a<4000000)
	{
		if (a%2 == 0)
			sum += a;
		a += b;
		b^=a; a^=b; b^=a;
	}
	printf ("%d\n", sum);
}
