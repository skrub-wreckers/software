import time
import tamproxy
from sw import hal
from sw import pins
import numpy as np

import matplotlib.pyplot as plt

if __name__ == '__main__':
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # some X and Y data
    x = np.ones(200) * float('nan')
    y = np.zeros(200)
    li, = ax.plot(x, y)

    # draw and show it
    fig.canvas.draw()
    plt.show(block=False)
    plt.ion()

    with tamproxy.TAMProxy() as tamp:
        sensor_l = hal.DigitalIR(tamp, pins.l_ir_short)
        sensor_r = hal.DigitalIR(tamp, pins.r_ir_short)
        sensor_b = hal.DigitalIR(tamp, pins.back_ir_short)
        sensors = [sensor_l, sensor_r]

        while True:
            readings = [s.val for s in sensors]
            if np.any(readings):
                print "seen!", readings

            time.sleep(0.05)