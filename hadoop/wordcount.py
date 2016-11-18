#! /usr/bin/python 
import sys 
from collections import defaultdict 

words = defaultdict(int)

for line in sys.stdin :
	for word in line.split() :
		words[word] += 1

for word ,count in sorted(words.items()):
	print "found  :" + word + " these many :" + count + " times."
