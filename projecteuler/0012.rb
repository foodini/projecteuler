require 'divisors'

def digits(val)
	if val<0 then val=-val end
	count=1
	while val>=10
		count+=1
		val/=10
	end
	count
end

i=1
test = 1
most = 0
while true
    count = num_unique_divisors(test)
    if count > most
        most = count
        if count >= 500
            puts test
            exit
        end
    end
    i+=1
    test += i
end
