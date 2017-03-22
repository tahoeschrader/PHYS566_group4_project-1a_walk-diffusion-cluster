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
###                "mass" of the cluster vs. its radius
###                     --- INCOMPLETE
###             3) Repeat the above 10 times for added accuracy in our extraction
###                of the fractal dimension. Figures are provided for a
###                representative sample (3-4) of our clusters.
###                     --- INCOMPLETE
################################################################################

from pylab import *
import random
import math
import numpy as np
from scipy.optimize import curve_fit

################################################################################
### Start with initializing values
################################################################################

# ------------------------------------------------------------------------------

start_radius = 100	# Radius at which random walkers are released
out_of_bounds = 120	# Radius where we throw out the random walker

# ------------------------------------------------------------------------------

################################################################################
### Define functions
################################################################################

# ------------------------------------------------------------------------------

# Defines the 2D radius of a walker from the origin with position (r[0],r[1])
def radius(r):
	return np.sqrt((r[0])**2+(r[1])**2)

# ------------------------------------------------------------------------------

# Checks if walker hits perimeter and update the perimeter
def boundary(state,walker,perimeter,cluster,cluster_rad):
    # Check through all perimeter sites ranges
	for i, item in enumerate(perimeter):
        # Determine whether walker coord == perimeter coord; if so add to cluster
		if walker[0]+105 == item[0] and walker[1]+105 == item[1]:
			cluster[item[0]][item[1]] = 1

            # Remove the old point from the perimeter, add to cluster
            perimeter.pop(i)

            # r_walker is radius of walker as defined above; add it to the cluster_radius list
			cluster_rad.append(r_walker)

			# Create new perimeter sites based on new cluster element
			new_site1=np.zeros(2)
            new_site1[0] = item[0]+1
            new_site1[1] = item[1]
            if cluster[item[0]+1][item[1]] != 1: # not on perimeter if cluster is here
                perimeter.append(new_site1)

            new_site2=np.zeros(2)
            new_site2[0] = item[0]-1
            new_site2[1] = item[1]
            if cluster[item[0]-1][item[1]] != 1: # not on perimeter if cluster is here
                perimeter.append(new_site2)

            new_site3 = np.zeros(2)
            new_site3[0] = item[0]
            new_site3[1] = item[1]+1
            if cluster[item[0]][item[1]+1] != 1: # not on perimeter if cluster is here
                perimeter.append(new_site3)

            new_site4=np.zeros(2)
            new_site4[0] = item[0]
            new_site4[1] = item[1]-1
            if cluster[item[0]][item[1]-1] != 1: # not on perimeter if cluster is here
                perimeter.append(new_site4)

            # show 'hit' if a walker has hit cluster, and thus the main loop needs new walker
            state = 'hit'

            # break when we do not need to cycle through perimeter
            break

	return state,cluster

# ------------------------------------------------------------------------------

# Find random point on a circle with starting radius away from origin point
def rand_point_on_circle():
	# pick x first or y first at the same prob. 1/2
	t = random.uniform(0,1)

	if t <=0.5:
        # Generate random x and y value to form circle with start_radius
		x = round(random.uniform(-100,100),0)
		y = round(math.sqrt(start_radius**2.0-x**2.0))

		# Positive or negative sign with both prob. 1/2
        rand = random.uniform(0,1)

		if rand <= 0.5:
			y = -1*y
		elif rand > 0.5:
			y = 1*y

	elif t > 0.5:
        # Generate random x and y value to form circle with start_radius
        y = round(random.uniform(-100,100),0)
        x = round(math.sqrt(start_radius**2.0-y**2.0))

        # Positive or negative sign with both prob. 1/2
        rand = random.uniform(0,1)

        if rand <= 0.5:
            x=-1*x
        elif rand > 0.5:
            x=1*x

	# Define walker using the x y values generated above (walker[0],walker[1])=(x,y)
    walker = np.zeros(2)
    walker[0] = x
    walker[1] = y

    return walker

# ------------------------------------------------------------------------------

# The following is used to find the fractal dimension
def curvefit(r,C,df):           # curvefit=log(m)=C+df*log(r), where df is the
    return C+(np.log10(r))*df   # fractal dimension and C is the prop. constant

# ------------------------------------------------------------------------------

################################################################################
### Runs the functions individually and then averages them
################################################################################

# ------------------------------------------------------------------------------

# The following is for individual Runs. Begin by initializing the counter
while_count = 1

while (while_count <= 10):
	# Initialize cluster 2D array; 0=cluster point; 1=cluster point
	#cluster=np.zeros((int(2*(start_radius)+3),int(2*(start_radius)+3)))
	#cluster[102][102]=1
    cluster = np.zeros((int(2*(start_radius)+10),int(2*(start_radius)+10)))
    cluster[105][105] = 1

	# Initialize first four perimeter points
	perimeter = []
	perimeter.append((105,104))
	perimeter.append((105,106))
	perimeter.append((104,105))
	perimeter.append((106,105))

	# Initialize cluster radius variable; tells the radius of a cluster point from origin as it is added
	cluster_rad = []
	cluster_rad.append(0)

	# Loop over random walkers until the cluster radius, R, is 100, which is radius of the starting circle
	R = 0
	walker_count = 0

    # Begin looper
	while R <= 100:
        # Add to counter
        walker_count+=1

		# Generate random walker on circle
        walker = rand_point_on_circle()

        # Initialize state of walker ('hit' or not)
        state = ''

        # Move walker until it hits cluster or is too far away to be considered a possible hit
		while state != 'hit':
			# Determine walker's single step direction
            rand_num=random.uniform(0,1)

            if rand_num <=0.25:
                walker[0] += 1                              # right
            elif rand_num > 0.25 and rand_num <= 0.50:
            	walker[0] -= 1			                	# left
            elif rand_num >0.50 and rand_num <= 0.75:
            	walker[1] += 1				                # up
            elif rand_num >0.75:
            	walker[1] -= 1			                  	# down

            # Determine radius of walker from origin
			r_walker = radius(walker)

			# If walker is close to the largest branch of the cluster then check to perimeter
			if r_walker <= max(cluster_rad)+5:
				state,cluster = boundary(state,walker,perimeter,cluster,cluster_rad)
				if state == 'hit':
					R=radius(walker)
                    break

			# Check if walker is out of bounds, break to generate new walker
			if r_walker >= out_of_bounds:
                break

	# Plot the cluster
    fig = plt.subplot()
    plt.title("Cluster from DLA Method", fontsize=20)
    plt.subplot(1,1,1)
	cmap = matplotlib.colors.ListedColormap(['white','blue'])
	bounds = [-.5,.5,1.5]
	norm = matplotlib.colors.BoundaryNorm(bounds,cmap.N)
	img = plt.imshow(cluster, interpolation='nearest', cmap=cmap, norm=norm)
	plt.xlabel("Horizontal Position [Arbitrary units]", fontsize=15)
	plt.ylabel("Vertical Position [Arbitrary units]", fontsize=15)
	savefig("LaTeX/DLA_crystal_final_%i.png" %(while_count))
	plt.show()

    # Initialize mass and walker counter arrays
	mass_radius = np.arange(5,105,5)
	mass_count=[0]*len(mass_radius)

    # Count the walkers
	if while_count==1:
        # Initialize avg mass array
		mass_count_avg=[0]*len(mass_radius)
	for i in range(len(mass_radius)):
        for j in range(len(cluster_rad)):
            if cluster_rad[j] <= mass_radius[i]:
                mass_count[i] = mass_count[i]+1
        	mass_count_avg[i] += mass_count[i]

    # Calculated values of mass from curve fit equation
    mass = curvefit(mass_radius,1,1.5)

    # Taking log to the base 10 for mass and the radius
	log_mass = np.log10(mass_count)
    log_radius = np.log10(mass_radius)

    # Perform curve fits
	popt, pcov = curve_fit(curvefit, mass_radius, log_mass)
	print "Constant,Fractal dimension:", popt

    # Analytically calculated mass from the fit parameters obtained to get the "fit curve"
	mass_analytic = curvefit(mass_radius, popt[0], popt[1])

	# Plotting fractal dimension relation
    fig = plt.subplot()
	plt.title("Mass distribution of DLA cluster on a log-log plot", fontsize=20)
    plt.subplot(1,1,1)
	plt.plot(log_radius, log_mass, 'r*', label="Raw data")
	plt.plot(log_radius, mass_analytic, 'k-', label="Fit curve")
	plt.legend()
	plt.xlabel("Radius of cluster", fontsize=15)
	plt.ylabel("Number of walkers within radius, mass", fontsize=15)
	plt.savefig("Fractal_dimension_final_%i.png" %(while_count))
	plt.show()

	print "mass_count:", mass_count
	print "mass_count_avg", mass_count_avg

    # Add to counter
    while_count+=1

# Getting average mass over 10 clusters
mass_count_avg[:] = [i/10 for i in mass_count_avg]
print "Final mass_count_avg", mass_count_avg

# ------------------------------------------------------------------------------

# The following is for averaging all the runs.

# Average Curve fit and function definition:
mass_avg = curvefit(mass_radius,1,1.5)
log_mass_avg = np.log10(mass_count_avg)
popt_avg,pcov_avg = curve_fit(curvefit, mass_radius, log_mass_avg)
print "Constant,Avegrage fractal dimension:", popt_avg
log_radius = np.log10(mass_radius)
mass_analytic = curvefit(mass_radius, popt_avg[0], popt_avg[1])

# Plotting fractal dimension relation:
fig = plt.subplot()
plt.title("Fractal dimensionality of DLA cluster averaged over 10 clusters log(m)-log(r)", fontsize=20)
plt.subplot(1,1,1)
plt.plot(log_radius, log_mass_avg, 'r*', label="Raw data")
plt.plot(log_radius, mass_analytic, 'k-', label="Fit curve")
plt.legend()
plt.xlabel("Radius of cluster", fontsize=15)
plt.ylabel("Number of walkers within radius, mass", fontsize=15)
plt.savefig("LaTeX/Fractal_dimension_final_avg.png")
plt.show()

# ------------------------------------------------------------------------------

# INCOMPLETE
