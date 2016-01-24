from sw.hal import *
from sw.gui import Window
from sw.vision import Camera, Vision, CameraPanel
from sw.mapping import Mapper
from sw import constants
import time

import cv2

from tamproxy import TAMProxy

if __name__ == "__main__":
    with TAMProxy() as tamproxy:
        drive = Drive(tamproxy)
        #arm = Arm(tamproxy, 10)
        #arm2 = Arm(tamproxy, 9)
        arms = Arms(tamproxy)

        m = Mapper(drive.odometer)
        cam = Camera(geom=constants.camera_geometry, id=0)
        v = Vision(cam)
        w = Window(500, [m, CameraPanel(500, v)])
        
        while True:
            try:
                v.update()
            except IOError:
                continue
            m.setCubePositions(v.cubes)
        
            c = w.get_key()
            move_cmd = None
            

            if c == 'q':
                break
            elif c == 'w':
                move_cmd = (0.2, 0)

            elif c == 's':
                move_cmd = (-0.2, 0)

            elif c == 'a':
                move_cmd = (0, 0.2)

            elif c == 'd':
                move_cmd = (0, -0.2)

            elif c == ' ':
                arms.green.up()
                time.sleep(1)
                arms.green.down()

            elif c == 'c':
                arms.red.up()
                time.sleep(0.9)
                arms.red.down()

            if move_cmd:
                drive.go(*move_cmd)
                time.sleep(0.25)
                drive.stop()
                print drive.l_enc.val, drive.r_enc.val