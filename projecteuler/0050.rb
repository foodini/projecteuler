require 'primes'

puts "997651  (3+542 more primes)"

prime_array = [2]

max = 1000000

(3...max).each do |i|
	if i%2 == 1 and i.prime? 
		prime_array.push i
	end	
end

largest_string=0
largest_prime=0
largest_string_start=0

(0...prime_array.size).each do |i|
	j=0
	sum=0
	while sum<max and i+j < prime_array.size
		sum += prime_array[i+j]
		j+=1
		if sum.prime? and j>largest_string and sum < max
			largest_string_start=i
			largest_string = j
			largest_prime = sum
		end
	end
end

puts "#{largest_prime}  (#{largest_string_start}+#{largest_string-1} more primes)"
