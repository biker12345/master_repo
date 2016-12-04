import numpy as np 
import matplotlib.pyplot as plt 
from sklearn.metrics import r2_score

np.random.seed(2)

pagespeed = np.random.normal(3.0,1.0,100)
purchasedAmount = np.random.normal(50.0,10.0,100)/pagespeed

trainx = pagespeed[:80]
testx = pagespeed[80:]

trainy = purchasedAmount[:80]
testy = purchasedAmount[80:]

# train data set 
#plt.scatter(trainx,trainy)
#plt.show()

#test data test 
#plt.scatter(testx,testy)
#plt.show()


x = np.array(trainx)
y = np.array(trainy)

point = np.poly1d(np.polyfit(x,y,2))

xp = np.linspace(0,7,100)
axes = plt.axes()
axes.set_xlim([0,7])
axes.set_ylim([0,200])
plt.scatter(x,y)
plt.plot(xp,point(xp),c='g')
plt.show()
 