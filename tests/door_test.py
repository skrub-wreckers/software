import tamproxy, tamproxy.devices
import numpy as np
import time
from math import pi

from sw.hal import Robot
from sw.gui import Window, ControlPanel

import cv2

""" Make sure the robot has enough clearance to release blocks """

N = 20
CLOSE_TO_WALL = 13

if __name__ == '__main__':
    with tamproxy.TAMProxy() as tamp:
        r = Robot(tamp)
        w = Window(500, [ControlPanel(r)])
        r.arms.silo_door.write(0)

        # If went all the way around without finding anything, pick the best direction 
        # = combine with side sensors and knowing angles
        
        # go every 10 degrees and check out what we've got
        # Turn around until the front of the robot is clear for N inches
        for i in xrange(N):
            print r.left_long_ir.distInches, r.right_long_ir.distInches
            if r.left_long_ir.distInches >= CLOSE_TO_WALL and r.right_long_ir.distInches >= CLOSE_TO_WALL:
                break
            r.drive.turn_angle(2*pi / N)

        r.arms.silo_door.write(180)
        time.sleep(0.5)
        r.drive.go_distance(6)
