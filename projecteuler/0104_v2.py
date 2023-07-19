#!/usr/bin/env python3

#got 329469 in 143m by just using bignum fib. This yielded a correct result in .6 seconds.

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

pandigital_set = set('123456789')
def is_pandigital(candidate):
  c = set(str(candidate))
  if c == pandigital_set:
    return True
  return False

#Up to 200000 values, starting w/ 30 digits, I've never seen the 19th digit bad.
#If I go lower than 18 digits, I get my first wrong answer (260932)
digits = 18
threshhold_val = 10**digits
fibgen = fib()

next_report_time = time.time() + 1.0
val = 0
while True:
  fid, val = next(fibgen)
  if val >= threshhold_val:
    break

#I know that these two values are the same length - I checked.
top_a = val
bottom_a = val
fid, val = next(fibgen)
top_b = val
bottom_b = val % 1000000000

if True:
  while True:
    while top_b > threshhold_val:
      top_a = top_a // 10
      top_b = top_b // 10

    top_c = top_a + top_b
    bottom_c = (bottom_a + bottom_b) % 1000000000

    top_candidate = str(top_c)[:10]
    if is_pandigital(bottom_c) and is_pandigital(top_candidate):
      print('k:', fid)
      exit(0)

    top_a = top_b
    top_b = top_c
    bottom_a = bottom_b
    bottom_b = bottom_c
    fid += 1
else:
  #runs forever, looking to see how many digits of the approximation are good.
  while True:
    while top_b > threshhold_val:
      top_a = top_a // 10
      top_b = top_b // 10

    top_c = top_a + top_b
    fid, val = next(fibgen)
    s = str(val)
    print('fid:', fid, 'len:', len(s))
    print('approx:', top_c)
    print('truncd:', s[:digits])
    for i, (a, t) in enumerate(zip(str(top_c),s)):
      if a != t:
        print('        ' + '='*i + 'X', i+1)
        break
    print('        =========|')
    top_a = top_b
    top_b = top_c
