import pins
from tamproxy.devices import Odometer
from tamproxy.devices import Gyro
from tamproxy.devices import Encoder
from tamproxy import TAMProxy

import time

if __name__ == "__main__":
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
        time.sleep(0.05)