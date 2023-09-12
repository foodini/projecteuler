Matrix = Hash.new(1000000000000)
Matrix[[-1,0]] = 0
Matrix[[0,-1]] = 0

row = 0
result = 0
STDIN.read.split("\n").each do |line|
    col = 0
    line.split(",").each do |cell|
        above = Matrix[[row-1, col]]
        left  = Matrix[[row, col-1]]
        #p "row:#{row}, col:#{col}, above:#{above}, left:#{left}"
        if above < left
            result = Matrix[[row, col]] = above + Integer(cell)
        else
            result = Matrix[[row, col]] = left + Integer(cell)
        end
        col = col + 1
    end
    row = row + 1
end

p result
