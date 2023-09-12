class Bignum
	def digits
		val = self
		if val<0 then val=-val end
		count=1
		while val>=10
			count+=1
			val/=10
		end
		count
	end
end

class Fixnum
	def digits
		val = self
		if val<0 then val=-val end
		count=1
		while val>=10
			count+=1
			val/=10
		end
		count
	end
end

count = 0
		
base = 1
while base < 10
	exponent = 1
	while true
		val = base ** exponent
		val_digits = val.digits
		if val_digits == exponent
			count+=1
		elsif val_digits < exponent
			break
		end
		exponent += 1
	end
	base += 1
end

puts count
