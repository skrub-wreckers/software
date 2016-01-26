import cv2
import numpy as np
from tamproxy import TAMProxy

from sw.hal import *
from sw.vision.window import Window
from sw.vision import Camera, Vision, Colors, CameraPanel
from sw.gui import Window
import sw.constants as constants
from sw.mapping import Mapper
import time

from sw.taskqueue import TaskCancelled


OUR_COLOR = Colors.RED


THEIR_COLOR = (Colors.RED | Colors.GREEN) & ~OUR_COLOR


ROUND_TIME = 20
SILO_TIME = ROUND_TIME - 30

def pick_up_cubes(r):
    while True:
        val = r.color_sensor.val
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
            print "No cube"
            r.drive.go(0, 0.1)
        elif abs(cube.angle_to) < np.radians(10):
            print "Going {}in to {}".format(cube.distance, cube)
            # limit distance
            to_go = cube.pos2
            if cube.distance > 60:
                to_go = to_go * 60 / cube.distance

            # transform to world space
            to_go = np.append(to_go, 1)
            dest = r.drive.odometer.robot_matrix.dot(to_go)

            task = r.drive.go_to(dest[:2], async=True)
            while not task.wait(0):
                if r.break_beams.blocked or r.color_sensor.val != Colors.NONE:
                    task.cancel()
                try:
                    yield
                except TaskCancelled:
                    task.cancel()
                    raise

            for _ in pick_up_cubes(r):
                yield

        else:
            print "Turning {} to {}".format(cube.angle_to, cube)
            r.drive.turn_angle(cube.angle_to)


if __name__ == "__main__":
    with TAMProxy() as tamproxy:
        r = Robot(tamproxy)

        m = Mapper(r.drive.odometer)
        cam = Camera(geom=constants.camera_geometry, id=2)
        v = Vision(cam)
        w = Window(500, [m, CameraPanel(500, v)])

        while w.get_key() != ' ':
            pass

        start_time = time.time()

        time_up = lambda: (time.time() - start_time) >= SILO_TIME

        task = main()


        while not time_up():
            print "Time remaining: {}".format(time.time() - start_time)
            task.next()

        try:
            task.throw(TaskCancelled())
        except TaskCancelled, StopIteration:
            pass

        r.arms.silo_door.open()
        time.sleep(0.5)
        Drive.go_distance(r.drive, 4)