### Group 4
### Computational Physics
### Spring, 2017

################################################################################
### This code will look at the 1D diffusion equation:
###       a) Analytically, we show that the spatial expectation value of the 1D
###          normal distribution equals sigma^2.
###             --- COMPLETE
###       b) Solve the 1D diff. eq. using the finite difference form and a
###          diffusion constant of D=2.
###             --- COMPLETE
### ----------------------------------------------------------------------------
### We are told to start from an initial density profile that is sharply peaked
### around x=0, but extends over a few grid sites (box profile).
###
### Verify (using a fit) that at later times the numerically calculated density
### profile corresponds to a Normal Distribution with sigma = sqrt(2Dt). Perform
### the fit over 5 different time snapshots with visibilty significant changes
### in the distribution.
################################################################################

import numpy as np
import matplotlib.pyplot as plt
import random as rng
from datetime import datetime
from scipy.optimize import curve_fit     # Curve fitting package

################################################################################
### Start with setting up the problem. Here, we create initial variables
################################################################################

# ------------------------------------------------------------------------------

diffconst = 2.0                       # diffusion constant (given)
xsteps = .03                        # a dx<1 is ideal for smoothness
xlength = 40
peak = 100                            # original box shaped density peak
tsteps = 0.5*xsteps**2/(2*diffconst)  # guarantees stability if dt <= dx^2/(2D)
                                      # so I made it .5 * dx^2/(2D) D !!!
duration = 5

# ------------------------------------------------------------------------------

################################################################################
### Define the diffusion equation solver and Gaussian model
################################################################################

# ------------------------------------------------------------------------------

def diffusion1D() :
    # Initialize the density and location vectors (in time and x)
    xlocation = np.arange(0,xlength,xsteps)
    tlocation = np.arange(0,duration,tsteps)
    x_iters = int(len(xlocation))               # total x iterations
    t_iters = int(len(tlocation))               # total t iterations
    density = np.zeros((x_iters,t_iters))       # size of all x and t
    # Define the boundary conditions
    # For t = 0, the first couple xlocations should be the peak size
    #find middle and place the peak there
    density[60:62,0] = peak

    # Iteratively solve the density equation
    for t in range(t_iters-1) :
        for x in range(x_iters-2) :
            density[x,t+1] = density[x,t] + diffconst * tsteps * (density[x+1,t] + density[x-1,t] - 2.0 * density[x,t])/xsteps**2
    return xlocation, density

# ------------------------------------------------------------------------------

def gaussian(x,sigma,amplitude,mu):
    return amplitude * (1.0 / (sigma*np.sqrt(2*np.pi))) * np.exp(-((x-mu)**2/(2*sigma**2)))

# ------------------------------------------------------------------------------

################################################################################
### Now plot the solutions
################################################################################

# ------------------------------------------------------------------------------

# Call the function
location,probability = diffusion1D()

# ------------------------------------------------------------------------------

#                             # BEGIN PLOT ONE
# This plot will look at the initial time snapshot of the diffusion equation

# Now plot
fig = plt.subplot()
plt.title('Initial Box Density',fontsize=20)
plt.subplot(1,1,1)
plt.plot(location,probability[:,0],color= 'tomato', label='distribution', lw=3)
plt.ylabel('density',fontsize=15)
plt.xlabel('$x$ location',fontsize=15)
plt.legend()
plt.grid()
plt.axis([0,5,0,110])
plt.grid()
fig.spines["top"].set_visible(False)
fig.spines["right"].set_visible(False)
plt.savefig("LaTeX/probdensityinit.png")

# Makes my figures show up
plt.show()

# ------------------------------------------------------------------------------

#                             # BEGIN PLOT TWO-SIX
# This plot will look at 5 snapshots in time of the diffusion solver and fit a
# gaussian to them. First, define points in time wrt timesteps

#max=int(probability.shape[1])
#t=[int(0.005*max),int(0.01*max),int(0.05*max),int(0.1*max),int(0.15*max), int(0.45*max)]

t=[10, 55, 110,510,1600,2000]

# To fit the gaussian, use the scipy function

#iterate through times
for i in t:
	# Calculate the time where we are taking snapshots
	snapshot = tsteps * i
	#initial values for the fit
	init_vals = [diffconst, peak, np.sqrt(2*diffconst*snapshot)]     # for (sigma,amplitude,mu)

	#fit using curve_fit package
	best_vals, covar = curve_fit(gaussian,location, probability[:,i], p0=init_vals)


	# Now develop plots
	fig = plt.subplot()
	plt.title('$1D$ Diffusion at $t=$%g w/ $\sigma=$%.2f'%(snapshot,np.sqrt(2.0*diffconst*snapshot)),fontsize=20)
	plt.plot(location, probability[:,i], color= 'tomato', label='distribution', lw=3)
	plt.plot(location, gaussian(location, best_vals[0],best_vals[1],best_vals[2] ),color='dodgerblue',linestyle='dashed', linewidth = 3, label='best fit, $\sigma = $%.2f' %best_vals[0])
	plt.ylabel('density',fontsize=15)
	plt.xlabel('$x$ location',fontsize=15)
	#plt.ylim([0,70])
	plt.xlim([0,5])
	plt.legend()
	plt.grid()
	fig.spines["top"].set_visible(False)
	fig.spines["right"].set_visible(False)
	plt.savefig("LaTeX/probdensityt{}.png".format(i))
	plt.show()

# COMPLETE
