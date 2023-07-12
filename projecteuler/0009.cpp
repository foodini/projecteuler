#include <stdio.h>
#include <stdlib.h>

int main()
{
	//There are solutions that are far better, compute-time, but
	//I'm screaming through these in human time.

	for (int a=1; a<999; a++)
	{
		for (int b=1; b<999-a; b++)
		{
			int c = 1000 - a - b;
			if (a*a + b*b == c*c)
			{
				printf ("%d\n", a*b*c);
				exit(0);
			}
		}
	}
}
