#include <stdio.h>

int main()
{
	long long sum_of_squares=0;
	long long square_of_sums=0;
	long long sum=0;
	long long square;

	for (long long i=1; i<=100; i++)
	{
		sum += i;
		square = i*i;
		sum_of_squares += square;
	}
	square_of_sums = sum*sum;
	if (square_of_sums > sum_of_squares)
		printf ("%lld\n", square_of_sums - sum_of_squares);
	else
		printf ("%lld\n", sum_of_squares - square_of_sums );
}
