from sw.hal import *
from sw.gui import Window, ControlPanel
from sw.vision import Camera, Vision, CameraPanel
from sw.mapping import Mapper
from sw import constants
import time

import cv2

from tamproxy import TAMProxy

if __name__ == "__main__":
    with TAMProxy() as tamproxy:
        r = Robot(tamproxy)

        m = Mapper(r.drive.odometer)
        cam = Camera(geom=constants.camera_geometry, id=2)
        v = Vision(cam)
        w = Window(500, [m, CameraPanel(v), ControlPanel(r)])

        while True:
            try:
                v.update()
            except IOError:
                continue
            m.update_cubes_from(v)

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
                r.arms.silo.up()
                r.arms.silo.down()

            elif c == 'c':
                r.arms.dump.up()
                r.arms.dump.down()

            elif c == 'v':
                r.silo.open()
            elif c == 'b':
                r.silo.close()

            if move_cmd:
                r.drive.go(*move_cmd)
                time.sleep(0.25)
                r.drive.stop()
                print r.drive.l_enc.val, r.drive.r_enc.val