sum = 0
(1<<1000).to_s.each_char do |i|
	sum += i.to_i
end
puts sum
