#!/usr/bin/env python3

def triangular_generator():
  n = 2
  while True:
    yield n*(n+1)//2
    n += 1

def pentagonal_generator():
  n = 2
  while True:
    val = n*(3*n-1)//2
    pents.add(val)
    yield val
    n += 1

def hexagonal_generator():
  n = 2
  while True:
    val = n*(2*n-1)
    hexes.add(val)
    yield(val)
    n += 1

pents = set()
max_pent = 1
hexes = set()
max_hex = 1

g3 = triangular_generator()
g5 = pentagonal_generator()
g6 = hexagonal_generator()

last_5 = next(g5)
last_6 = next(g6)

while True:
  last_3 = next(g3)
  while last_5 < last_3:
    last_5 = next(g5)
  while last_6 < last_3:
    last_6 = next(g6)

  if last_3 in pents and last_3 in hexes and last_3 > 40755:
    print(last_3)
    exit(0)
