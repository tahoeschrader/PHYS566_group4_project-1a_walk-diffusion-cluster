### Group 4
### Computational Physics
### Spring, 2017

################################################################################
### This code will run the percolation functions over various N. Needs the code
### from the file percolationClusterLabeling.py. We will:
### Run the code over various N 50x to create an average
###      --- COMPLETE
### Plot pc(N^-1) to extrapolate infinite size limit pc(0)
###      --- INCOMPLETE
### ----------------------------------------------------------------------------
### Then, for the special case where N = 100:
### Determine F(p>pc) = # spanning sites / # occupied sites average over 50x
###      --- INCOMPLETE
### Plot F = F0(p-pc)^beta
###      --- INCOMPLETE
### Fit the result to a power-ansatz law by plotting the log of both sides and
### extracting the slope with a line of best fit. P must not be too far above pc.
###      --- INCOMPLETE
################################################################################

# ------------------------------------------------------------------------------

from percolationClusterLabeling import mainFunction
import numpy
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# ------------------------------------------------------------------------------

################################################################################
### Define curve fitting functions
################################################################################

# ------------------------------------------------------------------------------

def func(x,a,b,c):
    return a*x/(b+x)+c

# ------------------------------------------------------------------------------

################################################################################
### Initialize variables
################################################################################

# ------------------------------------------------------------------------------

# Time how long it takes to complete this code
import time
start = time.time()
print("hello")

# Parameters
Nvalues = numpy.array([5,10,15,20,30,50,80])  # Range of N's
runs = 50                                     # Number of runs to average over
pValues=numpy.zeros(len(Nvalues))             # Array for the p-values, same length as N
count = 0                                     # Counter for the position in the pValues array

# ------------------------------------------------------------------------------

################################################################################
### Run through all of the N's
################################################################################

# ------------------------------------------------------------------------------

for N in Nvalues:
    sumPvalues = 0 # value for calculating average, sum all over and then divide by sums
    for i in range(0,runs) : # repeat 50x
        # IMPORTANT: to save GIF plug in TRUE, BUT need player AND takes long

        # Call the main function
        value, matrix = mainFunction(N, False)
        sumPvalues += value

    # Now, average the p values and update the counter
    pValues[count]=sumPvalues/runs
    count+=1

print(pValues)
print(matrix)

end = time.time()
print(end - start)


#Need plot for the x=N^-1 and Pc
x = 1. / Nvalues

#create a fit
#fit=numpy.polyfit(numpy.log(x),numpy.log(pValues),2)
#fit_fn=numpy.poly1d(fit)

best_vals, pcov = curve_fit(func,x, pValues)
print(best_vals)
print('The critical value is',str(round(best_vals[2],3)))

xMany = numpy.arange(0,0.2, 0.01)

fig = plt.subplot()
plt.title('Critical probability and the lattice size',fontsize=20)
plt.scatter(x, pValues, color= 'tomato', label='', lw=3)
plt.plot(xMany, xMany*best_vals[0]/(xMany+best_vals[1])+best_vals[2],color='dodgerblue',linestyle='dashed', linewidth = 3, label='best fit')
plt.ylabel('Critical probability, $p_c$',fontsize=15)
plt.xlabel('$N^{-1}$, N=size of matrix',fontsize=15)
plt.legend()
plt.grid()
fig.spines["top"].set_visible(False)
fig.spines["right"].set_visible(False)
plt.savefig("images/criticalProb.png")
plt.show()
