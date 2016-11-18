# A dictionary of movie critics and their ratings of a small
# set of movies .
from math import sqrt
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
      'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
      'The Night Listener': 3.0},
     'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
      'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
      'You, Me and Dupree': 3.5},
     'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
      'Superman Returns': 3.5, 'The Night Listener': 4.0},
     'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
      'The Night Listener': 4.5, 'Superman Returns': 4.0,
      'You, Me and Dupree': 2.5},
     'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
      'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
      'You, Me and Dupree': 2.0},
     'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
      'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
     'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}



def pearson_score(pref ,person, another_person):
	store = {}
	for item in pref[person] :
		if item in pref[another_person] : 
			store[item] = 1
	count = len(store)
	if count == 0 :
		return 0

	summation1 = sum([pref[person][element] for element in store]) 
	summation2 = sum([pref[another_person][element] for element in store ])

	sumsqaure1 = sum([pow(pref[person][element],2) for element in store]) 
	sumsqaure2 = sum([pow(pref[another_person][element],2) for element in store])

	product_sum = sum([pref[person][element] * pref[another_person][element] for element in store ])

	# calculate pearson score 
	num  = product_sum - (summation1*summation2 /count)
	den  = sqrt((sumsqaure1 - pow(summation1,2)/count) * (sumsqaure2 - pow(summation2,2)/count )) 
	if den == 0 : return 0

	rem = num/den

	return rem 

print pearson_score(critics,'Lisa Rose','Gene Seymour')  



