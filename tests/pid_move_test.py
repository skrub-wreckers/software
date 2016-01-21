from sw.hal import *
from sw.vision.window import Window as OldWindow
from sw.mapping import Mapper
from sw.gui import Window

import cv2

from tamproxy import TAMProxy

if __name__ == "__main__":
    with TAMProxy() as tamproxy:
        drive = RegulatedDrive(tamproxy)
        arms = Arms(tamproxy)

        w = OldWindow("Control here")
        m = Mapper(drive.odometer)
        w = Window(500, [m])

        while True:
            c = chr(cv2.waitKey(1) & 0xFF)
            move_cmd = None

            if c == 'q':
                break
            elif c == 'w':
                drive.turn_to(0)
            elif c == 'e':
                drive.go_to([24,0])
            elif c == 'd':
                drive.turn_to(np.pi)
            elif c == 's':
                drive.go_to([0,0])