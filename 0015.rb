class Fixnum
	def fact
		retval=1
		(1..self).each do |i|
			retval *= i
		end
		retval
	end
end

puts (4.fact / 2.fact) / 2.fact
puts (40.fact / 20.fact) / 20.fact
