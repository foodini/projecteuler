#!/usr/bin/env python3

import itertools

def submod_nonzero(pandigital, start_index, prime):
  i = int(''.join(pandigital[start_index:start_index+3]))
  return i % prime != 0

l = [str(i) for i in range(10)]

total = 0
for i in itertools.permutations(l):
  if(submod_nonzero(i, 1, 2) or submod_nonzero(i, 2, 3) or
     submod_nonzero(i, 3, 5) or submod_nonzero(i, 4, 7) or
     submod_nonzero(i, 5, 11) or submod_nonzero(i, 6, 13) or
     submod_nonzero(i, 7, 17)):
    continue
  print(i)
  total += int(''.join(i))

print(total)
