#!/usr/bin/env python3

# An embarrassingly easy one

prime = 28433
for i in range(7830457):
  prime *= 2
  prime %= 10000000000
prime += 1

print(prime)
