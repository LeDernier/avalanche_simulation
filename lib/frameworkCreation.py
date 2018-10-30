
#########################################################################################################################################################################
# Author : Remi Monthiller, remi.monthiller@etu.enseeiht.fr
# Adapted from the code of Raphael Maurin, raphael.maurin@imft.fr
# 30/10/2018
#
# Incline plane simulations
#
#########################################################################################################################################################################

from yade import pack

#############################################################################################
#############################################################################################

def createGround():
	"""Creates a big square ground and returns its id in O.bodies
	
	"""
	## Create the ground plane
	groundPlane = box(center = (0.,0.,0.), extents = (200,200,0), fixed = True, wire = False, color = (0.,1.,0.), material = 'Mat') # Flat bottom plane
	## Add the planes to the simulation
	O.bodies.append(groundPlane) # add the three planes to the simulation

#############################################################################################
#############################################################################################

def createChannel(widthChannel, lengthChannel, heightChannel, slopeChannel):
	"""Creates a channel and returns [idBottom, idLeftWall, idRightWall], the ids of the objects created in O.bodies
	
	Parameters:
	- widthChannel  -- width of the channel.
	- lengthChannel -- length of the channel.
	- heightChannel -- height of the channel.
	- slopeChannel  -- slope of the channel.
	
	"""
	# Create planes with boxes :
	
	## Create the bottom plane of the channel
	bottomPlane = box(center = (-lengthChannel * cos(slopeChannel)/2, widthChannel/2, lengthChannel/2 * sin(slopeChannel)), extents = (lengthChannel/2,widthChannel/2,0), orientation = ((0, 1, 0), slopeChannel), fixed = True, wire = False, color = (0.5,0.5,0.5), material = 'Mat')
	
	leftPlane = box(center = (-lengthChannel * cos(slopeChannel)/2 + heightChannel/2 * sin(slopeChannel), 0, lengthChannel/2 * sin(slopeChannel) + heightChannel/2 * cos(slopeChannel)), extents = (lengthChannel/2, 0, heightChannel/2), orientation = ((0, 1, 0), slopeChannel), fixed = True, wire = True, color = (0.3,0.3,0.3), material = 'Mat')
	
	rightPlane = box(center = (-lengthChannel * cos(slopeChannel)/2 + heightChannel/2 * sin(slopeChannel), widthChannel, lengthChannel/2 * sin(slopeChannel) + heightChannel/2 * cos(slopeChannel)), extents = (lengthChannel/2, 0, heightChannel/2), orientation = ((0, 1, 0), slopeChannel), fixed = True, wire = False, color = (0.3,0.3,0.3), material = 'Mat')
	
	## Add the planes to the simulation
	return O.bodies.append([bottomPlane, leftPlane, rightPlane])
	
#############################################################################################
#############################################################################################
	
def createRugosity(diameterPart, widthChannel, lengthChannel, slopeChannel):
	"""Creates a layer of regulary spaced spheres at the bottom of the channel simulating rugosity.
	
	Be careful, it increases a lot the computation cost.
	
	Parameters:
	- diameterPart  -- diameter of the spheres, the 'length' of the rugosity
	- widthChannel  -- width of the channel.
	- lengthChannel -- length of the channel.
	- heightChannel -- height of the channel.
	- slopeChannel  -- slope of the channel.
	
	"""
	L = np.linspace(0, lengthChannel, int(lengthChannel/diameterPart))
	W = np.linspace(0, widthChannel, int(lengthChannel/diameterPart))
	for x in L: #loop creating a set of sphere sticked at the bottom with a (uniform) random altitude comprised between 0.5 (diameter/12) and 5.5mm (11diameter/12) with steps of 0.5mm. The repartition along z is made around groundPosition.
		for y in W:
			O.bodies.append(sphere((-x * cos(slopeChannel), y, x * sin(slopeChannel)), diameterPart / 2., color = (0.3, 0.3, 0.3), fixed = True, material = 'Mat'))
			
#############################################################################################
#############################################################################################
			
def createPartBox(widthBox, lengthBox, heightBox, widthChannel, lengthChannel, slopeChannel):
	"""Creates a box at the top of the channel and returns [idBackPlane, idFrontPlane, idLeftPlane, idRightPlane], the ids of the objects created in O.bodies
	
	Parameters:
	- widthBox  -- width of the box.
	- lengthBox -- length of the box.
	- heightBox -- height of the box.
	- widthChannel  -- width of the channel.
	- lengthChannel -- length of the channel.
	- heightChannel -- height of the channel.
	- slopeChannel  -- slope of the channel.
	
	"""
	X = -lengthChannel * cos(slopeChannel)
	W = widthBox
	Y = (widthChannel - W)/2
	Z = lengthChannel * sin(slopeChannel) - tan(slopeChannel) * W/2
	H = heightBox + tan(slopeChannel) * W
	L = lengthBox
	
	backPlane = box(center = (X, Y + W/2, Z + H/2), extents = (0, W/2, H/2), fixed = True, wire = False, color = (1.,0.,0.), material = 'Mat') # Flat bottom plane
	
	frontPlane = box(center = (X + L, Y + W/2, Z + H/2), extents = (0, W/2, H/2), fixed = True, wire = False, color = (1.,0.,0.), material = 'Mat') # Flat bottom plane
	
	leftPlane = box(center = (X + L/2, Y, Z + H/2), extents = (L/2, 0, H/2), fixed = True, wire = False, color = (1.,0.,0.), material = 'Mat') # Flat bottom plane
	
	rightPlane = box(center = (X + L/2, Y + W, Z + H/2), extents = (L/2, 0, H/2), fixed = True, wire = False, color = (1.,0.,0.), material = 'Mat') # Flat bottom plane
	
	return O.bodies.append([backPlane, frontPlane, leftPlane, rightPlane])
	
#############################################################################################
#############################################################################################

def createPartCloud(widthBox, lengthBox, heightBox, widthChannel, lengthChannel, slopeChannel, diameterPart, number):
	"""Creates a particules cloud in a box at the top of the channel.
	
	Parameters:
	- widthBox      -- width of the box.
	- lengthBox     -- length of the box.
	- heightBox     -- height of the box.
	- widthChannel  -- width of the channel.
	- lengthChannel -- length of the channel.
	- heightChannel -- height of the channel.
	- slopeChannel  -- slope of the channel.
	- diameterPart  -- diameter of the spheres
	- number        -- number of particles
	
	"""
	X = -lengthChannel * cos(slopeChannel)
	W = widthBox
	Y = (widthChannel - W)/2
	Z = lengthChannel * sin(slopeChannel)
	H = heightBox
	L = lengthBox
	
	#Create the particle cloud
	partCloud = pack.SpherePack()
	partCloud.makeCloud(minCorner=(X,Y,Z),maxCorner=(X+L, Y+W, Z+H), rRelFuzz=0., rMean=diameterPart/2.0, num = number)
	partCloud.toSimulation(material='Mat') #Send this packing to simulation with material Mat
	
#############################################################################################
#############################################################################################
	
def createHouse(positionCoef, angle, widthHouse, lengthHouse, heightHouse, widthChannel, lengthChannel, slopeChannel):
	"""Creates a house and returns idHouse, the id of the object created in O.bodies
	
	Parameters:
	- positionCoef  -- position of the house along the channel, means at the top and 0 at the bottom.
	- angle         -- vertical angle of the house.
	- widthHouse    -- width of the house.
	- lengthHouse   -- length of the house.
	- heightHouse   -- height of the house.
	- widthChannel  -- width of the channel.
	- lengthChannel -- length of the channel.
	- heightChannel -- height of the channel.
	- slopeChannel  -- slope of the channel.
	
	"""
	X = widthHouse/2 - lengthChannel*cos(slopeChannel) * positionCoef
	Y = widthChannel / 2
	Z = lengthChannel * positionCoef * sin(slopeChannel) + heightHouse/2 * cos(slopeChannel) - widthHouse * sin(slopeChannel)
	
	house = box(center=(X, Y, Z),orientation=((0,0,1),angle),extents = (widthHouse/2, lengthHouse/2, heightHouse/2), fixed=True, wire=False,color=(1.,0.,0.), material = 'Mat')
	
	return O.bodies.append(house)
	
#############################################################################################
#############################################################################################
