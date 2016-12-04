from scipy.stats import norm 
import matplotlib.pyplot as plt 
import numpy as np 

values  = np.arange(-3,3,0.001)
plt.plot(values,norm.pdf(values))
