from sw.hal import *
from sw.vision.window import Window
from sw.vision import Camera, Vision
from sw.mapping import Mapper

import cv2

from tamproxy import TAMProxy

if __name__ == "__main__":
    with TAMProxy() as tamproxy:
        drive = Drive(tamproxy)
        arms = Arms(tamproxy)

        w = Window("Control here")
        m = Mapper(drive.odometer)
        cam = Camera(geom=constants.camera_geometry, id=0)
        v = Vision(cam)

        while True:
            try:
                v.update()
            except IOError:
                continue
            m.setCubePositions(v.cubes)
        
            c = chr(cv2.waitKey(1) & 0xFF)
            move_cmd = None

            if c == 'q':
                break
            elif c == 'w':
                drive.turn_angle(0)