from sw.hal import *
from sw.mapping import Mapper
from sw.gui import Window

import numpy as np

from tamproxy import TAMProxy

if __name__ == "__main__":
    with TAMProxy() as tamproxy:
        drive = RegulatedDrive(tamproxy)
        arms = Arms(tamproxy)

        m = Mapper(drive.odometer)
        w = Window(500, [m])
        t = None

        while True:
            c = w.get_key()

            if c == 'q':
                break
            elif c == 'w':
                t = drive.turn_to(0, async=True)
            elif c == 'e':
                t = drive.go_to([24,0], async=True)
            elif c == 'd':
                t = drive.turn_to(np.pi, async=True)
            elif c == 's':
                t = drive.go_to([0,0], async=True)
            elif c == ' ' and t:
                t.cancel()

            if t and t.wait(0):
                t = None