from sklearn.cluster import KMeans
import matplotlib.pyplot as  plt
from sklearn.preprocessing import scale
from numpy import random,float,array

def CreateClusterData(N,K):
    random.seed(10)
    pointsPerCluster = float(N)/K
    X = []
    for i in range (K) :
        incomeCentroid = random.uniform(20000.0,200000.0)
        ageCentroid = random.uniform(20.0,70.0)
        for j in range(int(pointsPerCluster)) :
            X.append([random.normal(incomeCentroid,10000.0),random.normal(ageCentroid,20.0)])
    X = array(X)

    return X

data = CreateClusterData(10,10)
print data

model = KMeans(n_clusters=10)
model = model.fit(scale(data))


print model.labels_

plt.figure(figsize=(8, 6))
plt.scatter(data[:,0], data[:,1], c=model.labels_.astype(float))
plt.show()