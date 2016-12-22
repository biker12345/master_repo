def string_compress (str1) :
	store_dict = {}
	for value in range(0,len(str1)) :
		if str1[value] in store_dict :
			store_dict[str1[value]] += 1
		else :
			store_dict[str1[value]] = 1

	return_string = ''
	for key,value in store_dict.items() :
		return_string += str(key)+str(value)

	return return_string




print string_compress("hhhhhAAAAABBBCCSSSJSJSJSJSJSJEEEeerrrEWWWWW")