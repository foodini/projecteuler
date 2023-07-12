require 'primes'

ul = 7
ulinc = 14
lr = 3
lrinc = 10
ur = 9
urinc = 16
ll = 5
llinc = 12

primes = 3
total = 5
size = 3
while true
	ul += ulinc
	if ul.prime? then primes += 1 end
	ulinc += 8

	ur += urinc
	if ur.prime? then primes += 1 end
	urinc += 8

	lr += lrinc
	if lr.prime? then primes += 1 end
	lrinc += 8

	ll += llinc
	if ll.prime? then primes += 1 end
	llinc += 8
	size += 2

	total += 4

	if primes*10 < total 
		puts size 
		exit 0
	end
end
