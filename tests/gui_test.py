from sw.mapping import Mapper
from sw.vision import Vision, CameraPanel, Camera
from sw.gui import window
from sw.hal import *
import sw.constants
import pygame

from tamproxy import TAMProxy

if __name__ == "__main__":
    cam = Camera(geom=constants.camera_geometry, id=0)
    v = Vision(cam)
    w = window.Window(500, [CameraPanel(500, v)])
    #with TAMProxy() as tamproxy:
    #    drive = Drive(tamproxy)
    #    w = window.Window(500, [Mapper(drive.odometer)])
    while True:
        pass
        #pygame.event.pump()