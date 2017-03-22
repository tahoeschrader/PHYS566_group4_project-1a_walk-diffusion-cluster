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

import numpy as np
import matplotlib.pyplot as plt
import random as rng
from datetime import datetime

################################################################################
### Start with initializing values
################################################################################

radius = 100




#########   Here is the updates from Xinmeng Tong for problem3    #########
#!/usr/bin/env python


"""
    PHY566 
	Group Project #1 Version A  Problem3
	
"""

from pylab import *
import random
import math
import numpy as np
from scipy.optimize import curve_fit

# Parameters of code
start_radius=100	# Radius at which random walkers are released
out_of_bounds=120	# Radius at which random walkers are considered to not reach cluster in sufficient amount of time (thrown out)

################################ Functions ################################# 

# Define the 2D radius of a walker from the origin with position (r[0],r[1])
def radius(r):
	return math.sqrt((r[0])**2+(r[1])**2)

# Dedine a function to determine whether a walker has hit perimter boundary state of cluster; if so add the walker to the cluster list; then update a new perimeter; if not, escape it
def boundary(state,walker,perimeter,cluster,cluster_rad):
	for i, item in enumerate(perimeter):		             				# Check through all perimeter sites ranges
		if walker[0]+105 == item[0] and walker[1]+105 == item[1]:			# Determine whether walker coord == perimeter coord; if so add to cluster
			cluster[item[0]][item[1]]=1				                     	
                        perimeter.pop(i)			            			# Remove the old perimeter point which is part of cluster now
			cluster_rad.append(r_walker)			                		# r_walker is radius of walker as defined above; add it to the cluster_radius list
                        
			# Create new perimeter sites based on new cluster element
			new_site1=np.zeros(2)						
                        new_site1[0]=item[0]+1
                        new_site1[1]=item[1]
                        if cluster[item[0]+1][item[1]] != 1:				# not a perimeter site if cluster point already occupies site
                                perimeter.append(new_site1)
                        new_site2=np.zeros(2)
                        new_site2[0]=item[0]-1
                        new_site2[1]=item[1]
                        if cluster[item[0]-1][item[1]] != 1:				# not a perimeter site if cluster point already occupies site
                                perimeter.append(new_site2)
                        new_site3=np.zeros(2)
                        new_site3[0]=item[0]
                        new_site3[1]=item[1]+1
                        if cluster[item[0]][item[1]+1] != 1:				# not a perimeter site if cluster point already occupies site
                                perimeter.append(new_site3)
                        new_site4=np.zeros(2)
                        new_site4[0]=item[0]
                        new_site4[1]=item[1]-1
                        if cluster[item[0]][item[1]-1] != 1:				# not a perimeter site if cluster point already occupies site
                                perimeter.append(new_site4)
                        state='hit'					                 		# show 'hit' if a walker has hit cluster, and thus the main loop needs new walker
                        break					                			# break when we do not need to cycle through perimeter
	return state,cluster

# Find random point on a circle with starting radius away from origin point 
def rand_point_on_circle():
	# pick x first or y fisrt at the same prob. 1/2, where we use t=random number(0,1) to decide which one is generated first
	t=random.uniform(0,1)
	if t <=0.5:
		x=round(random.uniform(-100,100),0)				            		# Generate random x value
		y=round(math.sqrt(start_radius**2.0-x**2.0))	     				# Generate corresponding y value forming a circle with start_radius
		
		#positive or negative sign with both prob. 1/2
        	rand=random.uniform(0,1)
		if rand <= 0.5:
			y = -1*y
		elif rand > 0.5:
			y = 1*y
	elif t > 0.5:
                y=round(random.uniform(-100,100),0)                         # Generate random y value
                x=round(math.sqrt(start_radius**2.0-y**2.0))                # Generate corresponding x value forming a circle with start_radius

                # positive or negative sign with both prob. 1/2
                rand=random.uniform(0,1)
                if rand <= 0.5:
                        x=-1*x
                elif rand > 0.5:
                        x=1*x


	# Define walker using the x y values generated above (walker[0],walker[1])=(x,y)
        walker=np.zeros(2)
        walker[0]=x
        walker[1]=y
        return walker

# For part b) 
# Use Curve fit to define a function curvefit=log(m)=C+df*log(r)
def curvefit(r,C,df):							        
	return C+(np.log10(r))*df					     	# log(m)=C+df*log(r), where df is the fractal dimension and C is the proportionality constant

############################## end of functions ##############################


############################## Loop over 10 times of cluster growth and collect data ##############################

while_count=1
#while (while_count <= 3):
while (while_count <= 10):
	#Initialize cluster 2D array; 0=cluster point; 1=cluster point
	#cluster=np.zeros((int(2*(start_radius)+3),int(2*(start_radius)+3)))
	#cluster[102][102]=1
        cluster=np.zeros((int(2*(start_radius)+10),int(2*(start_radius)+10)))
        cluster[105][105]=1

	# Initialize first four perimeter points
	perimeter=[]
	perimeter.append((105,104))
	perimeter.append((105,106))
	perimeter.append((104,105))
	perimeter.append((106,105))

	# Initialize cluster radius variable; tells the radius of a cluster point from origin as it is added
	cluster_rad=[]
	cluster_rad.append(0)


	# Loop over random walkers until the cluster radius, R, is 100, which is radius of the starting circle 
	R=0
	walker_count=0
	while R <= 100:
        	walker_count+=1
        	print "Walkers generated: ",walker_count
		# Generate random walker on circle
        	walker=rand_point_on_circle()
        	state=''											# Initialize state of walker ('hit' or not)
        	# Move walker until it hits cluster or is too far away to be considered a possible hit
		while state != 'hit':							
			# Determine walker's single step direction 
                	rand_num=random.uniform(0,1)
                	if rand_num <=0.25:
                        	walker[0]+=1				#right
                	elif rand_num > 0.25 and rand_num <= 0.50:	
                        	walker[0]-=1				#left
                	elif rand_num >0.50 and rand_num <= 0.75:
                        	walker[1]+=1				#up
                	elif rand_num >0.75:
                        	walker[1]-=1				#down
        		# Determine radius of walker from origin
			r_walker=radius(walker)
			# If walker is close to the largest brance of the cluster then check to the perimeter sites, otherwise continue (saves time)
			if r_walker <= max(cluster_rad)+5:
				state,cluster=boundary(state,walker,perimeter,cluster,cluster_rad)
				if state == 'hit':
					R=radius(walker)
                        		print "RADIUS=",R
                        		break
			# Check if walker is out of bounds
			if r_walker >= out_of_bounds:
                        	break					# Break loop to generate new walker


	# Plot cluster
	#np.savetxt("cluster_data.txt",cluster)
	plt.figure()
	cmap = matplotlib.colors.ListedColormap(['white','blue'])
	bounds = [-.5,.5,1.5]
	norm = matplotlib.colors.BoundaryNorm(bounds,cmap.N)
	img = plt.imshow(cluster,interpolation='nearest',cmap=cmap,norm=norm)
	plt.xlabel("Horizontal Position [Arbitrary units]")
	plt.ylabel("Vertical Position [Arbitrary units]")
	plt.title("Cluster from DLA Method")
	savefig("DLA_crystal_final_%i.pdf" %(while_count))
	plt.show()

	
	
	
	
	# Part b): Fractal dimensions:
	mass_radius=np.arange(5,105,5)					# Array for radius at which mass is calculated
	mass_count=[0]*len(mass_radius)					# Array to count the number of walkers inside the bounds of each radius array element 
	if while_count==1:
		mass_count_avg=[0]*len(mass_radius)			# Setting up the counts for the average mass values
	for i in range(len(mass_radius)):
    		for j in range(len(cluster_rad)):
        		if cluster_rad[j]<=mass_radius[i]:
            			mass_count[i]=mass_count[i]+1
        	mass_count_avg[i]+=mass_count[i]
        	
        # Curve fit:
        mass=curvefit(mass_radius,1,1.5)				# Calculated values of mass from curve fit equation
	log_mass=np.log10(mass_count)					# Taking log to the base 10 for mass
	popt,pcov=curve_fit(curvefit,mass_radius,log_mass)
	print "Constant,Fractal dimension:",popt
	log_radius=np.log10(mass_radius)				# Taking log to the base 10 for radius
    	
    	mass_analytic=curvefit(mass_radius,popt[0],popt[1])		# Analytically calculated mass from the fit parameters obtained to get the "fit curve"
									# already in log form as given by curvefit function
	# Plotting fractal dimension relation:
	plt.figure()
	plt.plot(log_radius,log_mass,'r*',label="Raw data")
	plt.plot(log_radius,mass_analytic,'k-',label="Fit curve")
	plt.legend()
	plt.xlabel("Radius of cluster")
	plt.ylabel("Number of walkers within radius, mass")
	plt.title("Mass distribution of DLA cluster on a log-log plot")
	plt.savefig("Fractal_dimension_final_%i.pdf" %(while_count))
	plt.show()

	print "mass_count:"
	print mass_count
	print "mass_count_avg"
	print mass_count_avg		
        while_count+=1    
        
mass_count_avg[:]=[i/10 for i in mass_count_avg]			# Getting average mass over 10 clusters
print "Final mass_count_avg"
print mass_count_avg



#Part c (Average to add accuracy)

# Average Curve fit and function definition:
mass_avg=curvefit(mass_radius,1,1.5)
log_mass_avg=np.log10(mass_count_avg)
popt_avg,pcov_avg=curve_fit(curvefit,mass_radius,log_mass_avg)
print "Constant,Avegrage fractal dimension:",popt_avg
log_radius=np.log10(mass_radius)
mass_analytic=curvefit(mass_radius,popt_avg[0],popt_avg[1])

# Plotting fractal dimension relation:
plt.figure()
plt.plot(log_radius,log_mass_avg,'r*',label="Raw data")
plt.plot(log_radius,mass_analytic,'k-',label="Fit curve")
plt.legend()
plt.xlabel("Radius of cluster")
plt.ylabel("Number of walkers within radius, mass")
plt.title("Fractal dimensionality of DLA cluster averaged over 10 clusters log(m)-log(r)")
plt.savefig("Fractal_dimension_final_avg.pdf")
plt.show()
