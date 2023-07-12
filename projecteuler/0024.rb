class Fixnum
    def factorial
        product=1
        (2..self).each {|i| product*=i}
        product
    end
end


#(0..20).each do |max_this_stage|
max_this_stage = 999999
begin
    available = [0,1,2,3,4,5,6,7,8,9]
    result = []

    while available.size > 0
        #If we have 10 digits left then we select the first if we have
        #a shorter distance to go than there are permutations which
        #have that digit at this position.
        size = available.size
        fact = (size-1).factorial
        pos = max_this_stage / fact
        result.push available[pos]
        available.delete available[pos]
        max_this_stage -= pos * fact
    end

    puts result.join
end
