from percolationClusterLabeling import mainFunction 
import numpy
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

import time
start = time.time()
print("hello")

NValues=[5,10,15,20,25,30,50,60]
for N in NValues:
    value, matrix=mainFunction(N, False)

end = time.time()
print('Time required for N=', N,end - start)

print(value)