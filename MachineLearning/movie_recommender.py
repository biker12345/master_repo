import pandas as pd
import numpy as np


r_cols = ['user_id','movie_id','rating']
ratings = pd.read_csv('/Users/saurabhpandey/Desktop/DataScience/ml-100k/u.data',sep='\t',names=r_cols,usecols=range(3))

m_cols = ['movie_id','title']
movies = pd.read_csv('/Users/saurabhpandey/Desktop/DataScience/ml-100k/u.item',sep='|',names=m_cols,usecols=range(2))

ratings = pd.merge(movies,ratings)

#print ratings.head()

movies_ratings = ratings.pivot_table(index=['user_id'],columns=['title'],values='rating')

#print movies_ratings.head()


starWarsRatings = movies_ratings['Star Wars (1977)']
starWarsRatings.head()

similar_movies = movies_ratings.corrwith(starWarsRatings)
similar_movies = similar_movies.dropna()
df = pd.DataFrame(similar_movies)
#print df.head(10)


#print  similar_movies.sort_values(ascending=False)

movieStats = ratings.groupby('title').agg({'rating':[np.size,np.mean]})
#print movieStats.head()

popularMovies =  movieStats['rating']['size'] >= 300
#print  popularMovies
new_list =  movieStats[popularMovies].sort_values([('rating', 'mean')], ascending=False)

#print new_list[:15]

df = movieStats[popularMovies].join(pd.DataFrame(similar_movies,columns=['similarity']))
#print df.head()
print df.sort_values(['similarity'],ascending=False)[:15]