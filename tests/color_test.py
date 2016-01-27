from tamproxy.devices import Color
import tamproxy
import pygame
import sys
import numpy as np
import time
import itertools
import os

if __name__ == '__main__':
    with tamproxy.TAMProxy() as tamp:
        color = Color(tamp, integrationTime=Color.INTEGRATION_TIME_2_4MS, gain=Color.GAIN_60X)
        screen = pygame.display.set_mode([500,500])
        max_c = np.float32([0,0,0,0])

        saves = []

        colors = dict(
            red=[],
            green=[],
            none=[]
        )

        ideal_colors = dict(
            red=[255, 0, 0],
            green=[0,255,0],
            none=[0, 0, 0]
        )

        names = colors.keys()
        i = 0

        while True:
            active_name = names[i]

            c_val = np.float32([color.r, color.g, color.b, color.c])

            screen.fill(np.clip(c_val[:3], 0, 255))
            pygame.draw.rect(
                screen,
                ideal_colors[active_name],
                (0, 0, 500, 50)
            )

            for row, cname in enumerate(names):
                for col, sample in enumerate(colors[cname]):
                    pygame.draw.rect(
                        screen,
                        np.clip(sample[:3], 0, 255),
                        (20*col, 20*row + 50, 20, 20)
                    )

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    saveloc = 'color-sensor'
                    if not os.path.exists(saveloc):
                        os.mkdir(saveloc)
                    for cname, samples in colors.iteritems():
                        np.save(os.path.join(saveloc, cname), np.stack(samples))
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.unicode == ' ':
                        colors[active_name].append(c_val)
                    elif event.unicode == '\r':
                        i = (i+1) % len(names)

            time.sleep(0.1)