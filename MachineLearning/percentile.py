import numpy as np 
import matplotlib.pyplot as plt 

values = np.random.normal(0,0.5,10000)

print "90 percentile of the data is :" , np.percentile(values,90)