from sw.mapping import Mapper
from sw.mapping.arena import Arena
from sw.vision import Vision, CameraPanel, Camera
from sw.gui import window, ControlPanel
from sw.hal import *
from sw import constants
import pygame
import time

from tamproxy import TAMProxy

if __name__ == "__main__":
    cam = Camera(geom=constants.camera_geometry, id=0)
    v = Vision(cam)
    with TAMProxy() as tamproxy:
        r = Robot(tamproxy)
        m = Mapper(r.drive.odometer, map=Arena.load('../sw/mapping/red_map.txt'))
        w = window.Window(500, [m, CameraPanel(v), ControlPanel(r)])#[Mapper(drive.odometer), CameraPanel(500, v)])
        while True:
            v.update()
            m.update_cubes_from(v)
            time.sleep(0.05)
            pass