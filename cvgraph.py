#! python2

import numpy as np
import scipy as sc
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pickle
import scipy.spatial
import scipy.io


colors = ['red', 'green', 'blue', 'black', 'white']

color_data = {
	c: np.load('{}.npy'.format(c)) for c in colors
}

with open('data.mat', 'wb') as f:
	scipy.io.savemat(f, color_data)

# discretize the image

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set(xlabel='R', ylabel='G', zlabel='B', xlim=[0, 255], ylim=[0, 255], zlim=[0, 255])
if False:
	for c in colors:
		data = color_data[c]
		hull = scipy.spatial.ConvexHull(data)
		ax.plot_trisurf(data[:, 0], data[:, 1], data[:, 2],triangles=hull.simplices, color=c)
else:
	for c in colors:
		data = color_data[c]
		data = (data // 8) * 8 + 4
		data = np.vstack({tuple(row) for row in data})
		color_data[c] = data

	with open('data-trunc.mat', 'wb') as f:
		scipy.io.savemat(f, color_data)

	for c in colors:
		data = color_data[c]
		ax.scatter(data[:, 0], data[:, 1], data[:, 2], marker='x', c=c)

	r, g = np.mgrid[0:3,0:3]*255
	b = r / 1.3

	#ax.plot_surface(r,g,b, color='blue')

	r = np.array([[0, 1], [0, 1]]) * 255
	g = r / 1.3
	b = np.array([[0, 0], [1, 1]]) * 255

	#ax.plot_surface(r,g,b,  color='green')


plt.show()

