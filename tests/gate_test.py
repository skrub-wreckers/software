from tamproxy.devices import *
from tamproxy import TAMProxy
import time
from sw.gui import Window
from sw import pins
from sw.hal.sensors import BreakBeams

if __name__ == "__main__":
    with TAMProxy() as tamp:
        
        w = Window(500, [])

        b = BreakBeams(tamp)

        while True:
            print b.blocked
            time.sleep(0.1)