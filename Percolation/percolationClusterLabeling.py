### main percolation file

import random
import numpy
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib import cm
import os
from matplotlib.cm import hot

#Percolation
########################################################################################
#BASE code for placing numbers and checking for neighbors, relabeling if needed
# ---- DONE
#--- Check for the spanning cluster
# ---- DONE

#Needs:
#--- Runner for part a (repeat # of times etc)



### General idea for the code:
    # Create a matrix with all 0
    # Given p:
    # 1. Select a random coordinate in row= random(0,N-1), col=random(0,N-1)
    # 2. Occipy that value with 1
    # 3. Repeat 1. But occupy with 1+1 value. Concurrently check if the neighbors have and n!=0 around.
    # 4. If yes, parse throung the matrix and replace every value of 1+1 with 1. 
    # Generalize

############################################
############################################
### DEFINE FUNCTIONS
############################################
############################################
# Function for relabeling the positions. Relabels all instances of passed number, picking the smallest
# Then checks back there are no neighboring clusters touching\
# Idea: call from CheckAround --> Relabel --> Call CheckAround --> Relabel etc. until no clusters near
def relabel(matrix, currentClusterNumber, adjacentNumber, row, col, N):
    #decide which number to keep. Assuming we are keeping the smallest
    if currentClusterNumber<adjacentNumber: 
        matrix[matrix==adjacentNumber]=currentClusterNumber #use built in numpy to relabel
    else:
        matrix[matrix==currentClusterNumber]=adjacentNumber
    checkAround(matrix, matrix[row][col], row, col, N)
    return matrix

#Function check around the point for neighbors. If found some up/below/left/right it calls the relabel()
# If not - returns the matrix back
def checkAround(matrix, clusterNumber, row, col, N):
    #All the if statements are needed to ensure we are not out of bounds
    if row-1>=0:
        if matrix[row-1][col]!=0 and matrix[row-1][col]!=clusterNumber:
            matrix=relabel(matrix, clusterNumber,matrix[row-1][col], row, col, N)
    if row+1<N:
        if matrix[row+1][col]!=0 and matrix[row+1][col]!=clusterNumber:
            relabel(matrix, clusterNumber,matrix[row+1][col], row, col, N)
    if col-1>=0:
        if matrix[row][col-1]!=0 and matrix[row][col-1]!=clusterNumber:
            matrix=relabel(matrix, clusterNumber,matrix[row][col-1], row, col, N)  
    if col+1<N:
        if matrix[row][col+1]!=0 and matrix[row][col+1]!=clusterNumber:
            matrix=relabel(matrix, clusterNumber,matrix[row][col+1], row, col, N)    
    return matrix

#Random placement of values. Calls the CheckAround function once the value is placed
# Keeps track of the number we are placing by increasing it every time by 1.
def randomPlacement(matrix, clusterNumber, N):
    random.seed() #seed random number generator
    row=int(random.random()*N) #select random row and column for placement
    col=int(random.random()*N)
    matrix[row][col]=clusterNumber #place number
    matrix=checkAround(matrix, clusterNumber, row, col, N) #check around for neighbors
    return matrix, clusterNumber+1


#This function determines if it is a cluster
def checkCluster(matrix, N):
    #check what nonzero values on the edges we have. If some coincide = we have a cluster
    upperRowNumbers=numpy.unique(matrix[0,:])
    leftColNumbers=numpy.unique(matrix[:,0])
    lowRowNumbers=numpy.unique(matrix[N-1,:])
    rightColNumbers=numpy.unique(matrix[:,N-1])


    #remove zeros
    upperRowNumbers=upperRowNumbers[upperRowNumbers!=0]
    leftColNumbers=leftColNumbers[leftColNumbers!=0]
    lowRowNumbers=lowRowNumbers[lowRowNumbers!=0]
    rightColNumbers=rightColNumbers[rightColNumbers!=0]

    #Check for common elements. For loop structure, alike the function any() in Python 
    for element1 in upperRowNumbers:
        for element2 in leftColNumbers:
            for element3 in lowRowNumbers:
                for element4 in rightColNumbers:
                    if element1==element2==element3==element4:
                        return True 
    return False

#Finding the p value for the matrix - count number of non-zero entries and 
# divide by the size of matrix N**2
def pValueCalc(matrix, N):
    return numpy.count_nonzero(matrix)/N**2

#Main runner for the function
#Takes in the matrix and evaluates everything
#RETURNS: pValue and matrix
def mainFunction(N, needGif):


    ###NOTE: if NeedGif - save all inetrmediate steps

    #check that the folder images exists
    if not os.path.isdir("images"):
        os.mkdir("images")
    
    #import the library if need gif
    if needGif:
        #Import there libraries if intend to save gif
        #NOTE: need imageio package, and ffmpeg. Refer to readme for more info
        import imageio


    #initialize variables for the run
    cluster=False
    clusterNumber=1 #initialize the cluster number
    matrix=numpy.zeros((N, N)) #initialize matrix
    counterLocal=0 #for the images saving


    #Define the map for the plot
    cmap=cm.autumn.from_list('whatever', ('skyblue', 'midnightblue'), N=30)
    cmap.set_bad(color='white')

    #fill in the matrix
    while not cluster: 
        matrix, clusterNumber=randomPlacement(matrix, clusterNumber, N)
        counterLocal+=1
        ###############
        # need gif
        if needGif and counterLocal%7==0:
            #save the pics for the animation
            matrixPlot = numpy.ma.masked_where(matrix < 0.05, matrix)
            plt.title("Percolation", fontsize=20)
            plt.matshow(matrixPlot, interpolation='nearest',cmap=cmap) #ocean, Paired
            plt.xlabel("direction, $x$", fontsize=15)
            plt.ylabel("direction, $y$", fontsize=15)
            plt.savefig("images/percolation{}.png".format(counterLocal))
            plt.show(block=False)
            plt.close()
        ###################
        if checkCluster(matrix, N): #check for cluster
            break #we have a cluster formed now
    
    #save the final plot
    if needGif:
        matrixPlot = numpy.ma.masked_where(matrix < 0.05, matrix)
        plt.title("Percolation", fontsize=20)
        plt.matshow(matrixPlot, interpolation='nearest',cmap=cmap) #ocean, Paired
        plt.xlabel("direction, $x$", fontsize=15)
        plt.ylabel("direction, $y$", fontsize=15)
        plt.savefig("images/percolation.png")
        plt.show(block=False)
    pValue=pValueCalc(matrix, N)


    ###############
    # need gif
    if needGif:
        with imageio.get_writer('images/movie.gif', mode='I') as writer:
            for i in numpy.arange(0,counterLocal,7):
                if i!=0:
                    filename="images/percolation"+str(i)+".png"
                    image = imageio.imread(filename)
                    writer.append_data(image)
                    os.remove(filename)
            image = imageio.imread("images/percolation.png")
            writer.append_data(image)
    ###################

    return (pValue, matrix)










