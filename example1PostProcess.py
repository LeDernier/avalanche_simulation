import matplotlib.pyplot as plt

time = []
with open("time.txt","r") as f:
	for line in f:
		time.append(float(line))

meanX = []
meanY = []
meanZ = []
with open("meanPos.txt","r") as f:
	for line in f:
		vect = line.split('[')[1].split(']')[0].split(',') # Parse list
		meanX.append(float(vect[0]))
		meanY.append(float(vect[1]))
		meanZ.append(float(vect[2]))
		
plt.title("Mean position of the flow over time.")

plt.plot(time, meanX, '-o', markevery=100, label='x') # markevery is just used to show less markers
plt.plot(time, meanY, '-v', markevery=100, label='y')
plt.plot(time, meanZ, '-s', markevery=100, label='z')
plt.xlabel("time (s)")
plt.ylabel("position (m)")
plt.legend()
plt.show()

