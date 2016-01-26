import tamproxy, tamproxy.devices
import time
from sw import pins
import numpy as np

from sw.vision import Colors
from sw.hal import Robot

import cv2

""" Test the breakbeam stuff """

if __name__ == '__main__':
    with tamproxy.TAMProxy() as tamp:
        r = Robot(tamp)
        print("init")

        while True:
            dir = r.break_beams.dir
            c = r.color_sensor.val
            if c != Colors.NONE:
                print "Saw {} cube".format(c)
                r.arms.silo.up()
                time.sleep(1)
                r.arms.silo.down()
            if dir is None:
                print "No beams broken"
            elif dir == 0:
                print "both broken"
            else:
                print "wiggling {}".format(dir)
                r.drive.go(steer=-dir*0.4)
                time.sleep(0.05)
                r.drive.go(steer=dir*0.2)
                time.sleep(0.15)
                r.drive.stop()

            time.sleep(0.05)
