from sw.mapping import Mapper
from sw.mapping.arena import Arena
from sw.vision import Vision, CameraPanel, Camera
from sw.gui import window
from sw.hal import *
from sw import constants
import pygame

from tamproxy import TAMProxy

if __name__ == "__main__":
    cam = Camera(geom=constants.camera_geometry, id=0)
    v = Vision(cam)
    #with TAMProxy() as tamproxy:
        #drive = Drive(tamproxy)
    w = window.Window(500, [Mapper(map=Arena.load('../sw/mapping/red_map.txt')),CameraPanel(v)])#[Mapper(drive.odometer), CameraPanel(500, v)])
    while True:
        pass