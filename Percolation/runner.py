#runner for the percolation
# IMPORTANT - need the code from the percolationClusterLabeling

from percolationClusterLabeling import mainFunction 
import numpy
import matplotlib.pyplot as plt


##### INPUT parameters
#Range of Ns
Nvalues=numpy.array([5,10,15,20,30, 50,80])
#Number or runs <----------- Need to be 50
runs=50

############ Runner
# Array for the p-values, same length as N
pValues=numpy.zeros(len(Nvalues))

#Counter for the position in the pValues array
count=0

#Parse through N sizes and all runs
for N in Nvalues:        
    sumPvalues=0 #value for calculating average, sum all over and then divide by sums
    for i in range(0,runs): #repeat specified number of times

        ## IMPORTANT: to save GIF parse TRUE, BUT need player AND takes long
        value, matrix=mainFunction(N, False) #call the main function. Does everything
        sumPvalues+=value
    print('Still working, found the p values for matrix of size ', N) #update for the user
    #now we have pvalues summer 'runs' times
    pValues[count]=sumPvalues/runs
    count+=1 #update counter

print(pValues)
print(matrix)


######
#Need plot for the x=N^-1 and Pc
x=1/Nvalues

#create a fit
fit=numpy.polyfit(x,pValues,1)
fit_fn=numpy.poly1d(fit)

fig = plt.subplot()
plt.title('Critical probability and the lattice size',fontsize=20)
plt.plot(x, pValues, color= 'tomato', label='', lw=3)
plt.plot(x, fit_fn(x),color='dodgerblue',linestyle='dashed', linewidth = 3, label='best fit')
plt.ylabel('Critical probability, $p_c$',fontsize=15)
plt.xlabel('$N^{-1}$, N=size of matrix',fontsize=15)
plt.legend()
fig.text(0.1,0.6,'Curve parameters: $N^{-1}*$'+str(round(fit[0],3))+'+'+str(round(fit[1],3)))
plt.grid()
fig.spines["top"].set_visible(False)
fig.spines["right"].set_visible(False)
plt.savefig("images/criticalProb.png")
plt.show()
