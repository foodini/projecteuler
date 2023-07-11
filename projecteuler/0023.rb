require 'divisors'

class Array
    def sum
        retval = 0
        each do |i|
            retval += i
        end
        retval
    end

    def search(i)
        min = 0
        max = size-1
        while (min < max-1)
            mid = (max+min)/2
            if i < self[mid]
                max = mid
            else
                min = mid
            end
        end
        if self[min] == i or self[max] == i then return i else return nil end
    end
end

def abundant(i)
    if unique_divisors(i)[0..-2].sum > i
        return i
    else
        return nil
    end
end

abundants = (1..28123).collect{|i| abundant(i)}.compact

sum = 0

(1..28125).each do |test|
    writable = false
    abundants.each do |this_abundant|
        if this_abundant>test then break end
        if abundants.search(test - this_abundant)
            writable = true
            break
        end
    end
    unless writable then sum += test end
end

puts sum
