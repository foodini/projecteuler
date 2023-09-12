#include <stdio.h>

// nine fours vs six sixes
int pyrs[37];
int cubes[37];

void roll(int sides, int remaining, int subtotal, int* counts) {
  if(remaining == 0) {
    counts[subtotal]++;
    return;
  }
  for(int i=1; i<=sides; i++) {
    roll(sides, remaining-1, subtotal+i, counts);
  }
}

int main() {
  for(int i=0; i < 37; i++) {
    pyrs[i] = cubes[i] = 0;
  }

  roll(4, 9, 0, pyrs);
  roll(6, 6, 0, cubes);

  double rolls=0;
  double wins=0;
  for(int p=9; p<=36; p++) {
    for(int c=6; c<=36; c++) {
      int games = pyrs[p] * cubes[c];
      rolls += games;
      if(p>c) {
        wins += games;
      }
    }
  }
  printf("%0.7lf\n", wins/rolls);
}
