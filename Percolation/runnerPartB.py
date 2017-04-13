### Group 4
### Computational Physics
### Spring, 2017

################################################################################
### For the special case where N = 100:
### Determine F(p>pc) = # spanning sites / # occupied sites average over 50x
###      --- COMPLETE
### Plot F vs p
###      --- COMPLETE
### Fit the result to a power-ansatz law by plotting the log of both sides and
### extracting the slope with a line of best fit. P must not be too far above pc.
###      --- COMPLETE
################################################################################


# ------------------------------------------------------------------------------
# To run this code we do the follwoing:
#
# 1. Run the previous code until we have found the spanning cluster
#       (edit the original code so that it returns the number label of the cluster)
# 2. Run the updates on the cluster by adding numbers in the similar fashion as before.
#        Every 5 numbers added (varied), check the p
# 3. Run intil p==1
# ------------------------------------------------------------------------------


from percolationClusterLabeling import mainFunction
from percolationClusterLabeling import randomPlacement
from percolationClusterLabeling import checkCluster


import numpy
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

################################################################################
### Define functions
################################################################################

def fractionInSpanning(N):
    value, matrix, spanningNumber, clusterNumberOriginal = mainFunction(N, False)
                # value is the p_c
                # matrix is the updated matrix
                # spanningNumber=nuber that forms cluster
                # clusterNumberOriginal = the maximum numbering of clusters placed.
                #        Need to make sume we do not add 1's when there were
                #        1's added to the matrix originally

    # Save the number of points added before cluster was formed
    # This spaces out measurements of p
    clusterNumber = clusterNumberOriginal

    # Now we need to place the numbers in the matrix and check p's
    # When p is greater then .97 we stop

    # Start at the critical value
    p = value
    numberInSpanning = numpy.count_nonzero(matrix==spanningNumber)
    FVector = numpy.array([numberInSpanning/clusterNumber])
    pVector = numpy.array([p])
    while p < .97 :
        matrix, clusterNumber = randomPlacement(matrix, clusterNumber, N)
        cluster, spanningNumber = checkCluster(matrix, N)
        spanningNumber = spanningNumber[0]
        # Cluster number = number of elements in the list-1

        # Number of elements in the spanning cluster
        numberInSpanning = numpy.count_nonzero(matrix==spanningNumber)

        # F value
        F = numberInSpanning/clusterNumber
        p = clusterNumber/N**2
        FVector = numpy.append(FVector,F)
        pVector = numpy.append(pVector,p)
        #print('F=',F, 'for p=', p)
    return pVector, FVector

################################################################################
### Define paramters, N is 100 and runs is 50
################################################################################

N = 100
runs = 50

# Run fractionInSpanning once to get the size of pVector
#pValue=numpy.arange(0.6, 1,0.01)

pSums, FSums = fractionInSpanning(N)
lengthMax = pSums.size
print(lengthMax)

# Do an average: select the shortest pVector, and truncate all based on that
# Save all p_c along the way to get the best p_c for power law
pC = 0
for i in range(0, runs-1) : # repeat 50x
        print('Still working, on the',i, 'run')
        pVector, FVector = fractionInSpanning(N)
        pC += pVector[0]
        if pVector.size < lengthMax :
                # define new max, truncate sums
                pSums = pSums[(lengthMax-pVector.size):]
                FSums = FSums[(lengthMax-pVector.size):]
                lengthMax = pVector.size
        elif pVector.size > lengthMax :
                # truncate pVector
                pVector = pVector[(pVector.size-lengthMax):]
                FVector = FVector[(FVector.size-lengthMax):]

        pSums += pVector
        FSums += FVector

# Average for F from sums
pVector = numpy.divide(pSums, runs)
FVector = numpy.divide(FSums, runs)
pC = pC/runs
print(pC)


# Variation near p_c is the critical exponent
# Note, that the first value is roughly around the max critical p we ever got
# So now we take ~first 10% of points and go the power fit (this is the measure of 'close' to p_c)
part = int(pVector.size*0.1)

# Truncate p and F
pCut = pVector[:part]
fCut = FVector[:part]

pCutlog = numpy.log(pCut-pC)
fCutlog = numpy.log(fCut)


# Do curve fit
def func(x, a, b):
        return a+b*(x)

best_vals, pcov = curve_fit(func,pCutlog, fCutlog, p0=[0.1,1/36])
print('beta is:',best_vals[1], 'theoretical', 5/36)

################################################################################
### Create plots
################################################################################

fig = plt.subplot()
plt.title('Fraction of sites in percolating cluster',fontsize=20)
plt.scatter(pVector,FVector, color= 'tomato', label='', lw=2)
plt.xlabel('p',fontsize=15)
plt.ylabel('$F$',fontsize=15)
plt.grid()
fig.spines["top"].set_visible(False)
fig.spines["right"].set_visible(False)
plt.savefig("images/fractionF.png")
plt.show(block=False)

fig = plt.subplot()
plt.title('Fraction of sites in percolating cluster',fontsize=20)
plt.scatter(pVector,FVector, color= 'tomato', label='', lw=2)
plt.plot(pCut,numpy.exp(best_vals[0])*(pCut-pC)**best_vals[1],color='dodgerblue',linestyle='dashed', linewidth = 3)
plt.xlabel('p',fontsize=15)
plt.ylabel('$F$',fontsize=15)
plt.grid()
fig.spines["top"].set_visible(False)
fig.spines["right"].set_visible(False)
plt.savefig("images/fractionFwithFit10perc.png")
plt.show(block=False)

#Compare: what if we take ~first 20% of points and go the power fit (this is the measure of 'close' to p_c)
part = int(pVector.size*0.2)
# Truncate p and F
pCut = pVector[:part]
fCut = FVector[:part]

pCutlog = numpy.log(pCut-pC)
fCutlog = numpy.log(fCut)

#do curve fit
best_vals, pcov = curve_fit(func,pCutlog, fCutlog, p0=[0.1,1/36])
print('beta is:',best_vals[1], 'theoretical', 5/36)


fig = plt.subplot()
plt.title('Fraction of sites in percolating cluster',fontsize=20)
plt.scatter(pVector,FVector, color= 'tomato', label='', lw=2)
plt.plot(pCut,numpy.exp(best_vals[0])*(pCut-pC)**best_vals[1],color='dodgerblue',linestyle='dashed', linewidth = 3)
plt.ylabel('$F$',fontsize=15)
plt.xlabel('$p$',fontsize=15)
plt.grid()
fig.spines["top"].set_visible(False)
fig.spines["right"].set_visible(False)
plt.savefig("images/fractionFwithFit20perc.png")
plt.show(block=False)
