def digits(i)
    count=0
    while i>0
        count+=1
        i/=10
    end
    count
end

num = 1
den = 1
count = 0
1000.times do
    num += den
    tmp = num
    num = den
    den = tmp
    num += den
    if digits(num) > digits(den) then count += 1 end
end

puts count
