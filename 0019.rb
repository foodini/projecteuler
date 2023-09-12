#due to the lack of the date class on this machine, I had to
#run this code elsewhere, but it works.
require 'date'

count = 0

(1901..2000).each do |year|
    (1..12).each do |month|
        day = Date.new(year, month, 1)
        if day.wday == 0 then count += 1 end
    end
end

puts count
