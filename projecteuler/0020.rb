class Fixnum
	def fact
		retval=1
		(1..self).each do |i|
			retval *= i
		end
		retval
	end
end

sum = 0
(100.fact).to_s.each_char do |i|
	sum += i.to_i
end
puts sum

