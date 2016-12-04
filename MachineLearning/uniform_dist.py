import numpy as np 
import matplotlib.pyplot as plt 

values = np.random.uniform(-10,10,10000)

plt.hist(values,100)
plt.show()