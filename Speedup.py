import pygame


class Speedup:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.size = (20, 20)

    def collides_with(self, x, y):
        return x == self.x and y == self.y

    def draw(self, screen, color):
        w, h = self.size
        pygame.draw.polygon(screen, color, [(self.x, self.y), (self.x + w / 2, self.y + h / 2), (self.x, self.y + h)])
        pygame.draw.polygon(screen, color, [(self.x + w/2, self.y), (self.x + w, self.y + h / 2), (self.x + w/2, self.y + h)])
