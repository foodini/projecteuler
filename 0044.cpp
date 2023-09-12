#include <stdio.h>
#include <vector>
#include <set>

using namespace std;

#include "util.h"

u128 next_pent_id = 1;
u128 largest_pent_val = 0;
set<u128> pent_set;
vector<u128> pent_vector;

void expand_by_one() {
  u128 pent = next_pent_id*(3*next_pent_id-1)/2;
  pent_set.insert(pent);
  pent_vector.push_back(pent);
  largest_pent_val = pent;
  next_pent_id++;
}

void expand_to(u128 u) {
  while(largest_pent_val < u) {
    expand_by_one();
  }
}

bool is_pent(u128 u) {
  expand_to(u);
  return pent_set.find(u) != pent_set.end();
}
// pair for which sum and difference is also in set, but for which
// the difference is minimized.

int main() {
  u128 foo = 12345;

  // We need a 1-indexed vector, so I'm sticking in a placeholder at 0
  pent_vector.push_back(0);

  u128 sum, diff;
  u128 min_diff = 1ULL<<63; // Damn well better be big enough.
  for(u128 i = 2; ; i++) {
    while(i >= next_pent_id) {
      expand_by_one();
    }
    for(u128 j = i-1; j > 0; j--) {
      sum = pent_vector[i] + pent_vector[j];
      diff = pent_vector[i] - pent_vector[j];
      if(is_pent(sum) && is_pent(diff)) {
        if(diff < min_diff) {
          min_diff = diff;
          print_u128(i, ' ');
          print_u128(j, ' ');
          print_u128(min_diff, '\n');
          exit(0); // I guess there's only one, 'cause the first one was right.
        }
      }
      if(diff > min_diff) {
        continue;
      }
    }
  }
}
