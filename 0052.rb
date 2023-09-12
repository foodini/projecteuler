i=1

def int_to_sorted_array(i)
	i.to_s.split(//).sort
end

while true do
	one = int_to_sorted_array(i)
	two = int_to_sorted_array(i*2)
	if one == two
		three = int_to_sorted_array(i*3)
		if two == three
			four = int_to_sorted_array(i*4)
			if three == four
				five = int_to_sorted_array(i*5)
				if four == five
					six = int_to_sorted_array(i*6)
					if five == six
						puts i
						exit 1
					end
				end
			end
		end
	end
	i+=1
end
