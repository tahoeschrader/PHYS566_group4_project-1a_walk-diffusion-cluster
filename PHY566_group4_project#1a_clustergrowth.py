from pylab import *
import random
import math
import numpy
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

################################################################################
### Initialize Variables
################################################################################

# ------------------------------------------------------------------------------

#initialize the list that would carry coordinates of the filled entries: (row, column, filled(0=empty, 1=filled))

matrixList=numpy.array([0,0,0])     # create a first entry of the matrix
radius = 100
seedX = 100                         # x coordinate of a seed particle
seedY = 100                         # y coordinate of a seed
squareSize = 201

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

print("Matrix List Initialized")

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
### Run the random walker to create a cluster
################################################################################

# ------------------------------------------------------------------------------

# Initialize the random walker counter
randomWalkersCount = 0

# Set the cluster to NOT be completed in size
completeCluster = False

#exitCircle = False #not reached the required radius
#nearEdge=False #not near the edge of the field

# Start running random walkers
nearEdgeCount=0 #keep track of number lost
while not completeCluster:
	# Release a walker
	randomWalkersCount += 1
	random.seed()

	# Generate a (Xstart, Ystart) for walker, need within radius
	location=randomAtRadius(radius, squareSize)

	# Initialize variables, like step counter, location array, Friend tag
	steps = 0
	#location = [xStart, yStart] # column and row on matrix
	foundFriend = False
	
	nearEdge=False #not near the edge of the field
	
	

    # Set an individual walker out, give up if it reached the edge of the board
	while not foundFriend and not nearEdge:# and steps < 2000:
        # Add to the step counter
		steps += 1

        # Run the checking/walking function
		locationNew,foundFriend, nearEdge, exitCircle = checkAround(location)

        # Save the location where the walker is located
		indexOnMatrix = location[1]*squareSize+location[0]+1

        # Add to the cluster if near a friend
		if foundFriend:
            # current location, replace with 1 and stop
			matrixList[indexOnMatrix] = [location[0],location[1],1]

        # If near an edge and its been a long time... give up this while loop,
        # which means use a break function (I think)
		#if nearEdge and steps == 1999:
		#	break

        # Otherwise, save the location
		else:
			location = locationNew
			
		
		#if steps>10000:
		#	nearEdge=True
			
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

print(matrixList)

# ------------------------------------------------------------------------------

################################################################################
### Create Plots
################################################################################

# ------------------------------------------------------------------------------

matrix = numpy.zeros((201,201))
for row1 in range (0,201):
	for col1 in range (0,201):
		value = matrixList[indexM(col1,row1)]
		matrix[row1,col1] = value[2]
print(matrix)

fig = plt.subplot()
plt.title("DLA Cluster", fontsize=20)
plt.imshow(matrix, interpolation='nearest')
plt.xlabel("direction, $x$", fontsize=15)
plt.ylabel("direction, $y$", fontsize=15)
plt.savefig('oneDLAcluster.png')
plt.show()
