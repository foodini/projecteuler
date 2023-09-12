require 'fact'

digits = 1
val = 9
while 9.fact * digits > val
	val = val*10+9
	digits += 1
end

#val now holds a number that is so large that its number of
#digits times the factorial of 9 is still smaller than itself.
#This should mean that there cannot be a larger number that 
#fits the description.

puts val

sum_of_all = 0

#NOTE!!!!  THey do  not figure that 1! or 2! count because,
#having only one digit, they do not count as sums.

(3..val).each do |i|
	if i%1000000 == 0 then puts i end
	sum = 0
	j=i
	while j>0
		sum += (j%10).fact
		j/=10
	end
	if sum == i 
		puts "--#{i}"
		sum_of_all += i
	end
end

puts sum_of_all
