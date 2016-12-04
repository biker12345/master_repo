from sklearn.cluster import KMeans
import matplotlib.pyplot as  plt
from sklearn import svm,datasets
from numpy import random,float,array
import numpy as np

def CreateClusterData(N,K):
    random.seed(10)
    pointsPerCluster = float(N)/K
    X = []
    Y = []
    for i in range (K) :
        incomeCentroid = random.uniform(20000.0,200000.0)
        ageCentroid = random.uniform(20.0,70.0)
        for j in range(int(pointsPerCluster)) :
            X.append([random.normal(incomeCentroid,10000.0),random.normal(ageCentroid,20.0)])
            Y.append(i)
    X = array(X)
    Y = array(Y)

    return X ,Y


def plotPredictions(clf):
    xx, yy = np.meshgrid(np.arange(0, 250000, 10),
                         np.arange(10, 70, 0.5))
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

    plt.figure(figsize=(8, 6))
    Z = Z.reshape(xx.shape)
    plt.contourf(xx, yy, Z, cmap=plt.cm.Paired, alpha=0.8)
    plt.scatter(X[:, 0], X[:, 1], c=Y.astype(np.float))
    plt.show()


(X,Y) = CreateClusterData(100,5)

#plt.figure(figsize=(8,6))
#plt.scatter(X[:,0],X[:,1],c=Y.astype(np.float))
#plt.show()
svc = svm.SVC(kernel='linear',C=1.0).fit(X,Y)
plotPredictions(svc)