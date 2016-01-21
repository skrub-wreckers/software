from sw.hal import *
from sw.mapping import Mapper
from sw.gui import Window

import numpy as np

from tamproxy import TAMProxy

if __name__ == "__main__":
    with TAMProxy() as tamproxy:
        drive = RegulatedDrive(tamproxy)

        m = Mapper(drive.odometer)
        w = Window(500, [m])
        while True:
            print 'A'
            drive.turn_to(0)
            drive.go_to([24,0])

            print 'B'
            drive.turn_to(np.pi * 0.5)
            drive.go_to([24,24])

            print 'C'
            drive.turn_to(np.pi)
            drive.go_to([0,24])

            print 'D'
            drive.turn_to(np.pi * 1.5)
            drive.go_to([0,0])