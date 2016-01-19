import pins
from tamproxy.devices import Odometer
from tamproxy.devices import Gyro
from tamproxy.devices import Encoder
from tamproxy import TAMProxy

import time
import cv2
import numpy as np
import math

if __name__ == "__main__":
    cv2.namedWindow("test")

    tamp = TAMProxy()
    gyro = Gyro(tamp, pins.gyro_cs, integrate=False)
    lEnc = Encoder(tamp, pins.l_encoder_a, pins.l_encoder_b, continuous = False)
    rEnc = Encoder(tamp, pins.r_encoder_a, pins.r_encoder_b, continuous = False)
    odo = Odometer(tamp, lEnc, rEnc, gyro, 0.0)
    
    while True:
        odo.update()
        lEnc.update()
        rEnc.update()
        print odo.val
        print lEnc.val
        print rEnc.val
        
        surf = np.ones((500,500,3))
        
        pos = (int(250*(odo.val.x/20.0))+250, -int(250*(odo.val.y/20.0))+250)
        cv2.line(surf, pos, (pos[0]+int(20*math.cos(odo.val.theta)), pos[1]-int(20*math.sin(odo.val.theta))), (0,0,0))
        cv2.circle(surf, pos, 5, (0,0,0))
        
        cv2.imshow("test", surf)
        
        time.sleep(0.05)
        
        c = chr(cv2.waitKey(1) & 0xFF)
        if c == 'q':
            break