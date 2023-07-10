#!/usr/bin/env python3

product = 1
factorials = {'0':1}
for x in range(1,10):
  product *= x
  factorials[f'{x}'] = product

print(factorials)

def next_step(val):
  sum = 0
  for c in str(val):
    sum += factorials[c]

  return sum

sixties = 0
for x in range(1000000):
  visited = set()
  val = x
  while val not in visited:
    visited.add(val)
    val = next_step(val)
  if len(visited) == 60:
    print(sixties, x)
    sixties += 1
print('Number of 60s:', sixties)
