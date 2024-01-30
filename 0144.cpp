#include <math.h>
#include <stdio.h>

#include "util.h"

/*
0.002s of user time.

real	0m0.351s
user	0m0.002s
sys	  0m0.003s

Nothing spectacular, but if I run into a bunch more problems that require
vector math, I'll put together some of the basic functions in util.

Rather than trying to solve the intersection point analytically, I opted for a
very basic approach that should be familiar to anyone with some basic precalc.
Any point that lies inside of the ellipse will evaluate (using the function
given, 4*x*x + y*y = 100) to a value less than 100. Any point outside the
ellipse will evaluate to something greater.

Given a start point and a direction the beam is travelling, I just binary search
for the point where the beam hits the edge. I do this by choosing three points
along that beam. One that is zero units away, one that is 25 units away, and one
that is halfway between them. I analyze the function at the halfway point. If
the halfway point is inside the ellipse, I know the "surface" of the ellipse is
between the halfway point and the most distant one. If the halfway point is
outside the ellipse, I know the surface is between the halfway and the near
point. With each step, I reset the near, far, and mid points and try again until
the equation value at the mid point is within a very small error of 100.

This gives me the intersection point. Some basic math gives me the normal to the
surface of the ellipse at that point, then some geometry to compute the
reflection vector, then do it all over again.

I chose this method because it's pretty familiar to me, having written a butt-
load of ray tracers and ray marchers. This method is pretty similar to a ray
marcher with a couple differences. First, I don't have a good way to compute a
DISTANCE from the surface of the ellipse, so I don't try. The distance function
in ray-marchers assumes very complex geometry, which I don't have to worry about
here, so I can just do the binary search.
*/

void normalize(f64 & x, f64 & y) {
  f64 len = sqrt(x*x+y*y);
  x /= len;
  y /= len;
}

f64 dot(f64 x0, f64 y0, f64 x1, f64 y1) {
  f64 retval = x0*x1 + y0*y1;
  return retval;
}

void reflect(f64 & dx, f64 & dy, f64 nx, f64 ny) {
  f64 d = dot(dx, dy, nx, ny);
  if(d < 0.0) {
    d = -d;
    dx = -dx;
    dy = -dy;
  }
  f64 rx, ry;

  dx = 2.0 * d * nx - dx;
  dy = 2.0 * d * ny - dy;
  normalize(dx, dy);
}

int main() {
  f64 x=0.0;
  f64 y=10.1;
  f64 dx = 1.4;
  f64 dy = -19.7;
  f64 nx, ny;

  u64 reflection_count = 0;
  while(true) {
    normalize(dx, dy);

    f64 min_t = 0.0;
    f64 max_t = 25.0;
    f64 mid_t = 10.0;
    while(true) {
      f64 test_x = x + dx*mid_t;
      f64 test_y = y + dy*mid_t;
      f64 f_of_p = (4*test_x*test_x + test_y*test_y);
      // Something I REALLY hate about this problem: the
      // result you get will depend very much upon the
      // epsilon you use here. If you remove a couple
      // zeroes, you'll get the wrong answer. How can we
      // be sure that the "right" answer IS the RIGHT
      // answer? Has anyone computed this with a few
      // thousand digits of accuracy?
      if(abs(f_of_p - 100.0) < 0.000000001) {
        x = test_x;
        y = test_y;
        break;
      }
      if(f_of_p > 100) {
        max_t = mid_t;
      } else {
        min_t = mid_t;
      }
      mid_t = (min_t + max_t) / 2.0;
    }
    f64 m = (-4*x) / y;
    nx = -m;
    ny = 1.0;
    normalize(nx, ny);
    if(y > 0.0) {
      nx = -nx;
      ny = -ny;
    }
    reflect(dx, dy, nx, ny);
    if(y > 0.0 && x >= -0.01 && x <= 0.01) {
      printf("%lu reflections\n", reflection_count);
      exit(0);
    }
    reflection_count++;
  }
}
