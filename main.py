import logging
import time
from math import pi

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

OUR_COLOR = Colors.GREEN
CAMERA_ID = 2

THEIR_COLOR = (Colors.RED | Colors.GREEN) & ~OUR_COLOR


ROUND_TIME = constants.round_time
SILO_TIME = ROUND_TIME - 20

USE_BREAKBEAM = False

def get_cube(r):
    val = r.color_sensor.val
    blocked = r.break_beams.blocked

    if val == Colors.NONE:
        if USE_BREAKBEAM and blocked:
            log.warn('Beam broken, but no color reading')
        return Colors.NONE

    if USE_BREAKBEAM and not blocked:
        log.warn('Color is {}, but beam not broken'.format(Colors.name(val)))
        return Colors.NONE

    return val

@asyncio.coroutine
def pick_up_cubes(r):
    while True:
        val = get_cube(r)

        if val == OUR_COLOR:
            r.drive.stop()
            r.arms.silo.up()
            log.info('Picked up {} block'.format(Colors.name(val)))
            r.arms.silo.down()
        elif val == THEIR_COLOR:
            r.drive.stop()
            r.arms.dump.up()
            log.info('Picked up {} block'.format(Colors.name(val)))
            r.arms.dump.down()
        else:
            break

        yield From(asyncio.sleep(0.05))

# Direction is the direction we want to turn in
@asyncio.coroutine
def avoid_wall(r, ir, bumper, dir):
    log.info('Avoiding wall to {}'.format('left' if dir == 1 else 'right'))
    if bumper.val:
        log.info("Bumper was hit; backing up")
        Drive.go_distance(r.drive, -1)
    yield From(r.drive.turn_angle(dir * np.radians(30)))
    while ir.val and bumper.val:
        log.info("turning to avoid wall")
        r.drive.go(0, dir*0.2)
        yield From(asyncio.sleep(0.05))
        yield From(pick_up_cubes(r))
    Drive.turn_angle(r.drive, np.pi/16*dir)
    Drive.go_distance(r.drive, 8)

@asyncio.coroutine
def search_for_cubes(r):
    # TODO: Replace with wall following soon
    if r.left_short_ir.val:
        yield From(r.drive.turn_speed(np.radians(-30)))
    else:
        yield From(r.drive.turn_speed(np.radians(30)))

@asyncio.coroutine
def find_cubes(r):
    try:
        search_task = None
        while True:
            yield
            # pick up any cubes we have
            yield From(pick_up_cubes(r))

            try:
                yield From(asyncio.get_event_loop().run_in_executor(None, v.update))
            except IOError:
                continue
            m.update_cubes_from(v)
            cube = v.nearest_cube()
            #print cube

            # start scanning for cubes
            if cube is None:
                if search_task is None:
                    log.info('No cubes in view - scanning')
                    search_task = asyncio.ensure_future(search_for_cubes(r))
                continue

            # we found a cube - stop scanning
            if search_task:
                search_task.cancel()
                search_task = None
                log.info('Stopped scanning')

            if abs(cube.angle_to) > np.radians(10):
                log.debug("Turning {} to {}".format(cube.angle_to, cube))
                yield From(r.drive.turn_angle(cube.angle_to))
            else:
                log.debug("Going {}in to {}".format(cube.distance, cube))
                # limit distance
                to_go = cube.pos2
                if cube.distance > 60:
                    to_go = to_go * 60 / cube.distance

                # transform to world space
                to_go = np.append(to_go, 1)
                dest = r.drive.odometer.val.robot_matrix.dot(to_go)

                task = asyncio.ensure_future(r.drive.go_to(dest[:2]))
                try:
                    while not task.done():
                        if get_cube(r) != Colors.NONE:
                            task.cancel()
                        if r.left_short_ir.val and r.right_short_ir.val and \
                            min(r.left_long_ir.distInches, r.right_long_ir.distInches) < constants.close_to_wall:
                            task.cancel()
                            log.debug("All sensors hit")
                            if r.left_bumper.val:
                                yield From(r.drive.turn_angle(np.radians(-120)))
                            else:
                                yield From(r.drive.turn_angle(np.radians(120)))
                        if r.left_bumper.val or r.left_short_ir.val:
                            log.debug("Left side triggered")
                            task.cancel()
                            yield From(avoid_wall(r,r.left_short_ir,r.left_bumper,-1))
                        if r.right_bumper.val or r.right_short_ir.val:
                            log.debug("Right side triggered")
                            task.cancel()
                            yield From(avoid_wall(r,r.right_short_ir,r.right_bumper,1))
                        yield From(asyncio.sleep(0.05))

                finally:
                    task.cancel()
    finally:
        if search_task:
            search_task.cancel()

@asyncio.coroutine
def clean_up(r):
    log.info('Doing round cleanup')
    r.drive.stop()

    startAngle = r.drive.odometer.val.theta

    # Turn until find good direction or if we spin all the way around
    r.drive.go(0, 0.15)
    gap_found = False
    while not gap_found and abs(r.drive.odometer.val.theta - startAngle) <= 2*pi:
        yield asyncio.sleep(0.05)
        if min(r.left_long_ir.distInches, r.right_long_ir.distInches) < constants.close_to_wall:
            gap_found = True
    r.drive.stop()
    r.silo.open()

    if gap_found:
        Drive.go_distance(r.drive, 6)


@asyncio.coroutine
def main(r):
    task = asyncio.ensure_future(find_cubes(r))
    try:
        yield From(asyncio.wait_for(task, SILO_TIME))
    except asyncio.TimeoutError:
        pass

    yield From(clean_up(r))

if __name__ == "__main__":
    with TAMProxy() as tamproxy:
        r = Robot(tamproxy)

        m = Mapper(r.drive.odometer, map=Arena.load('../sw/mapping/red_map.txt'))
        cam = Camera(geom=constants.camera_geometry, id=CAMERA_ID)
        v = Vision(cam)
        c = ControlPanel(r)
        w = Window(500, [m, CameraPanel(v), c])

        while not c.started:
            pass

        log.debug("started")

        loop = asyncio.get_event_loop()
        loop.set_debug(True)
        loop.run_until_complete(main(r))
        loop.close()