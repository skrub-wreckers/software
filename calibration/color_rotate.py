import logging
import time
import math
import os
import random

import cv2
import numpy as np
from trollius import From
import trollius as asyncio

from tamproxy import TAMProxy

from sw.hal import *
from sw.vision.window import Window
from sw.vision import Camera, Vision, Colors, CameraPanel
from sw.gui import Window, ControlPanel
from sw import constants
from sw.mapping import Mapper
from sw.mapping.arena import Arena

log = logging.getLogger('sw.test')

CAMERA_ID = 2
FILE_NAME_C = "none"
FILE_NAME_B = "bb"
colors = []
breakbeams = []

@asyncio.coroutine
def capture_color(r):
    try:
        while True:
            if c.started:
                yield From(asyncio.sleep(0.1))
                colors.append(r.color_sensor.raw_val)
                breakbeams.append((r.break_beams.l_beam._recv_pin.val, r.break_beams.r_beam._recv_pin.val,))
            yield
    finally:
        print "Saving results..."
        np.save(FILE_NAME_C, colors)
        np.save(FILE_NAME_B, breakbeams)

@asyncio.coroutine
def main(r):
    try:
        ctask = asyncio.ensure_future(capture_color(r))
        turn_task = None
        start_angle = 0
        while True:
            if c.started:
                if turn_task is None:
                    turn_task = asyncio.ensure_future(r.drive.turn_speed(np.radians(30)))
                    start_angle = r.drive.odometer.val.theta
            elif turn_task is not None:
                turn_task.cancel()
                turn_task = None
            if abs(r.drive.odometer.val.theta - start_angle) > 2*np.pi:
                if turn_task is not None:
                    turn_task.cancel()
                    c.started = False
                    turn_task = None

            if ctask.done():
                yield From(ctask)

            yield
            if w.get_key() == ' ':
                break
    finally:
        print "Finally in main"
        ctask.cancel()
        yield From(ctask)

if __name__ == "__main__":
    with TAMProxy() as tamproxy:
        r = Robot(tamproxy)

        m = Mapper(r.drive.odometer, map=Arena.load('../sw/mapping/red_map.txt'))
        cam = Camera(geom=constants.camera_geometry, id=2)
        v = Vision(cam)
        c = ControlPanel(r)
        w = Window(500, [m, CameraPanel(v), c])

        log.debug("started")

        loop = asyncio.get_event_loop()
        loop.set_debug(True)
        main_task = main(r)
        try:
            loop.run_until_complete(main_task)
        except KeyboardInterrupt:
            print "Interrupted"
            main_task.cancel()
            loop.run_forever()
        finally:
            loop.close()
