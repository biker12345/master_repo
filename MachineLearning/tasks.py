# import particular packages 
import numpy as np  
import matplotlib.pyplot as plt 
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder,scale
from sklearn.pipeline import Pipeline


lable_mapping = {}
trainset = []

group_data = pd.DataFrame({
    'group':  ['a','b','c','d'],
    
})

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

lable_list = MultiColumnLabelEncoder(columns = ['group']).fit_transform(group_data)
lable_mapping['a'] = lable_list['group'][0]
lable_mapping['b'] = lable_list['group'][1]
lable_mapping['c'] = lable_list['group'][2]
lable_mapping['d'] = lable_list['group'][3]

with open('test.csv') as f :
	line = f.readline()
	datasets = line.split(',')
	for loop in range (0,len(datasets)):
		indiset  = datasets[loop].split()
		trainset.append([int(indiset[0]),int(indiset[1]),lable_mapping[indiset[2]] ])
print trainset



X = np.array(trainset)

kmean = KMeans()
kmean.fit(X)
centroid = kmean.cluster_centers_
lables = kmean.labels_
print (centroid)
print(lables)

scat = plt.scatter(X[:,0],X[:,1],c=kmean.labels_,s=50)
plt.scatter(centroid[:,0],centroid[:,1],s=50,c='red',marker='+')

plt.colorbar(scat)
plt.show()
