### Group 4
### Computational Physics
### Spring, 2017

################################################################################
### This code will look at the 2D Random Walk: a random walker is simulated in
### 2D taking steps of unit length in +/- x or +/-y on a square lattice
###       a) plot <x_n> and <<x_n>^2> up to n=100 by averaging at least 10^4
###          different walks for each n>3
###             --- COMPLETE
###       b) show that motion is diffusive, i.e. that the mean square distance
###          from the starting point <r^2>~t and t~n... then determine the value
###          of the diffusion constant with an "eyeball" fit
###             --- COMPLETE
###           NOTE: did a polyfit, not "eyeball"
###      ADDITIONALLY: plot <distance>, find fit for the log(steps) log (distance),
###            found the equation for <distance> and overlay scatter with fit
###          +
###             additional plots for the random walks over different steps
###             plot of x-posiiton over 10 000 runs
################################################################################

import numpy
import random
import matplotlib.pyplot as plt

################################################################################
### Define initial variables and functions
################################################################################

# ------------------------------------------------------------------------------

# Create the random walker function
def randomWalk2D(x0,y0,n):
	#set up a first position
	position=numpy.matrix([x0,y0])
	d1=numpy.sqrt(x0**2+y0**2)
	displacement=numpy.array([d1])
	# random seed
	random.seed()
	# loop through
	for i in range(0,n-1):
		# get a random number in range (0,1)
		rand=random.random()
		# Assume equal probability to step in 4 directions
		# p=0.25
		if rand<=0.25: #step down
			xN=position[i,0]
			yN=position[i,1]-1
		elif .25<rand<=0.5: # step up
			xN=position[i,0]
			yN=position[i,1]+1
		elif .5<rand<=0.75: # step left
			xN=position[i,0]-1
			yN=position[i,1]
		else: # step right
			xN=position[i,0]+1
			yN=position[i,1]
		# Add the new position to the array
		position=numpy.vstack((position, numpy.array([xN,yN])))
		#extract the displacement using sqrt(x^2+y^2)
		displacementH = numpy.sqrt((x0 - position[i,0])**2 + (y0 - position[i,1])**2)
		displacement=numpy.append(displacement,displacementH)

	return position, displacement

# ------------------------------------------------------------------------------

# Check the function with the following parameters
# Start from a position in the origin
x0G = 0
y0G = 0
# Number of steps
n1000 = 1000
n20 = 20

# ------------------------------------------------------------------------------

################################################################################
### Create Plots
################################################################################

# ------------------------------------------------------------------------------

                                # PLOT ONE
# This plot is not explicitly asked for, but it shows that our random walker is
# working as it should.

# Call the random walker function for a test of 20 steps
positionN20, displacementN20 = randomWalk2D(x0G,y0G,n20)

# Take x and y for plotting
x=positionN20[:,0]
y=positionN20[:,1]

# Plot, overlay of colored scatter and line
fig = plt.figure()
fig.suptitle('Random walk representation ($20$ steps)',fontsize=25)

plt.scatter(x,y, c=range(len(x)),marker="o",s=50)
plt.plot(x,y, 'k')
plt.xlabel('distance $x$ ',fontsize=25)
plt.ylabel('distance $y$',fontsize=25)

plt.grid(True)
plt.show()

# Call the random walker function for a test of 1000 steps
positionN1000, displacementN1000 = randomWalk2D(x0G,y0G,n1000)

# Take x and y for plotting
x=positionN1000[:,0]
y=positionN1000[:,1]

# Plot, overlay of colored scatter and line
fig = plt.figure()
fig.suptitle('Random walk representation ($1000$ steps)',fontsize=25)

plt.scatter(x,y, c=range(len(x)),marker="o",s=50)
plt.plot(x,y, 'k')
plt.xlabel('distance $x$ ',fontsize=25)
plt.ylabel('distance $y$',fontsize=25)

plt.grid(True)
plt.show()

# ------------------------------------------------------------------------------

                                # PART A and B
                                
# This plot will be of <xn> , <xn^2>,<distance^2> and additionally <distance> up to n=100, averaged over 10^4 walks.

# We run a for-loop that calls the random walker 10^4 number of times (can be varied: runs)
# Then save the x-coordinate for every run in a matrix, where every run is a column
# And save the x^2-coordinate for every run in a  separate matrix
# In a separate for loop we then average over every row, and get <x> and <x^2>

#Specify parameters
runs=10000
nSteps=100
runX=numpy.zeros((nSteps,runs)) #empty matrix for mean values for x
runX2=numpy.zeros((nSteps,runs)) #empty matrix for mean squared values
dist=numpy.zeros((nSteps,runs)) #empty matrix for distance 
dist2=numpy.zeros((nSteps,runs)) #empty matrix for distance^2

#for loop from where random walker is called and matrix for (runs) is saved
for j in range(0,runs):
	walk, displacement=randomWalk2D(0,0,nSteps) #get a X,Y matrix with positions
	xValues=walk[:,0].flatten() #get x values for the random walks
	xValuesSquared=numpy.square(xValues) #get x^2 for the walk
	runX[:,j]=xValues #save x coordinates as one of the columns 
	runX2[:,j]=xValuesSquared #save x^2 coordinates as one of the columns
	dist[:,j]=displacement
	dist2[:,j]=numpy.square(displacement)

	

#initialize the empty matrix for means
meanAll=numpy.zeros(nSteps) #create an array for mean values
meanAllSq=numpy.zeros(nSteps) #create an array for mean of x^2 values
distAll=numpy.zeros(nSteps) #create an array for mean displacement
distAll2=numpy.zeros(nSteps) #create an array for mean displacement^2


#find averages
for row in range (0,nSteps): #for every row in the matrices runX and runX2
		meanAll[row]=numpy.mean(runX[row,:])
		meanAllSq[row]=numpy.mean(runX2[row,:])
		distAll[row]=numpy.mean(dist[row,:])
		distAll2[row]=numpy.mean(dist2[row,:])

	
n=range(4,nSteps) #range for n steps values for scatterplot

######## Find fit for the distance^2
fit=numpy.polyfit(n, distAll2[4:],1)
fitFunc=numpy.poly1d(fit) #define a function for a fit
print("Parameters for the fit: slope = ",fit[0],"shift: ",fit[1])


#NOTE: all graphs starts from n=4
		
#--------------- Plot <x>
plt.plot(meanAll[4:])
plt.title("Mean x-position for 10 000 runs", fontsize=15)
plt.xlabel("Step, n",fontsize=15)
plt.ylabel("Position on x-axis",fontsize=15)
plt.grid(True)
plt.show()

#--------------- Plot <x^2>
plt.plot(meanAllSq[4:])
plt.title("Mean x-squared position for 10 000 runs",fontsize=15)
plt.xlabel("Step, n",fontsize=15)
plt.ylabel("Value of x-squared",fontsize=15)
plt.grid(True)
plt.show()

##--------------- Plot <d^2>
plt.scatter(n,distAll2[4:])
plt.plot(n, fitFunc(n))
plt.title("Mean distance squared from origin for 10 000 runs",fontsize=15)
plt.xlabel("Step, n",fontsize=15)
plt.ylabel("Distance squared from origin",fontsize=15)
plt.grid(True)
plt.show()

##########################################################################################
################################### ADDITIONAL CALCULATIONS####################################
##########################################################################################
##########################################################################################


#------- Find fit for the mean distance travelled:
# Find log distance and log steps
# Should be a linear function a+bx, with the slope b equal to the power of t and 'exp(a)'=scaling

logN=numpy.log(n)
logDist=numpy.log(distAll[4:])

fitLog=numpy.polyfit(logN, logDist,1)
fitLogFunc=numpy.poly1d(fitLog)

print("Parameters for the log fit: slope = ",fitLog[0],"shift: ",fitLog[1])
print("Parameters for the power fit: power = ",fitLog[0],"scaling: ",numpy.exp(fitLog[1]))


#--------------- Plot log<d> vs log<N>
plt.scatter(logN,logDist)
plt.plot(logN, fitLogFunc(logN))
plt.title("Log-log plot, mean distance from origin,10 000 runs",fontsize=15)
plt.xlabel("Log step, n",fontsize=15)
plt.ylabel("Log distance from origin",fontsize=15)
plt.grid(True)
plt.show()


#--------------- Plot <d>
plt.scatter(n,distAll[4:])
plt.plot(n, numpy.exp(fitLog[1])*n**(fitLog[0]), 'r')
plt.title("Mean distance from origin for 10 000 runs",fontsize=15)
plt.xlabel("Step, n",fontsize=15)
plt.ylabel("Distance from origin",fontsize=15)
plt.grid(True)
plt.show()

#---------------------------Additional plot

#--------------- Plot x for 10^4 random walks
plt.plot(runX)
plt.title("Position x coordinate for 10 000 runs",fontsize=15)
plt.xlabel("Step, n",fontsize=15)
plt.ylabel("Position on x-axis",fontsize=15)
plt.grid(True)
plt.show()
