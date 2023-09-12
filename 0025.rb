a=1
b=1
term=1
min = 10**999

while true
    b+=a
    a=b-a
    term += 1
    #puts "#{a} #{term}"
    if a>min
        puts term
        exit 0
    end
end
