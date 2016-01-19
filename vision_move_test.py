from hal import *
import vision
from vision.window import Window
from vision import Camera, Vision, Colors
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

        cam = Camera(geom=constants.camera_geometry, id=2)
        v = vision.Vision(cam)
        while True:
            try:
                v.update()
            except IOError:
                continue
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
                drive.go_distance(cube.distance + 1)

                if cube.color == Colors.GREEN:
                    arms.green.up()
                    time.sleep(0.75)
                    arms.green.down()
                elif cube.color == Colors.RED:
                    arms.red.up()
                    time.sleep(0.75)
                    arms.red.down()
            else:
                print "Turning to cube", cube
                print cube.angle_to
                drive.turn_angle(cube.angle_to)