import time
import math
import csv

from tamproxy import TAMProxy
import cv2
import numpy as np
from Queue import Empty

from sw.mapping import Mapper
from sw.hal import Drive
from sw.gui import Window

def to_cv(val):
    """ np array to integer tuple """
    try:
        l = len(val)
    except Exception:
        return int(val)
    else:
        return tuple(val.astype(int))

if __name__ == "__main__":

    with TAMProxy() as tamp:
        d = Drive(tamp)
        odo = d.odometer
        mapper = Mapper(odo, size=500, ppi=250.0/20)

        w = Window(500, [mapper])

        with open('odo.csv', 'w') as logfile:
            logwriter = csv.writer(logfile)
            logwriter.writerow(('t',) + odo.Reading._fields)

            while True:
                # print time.time(), odo.val
                logwriter.writerow((time.time(),) + odo.val)

                c = w.get_key()
                if c == 'r':
                    odo.override_position(12, 12, np.pi / 8)
                elif c == 'q':
                    break