import sys
import threading
import time
import pygame
from Queue import Queue, Empty

class Window(object):
    def __init__(self, psize, panels):
        self.psize = psize
        self.panels = panels
        self.font = None
        #for panel in self.panels:
        #    panel.set_size(self.psize)
        
        self.bite = 0
        self.bite_dir = 10
        
        self.active_panel = None
        self.loop_thread = threading.Thread(target=self.loop)
        self.loop_thread.daemon = True
        self.loop_thread.start()

        self.keys = Queue()
        
        for panel in self.panels:
            panel.set_size(self.psize)

    def get_key(self):
        try:
            return self.keys.get_nowait()
        except Empty:
            return None

    def update(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.keys.put(event.unicode)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[1] > self.psize:
                    events.remove(event)
                    if event.pos[0]<100*len(self.panels):
                        self.active_panel = int(event.pos[0]/100.0)
                        pygame.display.set_caption("Stac-man: "+self.panels[self.active_panel].name)
                    else:
                        self.active_panel = None
                        pygame.display.set_caption("Stac-man")
        if self.active_panel is not None:
            self.panels[self.active_panel].update(events)

    def draw(self):
        self.screen.fill([100,100,100])
        if self.active_panel is None:
            pygame.draw.circle(self.screen, (255,255,0), (self.psize/2,self.psize/2), 75)
            #<hehehe>
            self.bite += self.bite_dir
            if self.bite == 100:
                self.bite_dir = -10
            if self.bite == 0:
                self.bite_dir = 10
            #</hehehe>
            pygame.draw.polygon(self.screen, (100,100,100), ((self.psize/2,self.psize/2),((self.psize/2)+100, (self.psize/2)-int(self.bite)),((self.psize/2)+100,(self.psize/2)+int(self.bite))))
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
        pygame.display.set_caption("Stac-man")
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