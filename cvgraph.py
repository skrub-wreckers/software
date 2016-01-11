#! python2

import numpy as np
import scipy as sc
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pickle
import scipy.spatial
import scipy.io


red = np.load("red.npy")
green = np.load("green.npy")
blue = np.load("blue.npy")

with open('data.mat', 'wb') as f:
	scipy.io.savemat(f, dict(red=red, green=green, blue=blue))

# discretize the image

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set(xlabel='R', ylabel='G', zlabel='B', xlim=[0, 255], ylim=[0, 255], zlim=[0, 255])
if False:
	rHull = scipy.spatial.ConvexHull(red)
	gHull = scipy.spatial.ConvexHull(green)
	bHull = scipy.spatial.ConvexHull(blue)

	ax.plot_trisurf(red[:, 0], red[:, 1], red[:, 2],triangles=rHull.simplices, color='red')
	ax.plot_trisurf(green[:, 0], green[:, 1], green[:, 2],triangles=gHull.simplices, color='green')
	ax.plot_trisurf(blue[:, 0], blue[:, 1], blue[:, 2],triangles=bHull.simplices, color='blue')
else:
	red   = (red // 4) * 4 + 2
	green = (green // 4) * 4 + 2
	blue = (blue // 4) * 4 + 2
	
	red   = np.vstack({tuple(row) for row in red})
	green = np.vstack({tuple(row) for row in green})
	blue = np.vstack({tuple(row) for row in blue})

	with open('data-trunc.mat', 'wb') as f:
		scipy.io.savemat(f, dict(red=red, green=green, blue=blue))

	ax.scatter(red[:, 0], red[:, 1], red[:, 2], marker='x', c='red')
	ax.scatter(green[:, 0], green[:, 1], green[:, 2], marker='x', c='green')
	ax.scatter(blue[:, 0], blue[:, 1], blue[:, 2], marker='x', c='blue')

	r, g = np.mgrid[0:3,0:3]*255
	b = r / 1.3

	#ax.plot_surface(r,g,b, color='blue')

	r = np.array([[0, 1], [0, 1]]) * 255
	g = r / 1.3
	b = np.array([[0, 0], [1, 1]]) * 255

	#ax.plot_surface(r,g,b,  color='green')


plt.show()

