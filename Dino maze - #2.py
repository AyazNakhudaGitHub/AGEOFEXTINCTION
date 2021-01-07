#http://dev.pygame.org/project-Rect+Collision+Response-1061-.html
#https://www.pygame.org/docs/ref/music.html#pygame.mixer.music.loadimport os
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
# Set up the display
pygame.display.set_caption("Dino Maze #2 - Find The Ending")
screen = pygame.display.set_mode((940, 590))

clock = pygame.time.Clock()
walls = [] # List to hold the walls
player = Player() # Create the player

# Holds the level layout in a list of strings.
level = [
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
"W    W    W   WWW W                                       W",
"W    W  W   W   W   WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW WW  W",
"W WWWW WWWWWWWW W W W    W   W                         W WW",
"W    W        W W W    W W W W WWWW WWWWWWWWWWWWWWW WWWW  W",
"WWWW WWWWWWWW W W WWWWWW W W W W    W W   W            WW W",
"W    W        W W      W W W     W  W   W WWWWWWWWW W WW  W",
"W WWWW WWWWWWWW W WWWW W W WWWWWWWW WWWWW W       W W  W WW",
"W    W        W   W    W W  W   W   W     W WWWWW W  W W  W",
"WWWW WWWWWWWW WWWWWWWW W WW W W W W W WWWWW     W WW W WW W",
"W             W        W WW   W   W W    WWWWWW W  W   W  W",
"WWWWW WW WWWWWWWW  WWWWW WWWWWWWWWW WWWW W      W  WWWWW WW",
"W      W        W   W                  W WWW WWWW         W",
"W WWWW W WWWWWWWWWW W WWWW WWWWWWWWWWW W   W    WWWWWWWWWWW",
"W W      WW    WW   W W W    W   W   W WWW WWW            W",
"W WWWWWWWW  WW WW WWW   W WW W W W W       W  WWWWWWWWWWW W",
"W W        WWW WW WWWWWWW WW W W W WWWWWWWWW              W",
"W   WWWWWWW    WW      W  WW W W W     W     WWWWWWWWWWWWWW",
"WWWWWWWWWWW WWWWWWWWWW WWWWW W W W WWW   WWWWW            W",
"W      W             W     W W W W  WWWWWWWWWWWWWWWWWWWW  W",
"W WWW  WWWWWW WWWWWW WWWWW W W W  W W   W                 W",
"W W W         W      W   W W W WW W W W W W  WWWWWWWWWWW  W",
"W W WWWWWW WWWW WWWW W W W W W  W W   W   W  W            W",
"W W WWWWWW WWWW    W   W W W    W WWWWWWWWWWWW WWWWWWWWWWWW",
"W W           WWWW WWWWWWW WWWW W         W               W",
"W WWWWWWWWWWW WW   W          WWWWWWWWWWW WWWWW WWWWWWWWW W",
"W       W   W  WW    WWWWWWW  WW   W WW   W   W W   W   W W",
"WWWWWW  W W WW  WW  W   W     W  W W    W   W W   W   W W W",
"W       W W  WW  WW   W W WWWWWWWW WWWWWWWWWW WWWWWWWWWWW W",
"W WWWWWWW WW  WW  WW  W W              WE           W     W",
"W W       WW  WWW WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW WWWWW",
"W WWW W       WWW W            W  W W W W   W   W   W W   W",
"W   W WWWW WWW    W WWWWWWWWWW W  W W W W W W W W W W W W W",
"W W W    W W   W  W          W W      W   W   W   W W W W W",
"W W WWWW W W WWW  WWWWWWWWW  W W  WWWWWWWWWWWWWWWWWWWWWWW W",
"W W      W   W               W                            W",
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
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
    
    # Move the player if an arrow key is pressed
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        player.move(-5, 0)
    if key[pygame.K_RIGHT]:
        player.move(5, 0)
    if key[pygame.K_UP]:
        player.move(0, -5)
    if key[pygame.K_DOWN]:
        player.move(0, 5)

    if player.rect.colliderect(end_rect):
        print("You win!")
        raise SystemExit
    # Draw the scene
    mazebgscreen = pygame.image.load("Gravel.gif")
    screen.blit(mazebgscreen,(0,0))
    for wall in walls:
        pygame.draw.rect(screen, (220, 220,220), wall.rect)
    pygame.draw.rect(screen, (255, 0, 0), end_rect)
    pygame.draw.rect(screen, (124,252,0), player.rect)
    pygame.display.flip()
pygame.quit()
