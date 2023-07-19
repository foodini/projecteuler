#include <stdio.h>

#include "util.h"

void print_u128(u128 u, char end) {
  u64 mask = -1ULL;
  u64 least = u & mask;
  u64 most = u >> 64;
  if(most)
    printf("%lu%lu", most, least);
  else
    printf("%lu", least);
  if(end)
    printf("%c", end);
}

double now() {
  timeval tv;
  gettimeofday(&tv, NULL);

  double retval = tv.tv_sec;
  retval += tv.tv_usec/1000000.0;
  return retval;
}

bool progress_timer() {
  static double next_print_time = 0.0;
  double current_time = now();
  if(current_time > next_print_time) {
    next_print_time = current_time + 1.0;
    return true;
  }
  return false;
}
