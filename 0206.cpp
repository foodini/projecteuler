#include <stdio.h>
#include <stdlib.h>

inline bool check(unsigned long long int arg)
{
    if(arg%10 != 0) return false;
    arg/=100;
    if(arg%10 != 9) return false;
    arg/=100;
    if(arg%10 != 8) return false;
    arg/=100;
    if(arg%10 != 7) return false;
    arg/=100;
    if(arg%10 != 6) return false;
    arg/=100;
    if(arg%10 != 5) return false;
    arg/=100;
    if(arg%10 != 4) return false;
    arg/=100;
    if(arg%10 != 3) return false;
    arg/=100;
    if(arg%10 != 2) return false;
    arg/=100;
    if(arg%10 != 1) return false;
    return true;
}

int main()
{
    for(unsigned long long int i=1010101010ULL; i<=1389026623ULL; i++)
        if(check(i*i))
        {
            printf ("%lld\n", i);
            exit (1);
        }
}
