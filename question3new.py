from pylab import *
import random
import math
import numpy
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


#operate on lists 

#initialize the list that would carry coordinates of the filled entries: (row, column, filled(0=empty, 1=filled))

matrixList=numpy.array([0,0,0]) #create a first entry of the matrix
radius=100
seedX=100 #x coordinate of a seed particle
seedY=100 #y coordinate of a seed
squareSize=201

for row in range (0,201):
	for col in range (0,201):
		if row==seedX and col==seedY:
			matrixList=numpy.vstack((matrixList, [row,col,1]))
		if numpy.sqrt((seedX-row)**2+(seedY-col)**2)>radius:
			matrixList=numpy.vstack((matrixList, [row,col,2]))
		else:
			matrixList=numpy.vstack((matrixList, [row,col,0]))
matrixList=numpy.delete(matrixList, 0, 0) #remove the first entry, was created to enable vstack option
completeCluster=False
randomWalkersCount=0

print("matrix list initialized")

def checkAround(location):
	foundFriend=False
	nearEdge=False	
	
	
	if (location[1]+1)>squareSize-1 or (location[1]-1)<1 or (location[0]+1)>squareSize-1 or (location[0]-1)<1:
		nearEdge=True
	
	if not nearEdge:
		neighborDown=matrixList[(location[1]+1)*squareSize+location[0]+1]
		if neighborDown[2]==1:
			foundFriend=True
		if neighborDown[2]==2:
			nearEdge=True
			
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
	
	if not foundFriend and not nearEdge:
		decide=random.random()
		if decide<0.25:
			location=[location[0]-1,location[1]]
		elif decide<0.5:
			location=[location[0]+1,location[1]]
		elif decide<0.75:
			location=[location[0],location[1]+1]
		else:
			location=[location[0],location[1]-1]
			
	return (location, foundFriend, nearEdge)


########## Run one cluster job

while not completeCluster:
	#release a walker
	randomWalkersCount+=1
	random.seed()
	
	#Generate a (Xstart, Ystart) for walker, need within radius
	withinCircle=False #identity to check if within circle
	while not withinCircle:
		xStart=randint(0,squareSize)
		yStart=randint(0,squareSize)
		if numpy.sqrt((seedX-xStart)**2+(seedY-yStart)**2)<radius:
			withinCircle=True #have a value
	
	#perform random walk, counting number of steps		
	steps=0
	location=[xStart, yStart] #column and row on matrix
	
	foundFriend=False
	#print("released walker")
	
	while not foundFriend and steps<2000:
		#location[1]*squareSize+location[0]+1 #important! Gives our position on matrix, no search
		
		steps+=1
		
		locationNew,foundFriend, nearEdge=checkAround(location)
		
		indexOnMatrix=location[1]*squareSize+location[0]+1

		#print(steps)
		
		if foundFriend: #found cluster
			matrixList[indexOnMatrix]=[location[0],location[1],1] #current location, replace with 1 and stop
		if nearEdge:
			#matrixList[indexOnMatrix]=[location[0],location[1],1] #current location, replace with 1 and stop
			steps=1000##############NEED TO BE CORRECTED
		else:
			location=locationNew
		#print(steps)

	if foundFriend and nearEdge or randomWalkersCount>4000:
		matrixList[indexOnMatrix]=[location[0],location[1],1] #current location, replace with 1 and stop
		print(randomWalkersCount)
		completeCluster=True
print(matrixList)
#Plot matrix

def indexM(x,y):
	return y*squareSize+x+1

matrix=numpy.zeros((201,201))
for row in range (0,201):
	for col in range (0,201):
		value=matrixList[indexM(col,row)]
		matrix[row,col]=value[2]
print(matrix)
plt.imshow(matrix, interpolation='nearest' )
plt.show()

		
		