### Group 4
### Computational Physics
### Spring, 2017

################################################################################
### This code will simulate the percolation transition on a N x N lattice by
### randomly filling lattice sites. Occupation probability is a fraction of all
### occupied sites among lattice sites in general. Therefore, each population
### step wil increase p. We want this code to:
###             a) Determine critical probability (p when spanning cluster occurs)
###                           --- COMPLETE
###             b) Determine pc and plot the cluster for N = 5, 10, 15, 20, 30,
###                50, and 80 across an average of 50x
###                            --- INCOMPLETE. Neither of these have been added
###             c) Plot pc(N^-1) to extrapolate infinite size limit pc(0)
################################################################################

# ------------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
import random as rnd

# ------------------------------------------------------------------------------

################################################################################
### Define initial variables
################################################################################

# ------------------------------------------------------------------------------

N = [5,10,15,20,30,50,80]       # lattice sizes to compute over
num_average = 50                # calculations to be averaged 50x

# ------------------------------------------------------------------------------

################################################################################
### Define the neighborhood for each spot on the grid.
################################################################################

# ------------------------------------------------------------------------------

def Neighborhood(new_location_row, new_location_col,current_N, current_lattice) :
    # Initialize all special sites to False
    top_edge = False
    bottom_edge = False
    left_edge = False
    right_edge = False

    # Define edge boundaries
    if new_location_row == 0 :
        top_edge = True
    if new_location_row == int(current_N - 1) :
        bottom_edge = True
    if new_location_col == 0 :
        left_edge = True
    if new_location_col == int(current_N - 1) :
        right_edge = True

    # Define neighbors for the corners. Call non-existant neighbors zero
    if top_edge and left_edge :
        neighbor_top = 0
        neighbor_bottom = current_lattice[new_location_row + 1, new_location_col]
        neighbor_left = 0
        neighbor_right = current_lattice[new_location_row, new_location_col + 1]
    elif top_edge and right_edge :
        neighbor_top = 0
        neighbor_bottom = current_lattice[new_location_row + 1, new_location_col]
        neighbor_left = current_lattice[new_location_row, new_location_col - 1]
        neighbor_right = 0
    elif bottom_edge and left_edge :
        neighbor_top = current_lattice[new_location_row - 1, new_location_col]
        neighbor_bottom = 0
        neighbor_left = 0
        neighbor_right = current_lattice[new_location_row, new_location_col + 1]
    elif bottom_edge and right_edge :
        neighbor_top = current_lattice[new_location_row - 1, new_location_col]
        neighbor_bottom = 0
        neighbor_left = current_lattice[new_location_row, new_location_col - 1]
        neighbor_right = 0

    # Define neighbors for edge cases not on the corner
    elif top_edge and not left_edge and not right_edge :
        neighbor_top = 0
        neighbor_bottom = current_lattice[new_location_row + 1, new_location_col]
        neighbor_left = current_lattice[new_location_row, new_location_col - 1]
        neighbor_right = current_lattice[new_location_row, new_location_col + 1]
    elif bottom_edge and not left_edge and not right_edge :
        neighbor_top = current_lattice[new_location_row - 1, new_location_col]
        neighbor_bottom = 0
        neighbor_left = current_lattice[new_location_row, new_location_col - 1]
        neighbor_right = current_lattice[new_location_row, new_location_col + 1]
    elif left_edge and not top_edge and not bottom_edge :
        neighbor_top = current_lattice[new_location_row - 1, new_location_col]
        neighbor_bottom = current_lattice[new_location_row + 1, new_location_col]
        neighbor_left = 0
        neighbor_right = current_lattice[new_location_row, new_location_col + 1]
    elif right_edge and not top_edge and not bottom_edge :
        neighbor_top = current_lattice[new_location_row - 1, new_location_col]
        neighbor_bottom = current_lattice[new_location_row + 1, new_location_col]
        neighbor_left = current_lattice[new_location_row, new_location_col - 1]
        neighbor_right = 0

    # Define neighbors for all the standard lattice positions
    else :
        neighbor_top = current_lattice[new_location_row - 1, new_location_col]
        neighbor_bottom = current_lattice[new_location_row + 1, new_location_col]
        neighbor_left = current_lattice[new_location_row, new_location_col - 1]
        neighbor_right = current_lattice[new_location_row, new_location_col + 1]

    return neighbor_top, neighbor_bottom, neighbor_left, neighbor_right

# ------------------------------------------------------------------------------

################################################################################
### Create the spanning cluster checker
################################################################################

# ------------------------------------------------------------------------------

def SpanningCluster(current_lattice, current_N) :
    # Grab the top edge data
    on_top = current_lattice[0, :]

    # Loop through each value in this N sized list and see if there's a common value
    for i in range(current_N) :
        if on_top[i] > 0 :
            # Grab the rest of the edge data
            on_bottom = current_lattice[current_N - 1, :]
            on_left = current_lattice[:, 0]
            on_right = current_lattice[:, current_N - 1]

            # Create an array of True/False values for the remaining edges to see
            # if there is a matching cluster number
            check_bottom = on_bottom == on_top[i]
            check_left = on_left == on_top[i]
            check_right = on_right == on_top[i]

            # Check if a value matches on the edges
            bottom_match = True in check_bottom
            left_match = True in check_left
            right_match = True in check_right

            # Finally, check to see if they are all true at the same time... a feat
            # which corresponds to the existance of a spanning cluster...
            spanning_cluster=False
            if bottom_match == True and left_match == True and right_match == True :
                spanning_cluster = True

                # Now break the loop since we have all the information we need
                break

    return spanning_cluster

# ------------------------------------------------------------------------------

################################################################################
### Create the Cluster Builder function
################################################################################

# ------------------------------------------------------------------------------

def ClusterBuilder(current_N) :
    # This function uses random numbers, so initialize a seed of system time
    seed = rnd.seed()

    # Begin by initializing an empty 2D lattice with zeros
    current_lattice = np.zeros((current_N,current_N))  # rows vs. columns

    # We want the cluster to build until a spanning cluster has been reached, so
    # we initalize a boolean spanning cluster checker to be False
    spanning_cluster = False

    # Occupy a random site of the lattice and label it as cluster no. 1, then
    # start the cluster counter
    current_lattice[rnd.randint(0,current_N - 1), rnd.randint(0,current_N - 1)] = 1
    cluster_counter = 1

    # Begin the loop!
    while not spanning_cluster :
        # Choose a new random lattice location in x and y
        new_location_row = rnd.randint(0,current_N - 1)
        new_location_col = rnd.randint(0,current_N-1)

        # Make sure this spot has not already been chosen
        if current_lattice[new_location_row,new_location_col] > 0 :
            continue

        # Now, obtain the values of lattice sites surrounding the new point
        top, bottom, left, right = Neighborhood(new_location_row, new_location_col,current_N, current_lattice)

        # If there are no neighbors, give this lattice point a value equal to
        # the cluster counter, add to the cluster counter, and continue the loop
        if top == 0 and bottom == 0 and left == 0 and right == 0 :
            current_lattice[new_location_row, new_location_col] = cluster_counter
            cluster_counter += 1

            # Note: we don't need to check for a spanning cluster here
            continue

        # If there's only one neighbor, give site the neighboring cluster number
        elif top > 0 and bottom == 0 and left == 0 and right == 0 :
            current_lattice[new_location_row, new_location_col] = top

            # Check for a spanning cluster and start the loop over
            spanning_cluster = SpanningCluster(current_lattice, current_N)
            continue

        elif top == 0 and bottom > 0 and left == 0 and right == 0 :
            current_lattice[new_location_row, new_location_col] = bottom

            # Check for a spanning cluster and start the loop over
            spanning_cluster = SpanningCluster(current_lattice, current_N)

            continue
        elif top == 0 and bottom == 0 and left > 0 and right == 0 :
            current_lattice[new_location_row, new_location_col] = left

            # Check for a spanning cluster and start the loop over
            spanning_cluster = SpanningCluster(current_lattice,current_N)
            continue

        elif top == 0 and bottom == 0 and left == 0 and right > 0 :
            current_lattice[new_location_row, new_location_col] = right

            # Check for a spanning cluster and start the loop over
            spanning_cluster = SpanningCluster(current_lattice,current_N)
            continue

        # Arriving here means there are multiple neighbors. Count clusters and
        # choose one at random to "win"
        nearby_clusters = 0

        # Turn the neighbor variables into a checkable list and make a list of
        # strings to help with sorting a cluster dictionary
        neighbors = [top, bottom, left, right]

        # Run through these neighbors and add to the cluster counter
        cluster_dict = {}
        for i in range(3) :
            if neighbors[i] > 0 :
                cluster_dict["neighbor {}".format(i + 1)] = neighbors[i]
                nearby_clusters += 1

        # Depending on the number of nearby clusters, we change the random number metric
        if nearby_clusters == 2 :
            # Pick random number between 0 and 1
            decision = rnd.random()

            # There are two possibilities, so 2 choices
            if decision < .50 : # Choice number one
                # Define the winner and loser
                winner = cluster_dict["neighbor 0"]
                loser = cluster_dict["neighbor 1"]

                # Set the new point equal to the winning neighbor
                current_lattice[new_location_row, new_location_col] = winner

                # Set all losers equal to the winner (using list comprehension rather than a nested for loop)
                current_lattice = np.array([[winner if current_lattice[i,j] == loser else current_lattice[i,j] for j in range(current_N)] for i in range(current_N)])

            else : # Choice number two
            # Define the winner and loser
                winner = cluster_dict["neighbor 1"]
                loser = cluster_dict["neighbor 0"]

                # Set the new point equal to the winning neighbor
                current_lattice[new_location_row, new_location_col] = winner

                # Set all losers equal to the winner (using list comprehension rather than a nested for loop)
                current_lattice = np.array([[winner if current_lattice[i,j] == loser else current_lattice[i,j] for j in range(current_N)] for i in range(current_N)])


            # Check for a spanning cluster and start the loop over
            spanning_cluster = SpanningCluster()
            continue

        elif nearby_clusters == 3 :
            # Pick random number between 0 and 1
            decision = rnd.random()

            # There are three possibilities, so 3 choices
            if decision < 1./3. * 1 : # Choice number one
                # Define the winner and loser
                winner = cluster_dict["neighbor 0"]
                loser1 = cluster_dict["neighbor 1"]
                loser2 = cluster_dict["neighbor 2"]

                # Set the new point equal to the winning neighbor
                current_lattice[new_location_row, new_location_col] = winner

                # Set all losers equal to the winner (using list comprehension rather than a nested for loop)
                current_lattice = np.array([[winner if current_lattice[i,j] == loser1 or current_lattice[i,j] == loser2 else current_lattice[i,j] for j in range(current_N)] for i in range(current_N)])

            elif decision < 2./3. * 1 : # Choice number two
            # Define the winner and loser
                winner = cluster_dict["neighbor 1"]
                loser1 = cluster_dict["neighbor 0"]
                loser2 = cluster_dict["neighbor 2"]

                # Set the new point equal to the winning neighbor
                current_lattice[new_location_row, new_location_col] = winner

                # Set all losers equal to the winner (using list comprehension rather than a nested for loop)
                current_lattice = np.array([[winner if current_lattice[i,j] == loser1 or current_lattice[i,j] == loser2 else current_lattice[i,j] for j in range(current_N)] for i in range(current_N)])

            else : # Choice number three
            # Define the winner and loser
                winner = cluster_dict["neighbor 2"]
                loser1 = cluster_dict["neighbor 0"]
                loser2 = cluster_dict["neighbor 1"]

                # Set the new point equal to the winning neighbor
                current_lattice[new_location_row, new_location_col] = winner

                # Set all losers equal to the winner (using list comprehension rather than a nested for loop)
                current_lattice = np.array([[winner if current_lattice[i,j] == loser1 or current_lattice[i,j] == loser2 else current_lattice[i,j] for j in range(current_N)] for i in range(current_N)])

            # Check for a spanning cluster and start the loop over
            spanning_cluster = SpanningCluster()
            continue

        elif nearby_clusters == 4 :
            # Pick random number between 0 and 1
            decision = rnd.random()

            # There are four possibilities, so 4 choices
            if decision < .25 : # Choice number one
                # Define the winner and loser
                winner = cluster_dict["neighbor 0"]
                loser1 = cluster_dict["neighbor 1"]
                loser2 = cluster_dict["neighbor 2"]
                loser3 = cluster_dict["neighbor 3"]

                # Set the new point equal to the winning neighbor
                current_lattice[new_location_row, new_location_col] = winner

                # Set all losers equal to the winner (using list comprehension rather than a nested for loop)
                current_lattice = np.array([[winner if current_lattice[i,j] == loser1 or current_lattice[i,j] == loser2 or current_lattice[i,j] == loser3 else current_lattice[i,j] for j in range(current_N)] for i in range(current_N)])

            elif decision < .5 : # Choice number two
            # Define the winner and loser
                winner = cluster_dict["neighbor 1"]
                loser1 = cluster_dict["neighbor 0"]
                loser2 = cluster_dict["neighbor 2"]
                loser3 = cluster_dict["neighbor 3"]

                # Set the new point equal to the winning neighbor
                current_lattice[new_location_row, new_location_col] = winner

                # Set all losers equal to the winner (using list comprehension rather than a nested for loop)
                current_lattice = np.array([[winner if current_lattice[i,j] == loser1 or current_lattice[i,j] == loser2 or current_lattice[i,j] == loser3 else current_lattice[i,j] for j in range(current_N)] for i in range(current_N)])

            elif decision < .75 : # Choice number three
            # Define the winner and loser
                winner = cluster_dict["neighbor 2"]
                loser1 = cluster_dict["neighbor 0"]
                loser2 = cluster_dict["neighbor 1"]
                loser3 = cluster_dict["neighbor 3"]

                # Set the new point equal to the winning neighbor
                current_lattice[new_location_row, new_location_col] = winner

                # Set all losers equal to the winner (using list comprehension rather than a nested for loop)
                current_lattice = np.array([[winner if current_lattice[i,j] == loser1 or current_lattice[i,j] == loser2 or current_lattice[i,j] == loser3 else current_lattice[i,j] for j in range(current_N)] for i in range(current_N)])

            else : # Choice number four
            # Define the winner and loser
                winner = cluster_dict["neighbor 3"]
                loser1 = cluster_dict["neighbor 0"]
                loser2 = cluster_dict["neighbor 1"]
                loser3 = cluster_dict["neighbor 2"]

                # Set the new point equal to the winning neighbor
                current_lattice[new_location_row, new_location_col] = winner

                # Set all losers equal to the winner (using list comprehension rather than a nested for loop)
                current_lattice = np.array([[winner if current_lattice[i,j] == loser1 or current_lattice[i,j] == loser2 or current_lattice[i,j] == loser3 else current_lattice[i,j] for j in range(current_N)] for i in range(current_N)])

            # Check for a spanning cluster and start the loop over
            spanning_cluster = SpanningCluster()
            continue

    # Now that we have the spanning cluster, we can calculate pc. Initialize
    # a counter
    occupied_sites = 0

    # Start counting
    for i in range(current_N) :
        for j in range(current_N) :
            if current_lattice[i,j] > 0 :
                occupied_sites += 1

    # Divide by total sites
    pc = float(occupied_sites / (current_N * current_N))



    return current_lattice, pc



############# DO the plots

#b) Determine pc and plot the cluster for N = 5, 10, 15, 20, 30,
###                50, and 80 across an average of 50x
###                            --- INCOMPLETE. Neither of these have been added
###             c) Plot pc(N^-1) to extrapolate infinite size limit pc(0)


print(ClusterBuilder(5))
