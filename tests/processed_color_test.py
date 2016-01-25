from sw.hal import ColorSensor
from sw.vision import Colors
import tamproxy
import pygame
import sys
import numpy as np
import time
import itertools
import os

if __name__ == '__main__':
    with tamproxy.TAMProxy() as tamp:
        color = ColorSensor(tamp)
        screen = pygame.display.set_mode([500,500])

        while True:
            val = color.val
            print val

            screen.fill(Colors.to_rgb(val))

            time.sleep(0.1)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()