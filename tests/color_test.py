from tamproxy.devices import Color
import tamproxy
import pygame
import sys
import numpy as np

if __name__ == '__main__':
    with tamproxy.TAMProxy() as tamp:
        color = Color(tamp, integrationTime=Color.INTEGRATION_TIME_101MS, gain=Color.GAIN_1X)
        screen = pygame.display.set_mode([500,500])
        max = np.array([0,0,0])
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            c = np.array([color.r, color.g, color.b])
            
            print c, color.c
            print color.colorTemp, color.lux
            screen.fill(np.clip(c, 0, 255))
            pygame.display.flip()