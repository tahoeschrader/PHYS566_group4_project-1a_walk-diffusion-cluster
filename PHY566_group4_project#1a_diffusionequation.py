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
###             --- CURRENTLY INCOMPLETE
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
from lmfit import Model                 # Curve fitting package

################################################################################
### Start with setting up the problem. Here, we create initial variables
################################################################################

# ------------------------------------------------------------------------------

diffconst = 2.0                       # diffusion constant (given)
xsteps = .05                          # a dx<1 is ideal for smoothness
xlength = 5
peak = 100                            # original box shaped density peak
tsteps = xsteps**2/(2*diffconst)/2.0  # guarantees stability if dt <= dx^2/(2D)
                                      # so I made it .5 * dx^2/(2D) D !!!
duration = 10

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
    density[0:5,0] = peak

    # Iteratively solve the density equation
    for t in range(t_iters - 1) :
        for x in range(x_iters - 2) :
            density[x,t+1] = density[x,t] + (diffconst * (tsteps/xsteps**2) * (density[x+1,t] + density[x-1,t] - 2.0 * density[x,t]))

    return xlocation, density

# ------------------------------------------------------------------------------

def Gaussian(x,sigma,amplitude,mu):
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
fig = plt.figure()
fig.suptitle('Initial Box Density',fontsize=25)

plt.subplot(1,1,1)
plt.plot(location,probability[:,0],'b-',label='distribution')
plt.ylabel('density',fontsize=20)
plt.xlabel('$x$ location',fontsize=20)
plt.legend()
plt.grid()
plt.axis([0,5,0,110])

plt.savefig("LaTeX\probdensityinit.png")

# Makes my figures show up
plt.show()

# ------------------------------------------------------------------------------

#                             # BEGIN PLOT TWO-SIX
# This plot will look at 5 snapshots in time of the diffusion solver and fit a
# gaussian to them. First, define points in time wrt timesteps
t1 = 10
t2 = 50
t3 = 500
t4 = 1000
t5 = 1600

# Calculate the time where we are taking snapshots
snapshot1 = tsteps * t1
snapshot2 = tsteps * t2
snapshot3 = tsteps * t3
snapshot4 = tsteps * t4
snapshot5 = tsteps * t5

# To fit the gaussian, I build the gaussian Model
gaussianmodel = Model(Gaussian)
fitresult1 = gaussianmodel.fit(probability[:,t1], x = location , amplitude = peak , sigma = diffconst , mu = np.sqrt(2*diffconst*snapshot1))
fitresult2 = gaussianmodel.fit(probability[:,t2], x = location , amplitude = peak , sigma = diffconst , mu = np.sqrt(2*diffconst*snapshot2))
fitresult3 = gaussianmodel.fit(probability[:,t3], x = location , amplitude = peak , sigma = diffconst , mu = np.sqrt(2*diffconst*snapshot3))
fitresult4 = gaussianmodel.fit(probability[:,t4], x = location , amplitude = peak , sigma = diffconst , mu = np.sqrt(2*diffconst*snapshot4))
fitresult5 = gaussianmodel.fit(probability[:,t5], x = location , amplitude = peak , sigma = diffconst , mu = np.sqrt(2*diffconst*snapshot5))

# Now I extract the best fit sigma's
sigma1 = fitresult1.best_values['sigma']
sigma2 = fitresult2.best_values['sigma']
sigma3 = fitresult3.best_values['sigma']
sigma4 = fitresult4.best_values['sigma']
sigma5 = fitresult5.best_values['sigma']

# Now develop plots

fig = plt.figure()
fig.suptitle('$1D$ Diffusion at $t=$%g w/ $\sigma=$%.2f'%(snapshot1,np.sqrt(2.0*diffconst*snapshot1)),fontsize=25)
plt.subplot(1,1,1)
plt.plot(location,probability[:,t1],'b-',label='distribution')
plt.plot(location, fitresult1.best_fit,'k--', linewidth = 3, label='best fit, $\sigma = $%.2f' %sigma1)
plt.ylabel('density',fontsize=20)
plt.xlabel('$x$ location',fontsize=20)
plt.legend()
plt.grid()
plt.savefig("LaTeX\probdensityt1.png")
plt.show()

fig = plt.figure()
fig.suptitle('$1D$ Diffusion at $t=$%g w/ $\sigma=$%.2f' %(snapshot2,np.sqrt(2.0*diffconst*snapshot2)),fontsize=25)
plt.subplot(1,1,1)
plt.plot(location,probability[:,t2],'b-',label='distribution')
plt.plot(location, fitresult2.best_fit,'k--', linewidth = 3, label='best fit, $\sigma = $%.2f' %sigma2)
plt.ylabel('density',fontsize=20)
plt.xlabel('$x$ location',fontsize=20)
plt.legend()
plt.grid()
plt.savefig("LaTeX\probdensityt2.png")
plt.show()

fig = plt.figure()
fig.suptitle('$1D$ Diffusion at $t=$%g w/ $\sigma=$%.2f' %(snapshot3,np.sqrt(2.0*diffconst*snapshot3)),fontsize=25)
plt.subplot(1,1,1)
plt.plot(location,probability[:,t3],'b-',label='distribution')
plt.plot(location, fitresult3.best_fit,'k--', linewidth = 3, label='best fit, $\sigma = $%.2f' %sigma3)
plt.ylabel('density',fontsize=20)
plt.xlabel('$x$ location',fontsize=20)
plt.legend()
plt.grid()
plt.savefig("LaTeX\probdensityt3.png")
plt.show()

fig = plt.figure()
fig.suptitle('$1D$ Diffusion at $t=$%g w/ $\sigma=$%.2f' %(snapshot4,np.sqrt(2.0*diffconst*snapshot4)),fontsize=25)
plt.subplot(1,1,1)
plt.plot(location,probability[:,t4],'b-',label='distribution')
plt.plot(location, fitresult4.best_fit,'k--', linewidth = 3, label='best fit, $\sigma = $%.2f' %sigma4)
plt.ylabel('density',fontsize=20)
plt.xlabel('$x$ location',fontsize=20)
plt.legend()
plt.grid()
plt.savefig("LaTeX\probdensityt4.png")
plt.show()

fig = plt.figure()
fig.suptitle('$1D$ Diffusion at $t=$%g w/ $\sigma=$%.2f'%(snapshot5,np.sqrt(2.0*diffconst*snapshot5)),fontsize=25)
plt.subplot(1,1,1)
plt.plot(location,probability[:,t5],'b-',label='distribution')
plt.plot(location, fitresult5.best_fit,'k--', linewidth = 3, label='best fit, $\sigma = $%.2f' %sigma5)
plt.ylabel('density',fontsize=20)
plt.xlabel('$x$ location',fontsize=20)
plt.legend()
plt.grid()
plt.savefig("LaTeX\probdensityt5.png")
plt.show()

# INCOMPLETE
