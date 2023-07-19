#!/usr/bin/env python3

#got 329469 in 143m 

import time

def fib():
  yield 1, 1
  yield 2, 1
  a = 1
  b = 1
  next_id = 3
  while True:
    a, b = b, a+b
    next_id += 1

    yield(next_id, b)

def is_pandigital(candidate):
  c = list(candidate)
  c.sort()
  if c == ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
    return True
  return False

fibgen = fib()

next_report_time = time.time() + 1.0
while True:
  fid, val = next(fibgen)
  if val >= 123456789:
    s = str(val)

    if next_report_time < time.time():
      print('ID:', fid, 'digits:', len(s))
      next_report_time = time.time() + 1.0

    starts_pandigital = is_pandigital(s[:9])
    if starts_pandigital:
      ends_pandigital = is_pandigital(s[-9:])
      if(ends_pandigital):
        print('s,e:', fid)
        exit(0)

