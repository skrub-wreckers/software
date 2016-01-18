from hal import *
import vision
from vision.window import Window
from vision import Camera, Vision
import cv2
import math
import numpy as np

import constants

from tamproxy import TAMProxy

if __name__ == "__main__":
    with TAMProxy() as tamproxy:
        drive = Drive(tamproxy)
        #arm = Arm(tamproxy, 10)
        #arm2 = Arm(tamproxy, 9)
        arms = Arms(tamproxy)

        w = Window("Vision test")
        cam = Camera(geom=constants.camera_geometry, id=2)
        v = vision.Vision(cam)
        while True:

            v.update()
            cube = v.nearest_cube()
            #print cube

            c = chr(cv2.waitKey(1) & 0xFF)
            if c == 'q':
                break

            if cube is None:
                print "No cube"
                drive.go(0, 0.05)
                
            elif abs(cube.angle_to) < np.radians(5):
                print "Cube str8 ahead", cube
                # todo: steer while moving?
                drive.go(0.2)
                time.sleep(cube.distance / 9)
                drive.go(0.1)
                time.sleep(0.1)
                drive.stop()


                arms.green.up()
                time.sleep(0.75)
                arms.green.down()
            else:
                print "Turning to cube", cube
                rtime = abs(cube.angle_to)/(math.pi*2)*4.45
                drive.turnIP(math.copysign(0.2, cube.angle_to))
                time.sleep(rtime)
                drive.stop()