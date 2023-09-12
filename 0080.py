#!/usr/bin/env python3

from mpmath import mp

mp.dps = 110

sum = 0
for i in range(2,101):
  sqrt = str(mp.sqrt(i))
  if len(sqrt) > 100:
    subsqrt = sqrt[0:101]
    #print(i, len(subsqrt))
    #print(sqrt)
    #print(f'  {subsqrt}')
    for c in subsqrt:
      if c != '.':
        sum += int(c)
    print(f'i: {i}', sum)

