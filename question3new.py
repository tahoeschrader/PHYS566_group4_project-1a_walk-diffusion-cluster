### Group 4
### Computational Physics
### Spring, 2017

################################################################################
### This code will simulate cluster growth in 2D using a Diffusion Limited
### Aggregation Model (DLA). There will be three parts to this code:
###             1) Use a circle of radius 100 as a starting point of the random
###                walkers and a seed at the origin and grow a cluster till it
###                reaches the edge of the circle.
###                     --- INCOMPLETE
###             2) Extract the fractal dimension of the cluster by plotting the
###                "mass" of the cluster vs. its randius
###                     --- INCOMPLETE
###             3) Repeat the above 10 times for added accuracy in our extraction
###                of the fractal dimension. Figures are provided for a
###                representative sample (3-4) of our clusters.
###                     --- INCOMPLETE
################################################################################

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

for row in range (0,201):
	for col in range (0,201):
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
	foundFriend = False
	nearEdge = False

    # Check if a walker is near the edge
	if (location[1] + 1) > squareSize - 1 or (location[1] - 1) < 1 or (location[0] + 1) > squareSize - 1 or (location[0] - 1) < 1:
		nearEdge = True

    # If not near the edge, check if the walker is near a neighbor
	if not nearEdge:
		neighborDown = matrixList[(location[1]+1)*squareSize+location[0]+1]
		if neighborDown[2] == 1:
			foundFriend = True
		if neighborDown[2] == 2:
			nearEdge = True

		neighborUp=matrixList[(location[1]-1)*squareSize+location[0]+1]
		if neighborUp[2]==1:
			foundFriend=True
		if neighborUp[2]==2:
			nearEdge=True

		neighborRight=matrixList[location[1]*squareSize+location[0]+1+1]
		if neighborRight[2]==1:
			foundFriend=True
		if neighborRight[2]==2:
			nearEdge=True

		neighborLeft=matrixList[location[1]*squareSize+location[0]]
		if neighborLeft[2]==1:
			foundFriend=True
		if neighborLeft[2]==2:
			nearEdge=True

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

	return (location, foundFriend, nearEdge)

# ------------------------------------------------------------------------------

def indexM(x,y):
	return y * squareSize + x + 1

# ------------------------------------------------------------------------------

################################################################################
### Run the random walker to create a cluster
################################################################################

# ------------------------------------------------------------------------------

# Initialize the random walker counter
randomWalkersCount = 0

# Set the cluster to NOT be completed in size
completeCluster = False

# Start running random walkers
while not completeCluster:
	# Release a walker
	randomWalkersCount += 1
	random.seed()

	# Generate a (Xstart, Ystart) for walker, need within radius
	withinCircle = False # identity to check if within circle
	while not withinCircle:
		xStart = randint(0,squareSize)
		yStart = randint(0,squareSize)
		if numpy.sqrt((seedX-xStart)**2+(seedY-yStart)**2) < radius:
			withinCircle = True # have a value

	# Initialize variables, like step counter, location array, Friend tag
	steps = 0
	location = [xStart, yStart] # column and row on matrix
	foundFriend = False

    # Set an individual walker out, if its puttering about at the edge near
    # 2000 steps, give up on it!
	while not foundFriend and steps < 2000:
        # Add to the step counter
		steps += 1

        # Run the checking/walking function
		locationNew,foundFriend, nearEdge = checkAround(location)

        # Save the location where the walker is located
		indexOnMatrix = location[1]*squareSize+location[0]+1

        # Add to the cluster if near a friend
		if foundFriend:
            # current location, replace with 1 and stop
			matrixList[indexOnMatrix] = [location[0],location[1],1]

        # If near an edge and its been a long time... give up this while loop,
        # which means use a break function (I think)
		if nearEdge and steps == 1999:
			break

        # Otherwise, save the location
		else:
			location = locationNew

    # Once it finds a friend a leaves the previous loop, we must check if it
    # is also touching a wall
	if foundFriend and nearEdge :
		matrixList[indexOnMatrix] = [location[0],location[1],1] # current location, replace with 1 and stop
		print(randomWalkersCount)
		completeCluster = True

print(matrixList)

# ------------------------------------------------------------------------------

################################################################################
### Create Plots
################################################################################

# ------------------------------------------------------------------------------

matrix = numpy.zeros((201,201))
for row in range (0,201):
	for col in range (0,201):
		value = matrixList[indexM(col,row)]
		matrix[row,col] = value[2]
print(matrix)

fig = plt.subplot()
plt.title("DLA Cluster", fontsize=20)
plt.imshow(matrix, interpolation='nearest')
plt.xlabel("direction, $x$", fontsize=15)
plt.ylabel("direction, $y$", fontsize=15)
plt.savefig('LaTeX/oneDLAcluster.png')
plt.show()

# ------------------------------------------------------------------------------
