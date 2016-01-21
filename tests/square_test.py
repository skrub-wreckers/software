from sw.hal import *
from sw.mapping import Mapper

import cv2

from tamproxy import TAMProxy

if __name__ == "__main__":
    with TAMProxy() as tamproxy:
        drive = RegulatedDrive(tamproxy)

        m = Mapper(drive.odometer)

        while True:
            print 'A'
            drive.go_to([24,0])
            print 'B'
            drive.go_to([24,24])
            print 'C'
            drive.go_to([0,24])
            print 'D'
            drive.go_to([0,0])