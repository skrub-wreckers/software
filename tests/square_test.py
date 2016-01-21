from sw.hal import *
from sw.mapping import Mapper

import cv2

from tamproxy import TAMProxy

if __name__ == "__main__":
    with TAMProxy() as tamproxy:
        drive = RegulatedDrive(tamproxy)

        m = Mapper(drive.odometer)

        while True:
            drive.go_to([24,0])
            drive.go_to([24,24])
            drive.go_to([0,24])
            drive.go_to([0,0])