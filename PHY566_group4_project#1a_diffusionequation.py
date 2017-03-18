### Group 4
### Computational Physics
### Spring, 2017

################################################################################
### This code will look at the 1D diffusion equation:
###       a) Analytically, we show that the spatial expectation value of the 1D
###          normal distribution equals sigma^2. WILL BE DERIVED IN LATEX PAPER
###             --- CURRENTLY INCOMPLETE
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

diffconst = 2.0                 # diffusion constant
xsteps = .1                     # an xdimension stepsize <1 is ideal
xlength = 100
peak = 100.0                    # this is where the box density sharply peaks
tsteps = 1
time = 100

# ------------------------------------------------------------------------------

################################################################################
### Define the diffusion equation solver
################################################################################
def diffusion1D() :
    # Initialize the density vector and xdimension to solve over
    xlocation = np.arange(0,xlength,xsteps)
    xiters = int(len(xlocation))
    titers = int(time/tsteps)
    density = np.zeros((xiters,titers))

    # Define the initial box density to be sharply peaked over a few sites in x
    # for the first time solve. I fix the last boundary condition to zero
    density[0:10,0] = peak
    density[xiters - 1,:] = 0.0   # xiters-1 is the final index

    # Iteratively solve the density equation
    for n in range(titers - 1) :
        for i in range(xiters - 2) : # Already fixed xiters-1 to be zero
            density[i,n+1] = density[i,n] + diffconst * tsteps / (xsteps**2) * (density[i+1,n] + density[i-1,n] - 2 * density[i,n])

    return xlocation, density

# ------------------------------------------------------------------------------

################################################################################
### Now plot the solutions
################################################################################
# ------------------------------------------------------------------------------


#                             # BEGIN PLOT ONE
# This plot will look at a time snapshot of the diffusion equation
xlocation,density = diffusion1D()
print density

# Now plot
fig = plt.figure()
fig.suptitle('Time Snapshot of $1D$ Diffusion Equation',fontsize=25)

plt.subplot(1,1,1)
plt.plot(xlocation,density[:,1],'b-',label='probability density')
plt.ylabel('probability density',fontsize=20)
plt.xlabel('$x$ location',fontsize=20)
plt.legend()
plt.grid()

#plt.savefig("LaTeX\probdensity0.png")

# Makes my figures show up
plt.show()
# INCOMPLETE
