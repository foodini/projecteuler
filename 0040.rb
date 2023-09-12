irrational = ""
(1..1000000).each do |i|
	irrational += i.to_s
end

printf "%d%d%d%d%d%d%d\n",
	irrational[0,1],
	irrational[9,1],
	irrational[99,1],
	irrational[999,1],
	irrational[9999,1],
	irrational[99999,1],
	irrational[999999,1]

