def permute(str1) :
	#import pdb ;pdb.set_trace()
	out = []
	if len(str1) == 1 :
		out = [str1]

	else :
		for i , let in enumerate(str1) :
			print i
			print "s[:i]="+str(str1[:i])
			print "s[i+1:]="+str(str1[i+1 :])
			for perm in permute(str1[:i] + str1[i+1:]):
				out += [let+perm]

	return out 


print permute("sau")