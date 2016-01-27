import tamproxy, tamproxy.devices
import numpy as np

from sw.hal import Robot
from sw.gui import Window, ControlPanel

import cv2

""" Make sure the robot has enough clearance to release blocks """

if __name__ == '__main__':
    with tamproxy.TAMProxy() as tamp:
        r = Robot(tamp)
        w = Window(500, ControlPanel(r))
        r.arm.silo_door.write(0)

        while w.get_key() != ' ':
            print r.left_long_ir, r.right_long_ir

        # Turn around until the front of the robot is clear for N inches
        # If we turn 
        # Then, open the doors and drive N inches forwards

        r.arms.silo_door.write(180)
        time.sleep(0.5)
        Drive.go_distance(r.drive, 6)
