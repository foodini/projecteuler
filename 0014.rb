max_chain_length = 0
which_number = -1
largest_j = 0

(2...1000000).each do |i|
	length = 1
	j=i
	while j!=1 do
		if j>largest_j then largest_j=j end
		length+=1
		if j%2 == 0
			j/=2
		else
			j = 3*j + 1
		end
	end
	if length > max_chain_length
		max_chain_length = length
		which_number = i
	end
end

puts "largest: #{largest_j}"
puts which_number
