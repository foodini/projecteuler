require 'primes'

largest = 0

pandigitals = []
new_pandigitals = []

(1..9).each do |digit|
	if pandigitals.size == 0
		pandigitals = ["1"]
	else
		pandigitals.each do |pd|
			(0...digit).each do |loc|
				#puts "'#{pd}'.insert(#{loc}, #{digit})"
				new = pd.clone
				new.insert(loc, digit.to_s)
				new_pandigitals.push new
			end
		end
		pandigitals = new_pandigitals
		new_pandigitals = []
	end
	pandigitals.each do |pd|
		int_val = pd.to_i
		if int_val > largest and int_val.prime?
			largest = int_val
		end
	end
end

puts largest
