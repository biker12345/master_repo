''' 
	python script to find anagrams 

'''
import collections 

def anagram (str1 , str2) :
	str2 = str2.replace(' ','')
	str1 = str1.replace(' ','')
	return sorted(str1) == sorted(str2)

str1 = "go0d"
str2 = "d go"

print anagram(str1,str2)