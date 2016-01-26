import cv2
import numpy as np
from tamproxy import TAMProxy

from sw.hal import *
from sw.vision.window import Window
from sw.vision import Camera, Vision, Colors, CameraPanel
from sw.gui import Window, ControlPanel
import sw.constants as constants
from sw.mapping import Mapper
import time

from sw.taskqueue import TaskCancelled

import logging

log = logging.getLogger('sw.test')

OUR_COLOR = Colors.GREEN
CAMERA_ID = 2

THEIR_COLOR = (Colors.RED | Colors.GREEN) & ~OUR_COLOR


ROUND_TIME = 180
SILO_TIME = ROUND_TIME - 20

def pick_up_cubes(r):
    
    while True:
        val = r.color_sensor.val
        blocked = r.break_beams.blocked
        if blocked or val != Colors.NONE:
            log.debug("Cube detection: beam={},sensor={}".format(blocked, val))
        if not blocked:
            break
        if val == OUR_COLOR:
            r.drive.stop()
            r.arms.silo.up()
            time.sleep(1.0)
            r.arms.silo.down()
        elif val == THEIR_COLOR:
            r.drive.stop()
            r.arms.dump.up()
            time.sleep(0.75)
            r.arms.dump.down()
        else:
            break
        yield

def avoid_wall(r, side, dir):
    Drive.go_distance(r.drive, 4)
    while side.val:
        r.drive.go(0, dir*0.2)
        time.sleep(0.05)
        for _ in pick_up_cubes(r):
            yield
    Drive.go_distance(r.drive, 4)
        
def main(r):
    while True:
        # pick up any cubes we have
        for _ in pick_up_cubes(r):
            yield

        try:
            v.update()
        except IOError:
            continue
        m.setCubePositions(v.cubes)
        cube = v.nearest_cube()
        #print cube

        if cube is None:
            #  print "No cube"
            r.drive.go(steer=0.1)
        elif abs(cube.angle_to) < np.radians(10):
            log.debug("Going {}in to {}".format(cube.distance, cube))
            # limit distance
            to_go = cube.pos2
            if cube.distance > 60:
                to_go = to_go * 60 / cube.distance

            # transform to world space
            to_go = np.append(to_go, 1)
            dest = r.drive.odometer.robot_matrix.dot(to_go)

            task = r.drive.go_to(dest[:2], async=True)
            while not task.wait(0):
                if r.break_beams.blocked and r.color_sensor.val != Colors.NONE:
                    task.cancel()
                if r.left_short_ir.val:
                    task.cancel()
                    for _ in avoid_wall(r,r.left_short_ir,-1):
                        yield
                if r.right_short_ir.val:
                    task.cancel()
                    for _ in avoid_wall(r,r.right_short_ir,1):
                        yield
                try:
                    yield
                except TaskCancelled:
                    task.cancel()
                    raise

            for _ in pick_up_cubes(r):
                yield

        else:
            log.debug("Turning {} to {}".format(cube.angle_to, cube))
            r.drive.turn_angle(cube.angle_to)


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

        start_time = time.time()

        time_up = lambda: (time.time() - start_time) >= SILO_TIME

        task = main(r)


        while not time_up():
            # print "Time remaining: {}".format(time.time() - start_time)
            task.next()

        try:
            task.throw(TaskCancelled())
        except TaskCancelled, StopIteration:
            pass

        r.drive.stop()
        r.arms.silo_door.write(180)
        time.sleep(0.5)
        Drive.go_distance(r.drive, 6)