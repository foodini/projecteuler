sum = 1;  #the center

ul = 7
ulinc = 14
lr = 3
lrinc = 10
ur = 9
urinc = 16
ll = 5
llinc = 12
(1..500).each do
	sum += ul
	ul += ulinc
	ulinc += 8

	sum += ur
	ur += urinc
	urinc += 8

	sum += lr
	lr += lrinc
	lrinc += 8

	sum += ll
	ll += llinc
	llinc += 8
end

puts sum
