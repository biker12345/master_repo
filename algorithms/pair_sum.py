def pair_sum(numbers , summation) :
	if len(numbers) < 2 :
		return False 

	seen = set()
	output = set()
	for num in numbers :
		target = summation - num

		if target not in seen :
			seen.add(num)

		else :
			output.add((min(num,target) , max(num,target)))
	
	print "\n".join(map(str,list(output)))


pair_sum([4,3,4,3],7)

