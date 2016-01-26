from sw.vision import Camera, Vision, Colors, CameraPanel
from sw.gui import Window
import sw.constants as constants
from sw.mapping import Mapper
import time
from tamproxy import TAMProxy
from sw.hal import Robot

if __name__ == "__main__":
    with TAMProxy() as tamproxy:
        r = Robot(tamproxy)

        m = Mapper(r.drive.odometer)
        cam = Camera(geom=constants.camera_geometry, id=1)
        v = Vision(cam)
        w = Window(500, [m, CameraPanel(500, v)])

        while True:
            time.sleep(0.1)
            print "Long Left IR ", r.left_long_ir.distInches, " Long Right IR ", r.right_long_ir.distInches
            print "Left Short IR ", r.left_short_ir.val, " Right Short IR ", r.right_short_ir.val, " Back Short IR ", r.back_short_ir.val
            print