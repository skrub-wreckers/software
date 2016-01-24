from tamproxy.devices import Color
import tamproxy
import pygame
import sys
import numpy as np
import time

if __name__ == '__main__':
    with tamproxy.TAMProxy() as tamp:
        color = Color(tamp, integrationTime=Color.INTEGRATION_TIME_101MS, gain=Color.GAIN_1X)
        screen = pygame.display.set_mode([500,500])
        max_c = np.float32([0,0,0])

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            c = np.float32([color.r, color.g, color.b])
            max_c = np.where(max_c > c, max_c, c)

            rel_c = (c / max_c * 255)

            print "{} / {} = {}".format(c, max_c, rel_c)
            print color.colorTemp, color.lux
            screen.fill(rel_c)
            pygame.display.flip()

            time.sleep(0.05)