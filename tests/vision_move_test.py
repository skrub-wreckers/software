import cv2
import numpy as np
from tamproxy import TAMProxy

from sw.hal import *
from sw.vision.window import Window
from sw.vision import Camera, Vision, Colors, CameraPanel
from sw.gui import Window
import sw.constants as constants
from sw.mapping import Mapper
import time

if __name__ == "__main__":
    with TAMProxy() as tamproxy:
        
        drive = Drive(tamproxy)
        #arm = Arm(tamproxy, 10)
        #arm2 = Arm(tamproxy, 9)
        arms = Arms(tamproxy)

        color = ColorSensor(tamproxy)
        
        m = Mapper(drive.odometer)
        cam = Camera(geom=constants.camera_geometry, id=1)
        v = Vision(cam)
        w = Window(500, [m, CameraPanel(500, v)])
        
        while True:
            try:
                v.update()
            except IOError:
                continue
            cube = v.nearest_cube()
            #print cube

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
                    val = color.val
                    if val == Colors.GREEN:
                        arms.green.up()
                        time.sleep(1.0)
                        arms.green.down()
                    elif val == Colors.RED:
                        arms.red.up()
                        time.sleep(0.75)
                        arms.red.down()
            else:
                print "Turning {} to {}".format(cube.angle_to, cube)
                drive.turn_angle(cube.angle_to)