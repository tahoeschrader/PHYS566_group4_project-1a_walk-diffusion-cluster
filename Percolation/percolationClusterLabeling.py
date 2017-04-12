### main percolation file

import random
import numpy
import matplotlib.pyplot as plt
from matplotlib import colors

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


def pValueCalc(matrix, N):
    return numpy.count_nonzero(matrix)/N







##########################################################################################


############################################
############################################
###### Run the code
############################################
############################################


####################### To test
###### For fixed N
N=40  #define size of matrix
matrix=numpy.zeros((N, N)) #initialize matrix

clusterNumber=1 #initialize the cluster number

cluster=False

while not cluster: #repeat 10 times
    matrix, clusterNumber=randomPlacement(matrix, clusterNumber, N)
    if checkCluster(matrix, N): #check for cluster
        break #we have a cluster formed now
    


print(matrix)

#Find the pvalue 
pValue=pValueCalc(matrix, N)

print(pValue)



