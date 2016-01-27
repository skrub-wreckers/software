import logging
import time
import math
import os

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

from sw.taskqueue import TaskCancelled

log = logging.getLogger('sw.test')

saveloc = 'color-sensor'

CAMERA_ID = 2
FILE_NAME = "none"
colors = []

@asyncio.coroutine
def capture_color():
    try:
        while True:
            sleep(0.1)
            colors.append(np.float32([color.r, color.g, color.b, color.c]))
    finally:
        np.save(os.path.join(saveloc, FILE_NAME), colors)
        

@asyncio.coroutine
def avoid_wall(r, side, dir):
    log.info('Avoiding wall to {}'.format('left' if dir == 1 else 'right'))
    Drive.go_distance(r.drive, 4)
    while side.val:
        r.drive.go(0, dir*0.2)
        yield From(asyncio.sleep(0.05))
    Drive.go_distance(r.drive, 4)

@asyncio.coroutine
def main(r):
    while True:
        try:
            v.update()
        except IOError:
            continue

        #print cube
        angle_to = math.pi*(random.randint(-180,180)/180.0)
        
        log.debug("Turning {}".format(angle_to))
        
        yield From(r.drive.turn_angle(angle_to))
        task = asyncio.ensure_future(r.drive.go_to(10))
        try:
            while not task.done():
                if r.left_short_ir.val:
                    task.cancel()
                    yield From(avoid_wall(r,r.left_short_ir,-1))
                if r.right_short_ir.val:
                    task.cancel()
                    yield From(avoid_wall(r,r.right_short_ir,1))

                yield From(asyncio.sleep(0.05))

        finally:
            task.cancel()

if __name__ == "__main__":
    with TAMProxy() as tamproxy:
        r = Robot(tamproxy)

        m = Mapper(r.drive.odometer, map=Arena.load('../sw/mapping/red_map.txt'))
        cam = Camera(geom=constants.camera_geometry, id=CAMERA_ID)
        v = Vision(cam)
        w = Window(500, [m, CameraPanel(v), ControlPanel(r)])

        while w.get_key() != ' ':
            pass

        log.debug("started")

        loop = asyncio.get_event_loop()
        loop.set_debug(True)
        loop.run_until_complete(main(r))
        loop.close()
