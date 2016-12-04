import numpy as np 
import matplotlib.pyplot as plt 


salary = np.random.normal(100.0,50.0,10000)

plt.hist(salary,50)
plt.show()

print salary.std()
print salary.var()
