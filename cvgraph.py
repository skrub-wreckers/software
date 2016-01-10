import numpy as np
import scipy as sc
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pickle
import scipy.spatial

with open("red.dat") as f:
	red = pickle.load(f)
with open("green.dat") as f:
	green = pickle.load(f)
	
rHull = scipy.spatial.ConvexHull(red)
gHull = scipy.spatial.ConvexHull(green)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(red[:, 0], red[:, 1], red[:, 2],triangles=rHull.simplices, color='red')
ax.plot_trisurf(green[:, 0], green[:, 1], green[:, 2],triangles=gHull.simplices, color='green')
ax.set(xlabel='R', ylabel='G', zlabel='B', xlim=[0, 255], ylim=[0, 255], zlim=[0, 255])
plt.show()

