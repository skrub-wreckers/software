import cv2
import numpy as np
from tamproxy import TAMProxy

from sw.hal import *
from sw.vision.window import Window
from sw.vision import Camera, Vision, Colors
import sw.constants as constants


if __name__ == "__main__":
    with TAMProxy() as tamproxy:
        drive = Drive(tamproxy)
        #arm = Arm(tamproxy, 10)
        #arm2 = Arm(tamproxy, 9)
        arms = Arms(tamproxy)

        cam = Camera(geom=constants.camera_geometry, id=2)
        v = Vision(cam)
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
                drive.go(0, 0.1)
            elif abs(cube.angle_to) < np.radians(3):
                print "Going {}in to {}".format(cube.distance, cube)
                if cube.distance > 60:
                    drive.go_distance(60)
                else:
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
                print "Turning {} to {}".format(cube.angle_to, cube)
                drive.turn_angle(cube.angle_to)