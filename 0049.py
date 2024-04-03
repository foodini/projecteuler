#!/usr/bin/env python3

from primes import is_prime

for first in range(1000,10000):
  for step in range(2, (10000-first)//2 + 1, 2):
    if not is_prime(first):
      continue

    second = first + step
    if not is_prime(second):
      continue

    first_sorted = sorted(list(str(first)))
    second_sorted = sorted(list(str(second)))
    if first_sorted != second_sorted:
      continue

    third = second + step
    if not is_prime(third):
      continue

    third_sorted = sorted(list(str(third)))
    if third_sorted != second_sorted:
      continue

    print(first, second, third)
