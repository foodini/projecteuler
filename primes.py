primes = dict()

def is_prime(p):
  if p not in primes:
    primes[p] = True
    for i in range(2, p//2+1):
      if p % i == 0:
        primes[p] = False
        break

  return primes[p]
