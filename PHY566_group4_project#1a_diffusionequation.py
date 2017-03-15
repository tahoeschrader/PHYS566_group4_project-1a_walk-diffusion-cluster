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
