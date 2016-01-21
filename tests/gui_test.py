from sw.mapping import Mapper
from sw.vision import Vision, CameraPanel, Camera
from sw.gui import window
from sw.hal import *
import sw.constants
import pygame

from tamproxy import TAMProxy

if __name__ == "__main__":
    #cam = Camera(geom=constants.camera_geometry, id=1)
    #v = Vision(cam)
    #with TAMProxy() as tamproxy:
        #drive = Drive(tamproxy)
        w = window.Window(500, [])#[Mapper(drive.odometer), CameraPanel(500, v)])
        while True:
            pass
        #pygame.event.pump()