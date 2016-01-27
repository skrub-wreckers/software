import tamproxy, tamproxy.devices
import numpy as np
import time
from math import pi

from sw.hal import Robot
from sw.gui import Window, ControlPanel

import cv2

""" Make sure the robot has enough clearance to release blocks """

CLOSE_TO_WALL = 13

if __name__ == '__main__':
    with tamproxy.TAMProxy() as tamp:
        r = Robot(tamp)
        w = Window(500, [ControlPanel(r)])
        r.arms.silo_door.write(0)

        # If went all the way around without finding anything, pick the best direction 
        # = combine with side sensors and knowing angles
        
        # Turn around until the front of the robot is clear for N inches or it has gone 360
        print r.left_long_ir.distInches, r.right_long_ir.distInches
        while r.left_long_ir.distInches >= CLOSE_TO_WALL and r.right_long_ir.distInches >= CLOSE_TO_WALL:
            print r.left_long_ir.distInches, r.right_long_ir.distInches
            r.drive.go(0, 0.1)

        r.drive.go(0, 0)

        # r.arms.silo_door.write(180)
        # time.sleep(0.5)
        # r.drive.go_distance(6)
