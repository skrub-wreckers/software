import time
import math
import csv

from tamproxy.devices import Odometer
from tamproxy.devices import Gyro
from tamproxy.devices import Encoder
from tamproxy import TAMProxy
import cv2
import numpy as np

import sw.pins
from sw.mapping import Mapper

def to_cv(val):
    """ np array to integer tuple """
    try:
        l = len(val)
    except Exception:
        return int(val)
    else:
        return tuple(val.astype(int))

if __name__ == "__main__":

    tamp = TAMProxy()
    gyro = Gyro(tamp, pins.gyro_cs, integrate=False)
    lEnc = Encoder(tamp, pins.l_encoder_a, pins.l_encoder_b, continuous = False)
    rEnc = Encoder(tamp, pins.r_encoder_a, pins.r_encoder_b, continuous = False)
    odo = Odometer(tamp, lEnc, rEnc, gyro, 0.2)

    mapper = Mapper(odo, size=500, ppi=250.0/20)

    with open('odo.csv', 'w') as logfile:
        logwriter = csv.writer(logfile)
        logwriter.writerow(('t',) + odo.Reading._fields)

        while True:
            odo.update()
            lEnc.update()
            rEnc.update()
            print time.time(), odo.val
            logwriter.writerow((time.time(),) + odo.val)

            c = chr(cv2.waitKey(50) & 0xFF)
            if c == 'q':
                break