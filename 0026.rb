# Kudos to David Parks on spitballing that remainders might be the key to this one.
#
# This could easily be done in one loop, but I wanted the logic units separated.
#
# Compute the array of remainders for 10^[0..i]/i.  When the remainders cycle, the
# decimal part cycles.  Note that there is an irrelevant bug in the cycle detection:
# 1/8 = 0.125, but the remainders will be 1, 2, 4, 0, 0, 0, (or nil, nil, nil) which
# is a 'cycle' of 1, though it happens after the point of interest.


Max = 1000
remainders = Hash.new
i=2
while i<Max
    j=0
    #printf "\b\b\b\b%4d", i
    remainders[i] = []
    while j<=i
        remainder = (10**j)%i
        remainders[i][j] = remainder
        j += 1
    end
    i += 1
end

#puts

largest = 0
result = 0

i=2
while i<Max
    j=1
    #printf "\b\b\b\b%4d", i
    while j<i
        index = remainders[i].index(remainders[i][j])
        unless index == j
            difference = j-index
            if difference > largest
                largest = difference
                result = i
            end
            break
        end
        j += 1
    end
    i += 1
end

#puts 
puts "1/#{result} cycle length: #{largest}: #{1.0/result}"
