from sw.hal import *
from sw.vision import Camera, Vision, CameraPanel
from sw.mapping import Mapper
from sw.gui import Window
import sw.constants
import sw.util
from sw import pins

import cv2

from tamproxy import TAMProxy
from tamproxy.devices import LongIR

if __name__ == "__main__":
    with TAMProxy() as tamproxy:
        drive = Drive(tamproxy)
        leftIR = LongIR(tamproxy, pins.l_ir_long)
        rightIR = LongIR(tamproxy, pins.r_ir_long)

        left_pid = sw.util.PID(0.1, setpoint=20)
        right_pid = sw.util.PID(0.1, setpoint=20)

        m = Mapper(drive.odometer)
        cam = Camera(geom=sw.constants.camera_geometry, id=0)
        v = Vision(cam)
        w = Window(500, [m,CameraPanel(500, v)])

        while True:
            try:
                v.update()
            except IOError:
                continue
            m.setCubePositions(v.cubes)

            print "Right: {:.1f}, Left:  {:.1f}".format(
                rightIR.distInches, leftIR.distInches)

            if leftIR.distInches < 14 and rightIR.distInches < 14:
                print("corner")
                drive.go(steer=0.1)
            elif rightIR.distInches < leftIR.distInches:
                left_pid.reset()
                steer = right_pid.iterate(rightIR.distInches)
                print("right {}".format(steer))
                drive.go(0.1, sw.util.clamp(steer, -0.2, 0.2))
            else:
                right_pid.reset()
                steer = left_pid.iterate(leftIR.distInches)
                print("left {}".format(steer))
                drive.go(0.1, sw.util.clamp(-steer, -0.2, 0.2))

            time.sleep(0.05)

