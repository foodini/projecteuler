#include <stdio.h>

#include <algorithm>

#include "util.h"

// You couldn't generate the string if you wanted to. It would be terabytes
// long. Just doing the recursion here puts us well over the 60s CPU limit.
// I think I'm at about an hour with it.
//
// I think the correct solution is to look at how each level affects the state
// of the x, y, dx, dy, steps_taken and work out how many of each level are
// required to get to 10**12. Essentially, where's the 10**12th node in a
// binary tree of depth 50? I have mixed feelings about solving that problem.
// I CAN compute it in a few hours. Is it cheating to stop there or am I
// obligated to go with the version that'll take me a couple hours and compute
// in a sec?

s64 x = 0;
s64 y = 0;
s64 dx = 0;
s64 dy = 1;
u64 depth = 0;
u64 steps_taken = 0;
u64 max_steps = 1000000000000UL;
u64 max_depth = 50;
double next_update_time = 0.0;

void R() {
  std::swap(dx, dy);
  dy = -dy;
}

void L() {
  std::swap(dx, dy);
  dx = -dx;
}

void F() {
  x += dx;
  y += dy;
  steps_taken++;
  if(steps_taken == max_steps) {
    printf("%ld,%ld\n", x, y);
    exit(0);
  }
}

void b();

void a() {
  double t = now();
  if(t > next_update_time) {
    next_update_time = t + 1.0;
    printf("%f\n", (double)steps_taken/max_steps);
  }
  depth++;
  if(depth < max_depth) {
    a(); R(); b(); F(); R();
  }
  depth--;
}

void b() {
  depth++;
  if(depth < max_depth) {
    L(); F(); a(); L(); b();
  }
  depth--;
}

int main() {
  F(); a();
}
