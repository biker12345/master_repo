import numpy as np 
import matplotlib.pyplot as plt 
from sklearn.metrics import r2_score

np.random.seed(2)

pagespeed = np.random.normal(3.0,1.0,1000)
purchasedAmount = np.random.normal(50.0,10.0,1000)/pagespeed

x = np.array(pagespeed)
y = np.array(purchasedAmount)
point = np.poly1d(np.polyfit(x,y,7s))

print point
xp = np.linspace(0,7,100)
plt.scatter(x,y)
plt.plot(xp,point(xp),c='r')
plt.show()

rscore = r2_score(y,point(x))

print rscore


