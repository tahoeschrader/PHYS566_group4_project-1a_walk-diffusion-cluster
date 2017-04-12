from percolationClusterLabeling import mainFunction 
import numpy
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

import time


NValues=numpy.array([5,10,15,20,25,30,50,60, 70, 80, 100])
timeArray=numpy.zeros(NValues.size)
count=0
for N in NValues:
    start = time.time()
    print("Started calculation for N=", N)
    value, matrix=mainFunction(N, False)
    end = time.time()
    print('Time required for N=', N,end - start)
    timeArray[count]=end - start
    count+=1
    
print(timeArray)



fig = plt.subplot()
plt.title('Time required to run percolation for varied N',fontsize=20)
plt.plot(NValues, timeArray, color= 'tomato', label='', lw=3)
plt.ylabel('Time (s)',fontsize=15)
plt.xlabel('Size N',fontsize=15)
plt.grid()
fig.spines["top"].set_visible(False)
fig.spines["right"].set_visible(False)
plt.savefig("images/timeElapsed.png")
plt.show()


print(value)