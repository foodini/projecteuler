sum = 0
(1...1000000).each do |i|
	str2 = i.to_s(2)
	str10 = i.to_s
	if str2 == str2.reverse and str10==str10.reverse then sum += i end
end

puts sum
