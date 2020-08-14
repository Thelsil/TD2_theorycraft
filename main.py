from scripts.builds.get_TrashBuild import get_TrashBuild
from scripts.builds.get_optiARBuild import get_optiARBuild
from src.faceTrade_simulation import faceTrade_simulation

# Example on how to run a 1v1 facetrade simulation.
# Pre-defined builds are located in scripts/builds, check these files to understand how to make your own builds!

# Simulation setup.
shootingRange   = 15    # Set the shooting range between players (in meter).
numSimulSamples = 10**6 # Number of 1v1 to simulate. If it takes too long, lower this number.

# Instanciate a well designed AR build.
nBlueCore   = 5 # The number of blue core can be configured for the main build.
good_build  = get_optiARBuild(nBlueCore)

# Instanciate a badly designed AR build from a certain youtuber...
bad_build    = get_TrashBuild()

# Run the simulation!
simulResults = faceTrade_simulation(good_build, bad_build, shootingRange, numSimulSamples)

# Display the simulation results in the console.
simulResults.display()





