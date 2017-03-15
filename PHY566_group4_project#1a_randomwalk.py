#question 1, part A, 2D random walk

import numpy
import random
import matplotlib.pyplot as plt


#Create a function
def randomWalk2D(x0,y0,n):
	#set up a first position 
	position=numpy.matrix([x0,y0])
	#random seed
	random.seed()
	#loop through
	for i in range(0,n):
		#get a random number in range (0,1)
		rand=random.random()
		#Assume equal probability to step in 4 directions 
		# p=0.25
		if rand<=0.25: #step down
			xN=position[i,0]
			yN=position[i,1]-1
		elif .25<rand<=0.5: #step up
			xN=position[i,0]
			yN=position[i,1]+1
		elif .5<rand<=0.75: #step left
			xN=position[i,0]-1
			yN=position[i,1]
		else: #step right
			xN=position[i,0]+1
			yN=position[i,1]
		#Add the new position to the array
		position=numpy.vstack((position, numpy.array([xN,yN])))
	return position


#Check the function with the following parameters
#start from a position in the origin
x0G=0
y0G=0
#number of steps
n=1000

#Call the function
positionN=randomWalk2D(x0G,y0G,n)

#Take x and y for plotting
x=positionN[:,0]
y=positionN[:,1]

#Plot, overlay of colored scatter and line
plt.scatter(x,y, c=range(len(x)),marker="o",s=50)
plt.plot(x,y, 'k')
plt.title('Random walk representation')
plt.grid(True)
plt.show()



