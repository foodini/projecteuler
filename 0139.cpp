#include <math.h>
#include <stdio.h>

#include "util.h"

/*
8s of runtime, though I was on battery at the time.

This takes a little explaining...

Call the short leg of the triple a, the long leg b, the size of the inscribed
box l and the size of the excribed box L. Maybe I should have gone with h for
the long leg.

Anyway. You don't want to try all the pythagorean triples and see if the
inscribed triangle's length is an integer divisor of the excribed triangle.
You'll end up doing a buttload of unnecessary work.

Instead, I started with the size of the inscribed square (l), iterated over all
the multiples of l to generate all the possible values of L. Given l and L, I
needed a way to compute a and b.

We know:
  (1) L^2 = a^2 + b^2
also:
  (2) b = a + l

To eliminate b, we substitute (2) into (1):
  (3) L^2 = 2a^2 + 2al + l^2

Collecting everything to one side gives us:
  (4) L^2 - l^2 = 2a^2 + 2al

Dividing by two:
  (5) L^2 - l^2
      ---------  =  a^2 + al
          2

Rearranging:
  (6)            L^2 - l^2
      a^2 + al - ---------  =  0
                     2

The quadratic equation (for an equation of the form x = Aa^2 + Bx + C = 0)
  (7)     -B +- sqrt(B^2 - 4AC)
      a = ---------------------
                  2A

We'll use:
  A = 1
  B = l
  C = (-L^2 + l^2)/2

This gives us (dropping the +-, since negatives are not of interest to us):
  (8)     -l + sqrt(l^2 + 2(L^2 - l^2))
      a = -----------------------------
                        2

Any time a is not exactly an integer, our l and L don't participate in a
Pythagorean Triple.

I don't know if there are any ways to reduce the search space further.
*/

s64 max_size = 100000000;
u64 count = 0;

int main() {
  s64 a;
  s64 b;
  s64 L;
  for(s64 l = 1; l < max_size/2; l++) {
    for(s64 tiles = 2; tiles * l < max_size/2; tiles++) {
      L = tiles * l;
      a = (-l + sqrt(l*l + 2*(L*L-l*l)))/2;
      b = a + l;
      // If that sqrt didn't come up an int, this'll fail:
      if(a*a+b*b == L*L && a+b+L < max_size) {
        //printf("a:%ld b:%ld L:%ld l:%ld tiles:%ld\n", a, b, L, l, tiles);
        count++;
      }
    }
  }
}

