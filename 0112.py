#!/usr/bin/env python3

def is_bouncy(n):
  increasing = False
  decreasing = False
  chars = str(n)

  for i in range(1, len(chars)):
    if chars[i] > chars[i-1]:
      increasing = True
    if chars[i-1] > chars[i]:
      decreasing = True

  if increasing and decreasing:
    return True

i = 100
bouncers = 0
while True:
  if is_bouncy(i):
    bouncers += 1
  fraction = bouncers/i
  if fraction == 0.99:
    print(i, bouncers/i)
    exit(0)
  i += 1
