from sw.hal import *
from sw.mapping import Mapper
from sw.gui import Window

from trollius import From
import trollius as asyncio
import numpy as np

from tamproxy import TAMProxy

@asyncio.coroutine
def main_task():
    t = None
    while True:
        c = w.get_key()

        if c == 'q':
            break
        elif c == ' ':
            if t: t.cancel()
            t = asyncio.ensure_future(drive.turn_speed(np.radians(30)))
        elif c == 'w':
            if t: t.cancel()
            t = asyncio.ensure_future(drive.turn_to(0))
        elif c == 'e':
            if t: t.cancel()
            t = asyncio.ensure_future(drive.go_to([24,0]))
        elif c == 'd':
            if t: t.cancel()
            t = asyncio.ensure_future(drive.turn_to(np.pi))
        elif c == 's':
            if t: t.cancel()
            t = asyncio.ensure_future(drive.go_to([0,0]))
        elif c == ' ' and t:
            t.cancel()

        yield From(asyncio.sleep(0.05))

if __name__ == "__main__":
    with TAMProxy() as tamproxy:
        drive = RegulatedDrive(tamproxy)

        m = Mapper(drive.odometer)
        w = Window(500, [m])

        loop = asyncio.get_event_loop()
        loop.run_until_complete(main_task())
        loop.close()