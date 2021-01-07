import pygame
from pygame.locals import *
from random import randint


class Horse(pygame.sprite.Sprite):
    #State constants make it easy to control which set of images we will use
    STANDING_RIGHT = 0
    WALKING_RIGHT = 1
    RUNNING_RIGHT = 2
    STANDING_LEFT = 3
    WALKING_LEFT = 4
    RUNNING_LEFT = 5
    loaded = False #we only need to load images once (if multiple Horses)
    
    def __init__(self, x=0, y=0, state=0, dx=0):
        pygame.sprite.Sprite.__init__(self)
        if not Horse.loaded:
            Horse.load_images(self)
            
        self.image = Horse.stand_right_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.frame = 0
        self.dx = dx
        self.state = state

    def load_images(self):
        Horse.loaded = True

        Horse.run_right_images = [] #class-level variables, for all Horses to share
        for i in range(1, 12):
            temp_image = pygame.image.load("images/horse_run_r%02i.bmp" %(i)).convert()
            temp_image.set_colorkey(temp_image.get_at((0,0)))
            Horse.run_right_images.append(temp_image)
        Horse.walk_right_images = []
        for i in range(1, 10):
            temp_image = pygame.image.load("images/Walk (%2i).png" %(i)).convert()
            temp_image.set_colorkey(temp_image.get_at((0,0)))
            Horse.walk_right_images.append(temp_image)

        Horse.run_left_images = []
        for i in range(1, 12):
            temp_image = pygame.image.load("images/horse_run_l%02i.bmp" %(i)).convert()
            temp_image.set_colorkey(temp_image.get_at((0,0)))
            Horse.run_left_images.append(temp_image)
        Horse.walk_left_images = []
        for i in range(1, 10):
            temp_image = pygame.image.load("images/Walkl (%2i).png" %(i)).convert()
            temp_image.set_colorkey(temp_image.get_at((0,0)))
            Horse.walk_left_images.append(temp_image)

        Horse.stand_right_images = []
        for i in range(1, 14):
            temp_image = pygame.image.load("images/horse_eating_r%02i.bmp" %(i)).convert()
            temp_image.set_colorkey(temp_image.get_at((0,0)))
            Horse.stand_right_images.append(temp_image)
        Horse.stand_left_images = []
        for i in range(1, 14):
            temp_image = pygame.image.load("images/horse_eating_l%02i.bmp" %(i)).convert()
            temp_image.set_colorkey(temp_image.get_at((0,0)))
            Horse.stand_left_images.append(temp_image)

    def update(self):
        #grab the approprite image surface from whatever is the current state.
        #Using mudulus allows us to 'wrap around' the list of images
        self.frame += 1
        if self.state == Horse.STANDING_RIGHT:
            self.image = Horse.stand_right_images[self.frame%len(Horse.stand_right_images)]
            self.dx = 0
        elif self.state == Horse.WALKING_RIGHT:
            self.image = Horse.walk_right_images[self.frame%len(Horse.walk_right_images)]
            self.dx = 3
        elif self.state == Horse.RUNNING_RIGHT:
            self.image = Horse.run_right_images[self.frame%len(Horse.run_right_images)]
            self.dx = 7
        elif self.state == Horse.STANDING_LEFT:
            self.image = Horse.stand_left_images[self.frame%len(Horse.stand_left_images)]
            self.dx = 0
        elif self.state == Horse.WALKING_LEFT:
            self.image = Horse.walk_left_images[self.frame%len(Horse.walk_left_images)]
            self.dx = -3
        elif self.state == Horse.RUNNING_LEFT:
            self.image = Horse.run_left_images[self.frame%len(Horse.run_left_images)]
            self.dx = -7
            
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
pygame.display.set_caption("Animation! (press c/v/n/m/space)")
background = pygame.Surface(game_size)
background = background.convert()
background.fill((255, 255, 25))
screen.blit(background, (0,0))

all_sprites = pygame.sprite.Group()
horse = Horse(100, 200, randint(0, 5))
all_sprites.add(horse)

clock = pygame.time.Clock()
keep_going = True
while keep_going:
    clock.tick(24)
    for ev in pygame.event.get():
        if ev.type == QUIT:
            keep_going = False
        elif ev.type == KEYDOWN:
            if ev.key == K_SPACE and horse.state in [Horse.STANDING_RIGHT, Horse.WALKING_RIGHT, Horse.RUNNING_RIGHT]:
                horse.state = Horse.STANDING_RIGHT
            elif ev.key == K_SPACE and horse.state in [Horse.STANDING_LEFT, Horse.WALKING_LEFT, Horse.RUNNING_LEFT]:
                horse.state = Horse.STANDING_LEFT
            elif ev.key == K_n:
                horse.state = Horse.WALKING_RIGHT
            elif ev.key == K_m:
                horse.state = Horse.RUNNING_RIGHT
            elif ev.key == K_v:
                horse.state = Horse.WALKING_LEFT
            elif ev.key == K_c:
                horse.state = Horse.RUNNING_LEFT

    
    all_sprites.clear(screen, background)
    all_sprites.update()
    all_sprites.draw(screen)
    
    pygame.display.flip()

pygame.quit()
