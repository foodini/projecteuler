products = Hash.new

i = 1
while i <= 9876
    j = 1
    while j <= 9876
        product = i * j
        str = i.to_s + j.to_s + product.to_s
        if str.length > 10
            break
        end
        if str.length == 9 and str.index('1') and str.index('2') and str.index('3') and str.index('4') and
            str.index('5') and str.index('6') and str.index('7') and str.index('8') and str.index('9')

            products[product] = true
        end
        j += 1
    end
    i += 1
end

sum = 0
products.keys.each {|i| sum += i}
puts sum
