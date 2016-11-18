#! /usr/bin/python
''' map reduce program to make email pattern matching efficient '''

import csv 
import re
from collections import defaultdict,Counter 
import math


def normalize(sample_text,name='normal'):
	regex = '[^A-Za-z0-9]+'
	return re.sub(regex,'',str(sample_text).partition('@')[0])


def get_cosine(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())
     numerator = sum([vec1[x] * vec2[x] for x in intersection])

     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator

def text_to_vector(text):
	WORD = re.compile(r'\w+')
	words = WORD.findall(text)
	return Counter(words)

def cos(sample1,sample2):
	sample1 = normalize(sample1,'cos')
	sample2 = normalize(sample2,'cos')
	vector1 = text_to_vector(' '.join(sample1))
	vector2 = text_to_vector(' '.join(sample2))
	cosine = get_cosine(vector1, vector2)
	return int(cosine*100)


def lcs(a, b):
	a = normalize(a)
	b = normalize(b)
	lengths = [[0 for j in range(len(b)+1)] for i in range(len(a)+1)]
	for i, x in enumerate(a):
		for j, y in enumerate(b):
			if x == y:
				lengths[i+1][j+1] = lengths[i][j] + 1
			else:
				lengths[i+1][j+1] = max(lengths[i+1][j], lengths[i][j+1])
	result = ""
	x, y = len(a), len(b)
	while x != 0 and y != 0:
		if lengths[x][y] == lengths[x-1][y]:
			x -= 1
		elif lengths[x][y] == lengths[x][y-1]:
			y -= 1
		else:
			assert a[x-1] == b[y-1]
			result = a[x-1] + result
			x -= 1
			y -= 1
	return (float(len(result))/len(a))*100 






map_list = []#[ 'pillaimanoj27@gmail.com', 'prasanth.pillai1983@gmail.com']
def map_function():
	with open('neha.csv','rU') as f :
		reader = csv.DictReader(f)
		for row in reader:
			print row
			map_list.append(row.get('email')) 
	outer_counter = 0
	for email in map_list :
		outer_counter += 1
		inner_counter = 0
		for second_email in map_list :
			inner_counter += 1
			if (inner_counter == outer_counter):
				continue;
			value =  str(int(lcs(email,second_email)))+ str('#')+str(int(cos(email,second_email)))
			print str(email)+" "+str(value)

def check():
	value =  str(int(lcs(map_list[0],map_list[1])))+ str('#')+str(int(cos(map_list[0],map_list[1])))
	print str(value)

#check()
map_function()
