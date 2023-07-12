def factors(i)
    retval = Hash.new()
    while i!=1
        (2..i).each do |f|
            if i%f == 0
                i/=f
                retval[f]=true
                break
            end
        end
    end
    retval.size
end

sequence_length = 4

i=2
count = 0
lastcount = -1
consecutive=1
while true
    count = factors(i)
    if count == lastcount
        consecutive+=1
    else
        consecutive=1
        lastcount=count
    end
    if consecutive==sequence_length && count==sequence_length
        puts i-sequence_length+1
        exit 0
    end
    i += 1
end
