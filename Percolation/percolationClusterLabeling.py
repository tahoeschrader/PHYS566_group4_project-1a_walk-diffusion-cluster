### Group 4
### Computational Physics
### Spring, 2017

################################################################################
### This code will simulate the percolation transition on a N x N lattice by
### randomly filling lattice sites. Occupation probability is a fraction of all
### occupied sites among lattice sites in general. Therefore, each population
### step wil increase p. We want this code to:
### BASE code for placing numbers and checking for neighbors, relabeling if needed
###      ---- COMPLETE
### Check for the spanning cluster
###      ---- COMPLETE
### Determine pc
###      --- COMPLETE
### Create GIF of the peroclating cluster being created
###      --- COMPLETE
################################################################################

# ------------------------------------------------------------------------------

import random
import numpy
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib import cm
import os
from matplotlib.cm import hot

# ------------------------------------------------------------------------------


################################################################################
### Define functions
################################################################################

# ------------------------------------------------------------------------------

# Function for relabeling the positions. [Our metric: choose smaller cluster #]
def relabel(matrix, currentClusterNumber, adjacentNumber, row, col, N):
    #decide which number to keep. Assuming we are keeping the smallest
    if currentClusterNumber < adjacentNumber :
        matrix[matrix == adjacentNumber] = currentClusterNumber # relabels entire matrix at once
    else:
        matrix[matrix == currentClusterNumber] = adjacentNumber # relabels entire matrix at once

    # Check for extra neighbors with checkAround()
    matrix = checkAround(matrix, matrix[row][col], row, col, N)
    return matrix

# Function for checking neighbors. If found, call relabel().
def checkAround(matrix, clusterNumber, row, col, N):
    # All the if statements are needed to ensure we are not out of bounds
    if row-1 >= 0 :
        if matrix[row-1][col] != 0 and matrix[row-1][col] != clusterNumber :
            matrix = relabel(matrix, clusterNumber, matrix[row-1][col], row, col, N)
    if row+1 < N :
        if matrix[row+1][col] != 0 and matrix[row+1][col] != clusterNumber :
            matrix = relabel(matrix, clusterNumber, matrix[row+1][col], row, col, N)
    if col-1 >= 0 :
        if matrix[row][col-1] != 0 and matrix[row][col-1] != clusterNumber :
            matrix = relabel(matrix, clusterNumber, matrix[row][col-1], row, col, N)
    if col+1 < N :
        if matrix[row][col+1] != 0 and matrix[row][col+1] != clusterNumber :
            matrix = relabel(matrix, clusterNumber, matrix[row][col+1], row, col, N)
    return matrix

# Function to choose random spot on the lattice.
def generateRandomPosition(N):
    random.seed() # seed random number generator
    row = int(random.random()*N) # select random row and column for placement
    col = int(random.random()*N)
    return row, col

# Function to turn a random unoccupied spot into a cluster
def randomPlacement(matrix, clusterNumber, N):
    row, col = generateRandomPosition(N)
    while matrix[row][col] != 0 :
        row, col = generateRandomPosition(N)
    matrix[row][col] = clusterNumber # place number

    # Check for neighbors with checkAround()
    matrix = checkAround(matrix, clusterNumber, row, col, N)
    return matrix, clusterNumber+1


# Function to look for a spanning cluster
def checkCluster(matrix, N) :
    # return an array of all the cluster numbers on each edge
    upperRowNumbers = numpy.unique(matrix[0,:])
    leftColNumbers = numpy.unique(matrix[:,0])
    lowRowNumbers = numpy.unique(matrix[N-1,:])
    rightColNumbers = numpy.unique(matrix[:,N-1])


    # remove the zeros from that list
    upperRowNumbers = upperRowNumbers[upperRowNumbers!=0]
    leftColNumbers = leftColNumbers[leftColNumbers!=0]
    lowRowNumbers = lowRowNumbers[lowRowNumbers!=0]
    rightColNumbers = rightColNumbers[rightColNumbers!=0]

    # Check for common elements. Result is an empty list if no common elements.
    match = list(set(upperRowNumbers).intersection(leftColNumbers).intersection(lowRowNumbers).intersection(rightColNumbers))
    if match == [] :
        return False,0

    return True, match

# Function that finds the p value for the matrix - count number of non-zero entries and
# divide by the size of matrix N**2
def pValueCalc(matrix, N):
    return numpy.count_nonzero(matrix) / (N**2)

# ------------------------------------------------------------------------------

################################################################################
### This final function runs everything to build the cluster and obtain p
###         RETURNS: pValue and matrix
################################################################################

# ------------------------------------------------------------------------------

def mainFunction(N, needGif):
    ### NOTE: if NeedGif - save all intermediate steps

    # Check that the folder images exists
    if not os.path.isdir("images"):
        os.mkdir("images")

    # Import the library if needGif
    if needGif:
        #Import these libraries if you intend to save a gif
        # NOTE: need imageio package, and ffmpeg. Refer to readme for more info
        import imageio


    # Initialize variables for the run
    cluster = False
    clusterNumber = 1            # initialize first cluster to be "1"
    matrix = numpy.zeros((N, N)) # initialize matrix with zeros
    counterLocal = 0             # for the images saving


    # Define the map for the plot
    cmap = cm.autumn.from_list('whatever', ('skyblue', 'midnightblue'), N=30)
    cmap.set_bad(color='white')

    # Fill in the matrix
    while not cluster:
        matrix, clusterNumber = randomPlacement(matrix, clusterNumber, N)
        counterLocal += 1
        ###############
        # need gif
        if needGif and counterLocal%7 == 0 :
            # save the pics for the animation
            matrixPlot = numpy.ma.masked_where(matrix < 0.05, matrix)
            plt.title("Percolation", fontsize=20)
            plt.matshow(matrixPlot, interpolation='nearest', cmap=cmap) #ocean, Paired
            plt.xlabel("direction, $x$", fontsize=15)
            plt.ylabel("direction, $y$", fontsize=15)
            plt.savefig("images/percolation{}.png".format(counterLocal))
            plt.show(block=False)
            plt.close()
        ###################

        clusterFormed, spanningNumber=checkCluster(matrix, N)
        if clusterFormed : # check for cluster
            break # we have a cluster formed now

    # save the final plot
    if needGif :
        matrixPlot = numpy.ma.masked_where(matrix < 0.05, matrix)
        plt.title("Percolation", fontsize=20)
        plt.matshow(matrixPlot, interpolation='nearest',cmap=cmap) #ocean, Paired
        plt.xlabel("direction, $x$", fontsize=15)
        plt.ylabel("direction, $y$", fontsize=15)
        plt.savefig("images/percolation.png")
        plt.show(block=False)
    pValue = pValueCalc(matrix, N)


    ###############
    # need gif
    if needGif:
        with imageio.get_writer('images/movie.gif', mode='I') as writer:
            for i in numpy.arange(0,counterLocal,7):
                if i!=0:
                    filename = "images/percolation"+str(i)+".png"
                    image = imageio.imread(filename)
                    writer.append_data(image)
                    os.remove(filename)
            image = imageio.imread("images/percolation.png")
            writer.append_data(image)
    ###################

    return (pValue, matrix, spanningNumber, clusterNumber)
