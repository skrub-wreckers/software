import numpy as np
import matplotlib.pyplot as plt

fix, axs = plt.subplots(3, 2)

for i, cname in enumerate(['none', 'red', 'green']):
    try:
        bb = np.load('bb-{}.npy'.format(cname))
        color = np.load('{}.npy'.format(cname))
    except:
        continue

    ax1, ax2 = axs[i,:]

    ax1.plot(bb[:,0], label='Left')
    ax1.plot(bb[:,1], label='Right')
    ax1.set(ylim=[0, 65536], title='Breakbeams')


    ax2.plot(color[:,0], color='r', label='R')
    ax2.plot(color[:,1], color='g', label='G')
    ax2.plot(color[:,2], color='b', label='B')
    ax2.plot(color[:,3], color='k', label='C')
    ax2.set(title='Color sensor', ylim=[0, 1024])

plt.show()