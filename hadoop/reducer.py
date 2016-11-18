#! /usr/bin/python 
import sys

previous_key = None 
total = 0


def output(previous_key,total):
	if previous_key is not None :
		print "%s was found thes many %d time(s)" % (previous_key,total)


for line in sys.stdin :
	key , value = line.split(" ",1)
	if key != previous_key :
		output(previous_key,total)
		previous_key = key 
		total = 0
	total += int(value)


output(previous_key,total)

