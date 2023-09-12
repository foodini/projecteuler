#include <stdio.h>
#include "int_sqrt.h"
#include <math.h>

//Had a real winner w ith this solution.  Algorithm worked and gave
//correct answer on the first try.

int main()
{
	int max_solutions=0;
	int max_solutions_p=0;
	int numerator;
	int denominator;
	int other_leg;
	int potential_hypotenuse;
	int leg_squared;
	int other_leg_squared;
	//I'm going to increase the length of one leg from 
	//1 to 292 - the max leg length of an isocoles triangle
	//of perimeter 1000.
	for (int p=3; p<=1000; p++)
	{
		int solutions=0;
		int maxleg = (int)(p/(2.0+1.41421356));
		for (int leg=1; leg<=maxleg; leg++)
		{
			//I worked out the math on this.  For a right
			//triangle of perimeter p, leg length l, the
			//length of the other leg is (p^2-2pl)/(2p-2l)
			numerator = p*p-2*p*leg;
			denominator = 2*p-2*leg;
			if (numerator%denominator == 0)
			{
				other_leg = numerator/denominator;
				leg_squared = leg*leg;
				other_leg_squared = other_leg*other_leg;
				potential_hypotenuse = int_sqrt(leg_squared+other_leg_squared);
				if (leg+other_leg+potential_hypotenuse == p)
					solutions++;
			}
		}
		if (solutions > max_solutions)
		{
			max_solutions = solutions;
			max_solutions_p = p;
		}
	}
	printf ("%d\n", max_solutions_p);
}
