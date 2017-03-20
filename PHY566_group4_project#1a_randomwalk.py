### Group 4
### Computational Physics
### Spring, 2017

################################################################################
### This code will look at the 2D Random Walk: a random walker is simulated in
### 2D taking steps of unit length in +/- x or +/-y on a square lattice
###       a) plot <x_n> and <<x_n>^2> up to n=100 by averaging at least 10^4
###          different walks for each n>3
###             --- INCOMPLETE
###       b) show that motion is diffusive, i.e. that the mean square distance
###          from the starting point <r^2>~t and t~n... then determine the value
###          of the diffusion constant with an "eyeball" fit
###             --- INCOMPLETE
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
	# random seed
	random.seed()
	# loop through
	for i in range(0,n):
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

	# Extract the final displacement from origin with pythagorean theorem
	displacement = numpy.sqrt((x0 - position[n-1,0])**2 + (y0 - position[n-1,1])**2)

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
plt.savefig("LaTeX/run20.png")
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
plt.savefig("LaTeX/run1000.png")
plt.show()

# ------------------------------------------------------------------------------

                                # PLOT TWO
# This plot will be of <xn> and <xn^2> up to n=100, averaged over 10^4 walks.
# First, we must obtain this data. A loop is run that calls randomWalk2D x 10^4

# Want a for loop to run a random walker over a bunch of different n's. Initialize
# the averaged displacement vectors
xn = numpy.zeros(100)					# we are told to solve for n=100 values
xn2 = numpy.zeros(100)

# Now, begin the loops
for n in range(4,104) :				    # skip n=0,1,2,3 because they are trivial
	# Initialize the displacement vector to have 10^4 spots to be averaged
	displacement = numpy.zeros(10**4)

	# Initialize a counter
	counter = 0

	# Begin the averaging loop
	while counter < 10**4 :
		position, displacement[counter] = randomWalk2D(x0G,y0G,n)

		# Add to the counter
		counter = int(counter + 1)

	# Average the final displacement and save it to xn and xn2. Recall we only
	# started at 4 so I must subtract this from the index
	xn[n-4] = sum(displacement)/n
	xn2[n-4] = (sum(displacement)/n)**2

# Create a range of n values for plotting from 4 to 103 (thats 100 n values)
nrange = numpy.arange(4,104)

# Now, plot
fig = plt.figure()
fig.suptitle('Motion over $10^4$ Walkers',fontsize=25)


plt.plot(nrange,xn, 'k-', label='$\langle x_n \\rangle$')
plt.plot(nrange,xn2, 'r-', label='$\langle x_n^2 \\rangle$')
plt.xlabel('number of steps $n$ ',fontsize=25)
plt.ylabel('displacement $x_n$',fontsize=25)

plt.grid()
plt.savefig("LaTeX/motionofmanywalkers.png")
plt.show()
