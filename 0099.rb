values = []

largest = 0
largest_base = 0
largest_exp = 0
largest_line_num = 0

File.open("0099.txt") do |fd|
    i=1
    while not fd.eof?
        line = fd.readline
        line =~ /^([0-9]+),([0-9]+)$/
        base = $1
        exp = $2
        base = base.to_i
        exp = exp.to_i
        val = exp * Math.log(base)
        if val > largest
            largest = val
            largest_base = base
            largest_exp = exp
            largest_line_num = i
        end
        i+=1
    end
end

puts largest_line_num
