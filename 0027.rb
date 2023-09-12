require 'primes'

max_n = 0
max_a = 0
max_b = 0

(-1000..1000).each do |a|
    (-1000..1000).each do |b|
        n=0
        while n*n+a*n+b > 1 and (n*n+a*n+b).prime?
            n+=1
        end
        if n > max_n
            max_a = a
            max_b = b
            max_n = n
        end
    end
end

puts max_a*max_b
