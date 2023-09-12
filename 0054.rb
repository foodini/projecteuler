rank_hash = Hash.new
rank_hash["2"] = 2
rank_hash["3"] = 3
rank_hash["4"] = 4
rank_hash["5"] = 5
rank_hash["6"] = 6
rank_hash["7"] = 7
rank_hash["8"] = 8
rank_hash["9"] = 9
rank_hash["T"] = 10
rank_hash["J"] = 11
rank_hash["Q"] = 12
rank_hash["K"] = 13
rank_hash["A"] = 14

def flush(suits)
    suits.uniq.size == 1
end

def straight(ranks) 
    ranks.uniq.size == 5 and ranks.max == ranks.min + 4
end

def get_counts(ranks)
    counts = Hash.new(0)
    ranks.each {|i| counts[i] += 1}
    counts.values
end

def pack_value(top, ranks)
    retval = top.to_s
    #ranks.sort.reverse.each {|i| retval += sprintf "%02d", i}
    #I want the actual hash this time, so I'm not using the get_counts
    counts = Hash.new(0)
    #puts "ranks:"
    #puts ranks.inspect
    ranks.each {|i| counts[i] += 1}
    #puts "counts:"
    #puts counts.inspect
    groups = Hash.new([])
    counts.each_pair {|rank,count| if groups[count].size >0 then groups[count].push(rank) else groups[count]=[rank] end}
    #puts "groups:"
    #puts groups.inspect
    #puts
    if groups[4].size > 0 
        retval += sprintf "%02d%02d%02d%02d%02d", groups[4][0], groups[4][0], groups[4][0], groups[4][0], groups[1][0]
    elsif groups[3].size > 0
        if groups[2].size > 0
            retval += sprintf "%02d%02d%02d%02d%02d", groups[3][0], groups[3][0], groups[3][0], groups[2][0], groups[2][0]
        else
            groups[1].sort!
            retval += sprintf "%02d%02d%02d%02d%02d", groups[3][0], groups[3][0], groups[3][0], groups[1][1], groups[1][0]
        end
    elsif groups[2].size == 2
        groups[2].sort!
        retval += sprintf "%02d%02d%02d%02d%02d", groups[2][1], groups[2][1], groups[2][0], groups[2][0], groups[1][0]
    elsif groups[2].size == 1
        groups[1].sort!
        retval += sprintf "%02d%02d%02d%02d%02d", groups[2][0], groups[2][0], groups[1][2], groups[1][1], groups[1][0]
    else
        groups[1].sort.reverse.each {|i| retval += sprintf "%02d", i}
    end
    retval.to_i
end

def hand_value(hand, rank_hash)
    hand = hand.split(/ /)
    ranks = hand.collect do |c|
        rank_hash[c[0]]
    end
    suits = hand.collect {|c| c[1]}
    flushed = flush(suits)
    straighted = straight(ranks)
    if flushed and straighted then return pack_value(9, ranks) end
    counts = get_counts(ranks) 
    if counts.include?(4) then return pack_value(8, ranks) end
    trio = counts.include?(3)
    pair = counts.include?(2)
    if trio and pair then return pack_value(7, ranks) end
    if flushed then return pack_value(6, ranks) end
    if straighted then return pack_value(5, ranks) end
    if trio then return pack_value(4, ranks) end
    if pair and counts.size == 3 then return pack_value(3, ranks) end
    if pair then return pack_value(2, ranks) end
    return pack_value(1, ranks)
end

p1_wins = 0
File.open("54.txt", "r") do |fd|
    while not fd.eof?
        line = fd.readline
        p1 = line[0..13]
        p2 = line[15..-1]
        if hand_value(p1, rank_hash) > hand_value(p2, rank_hash) 
            #puts "#{p1} >  #{p2}"
            #puts "#{hand_value(p1, rank_hash)}  #{hand_value(p2, rank_hash)}"
            p1_wins += 1
        else
            #puts "#{p1} <= #{p2}"
            #puts "#{hand_value(p1, rank_hash)}  #{hand_value(p2, rank_hash)}"
        end
    end
end

puts p1_wins
