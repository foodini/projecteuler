#include <stdio.h>
#include "primes.h"

int main()
{
    int square;
    int root;
    for (int i=9;;i+=2)
    {
        bool can=false;
        if (!is_prime(i))
        {
            for (root=1; (square=root*root)<i; root++)
            {
                if (is_prime(i-square*2))
                {
                    can=true;
                    break;
                }
            }
            if (can==false)
            {
                printf ("%d\n", i);
                exit(0);
            }
        }
    }
}
