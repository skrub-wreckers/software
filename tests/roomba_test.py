from sw.hal import *
from sw.vision import Camera, Vision, CameraPanel
from sw.mapping import Mapper
from sw.gui import Window
import sw.constants

import cv2

from tamproxy import TAMProxy
from tamproxy.devices import LongIR, ShortIR

if __name__ == "__main__":
    with TAMProxy() as tamproxy:
        drive = Drive(tamproxy)
        frontIR = LongIR(tamproxy, 4)
        rightIR = ShortIR(tamproxy, 5)
        
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

            drive.go(0.2, -1*(rightIR.distInches-10))
            
            while frontIR.distInches < 10:
                drive.turnAngle(-10)


            """if c == 'q':
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
                arms.green.up()
                time.sleep(0.75)
                arms.green.down()

            elif c == 'c':
                arms.red.up()
                time.sleep(0.9)
                arms.red.down()

            if move_cmd:
                drive.l_enc.update()
                drive.r_enc.update()
                drive.go(*move_cmd)
                time.sleep(0.25)
                drive.stop()
                print drive.l_enc.val, drive.r_enc.val"""