import numpy as np
import matplotlib.pyplot as plt

from sw.hal import ColorSensor

fix, axs = plt.subplots(3, 3)
# fig2, axs2 = plt.subplots(3, 2)

bbs = {}
colors = {}

for i, cname in enumerate(['none', 'red', 'green']):
    try:
        bb = np.load('bb-{}.npy'.format(cname))
        color = np.load('{}.npy'.format(cname))
    except:
        continue

    bbs[cname] = bb
    colors[cname] = color

    ax1, ax2, ax3 = axs[i,:]

    ax1.plot(bb[:,0], label='Left')
    ax1.plot(bb[:,1], label='Right')
    ax1.legend()
    ax1.set(ylim=[0, 32768], title='Breakbeams ({})'.format(cname))
    ax1.grid()


    ax2.plot(color[:,0], color='r', label='R')
    ax2.plot(color[:,1], color='g', label='G')
    ax2.plot(color[:,2], color='b', label='B')
    ax2.plot(color[:,3], color='k', label='C')
    ax2.legend()
    ax2.set(title='Color sensor ({})'.format(cname), ylim=[0, 1024])

    p = ColorSensor.project(color)
    ax3.plot(p[:,0], label='0')
    ax3.plot(p[:,1], label='1')
    ax3.legend()

    # ax1, ax2 = axs2[i,:]

all_colors = 

plt.show()