import pygame

from Speedup import Speedup


class Mirror(Speedup):

    def draw(self, screen, color):
        w, h = self.size

        pygame.draw.rect(screen, color, (self.x + 15, self.y, 5, h))
        pygame.draw.lines(screen, color, False, [(self.x, self.y), (self.x + 15, self.y + h/2), (self.x, self.y + h)])
