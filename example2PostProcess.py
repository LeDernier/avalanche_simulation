import mayavi.mlab as m

time = []
with open("time.txt","r") as f:
	for line in f:
		time.append(float(line))

forceX = []
forceY = []
forceZ = []

originX = []
originY = []
originZ = []

i = 0
with open("forceOnObject.txt","r") as f:
	for line in f:
		vect = line.split('[')[1].split(']')[0].split(',') # Parse list
		
		forceX.append(float(vect[0]))
		forceY.append(float(vect[1]))
		forceZ.append(float(vect[2]))
		
		originX.append(0.0)
		originY.append(time[i])
		originZ.append(0.0)
		
		i += 1

m.quiver3d(originX, originY, originZ, forceX, forceY, forceZ)

# m.title('Force applied on the house over time')
m.vectorbar(orientation='vertical')
m.ylabel('time (s)')
m.axes()

m.show()
