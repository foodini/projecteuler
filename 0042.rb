words = []
File.open("words.txt") do |fd|
    str = fd.read
    words = str.gsub(/"/, "").split(/,/)
end

t_nums = Hash.new
i = 1
while i <= 26
    t_nums[i*(i+1)/2] = true
    i += 1
end

count = 0

words.each do |word|
    len = word.length
    sum = -64 * len
    for i in 0...len do
        sum += word[i]
    end
    if t_nums[sum] then count += 1 end
end

puts count
