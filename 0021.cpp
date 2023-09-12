#include <stdio.h>
int sum_of_divisors(int i)
{
    int sum=0;
    for (int j=1; j<i; j++)
    {
        if (i%j==0) sum += j;
    }
    return sum;
}

int main()
{
    int partner;
    int sum=0;
    for (int i=0; i<10000; i++)
    {
        partner = sum_of_divisors(i);
        if (partner!=i && sum_of_divisors(partner)==i)
            sum += i;
    }
    printf ("%d\n", sum);
}
