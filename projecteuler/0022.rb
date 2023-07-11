def score(name)
    sum = 0
    name.each_byte do |b|
        sum += (b - 64)
    end
    sum
end

File.open("0022.txt", "r") do |fd|
    sum = 0
    line = 1
    while not fd.eof?
        name = fd.readline
        name.chomp!
        sum += line * score(name)
        line += 1
    end
    puts sum
end

