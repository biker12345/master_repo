def reverse_sent(sentense) :
	import pdb;pdb.set_trace()
	sentense = sentense.strip()
	sentense = sentense.split()
	modified = ''
	for index in range(0,len(sentense)) :
		modified += ' ' + sentense[len(sentense)-(index+1)]

	return modified.strip()
	#return ' '.join(sentense.split()[::-1])

print reverse_sent("hello brother how are you    ")