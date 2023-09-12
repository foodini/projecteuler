cubes = Hash.new()

i=1
last_cube_length = 0

while true do
	val = (i*i*i).to_s.split(//).sort
	if val.size > last_cube_length
		cubes.each_pair do |k,v|
			smallest = v[0]
			v.each do |candidate_smallest|
				if candidate_smallest < smallest then smallest = candidate_smallest end
			end
			if v.size == 5 
				puts smallest*smallest*smallest
				exit 0
			end
		end
		cubes = Hash.new()
		last_cube_length = val.size
	end
	if cubes[val] == nil
		cubes[val] = [i]
	else
		cubes[val].push i
	end
	i+=1
end

