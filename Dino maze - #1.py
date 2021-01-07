#http://dev.pygame.org/project-Rect+Collision+Response-1061-.html
#https://www.pygame.org/docs/ref/music.html#pygame.mixer.music.load
import os
import random
import pygame

# Class for the orange dude
class Player(object):
    def __init__(self):
        self.rect = pygame.Rect(20, 20, 13, 13)

    def move(self, dx, dy):
        
        # Move each axis separately. Note that this checks for collisions both times.
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)
    
    def move_single_axis(self, dx, dy):
        
        # Move the rect
        self.rect.x += dx
        self.rect.y += dy

        # If you collide with a wall, move out based on velocity
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0: # Moving right; Hit the left side of the wall
                    self.rect.right = wall.rect.left
                if dx < 0: # Moving left; Hit the right side of the wall
                    self.rect.left = wall.rect.right
                if dy > 0: # Moving down; Hit the top side of the wall
                    self.rect.bottom = wall.rect.top
                if dy < 0: # Moving up; Hit the bottom side of the wall
                    self.rect.top = wall.rect.bottom

# Nice class to hold a wall rect
class Wall(object):
    
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 13, 13)

# Initialise pygame
pygame.init()
pygame.mixer.music.load("BGM.wav")
pygame.mixer.music.play(-1)
# Set up the displayF
pygame.display.set_caption("Dino Maze #1 - Find The Ending")
screen = pygame.display.set_mode((795, 285))


clock = pygame.time.Clock()
walls = [] # List to hold the walls
player = Player() # Create the player

# Holds the level layout in a list of strings.
level = [
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
"W   WW       W   W   W   W   W  W           W    W",
"W   WW W W W   W W W       W      WWWWW W W W WW W",
"W      W W WWWWW WWWWWW WWWWWW  WWW       W WWWW W", 
"WWWWWWWW W WW    W      W   WW  W   WWWWWWW      W",
"W        W WW WW WWWWWWWW WWW  WW WW      WWWWWWWW",
"W WWWWWWWW WW W           WW  W   W  WWWW WW     W",
"W           W W WWWWWWWWWWW  W  WW  W   W WW W W W",
"WW WWW WWWW W W        W    W  WW  W  WWW WW W WWW",   
"W  W   WW   W WWWWWW WWWW  W  WW  WWW  WW    W   W",  
"W  W W W  WWW W   W       WW     WWWW  WWWWWWWWW W",  
"W      W  W   W W W  W WWWWWWWWWWWW   WW W   W   W",
"WW WWWWW  W WWW WWWW W        W     W W    W   W W",
"W      W  W   W  WW  WWWWWWWW W WWWWWWW WWWW WWWWW",
"WWWWWW WW   W    W  WWW   W   W      W  W WW W   W",
"W   W  W WWWWWWW WWWWWW W W W WWWWWW WWWW WW   E W",
"W W    W             W  W   W             WWWW   W",
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
]

# Parse the level string above. W = wall, E = exit
x = y = 0
for row in level:
    for col in row:
        if col == "W":
            
            Wall((x, y))
        if col == "E":
            end_rect = pygame.Rect(x, y, 16, 16)
        x += 16
    y += 16
    x = 0

running = True
while running:
    
    clock.tick(60)
    
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False
    
    # key code
    key = pygame.key.get_pressed()
    if key[pygame.K_UP]:
        player.move(0, -4)
    if key[pygame.K_DOWN]:
        player.move(0, 4)
    if key[pygame.K_LEFT]:
        player.move(-4, 0)
    if key[pygame.K_RIGHT]:
        player.move(4, 0)

    if player.rect.colliderect(end_rect):
        print("You win!") # call second Level Function here
        raise SystemExit
    
    # Background/Colour of maze
    mazebgscreen = pygame.image.load("Gravel.gif")
    screen.blit(mazebgscreen,(0,0))
    for wall in walls:
        pygame.draw.rect(screen, (220, 220,220), wall.rect)
    pygame.draw.rect(screen, (255, 0, 0), end_rect)
    pygame.draw.rect(screen, (124,252, 0), player.rect)
    pygame.display.flip()
pygame.quit()
