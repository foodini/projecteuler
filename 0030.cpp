#include <stdio.h>

typedef unsigned long long int u64;

bool fifth_sum(u64 i)
{
    u64 sum=0;
    u64 digit=0;
    u64 tmp = i;
    while (tmp)
    {
        digit = tmp%10;
        sum += digit*digit*digit*digit*digit;
        tmp /= 10;
    }
    return sum == i;
}

int main()
{
    u64 sum = 0;
    for (u64 i=2; i<=194979; i++)
    {
        if (fifth_sum(i))
        {
            sum += i;
        }
    }
    printf("How do you know when to stop?  %lld\n", sum);
}
