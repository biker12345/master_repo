import pandas as pd

r_cols = ['user_id','movie_id','rating']
ratings = pd.read_csv('/Users/saurabhpandey/Desktop/DataScience/ml-100k/u.data',sep='\t',names=r_cols,usecols=range(3))

m_cols = ['movie_id','title']
movies = pd.read_csv('/Users/saurabhpandey/Desktop/DataScience/ml-100k/u.item',sep='|',names=m_cols,usecols=range(2))

ratings = pd.merge(movies,ratings)
user_ratings = ratings.pivot_table(index=['user_id'],columns=['title'],values='rating')
#corrMatrix = user_ratings.corr()
corrMatrix = user_ratings.corr(method='pearson',min_periods=100)
#print corrMatrix.head()

myRatings = user_ratings.loc[0].dropna()
print myRatings

simCandidates = pd.Series()
for i in range(0, len(myRatings.index)):
    #print "Adding sims for " + myRatings.index[i] + "..."
    # Retrieve similar movies to this one that I rated
    sims = corrMatrix[myRatings.index[i]].dropna()
    # Now scale its similarity by how well I rated this movie
    sims = sims.map(lambda x: x * myRatings[i] if myRatings[i] >= 3 else x * myRatings[i] - myRatings[i] )
    # Add the score to the list of similarity candidates
    simCandidates = simCandidates.append(sims)

# Glance at our results so far:
#print "sorting..."
simCandidates.sort_values(inplace = True, ascending = False)
#print simCandidates.head(10)
simCandidates = simCandidates.groupby(simCandidates.index).sum()
simCandidates.sort_values(inplace = True, ascending = False)
filteredSims = simCandidates.drop(myRatings.index)
print filteredSims.head(10)