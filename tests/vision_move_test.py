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
        
        drive = RegulatedDrive(tamproxy)
        #arm = Arm(tamproxy, 10)
        #arm2 = Arm(tamproxy, 9)
        arms = Arms(tamproxy)

        color = ColorSensor(tamproxy)
        
        m = Mapper(drive.odometer)
        cam = Camera(geom=constants.camera_geometry, id=1)
        v = Vision(cam)
        w = Window(500, [m, CameraPanel(500, v)])

        def pick_up_cubes():
            while True:
                val = color.val
                if val == Colors.GREEN:
                    drive.stop()
                    arms.green.up()
                    time.sleep(1.0)
                    arms.green.down()
                elif val == Colors.RED:
                    drive.stop()
                    arms.red.up()
                    time.sleep(0.75)
                    arms.red.down()
                else:
                    break

        while True:
            # pick up any cubes we have
            pick_up_cubes()

            try:
                v.update()
            except IOError:
                continue
            m.setCubePositions(v.cubes)
            cube = v.nearest_cube()
            #print cube

            if cube is None:
                print "No cube"
                drive.go(0, 0.1)
            elif abs(cube.angle_to) < np.radians(10):
                print "Going {}in to {}".format(cube.distance, cube)
                to_go = cube.pos2
                if cube.distance > 60:
                    to_go = cube.pos2 * 60 / cube.distance

                to_go = np.append(to_go, 1)
                dest = drive.odometer.robot_matrix.dot(to_go)

                drive.go_to(dest[:2])
                pick_up_cubes()
            else:
                print "Turning {} to {}".format(cube.angle_to, cube)
                drive.turn_angle(cube.angle_to)