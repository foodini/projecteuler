#include <stdio.h>

char buf[6000000];

#define INTAT(a) (buf[a]-'0')

int main()
{
	char *ptr = buf;
	int bytes;
	//I start at zero so that my indices match up.  They refer to the first
	//location as 1, so I need junk in the first byte to make the 'th object a
	//a 1.
	for (int i=0; i<1000000; i++)
	{
		bytes = sprintf(ptr, "%d", i);
		ptr += bytes;
	}
	printf ("%d\n", INTAT(1)*INTAT(10)*INTAT(100)*INTAT(1000)*INTAT(10000)*INTAT(100000)*INTAT(1000000));
	return 0;
}
