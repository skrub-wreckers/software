from sw.hal import *
from sw.vision.window import Window
from sw.mapping import Mapper

import cv2

from tamproxy import TAMProxy

if __name__ == "__main__":
    with TAMProxy() as tamproxy:
        drive = RegulatedDrive(tamproxy)
        arms = Arms(tamproxy)

        w = Window("Control here")
        m = Mapper(drive.odometer)

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