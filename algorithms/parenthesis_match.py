def paren_match(s) :

	if len(s) % 2 != 0 :
		return False 

	opening = set("({[")
	match =  set([('(',')') , ('[',']') ,('{','}')])
	stack = []

	for paren in s :
		if paren in opening :
			stack.append(paren)

		else :
			if len(stack) == 0:
				return False

			last_open = stack.pop()

			if (last_open,paren) not in match :
				return False

	return len(stack) == 0





print paren_match("[[({})]]") 