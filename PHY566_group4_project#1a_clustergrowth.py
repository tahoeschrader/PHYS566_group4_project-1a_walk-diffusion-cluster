### Group 4
### Computational Physics
### Spring, 2017

################################################################################
### This code will simulate cluster growth in 2D using a Diffusion Limited
### Aggregation Model (DLA). There will be three parts to this code:
###             1) Use a circle of radius 100 as a starting point of the random
###                walkers and a seed at the origin and grow a cluster till it
###                reaches the edge of the circle.
###                     --- COMPLETE
###             2) Extract the fractal dimension of the cluster by plotting the
###                "mass" of the cluster vs. its randius
###                     --- COMPLETE
###             3) Repeat the above 10 times for added accuracy in our extraction
###                of the fractal dimension. Figures are provided for a
###                representative sample (3-4) of our clusters.
###                     --- COMPLETE
################################################################################

from pylab import *
import random
import math
import numpy
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# ------------------------------------------------------------------------------

################################################################################
### Define functions
################################################################################

# ------------------------------------------------------------------------------

# This functions checks the perimeter and then embarks on a random walk
def checkAround(location):
	foundFriend = False #found another particle
	exitCircle = False #reached the required radius
	nearEdge=False #near the edge of the field


    # Check if a walker is near the edge
	if (location[1] + 1) > squareSize - 1 or (location[1] - 1) < 1 or (location[0] + 1) > squareSize - 1 or (location[0] - 1) < 1:
		nearEdge = True

    # If not near the edge, check if the walker is near a neighbor or reached the required radius
	if not nearEdge:
		neighborDown = matrixList[(location[1]+1)*squareSize+location[0]+1]
		if neighborDown[2] == 1:
			foundFriend = True
		if neighborDown[2] == 2:
			exitCircle = True

		neighborUp=matrixList[(location[1]-1)*squareSize+location[0]+1]
		if neighborUp[2]==1:
			foundFriend=True
		if neighborUp[2]==2:
			exitCircle=True

		neighborRight=matrixList[location[1]*squareSize+location[0]+1+1]
		if neighborRight[2]==1:
			foundFriend=True
		if neighborRight[2]==2:
			exitCircle=True

		neighborLeft=matrixList[location[1]*squareSize+location[0]]
		if neighborLeft[2]==1:
			foundFriend=True
		if neighborLeft[2]==2:
			exitCircle=True

    # After checking locations, if locations are good, start the random walk
	if not foundFriend and not nearEdge:
		decide = random.random()
		if decide<0.25:
			location = [location[0] - 1,location[1]]
		elif decide<0.5:
			location = [location[0] + 1,location[1]]
		elif decide<0.75:
			location = [location[0],location[1] + 1]
		else:
			location = [location[0],location[1] - 1]

	return (location, foundFriend, nearEdge, exitCircle)

# ------------------------------------------------------------------------------
#Function that relates the position (X,Y) on the graph with the row of matrix list
def indexM(x,y):
	return y * squareSize + x + 1

# ------------------------------------------------------------------------------
#Function the generates the random location, at the specified radius
def randomAtRadius(radius, squareSize):
	theta = 2*numpy.pi*random.random() #generate random X
	x=int(radius*numpy.cos(theta))+radius
	y=int(radius*numpy.sin(theta))+radius
	location=[x, y]
	return location


################################################################################
### Initialize Variables
################################################################################

# ------------------------------------------------------------------------------

fractalDim=numpy.array([0])

for i in range(10):
	i+=1
	mass=numpy.array([0])

	radiusArray=[10, 20, 30, 40, 50, 60, 70, 80, 90]

	for radius in radiusArray:

		#initialize variables that are dependent upon the radius
		#note - we add 2 to the parameters to get a thick broder between the edges of the disk and square
		seedX = radius+2                        # x coordinate of a seed particle
		seedY = radius+2                         # y coordinate of a seed
		squareSize = radius*2+5


		#initialize the list that would carry coordinates of the filled entries: (row, column, filled(0=empty, 1=filled))
		matrixList=numpy.array([0,0,0])     # create a first entry of the matrix
		#populate the matrix list using a for loop
		for row in range (0,squareSize):
			for col in range (0,squareSize):
				if row==seedX and col==seedY:
					matrixList=numpy.vstack((matrixList, [row,col,1]))
				if numpy.sqrt((seedX-row)**2+(seedY-col)**2)>radius:
					matrixList=numpy.vstack((matrixList, [row,col,2]))
				else:
					matrixList=numpy.vstack((matrixList, [row,col,0]))

		# Remove the first entry, was created to enable vstack option
		matrixList = numpy.delete(matrixList, 0, 0)

		#account for the re-scaling of the field
		radius+=2

		print("Matrix List Initialized")


		################################################################################
		### Run the random walker to create a cluster
		################################################################################

		# ------------------------------------------------------------------------------

		# Initialize the random walker counter
		randomWalkersCount = 0

		# Set the cluster to NOT be completed in size
		completeCluster = False

		# Start running random walkers
		nearEdgeCount=0 #keep track of number lost at the edge of the whole field

		while not completeCluster:
			# Release a walker
			randomWalkersCount += 1
			random.seed()

			# Generate a (Xstart, Ystart) for walker, need within radius
			location=randomAtRadius(radius, squareSize)

			# Initialize variables, like step counter, Friend tag and near edge identifier
			steps = 0
			foundFriend = False #not near other particle
			nearEdge=False #not near the edge of the field


			# Set an individual walker out, stop if found a 'friend', give up if it reached the edge of the board
			while not foundFriend and not nearEdge:
				# Add to the step counter
				steps += 1

				# Run the checking/walking function
				locationNew,foundFriend, nearEdge, exitCircle = checkAround(location)

				# Save the location where the walker is located
				# calculated based on the matrix
				indexOnMatrix = location[1]*squareSize+location[0]+1

				# Add to the cluster if near a friend
				if foundFriend:
					# current location, replace with 1 and stop
					matrixList[indexOnMatrix] = [location[0],location[1],1]

				# Otherwise, save the location
				else:
					location = locationNew

				#if wandered off to the edge of the square - count it as "lost", update counter
				if nearEdge:
					nearEdgeCount+=1


			#print update
			if randomWalkersCount in (100, 1000, 5000, 8000, 10000, 20000, 300000, 400000):
				print("still working, have added ", randomWalkersCount, " random walkers", ". Lost at edge ", nearEdgeCount)
			if randomWalkersCount==400000:
				print("CAUTION: had to break the cycle, taking too much iterations")
				completeCluster = True

			# Once it finds a friend and leaves the previous loop, we must check if it
			# is also touching a circular wall
			if foundFriend and exitCircle:
				matrixList[indexOnMatrix] = [location[0],location[1],1] # current location, replace with 1 and stop
				print("Random walkers in the cluster: ",randomWalkersCount-nearEdgeCount)
				completeCluster = True

		#Update the mass of the cluster
		mass=numpy.append(mass, randomWalkersCount-nearEdgeCount)
		print(matrixList)

		matrix = numpy.zeros((squareSize,squareSize))
		for row1 in range (0,squareSize):
			for col1 in range (0,squareSize):
				value = matrixList[indexM(col1,row1)]
				matrix[row1,col1] = value[2]
		print(matrix)


		label=str(radius)+"run"+str(i)
		fig = plt.subplot()
		plt.title("DLA Cluster", fontsize=20)
		plt.matshow(matrix, interpolation='nearest')
		plt.xlabel("direction, $x$", fontsize=15)
		plt.ylabel("direction, $y$", fontsize=15)
		plt.savefig("oneDLAcluster{}.png".format(label))
		plt.show(block=False)

	#delete the first entry in mass, since
	mass = numpy.delete(mass,0)
	radius=numpy.add(radius,2) #add two as we rescaled during calculations



	#------- Find fit for mass and radius of the cluster:
	# Find log radius and log mass
	# Should be a linear function a+bx, with the slope b equal to the power of t and 'a'=scaling

	#Find Log of all the arrays
	logRadius=numpy.log(radiusArray)
	logMass=numpy.log(mass)

	#Fit a log function using numpy polyfit
	fitLog=numpy.polyfit(logRadius, logMass,1)
	fitLogFunc=numpy.poly1d(fitLog)

	#print out the results
	print("Parameters for the log fit: slope = ",fitLog[0],"shift: ",fitLog[1])
	print("Parameters from the log fit: form is e^",fitLog[1],"*r^",fitLog[0])

	# ------------------------------------------------------------------------------

	################################################################################
	### Create Plots
	################################################################################

	# ------------------------------------------------------------------------------

	#--------------- Plot log
	fig4=plt.subplot()
	plt.scatter(logRadius,logMass, color='tomato', edgecolors='tomato', s=30)
	plt.plot(logRadius, fitLogFunc(logRadius),color='dodgerblue', lw=3)
	plt.title("Log-log plot, mass vs radius",fontsize=20)
	plt.xlabel("Log radius",fontsize=15)
	plt.ylabel("Log mass",fontsize=15)
	plt.grid(True)
	fig4.spines["top"].set_visible(False)
	fig4.spines["right"].set_visible(False)
	plt.savefig('logRadiusMass{}.png'.format(i))
	show(block=False)

	"""
	#--------------- Plot with fit
	fig5=plt.subplot()
	plt.scatter(radiusArray,mass,color='tomato', edgecolors='tomato', s=30)
	plt.plot(radiusArray, numpy.exp(fitLog[1])*radiusArray**(fitLog[0]),color='dodgerblue', lw=3)
	plt.title("Plot of mass vs radius",fontsize=20)
	plt.xlabel("Radius",fontsize=15)
	plt.ylabel("Mass",fontsize=15)
	plt.grid(True)
	fig5.spines["top"].set_visible(False)
	fig5.spines["right"].set_visible(False)
	plt.savefig('radiusMass.png')
	plt.draw()#plt.show(block=False)
	plt.show()
	"""

	fractalDim=numpy.append(fractalDim, fitLog[0])

print("Resulting fractal dimensions ",fractalDim)

# Status?
