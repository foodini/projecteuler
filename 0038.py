#!/usr/bin/env python3

for i in range(1,10000):
  concat = str(i)
  for m in range(2,11):
    if len(concat) > 9:
      break
    if len(concat) == 9:
      s = set(concat)
      if len(s) == 9 and '0' not in s:
        print (i, m-1, concat)
      break
    concat += str(i*m)
