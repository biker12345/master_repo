# import particular packages 
import numpy as np  
import matplotlib.pyplot as plt 
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder,scale
from sklearn.pipeline import Pipeline


#class for label encoding 
class MultiColumnLabelEncoder:
    def __init__(self,columns = None):
        self.columns = columns # array of column names to encode

    def fit(self,X,y=None):
        return self # not relevant here

    def transform(self,X):
        '''
        Transforms columns of X specified in self.columns using
        LabelEncoder(). If no columns specified, transforms all
        columns in X.
        '''
        output = X.copy()
        if self.columns is not None:
            for col in self.columns:
                output[col] = LabelEncoder().fit_transform(output[col])
        else:
            for colname,col in output.iteritems():
                output[colname] = LabelEncoder().fit_transform(col)
        return output

    def fit_transform(self,X,y=None):
        return self.fit(X,y).transform(X)


# temp  variables 
lable_mapping = {}
trainset = []

# label encoding variable 
group_data = pd.DataFrame({
    'group':  ['a','b','c','d'],
    
})

# label encoding based on group column variables
lable_list = MultiColumnLabelEncoder(columns = ['group']).fit_transform(group_data)

# label mapping based on the groups 
# hardcoded because of small group size 
lable_mapping['a'] = lable_list['group'][0]
lable_mapping['b'] = lable_list['group'][1]
lable_mapping['c'] = lable_list['group'][2]
lable_mapping['d'] = lable_list['group'][3]

# open file to read values 
# xlsx can be read by pandas , but as dataset was small converted it into a csv 
with open('test.csv') as f :
	# all the data loaded 
	line = f.readline()
	# data breaked at ','
	# i.e [ 1 3 a , 1 4 b ,....]
	datasets = line.split(',')
	# loop through the dataset list 
	for loop in range (0,len(datasets)):
		# split the each individual dataset on ' '
		# i.e [1,3,a]
		indiset  = datasets[loop].split()
		# append data to convert it into trainset 
		trainset.append([int(indiset[0]),int(indiset[1]),lable_mapping[indiset[2]] ])



# convert the data into numpy array 
# due to performance of np array's over normal python arrays
X = np.array(trainset)

# initialize the Kmeans class 
kmean = KMeans()

# fit the variables 
kmean.fit(X)
# get the centroid values 
centroid = kmean.cluster_centers_
# get the cluster id /labels 
lables = kmean.labels_
print (centroid)
print(lables)

#plot the cluster points with same color to same cluster values 
scat = plt.scatter(X[:,0],X[:,1],c=kmean.labels_,s=50)
# plot the centroids 
plt.scatter(centroid[:,0],centroid[:,1],s=50,c='red',marker='+')

# plot the color bar to show the scale based on cluster id 
plt.colorbar(scat)

# show the  graph 
plt.show()
