from sklearn.cluster import KMeans
import matplotlib.pyplot as  plt
from sklearn.preprocessing import scale
from numpy import random,float,array
import numpy as np

def CreateClusterData(N,K):
    X = np.array([
            [20,3,0],
            [14,1,1],
            [55,2,2],
            [76,2,3],
            [22,2,1],
            [75,2,0],
            [98,1,0],
            [23,2,1],
            [94,2,3],
            [12,2,2],
            [45,1,0],
            [76,2,1],
            [67,2,2],
            [54,2,2],
            [77,1,0],
            [34,1,3],
            [87,2,3],
            [78,2,0],
            [90,1,2],
            [44,3,3]
    ]) 


    return X

data = CreateClusterData(20,4)
print data

model = KMeans(n_clusters=4)
model = model.fit(scale(data))


print model.labels_

plt.figure(figsize=(8, 6))
plt.scatter(data[:,0], data[:,1], c=model.labels_.astype(float))
plt.show()