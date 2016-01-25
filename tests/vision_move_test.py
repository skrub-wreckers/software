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


OUR_COLOR = Colors.RED
THEIR_COLOR = (Colors.RED | Colors.GREEN) & ~OUR_COLOR

if __name__ == "__main__":
    with TAMProxy() as tamproxy:
        r = Robot(tamproxy)

        m = Mapper(r.drive.odometer)
        cam = Camera(geom=constants.camera_geometry, id=1)
        v = Vision(cam)
        w = Window(500, [m, CameraPanel(500, v)])

        def pick_up_cubes():
            while True:
                val = r.color.val
                if val == OUR_COLOR:
                    r.drive.stop()
                    r.arms.silo.up()
                    time.sleep(1.0)
                    r.arms.silo.down()
                elif val == THEIR_COLOR:
                    r.drive.stop()
                    r.arms.dump.up()
                    time.sleep(0.75)
                    r.arms.dump.down()
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
                r.drive.go(0, 0.1)
            elif abs(cube.angle_to) < np.radians(10):
                print "Going {}in to {}".format(cube.distance, cube)
                to_go = cube.pos2
                if cube.distance > 60:
                    to_go = cube.pos2 * 60 / cube.distance

                to_go = np.append(to_go, 1)
                dest = r.drive.odometer.robot_matrix.dot(to_go)

                r.drive.go_to(dest[:2])
                pick_up_cubes()
            else:
                print "Turning {} to {}".format(cube.angle_to, cube)
                r.drive.turn_angle(cube.angle_to)