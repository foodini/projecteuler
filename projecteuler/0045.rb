$nt = 286
$np = 166
$nh = 144

$t = 0
$p = 0
$h = 0

def update_t
    #puts "t #{$nt} #{$t}"
    $nt += 1
    $t = ($nt)*(($nt)+1)/2
end

def update_p
    #puts "p #{$np} #{$p}"
    $np += 1
    $p = ($np)*3*(($np)-1)/2
end

def update_h
    #puts "h #{$nh} #{$h}"
    $nh += 1
    $h = ($nh)*2*(($nh)-1)
end

update_t
update_p
update_h

done = false
until done
    if $t<$p or $t<$h
        update_t
    elsif $p<$t or $p<$h
        update_p
    elsif $h<$t or $h<$p
        update_h
    else
        done = true
    end
end

p $t
