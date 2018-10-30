
#########################################################################################################################################################################
# Author : Remi Monthiller, remi.monthiller@etu.enseeiht.fr
# Adapted from the code of Raphael Maurin, raphael.maurin@imft.fr
# 30/10/2018
#
# Incline plane simulations
#
#########################################################################################################################################################################

execfile("./lib/utils.py")
	
#############################################################################################
#############################################################################################
	
def deleteObjects(objectIds, timeLim):
	"""Deletes objects passed a time limite.
	
	Parameters:
	- objectIds -- the ids of the objects to delete
	- timeLim   -- time limit
	
	"""
	if O.time >= timeLim :		
	   	gravDepo.dead = True
	   	for idr in objectIds:
	   		O.bodies.erase(idr)
		
#############################################################################################
#############################################################################################
								           
def getMeanPos():
	"""Returns the current mean position value of the dynamic objects as a Vector3
	
	"""
	vect = Vector3(0,0,0)
	n=0.0
	for body in O.bodies :
		if body.dynamic == True :
			vect += body.state.pos
			n+=1.0
	vect /= n
	return [vect[0], vect[1], vect[2]]
	
#############################################################################################
#############################################################################################

def getMeanVel():
	"""Returns the current mean velocity value of the dynamic objects as a Vector3
	
	"""
	vect = Vector3(0,0,0)
	n=0.0
	for body in O.bodies :
		if body.dynamic == True :
			vect += body.state.vel
			n+=1.0
	vect /= n
	return [vect[0], vect[1], vect[2]]

#############################################################################################
#############################################################################################

def getMaxVel():
	"""Returns the current max velocity value of the dynamic objects as a Vector3
	
	"""
	maxVel = Vector3(0,0,0)
	for body in O.bodies :
		if body.dynamic == True and length_vector3(body.state.vel) > length_vector3(max_vel):
			maxVel = body.state.vel
	return [maxVel[0], maxVel[1], maxVel[2]]

#############################################################################################
#############################################################################################

def getMaxX():
	"""Returns the current max x position value of the dynamic objects as a float
	
	"""
	maxX = -10000000
	for body in O.bodies :
		if body.dynamic == True and body.state.pos[0] > maxX:
			maxX = body.state.pos[0]
	return maxX

#############################################################################################
#############################################################################################

def getMaxY():
	"""Returns the current max y position value of the dynamic objects as a float
	
	"""
	maxY = -10000000
	for body in O.bodies :
		if body.dynamic == True and body.state.pos[1] > maxY:
			maxY = body.state.pos[1]
	return maxY

#############################################################################################
#############################################################################################

def getForceOnObject(idObject):
	"""Returns the total current applied force on an object
	
	Parameter:
	- idObject -- The id of the object
	
	"""
	vect = Vector3(0,0,0)
	for intr in O.bodies[idObject].intrs():
		vect += intr.phys.normalForce
		vect += intr.phys.shearForce
	return [vect[0], vect[1], vect[2]]
	
#############################################################################################
#############################################################################################
	
def getNormalForceOnObject(idObject):
	"""Returns the total current applied normal force on an object
	
	Parameter:
	- idObject -- The id of the object
	
	"""
	vect = Vector3(0,0,0)
	for intr in O.bodies[idObject].intrs():
		vect += intr.phys.normalForce
	return [vect[0], vect[1], vect[2]]
	
#############################################################################################
#############################################################################################
