import matplotlib.pyplot as plt
import numpy as np

colors = [
	('red', 'r'),
	('green', 'g'),
	('none', 'k')
]

dims = ['R', 'G', 'B','C']

fig, plts = plt.subplots(4,4, sharex='col', sharey='row')

all_data = {}

for cname, mplname in colors:
    data = np.load(cname + '.npy')
    all_data[cname] = data

    mean = np.mean(data, axis=0)


    for i in range(4):
        for j in range(4):
            if i < j:
                plts[j, i].scatter(data[:,i], data[:,j], color=mplname)
                plts[j, i].grid()


    for i in range(4):
        plts[-1, i].set(xlabel=dims[i])

    for j in range(4):
        plts[j, 0].set(ylabel=dims[j])


import matplotlib.mlab

all_data_vals = np.concatenate(all_data.values())

origin = np.mean(all_data['none'], axis=0)

scale = np.max(np.sum((all_data_vals - origin)*(all_data_vals - origin), axis=-1))




U, s, Vh = np.linalg.svd(all_data_vals - origin, full_matrices=False)
flatten = Vh[:2,:] / np.sqrt(scale)

fig, ax = plt.subplots(1, 1)

for cname, mplname in colors:
    # res = pca.project(all_data[cname])
    res = (all_data[cname] - origin).dot(flatten.T)


    ax.scatter(res[:,0], res[:,1], color=mplname)

print 'ORIGIN = {!r}'.format(origin)
print 'WEIGHTS = {!r}'.format(flatten)

plt.show()