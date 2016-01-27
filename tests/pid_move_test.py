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

        new_t = None

        if c == 'q':
            break
        elif c == 'm':
            new_t = drive.turn_speed(np.radians(5))
        elif c == 'w':
            new_t = drive.turn_to(0)
        elif c == 'e':
            new_t = drive.go_to([24,0])
        elif c == 'd':
            new_t = drive.turn_to(np.pi)
        elif c == 's':
            new_t = drive.go_to([0,0])
        elif c == ' ' and t:
            t.cancel()
            try:
                yield From(t)
            except asyncio.CancelledError:
                pass

        if new_t:
            if t:
                t.cancel()
                try:
                    yield From(t)
                except asyncio.CancelledError:
                    pass
            t = asyncio.ensure_future(new_t)

        yield From(asyncio.sleep(0.05))

if __name__ == "__main__":
    with TAMProxy() as tamproxy:
        drive = RegulatedDrive(tamproxy)

        m = Mapper(drive.odometer)
        w = Window(500, [m])

        loop = asyncio.get_event_loop()
        loop.run_until_complete(main_task())
        loop.close()