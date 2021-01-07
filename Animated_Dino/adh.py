import pygame
from pygame.locals import *
from random import randint


class Dino(pygame.sprite.Sprite):
    #State constants make it easy to control which set of images we will use
    STANDING_RIGHT = 0
    WALKING_RIGHT = 1
    #RUNNING_RIGHT = 2
    STANDING_LEFT = 3
    WALKING_LEFT = 4
    #RUNNING_LEFT = 5
    loaded = False #we only need to load images once (if multiple Horses)
    
    def __init__(self, x=0, y=0, state=0, dx=0):
        pygame.sprite.Sprite.__init__(self)
        if not Dino.loaded:
            Dino.load_images(self)
            
        self.image = Dino.stand_right_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.frame = 0
        self.dx = dx
        self.state = state

    def load_images(self):
        Dino.loaded = True

        Dino.walk_right_images = []
        for i in range(1, 10):
            temp_image = pygame.image.load("images/Walk (%2i).png" %(i)).convert()
            temp_image.set_colorkey(temp_image.get_at((0,0)))
            Dino.walk_right_images.append(temp_image)

        Dino.walk_left_images = []
        for i in range(1, 10):
            temp_image = pygame.image.load("images/Walkl (%2i).png" %(i)).convert()
            temp_image.set_colorkey(temp_image.get_at((0,0)))
            Dino.walk_left_images.append(temp_image)

        Dino.stand_right_images = []
        for i in range(1, 12):
            temp_image = pygame.image.load("images/Jump (%2i).png" %(i)).convert()
            temp_image.set_colorkey(temp_image.get_at((0,0)))
            Dino.stand_right_images.append(temp_image)
            
        Dino.stand_left_images = []
        for i in range(1, 12):
            temp_image = pygame.image.load("images/Jumpl (%2i).png" %(i)).convert()
            temp_image.set_colorkey(temp_image.get_at((0,0)))
            Dino.stand_left_images.append(temp_image)

    def update(self):
        #grab the approprite image surface from whatever is the current state.
        #Using mudulus allows us to 'wrap around' the list of images
        self.frame += 1
        if self.state == Dino.STANDING_RIGHT:
            self.image = Dino.stand_right_images[self.frame%len(Dino.stand_right_images)]
            self.dx = 0
        elif self.state == Dino.WALKING_RIGHT:
            self.image = Dino.walk_right_images[self.frame%len(Dino.walk_right_images)]
            self.dx = 3
        elif self.state == Dino.STANDING_LEFT:
            self.image = Dino.stand_left_images[self.frame%len(Dino.stand_left_images)]
            self.dx = 0
        elif self.state == Dino.WALKING_LEFT:
            self.image = Dino.walk_left_images[self.frame%len(Dino.walk_left_images)]
            self.dx = -3
            
        #Handle the edges
        self.rect.centerx += self.dx     
        if self.rect.left > screen.get_width():
            self.rect.right = 0
            self.rect.centery = randint(0+self.rect.height/2, screen.get_height()-self.rect.height/2)
        elif self.rect.right < 0:
            self.rect.left = screen.get_width()
            self.rect.centery = randint(0+self.rect.height/2, screen.get_height()-self.rect.height/2)
        

game_size = (640, 480)
screen = pygame.display.set_mode(game_size)
pygame.display.set_caption("Dino Run: <- and -> to move, space to jump")
background = pygame.Surface(game_size)
background = background.convert()
background.fill((255, 255, 25))
screen.blit(background, (0,0))

all_sprites = pygame.sprite.Group()
dino = Dino(100, 200, randint(0, 5))
all_sprites.add(dino)

clock = pygame.time.Clock()
keep_going = True
while keep_going:
    clock.tick(24)
    for ev in pygame.event.get():
        if ev.type == QUIT:
            keep_going = False
        elif ev.type == KEYDOWN:
            if ev.key == K_SPACE and dino.state in [Dino.STANDING_RIGHT, Dino.WALKING_RIGHT]:
                dino.state = Dino.STANDING_RIGHT
            elif ev.key == K_SPACE and dino.state in [Dino.STANDING_LEFT, Dino.WALKING_LEFT]:
                dino.state = Dino.STANDING_LEFT
            elif ev.key == K_RIGHT:
                dino.state = Dino.WALKING_RIGHT
            elif ev.key == K_LEFT:
                dino.state = Dino.WALKING_LEFT

    
    all_sprites.clear(screen, background)
    all_sprites.update()
    all_sprites.draw(screen)
    
    pygame.display.flip()

pygame.quit()
