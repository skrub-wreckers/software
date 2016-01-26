from sw.mapping import Mapper
from sw.mapping.arena import Arena
from sw.vision import Vision, CameraPanel, Camera
from sw.gui import window, ControlPanel
from sw.hal import *
from sw import constants
import pygame

from tamproxy import TAMProxy

if __name__ == "__main__":
    cam = Camera(geom=constants.camera_geometry, id=0)
    v = Vision(cam)
    with TAMProxy() as tamproxy:
        r = Robot(tamproxy)
        w = window.Window(500, [Mapper(r.drive, map=Arena.load('../sw/mapping/red_map.txt')), CameraPanel(v), ControlPanel(r)])#[Mapper(drive.odometer), CameraPanel(500, v)])
        while True:
            pass