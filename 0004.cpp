#include <stdio.h>
#include <stdlib.h>
#include <string.h>

bool pal(char *buf)
{
	char * begin = buf;
	char * end = buf + strlen(buf) - 1;

	while (begin <= end)
	{
		if (*begin != *end)
			return false;
		begin++;
		end--;
	}
	return true;
}

int main()
{
	int a, b, product, max=0;
	char buf[80];
	
	for (a=100; a<=999; a++)
	{
		for (b=100; b<999; b++)
		{
			product = a*b;
			sprintf (buf, "%d", product);
			if (pal(buf) && product>max)
				max = product;
		}
	}
	printf ("%d\n", max);
}
