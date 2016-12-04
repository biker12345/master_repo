import pandas as pd
import numpy as np
from scipy import spatial
import operator


def ComputeDistance(a,b):
    genreA = a[1]
    genreB = b[1]
    genre_distance = spatial.distance.cosine(genreA,genreB)
    popularityA = a[2]
    popularityB = b[2]
    popularity_distance = abs(popularityA-popularityB)
    return genre_distance + popularity_distance

def getNeighbours(movieID,K):
    distances = []
    for movie in movieDict :
        if (movie != movieDict) :
            dist = ComputeDistance(movieDict[movie],movieDict[movieID])
            distances.append((movie,dist))
    distances.sort(key=operator.itemgetter(1))
    nbhrs = []
    for x in range (K):
        nbhrs.append(distances[x][0])

    return nbhrs

r_cols = ['user_id','movie_id','rating']
ratings = pd.read_csv('/Users/saurabhpandey/Desktop/DataScience/ml-100k/u.data',sep='\t',names=r_cols,usecols=range(3))

moviesProperties = ratings.groupby('movie_id').agg({'rating':[np.size,np.mean]})

#print  moviesProperties.head(10)

moviesNumRatings = pd.DataFrame(moviesProperties['rating']['size'])
movies_normalized_num_rating = moviesNumRatings.apply(lambda x : (x - np.min(x))/(np.max(x)-np.min(x)))

#print movies_normalized_num_rating.head(10)


movieDict = {}
with open(r'/Users/saurabhpandey/Desktop/DataScience/ml-100k/u.item') as f:
    temp = ''
    for line in f:
        fields = line.rstrip('\n').split('|')
        movieID = int(fields[0])
        name = fields[1]
        genres = fields[5:25]
        genres = map(int, genres)
        movieDict[movieID] = (name, genres, movies_normalized_num_rating.loc[movieID].get('size'), moviesProperties.loc[movieID].rating.get('mean'))

#print movieDict[1]


K = 10
avgRatings = 0
neighbours = getNeighbours(1,K)
ordered_list = pd.Series()
for n in neighbours :
    avgRatings += movieDict[n][3]
    print movieDict[n][0]  + " " + str(movieDict[n][3])

avgRatings = float(avgRatings)/K

print avgRatings



