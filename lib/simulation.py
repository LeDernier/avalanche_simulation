 #########################################################################################################################################################################
# Author : Remi Monthiller, remi.monthiller@etu.enseeiht.fr
# Adapted from the code of Raphael Maurin, raphael.maurin@imft.fr
# 30/10/2018
#
# Incline plane simulations
#
#########################################################################################################################################################################

# Import files
execfile("./lib/frameworkCreation.py")
execfile("./lib/inSimulationUtils.py")

####################################################################################################################################
####################################################  DATA LOGGING  #########################################################
####################################################################################################################################

logExecs=[]
def addLogData(fileName,evalfunc):
	"""Creates a new log file and prepare to store values returned by execfunc during the simulation. 
	
	Parameters:
	- fileName  -- name of the log file
	- execfunc  -- python expression to evaluate and so that its result will be stored
	
	"""
	f = open(fileName,"w")
	logExecs.append([f, evalfunc])
	
def logData():
	"""Loggs the data.
	
	"""
	for [f, evalfunc] in logExecs:
		f.write(str(eval(evalfunc)))
		f.write("\n")

####################################################################################################################################
####################################################  SIMULATION DEFINITION  #########################################################
####################################################################################################################################

def simulation(paramsPart, paramsPartsPack, paramsMat, paramsChannel, paramsHouse):
	"""Creates a simulation.
	
	Parameters:
	- [diameterPart, densPart, phiPartMax, restitCoef, partFrictAngle] -- parameters relative to the particles
	- [number, lengthBox, widthBox, heightBox]                         -- parameters relative to the particle cloud
	- [normalStiffness, youngMod, poissonRatio]                        -- parameters relative to the particles' material
	- [slopeChannel, lengthChannel, widthChannel, heightChannel]       -- parameters relative to the channel
	- [positionCoef, angleHouse, lengthHouse, widthHouse, heightHouse] -- parameters relative to the house
	
	"""
	[idHouse, idsToRemove] = frameworkCreation(paramsPart, paramsPartsPack, paramsMat, paramsChannel, paramsHouse)
	engineCreation(idsToRemove)
	O.saveTmp() # User can reload simulation
	
#############################################################################################
#############################################################################################

def simulationWait(paramsPart, paramsPartsPack, paramsMat, paramsChannel, paramsHouse, simulationTime):
	"""Creates a simulation, runs it and wait until its finished.
	
	Parameters:
	- [diameterPart, densPart, phiPartMax, restitCoef, partFrictAngle] -- parameters relative to the particles
	- [number, lengthBox, widthBox, heightBox]                         -- parameters relative to the particle cloud
	- [normalStiffness, youngMod, poissonRatio]                        -- parameters relative to the particles' material
	- [slopeChannel, lengthChannel, widthChannel, heightChannel]       -- parameters relative to the channel
	- [positionCoef, angleHouse, lengthHouse, widthHouse, heightHouse] -- parameters relative to the house
	
	"""
	O.reset() # return to nothing
	
	[idHouse, idsToRemove] = frameworkCreation(paramsPart, paramsPartsPack, paramsMat, paramsChannel, paramsHouse)
	engineCreation(idsToRemove)
	
	O.run(simulationTime) # Run the simulation
	O.wait() # Wait until the simulation is finished
	
#############################################################################################
#############################################################################################

def frameworkCreation(paramsPart, paramsPartsPack, paramsMat, paramsChannel, paramsHouse):
	"""Creates the framework and returns [idHouse, [idWallFront, idWallLeft, idWallRight]], ids of some of the objects created in O.bodies.
	
	Parameters:
	- [diameterPart, densPart, phiPartMax, restitCoef, partFrictAngle] -- parameters relative to the particles
	- [number, lengthBox, widthBox, heightBox]                         -- parameters relative to the particle cloud
	- [normalStiffness, youngMod, poissonRatio]                        -- parameters relative to the particles' material
	- [slopeChannel, lengthChannel, widthChannel, heightChannel]       -- parameters relative to the channel
	- [positionCoef, angleHouse, lengthHouse, widthHouse, heightHouse] -- parameters relative to the house
	
	"""
	[diameterPart, densPart, phiPartMax, restitCoef, partFrictAngle] =  paramsPart
	[number, lengthBox, widthBox, heightBox] =  paramsPartsPack
	[normalStiffness, youngMod, poissonRatio] =  paramsMat
	[slopeChannel, lengthChannel, widthChannel, heightChannel] =  paramsChannel
	[positionCoef, angleHouse, lengthHouse, widthHouse, heightHouse] =  paramsHouse
	
	# Material definition
	
	O.materials.append(ViscElMat(en=restitCoef, et=0., young=youngMod, poisson=poissonRatio, density=densPart, frictionAngle=partFrictAngle, label='Mat')) 

	######################################################################################
	### Framework creation
	######################################################################################
	
	createGround()
	createChannel(widthChannel, lengthChannel, heightChannel, slopeChannel)
	# createRugosity(diameterPart, widthChannel, lengthChannel, slopeChannel)
	[idWallBack, idWallFront, idWallLeft, idWallRight] = createPartBox(widthBox, lengthBox, heightBox, widthChannel, lengthChannel, slopeChannel)
	createPartCloud(widthBox, lengthBox, heightBox, widthChannel, lengthChannel, slopeChannel, diameterPart, number)
	idHouse = createHouse(positionCoef, angleHouse, lengthHouse, widthHouse, heightHouse, widthChannel, lengthChannel, slopeChannel)
	
	return [idHouse, [idWallFront, idWallLeft, idWallRight]]
	
#############################################################################################
#############################################################################################

def engineCreation(idsToRemove):
	"""Creates the engine.
	
	Parameters:
	- idsToRemove -- the ids (as an list) of the objects you want to remove after 1 sec of simulation.
	
	"""
	######################################################################################
	### Simulation loop
	######################################################################################
	
	O.engines = [
		# Reset the forces
		ForceResetter(),
		# Detect the potential contacts
		InsertionSortCollider([Bo1_Sphere_Aabb(), Bo1_Wall_Aabb(),Bo1_Facet_Aabb(),Bo1_Box_Aabb()],label='contactDetection',allowBiggerThanPeriod = True),
		# Calculate the different interactions
		InteractionLoop(
		[Ig2_Sphere_Sphere_ScGeom(), Ig2_Box_Sphere_ScGeom(),Ig2_Facet_Sphere_ScGeom()],
		[Ip2_ViscElMat_ViscElMat_ViscElPhys()],
		[Law2_ScGeom_ViscElPhys_Basic()]
		,label = 'interactionLoop'),				
		# Gravity deposition
		PyRunner(command='deleteObjects(' + str(idsToRemove) + ', 1)',virtPeriod = 0.01,label = 'gravDepo'),
		PyRunner(command='logData()',virtPeriod = 0.01,label = 'logs'),
		#GlobalStiffnessTimeStepper, determine the time step for a stable integration
		GlobalStiffnessTimeStepper(defaultDt = 1e-4, viscEl = True,timestepSafetyCoefficient = 0.7,  label = 'GSTS'),
		# Integrate the equation and calculate the new position/velocities...
		NewtonIntegrator(gravity=(0,0,-9.81), label='newtonIntegr')
		]
		
	gravDepo.dead = False
	logs.dead = False
	
#############################################################################################
#############################################################################################

