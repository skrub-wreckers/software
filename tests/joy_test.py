from sw.hal import *
from sw.gui import Window, ControlPanel, JoystickInterface
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
        j = JoystickInterface()

        while True:
            try:
                v.update()
            except IOError:
                continue
            m.update_cubes_from(v)

            j.set_bumpers(r.left_bumper.val, r.right_bumper.val)

            if j.left_arm:
                r.drive.stop()
                r.arms.silo.up()
                while j.left_arm: pass
                r.arms.silo.down()

            elif j.right_arm:
                r.drive.stop()
                r.arms.dump.up()
                while j.right_arm: pass
                r.arms.dump.down()

            elif j.open_silo:
                r.silo.open()

            elif j.close_silo:
                r.silo.close()

            else:
                throttle, steer = j.move_cmd
                r.drive.go(throttle * 0.25, steer * 0.25)