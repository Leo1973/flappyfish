import pygame
from pygame.locals import *
SCREEN_SIZE = (200,200)
def load_image(file, width, number):
    surface = pygame.image.load(file).convert_alpha()
    height = surface.get_height() 
    return [surface.subsurface(
        Rect((i * width, 0), (width, height))
        ) for i in range(number)]
class fish(pygame.sprite.Sprite):
    #_life = 100
    images = []
    def __init__(self):
        self.order = 0
        self.rate = 200
        self.height = 60
        self.number = 3
        pygame.sprite.Sprite.__init__(self)
        self.images = load_image("bird.png",80, 3)
        self.image = self.images[self.order]
        #self.rect = Rect(0, 0, self.width, self.height)
        #self.life = self._life
        self.passed_time = 0
 
    def update(self, passed_time):
        self.passed_time += passed_time
        self.order = ( self.passed_time / self.rate ) % self.number
        if self.order == 0 and self.passed_time > self.rate:
            self.passed_time = 0
        self.image = self.images[int(self.order)]

    def render(self,screen):
        screen.blit(self.image,(0,0))

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE,0,32)#窗口
Fish = fish()
clock = pygame.time.Clock()
while True:

    #screen = pygame.display.set_mode(SCREEN_SIZE,0,32)#窗口

    passed_time = clock.tick(100)
    print (passed_time)
    Fish.update(passed_time)
    screen.fill((0,0,0))
    #Fish.render(screen)
    #Fish.order = 1
    #Fish.render(screen)
    Fish.order = 2
    Fish.render(screen)
    for event in pygame.event.get():
            if event.type == QUIT:
                exit()
    pygame.display.update()

