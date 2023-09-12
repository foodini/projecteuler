#include <stdio.h>

void reduce(int & n, int & d)
{
    int i;
    do
    {
        for (i=2; i<n && i<d; i++)
        {
            if (n%i==0 && d%i==0)
            {
                n/=i;
                d/=i;
                break;
            }
        }
    } while (i!=n && i!=d);
}

int main()
{
    double t_s = 3.0/7.0;
    double n_doub;
    double largest_n_doub=0.0;
    int n;
    int largest_n=0;
    int largest_d=0;
    int d;
    for (d=1; d<=1000000; d++)
    {
        n = (int)((double)d*t_s);
        n_doub = (double)n/(double)d;
        if (n_doub>largest_n_doub && n_doub < t_s)
        {
            largest_n = n;
            largest_d = d;
            largest_n_doub = n_doub;
        }
    }
    reduce(largest_n,largest_d);
    printf ("%d\n", largest_n);
}
