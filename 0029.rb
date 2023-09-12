# I should try to think through the mathematical way of doing this one...

e = Hash.new

a=2
while a <= 100
    b=2
    while b <= 100
        e[a**b] = true
        b += 1
    end
    a += 1
end

puts e.size
