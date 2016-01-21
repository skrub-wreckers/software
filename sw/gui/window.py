import pygame
import sys
import threading
import time
from sw.mapping import Mapper

class Window():
    def __init__(self, psize, panels):
        self.psize = psize
        self.panels = panels
        self.font = None
        #for panel in self.panels:
        #    panel.set_size(self.psize)
        self.active_panel = None
        self.loop_thread = threading.Thread(target=self.loop)
        self.loop_thread.daemon = True
        self.loop_thread.start()
        
    def update(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[1] > self.psize:
                    events.remove(event)
                    if event.pos[0]<100*len(self.panels):
                        self.active_panel = int(event.pos[0]/100.0)
                        pygame.display.set_caption("Stackman: "+self.panels[self.active_panel].name)
                    else:
                        self.active_panel = None
                        pygame.display.set_caption("Stackman")
        if self.active_panel is not None:
            self.panels[self.active_panel].update(events)
        
    def draw(self):
        self.screen.fill([100,100,100])
        pygame.draw.circle(self.screen, (255,255,0), (self.psize/2,self.psize/2), 75)
        pygame.draw.polygon(self.screen, (100,100,100), ((self.psize/2,self.psize/2),((self.psize/2)+100, (self.psize/2)-100),((self.psize/2)+100,(self.psize/2)+100)))
        pygame.draw.line(self.screen, (0,0,0), (0, self.psize), (self.psize, self.psize))
        if self.active_panel is not None:
            self.panels[self.active_panel].draw(self.screen.subsurface([0,0,self.psize,self.psize]))
        for panelID in range(0, len(self.panels)):
            pos = (100*panelID+5,self.psize+5, 90, 40)
            t_surf = self.font.render(self.panels[panelID].name, True, (0,0,0))
            pygame.draw.rect(self.screen, (255,255,255), pos)
            self.screen.blit(t_surf, [pos[0]+45-(t_surf.get_width()/2),pos[1]+20-(t_surf.get_height()/2),])
        pygame.display.flip()
        
    def loop(self):
        pygame.init()
        self.screen = pygame.display.set_mode([self.psize, self.psize+50])
        self.font = pygame.font.Font(None, 20)
        pygame.display.set_caption("Stackman")
        #Setup icon
        icsurf = pygame.surface.Surface((32,32), pygame.SRCALPHA)
        icsurf.fill((0,0,0,0))
        pygame.draw.circle(icsurf,(255,255,0),(15,15),14)
        pygame.draw.polygon(icsurf,(0,0,0,0),((15,15),(35,-5),(35,35)))
        pygame.display.set_icon(icsurf)
        while True:
            self.update()
            self.draw()
            time.sleep(0.05)