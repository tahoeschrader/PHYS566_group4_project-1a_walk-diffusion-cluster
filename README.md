# Computational Physics (PHYS566) Group Projects
These group projects are for PHYS566 at Duke University. The group members are Tahoe, Ksenia, and Xinmeng. The first project involved creating random walks, solving the diffusion equation, and building a DLA Cluster. The readme for this part of the project is not very fleshed out. 

The second project studied percolation among a 2D cluster. 

## Percolation 
Percolation is when a cluster becomes a spanning cluster. A spanning cluster is a cluster that extends to all boundaries in its environment. So, for a 2D box, the cluster must touch the ends of all four sides. 

This is a computationally easy feat to enact:
1. Generate a 2D lattice
2. Populate a single lattice site at random and define it to be a cluster
3. Populate another single lattice site at random
4. If the new site touches an old site, define it to be a part of that cluster, otherwise define it as a new cluster
5. If the new site touches multiple old sites, randomly choose one cluster to "win" and redefine all touching clusters to be a part of the "winning" cluster
6. Repeat until the same cluster touches all four sides


