def digital_sum(i)
    sum=0
    while i > 0
        sum += i%10
        i /= 10
    end
    sum
end
max = 0
(1...100).each do |a|
    (1...100).each do |b|
        sum = digital_sum(a**b)
        if sum>max then max = sum end
    end
end

puts max
