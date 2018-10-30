# import lib
import matplotlib.pyplot as plt

# import simulation
execfile('./lib/simulation.py')

# definition of parameters

#############################################################################
###### Parameter Definition
#############################################################################

### Particles ################################################

diameterPart = 1e-1	#Diameter of the particles, in meter
densPart = 300		#density of the particles, in kg/m3
phiPartMax = 0.61	#Value of the dense packing solid volume fraction, dimensionless
restitCoef = 0.5	#Restitution coefficient of the particles, dimensionless

#########################################################################################################################################################################
# Author : Remi Monthiller, remi.monthiller@etu.enseeiht.fr
# Adapted from the code of Raphael Maurin, raphael.maurin@imft.fr
# 30/10/2018
#
# Incline plane simulations
#
#########################################################################################################################################################################

partFrictAngle = atan(0.5)	#friction angle of the particles, in radian

paramsPart = [diameterPart, densPart, phiPartMax, restitCoef, partFrictAngle]

### Particles container ################################################

number = 900
lengthBox = 10 * diameterPart	# length of the container 
widthBox = 20 * diameterPart	# Spanwise length of the container
heightBox = 10 * diameterPart	# Height of the container


paramsPartsPack = [number, lengthBox, widthBox, heightBox]


### Material Definition ################################################

normalStiffness = 1e4 # Minimal normal stiffness to be in the rigid particle limit (cf Roux and Combe 2002)
youngMod = 1e7 # NormalStiffness/diameterPart	#Young modulus of the particles from the stiffness wanted.
poissonRatio = 0.5	# Poisson's ratio of the particles. Classical values, does not have much influence

paramsMat = [normalStiffness, youngMod, poissonRatio]


### Inclined channel ################################################

slopeChannel = 10. * pi / 180.	# Inclination angle of the channel slope, in radian
lengthChannel = 100 * diameterPart	# length of the channel
widthChannel = 50 * diameterPart	# Spanwise length of the channel
heightChannel = 10 * diameterPart # Height of the channel

paramsChannel = [slopeChannel, lengthChannel, widthChannel, heightChannel]

### House ################################################
	
positionCoef = 0.5
angleHouse = 45.0
lengthHouse = 10 * diameterPart
widthHouse = 20 * diameterPart
heightHouse = 10 * diameterPart

paramsHouse = [positionCoef, angleHouse, lengthHouse, widthHouse, heightHouse]

#############################################################################
###### Framework Creation
#############################################################################

[idHouse, idsToRemove] = frameworkCreation(paramsPart, paramsPartsPack, paramsMat, paramsChannel, paramsHouse) # Creates framework separately

#############################################################################
###### Add Data To store
#############################################################################

addLogData("time.txt","O.time - 1.0") # Store time
addLogData("forceOnObject.txt","getForceOnObject(" + str(idHouse) + ")") # Store force applied on the house. 

#############################################################################
###### Simulation Call
#############################################################################

engineCreation(idsToRemove) # Creates engine
