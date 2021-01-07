#By: Tommy, Steven, Hunter and Ayaz
#Date: June 6, 2018
#Purpose: This is a game where a player must avoid obstacles and enemies to reach a final destination.

#http://dev.pygame.org/project-Rect+Collision+Response-1061-.html



#get a high score counter make better graphics
#animations
#make new background make bteer graphics for buttons make instruction page with the new gif enemies 
#add a screen that describes the items 
#use stevens collide code to exit the level
#wrtie up psuedocode



#Import all the moduals here becuase you can't import them in a function

import pygame, random, sys
from pygame.locals import *
import os
import random
import pygame

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((940,600))

pygame.mixer.music.load("Off Limits.wav")
pygame.mixer.music.play(-1)

background = (0,0,0)


def instructionspage():

    global backButton

    InstructionSurface = pygame.display.set_mode((940,600),0,0)
    instructionimage = pygame.image.load("instructions page finished.gif")
    InstructionSurface.blit(instructionimage,(0,0))
    pygame.display.update()

    back = pygame.image.load("Quit.png")# change this to back
    backButton = back.get_rect()
    backButton.move_ip(650,395)
    InstructionSurface.blit(back,backButton)
    pygame.display.update()
    backbuttonloop()





def backbuttonloop():
    loop = True
    
    while loop:
        for event in pygame.event.get():
            if event.type == QUIT:             
                quitgame()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos = event.pos
                    if backButton.collidepoint(mousePos):
                        format(mousePos)
                        mainmenu()
                        

            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    pygame.quit()

    

def quitgame():
    pygame.quit()
    quit()


def mainmenu():
    global playButton
    global instructionsButton
    global qtButton

    wSurface = pygame.display.set_mode((940, 600),0,0)
    wSurface.fill(background)

    backgroundimage = pygame.image.load("NewStartScreen.gif")
    wSurface.blit(backgroundimage,(0,0))

    play = pygame.image.load('PlayGame.png')
    playButton = play.get_rect()
    playButton.move_ip(105, 300)
    wSurface.blit(play,playButton)

    instructions = pygame.image.load('Instructions.png')
    instructionsButton = instructions.get_rect()
    instructionsButton.move_ip(380,300)
    wSurface.blit(instructions,instructionsButton)

    qt = pygame.image.load('Quit.png')
    qtButton = qt.get_rect()
    qtButton.move_ip(650, 300)
    wSurface.blit(qt, qtButton)


    pygame.display.flip()

    func = True
    
    while func:
        for event in pygame.event.get():
            if event.type == QUIT:             
                quitgame()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos = event.pos  
                    if playButton.collidepoint(mousePos):
                        #print('button was pressed at {0}'.format(mousePos))
                        level1()

                    elif instructionsButton.collidepoint(mousePos): #change the if back into an elif when u un comment theprevious statement
                        format(mousePos)
                        instructionspage()

                    elif qtButton.collidepoint(mousePos):
                        format(mousePos)
                        pygame.quit()

                        
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    pygame.quit()

def level1():
    # Global constants
     
    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
     
    # Screen dimensions
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
     
     
    class Player(pygame.sprite.Sprite):
        """
        This class represents the bar at the bottom that the player controls.
        """
     
        # -- Methods
        def __init__(self):
            """ Constructor function """
     
            # Call the parent's constructor
            super(Player,self).__init__()
            
            # This is an image loaded from the disk.
            self.image = pygame.image.load("images/Walk ( 1).gif").convert_alpha()
     
            # Set a referance to the image rect.
            self.rect = self.image.get_rect()
     
            # Set speed vector of player
            self.change_x = 0
            self.change_y = 0
     
            # List of sprites we can bump against
            self.level = None

            # Load images (player)
            self.frame = 0
            
            self.walk_right_images = []
            for i in range(1, 10):
                temp_image = pygame.image.load("images/Walk (%2i).gif" %(i)).convert_alpha()
                self.walk_right_images.append(temp_image)

            self.walk_left_images = []
            for i in range(1, 10):
                temp_image = pygame.image.load("images/Walkl (%2i).gif" %(i)).convert_alpha()
                self.walk_left_images.append(temp_image)
            
        def update(self):
            """ Move the player. """
            # Gravity
            self.calc_grav()
     
            # Move left/right
            self.rect.x += self.change_x
     
            # See if we hit anything
            block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
            for block in block_hit_list:
                # If we are moving right,
                # set our right side to the left side of the item we hit
                if self.change_x > 0:
                    self.rect.right = block.rect.left
                elif self.change_x < 0:
                    # Otherwise if we are moving left, do the opposite.
                    self.rect.left = block.rect.right
     
            # Move up/down
            self.rect.y += self.change_y
     
            # Check and see if we hit anything
            block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
            for block in block_hit_list:
     
                # Reset our position based on the top/bottom of the object.
                if self.change_y > 0:
                    self.rect.bottom = block.rect.top
                elif self.change_y < 0:
                    self.rect.top = block.rect.bottom
     
                # Stop our vertical movement
                self.change_y = 0
     
        def calc_grav(self):
            """ Calculate effect of gravity. """
            if self.change_y == 0:
                self.change_y = 1
            else:
                self.change_y += .35
     
            # See if we are on the ground.
            if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
                self.change_y = 0
                self.rect.y = SCREEN_HEIGHT - self.rect.height
     
        def jump(self):
            """ Called when user hits 'jump' button. """
     
            # move down a bit and see if there is a platform below us.
            # Move down 2 pixels because it doesn't work well if we only move down 1
            # when working with a platform moving down.
            self.rect.y += 2
            platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
            self.rect.y -= 2
     
            # If it is ok to jump, set our speed upwards
            if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
                self.change_y = -10
     
        # Player-controlled movement:
        def go_left(self):
            """ Called when the user hits the left arrow. """
            self.change_x = -6
            self.image = self.walk_left_images[self.frame%len(self.walk_left_images)]
            
        def go_right(self):
            """ Called when the user hits the right arrow. """
            self.change_x = 6
            self.image = self.walk_right_images[self.frame%len(self.walk_right_images)]
            
        def stop(self):
            """ Called when the user lets off the keyboard. """
            self.change_x = 0

###########################################################################3
    class Enemy(pygame.sprite.Sprite):
        def __init__(self):
            """ Constructor function """
     
            # Call the parent's constructor
            super(Enemy,self).__init__()
            
            # This is an image loaded from the disk.
            self.image = pygame.image.load("images/Caveman ( 1).gif").convert_alpha()
     
            # Set a referance to the image rect.
            self.rect = self.image.get_rect()
     
            # Set speed vector of enemy
            self.change_x = 0
            self.change_y = 0
     
            # List of sprites we can bump against
            self.level = None

            # Load images (enemy 1)
            self.frame = 0
            self.caveman_right_images = []
            for i in range(1, 9):
                temp_image = pygame.image.load("images/Caveman (%2i).gif" %(i)).convert_alpha()
                self.caveman_right_images.append(temp_image)

            self.caveman_left_images = []
            for i in range(1, 9):
                temp_image = pygame.image.load("images/Cavemanl (%2i).gif" %(i)).convert_alpha()
                self.caveman_left_images.append(temp_image)

        def update(self):
            # Move left/right
            self.rect.x += self.change_x
     
            # See if we hit anything
            block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
            for block in block_hit_list:
                # If we are moving right,
                # set our right side to the left side of the item we hit
                if self.change_x > 0:
                    self.rect.right = block.rect.left
                elif self.change_x < 0:
                    # Otherwise if we are moving left, do the opposite.
                    self.rect.left = block.rect.right
     
            # Move up/down
            self.rect.y += self.change_y
     
            # Check and see if we hit anything
            block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
            for block in block_hit_list:
     
                # Reset our position based on the top/bottom of the object.
                if self.change_y > 0:
                    self.rect.bottom = block.rect.top
                elif self.change_y < 0:
                    self.rect.top = block.rect.bottom
     
                # Stop our vertical movement
                self.change_y = 0
            
#####################################################################
    class Platform(pygame.sprite.Sprite):
        """ Platform the user can jump on """
     
        def __init__(self, width, height):
            """ Platform constructor. Assumes constructed with user passing in
                an array of 5 numbers like what's defined at the top of this code.
                """
            super(Platform, self).__init__()
     
            self.image = pygame.Surface([width, height])
            self.image.fill(GREEN)
            self.rect = self.image.get_rect()
     
     
    class Level():
        """ This is a generic super-class used to define a level.
            Create a child class for each level with level-specific
            info. """
     
        def __init__(self, player, enemy):
            """ Constructor. Pass in a handle to player. Needed for when moving
                platforms collide with the player. """
            self.platform_list = pygame.sprite.Group()
            self.enemy_list = pygame.sprite.Group()
            self.player = player
            self.enemy = enemy
     
            # How far this world has been scrolled left/right
            self.world_shift = 0
     
        # Update everythign on this level
        def update(self):
            """ Update everything in this level."""
            self.platform_list.update()
            self.enemy_list.update()
     
        def draw(self, screen):
            """ Draw everything on this level. """
     
            # Draw the background
            firstlevelbg = pygame.image.load("firstlevel.gif")
            screen.blit(firstlevelbg,(0,0))
            #pygame.display.update()

            # Draw all the sprite lists that we have
            self.platform_list.draw(screen)
            self.enemy_list.draw(screen)
     
        def shift_world(self, shift_x):
            """ When the user moves left/right and we need to scroll
            everything: """
     
            # Keep track of the shift amount
            self.world_shift += shift_x
     
            # Go through all the sprite lists and shift
            for platform in self.platform_list:
                platform.rect.x += shift_x
     
            for enemy in self.enemy_list:
                enemy.rect.x += shift_x
     
     
    # Create platforms for the level
    class Level_01(Level):
        """ Definition for level 1. """
     
        def __init__(self, player, enemy):
            """ Create level 1. """
     
            # Call the parent constructor
            Level.__init__(self, player, enemy)
     
            self.level_limit = -2000
     
            # Array with width, height, x, and y of platform
            level = [[150, 100, 500, 530],          #first number controls the length of the box                       
                     [150, 100, 900, 530],          #second number controls the height of the box  
                     [150, 200, 1000, 400],         # third number controls how deep into the map the box is           
                     [50, 40, 750, 250],
                     [150, 150, 1400, 450],
                     [50, 40, 1700, 300],           #last number controls how close to the ground the box is (430 is th closest to the ground
                     [150, 100, 1900, 530],
                     [150, 1000, 1800, 530],
                   ]
            # Go through the array above and add platforms
            for platform in level:
                block = Platform(platform[0], platform[1])
                block.rect.x = platform[2]
                block.rect.y = platform[3]
                block.player = self.player
                self.platform_list.add(block)

            self.platform_list.add(enemy)

     
    def main():
        """ Main Program """
        pygame.init()
     
        # Set the height and width of the screen
        size = [SCREEN_WIDTH, SCREEN_HEIGHT]
        screen = pygame.display.set_mode(size)
     
        pygame.display.set_caption("Side-scrolling Platformer")
     
        # Create the player
        player = Player()
        enemy = Enemy()
        # Create all the levels
        level_list = []
        level_list.append(Level_01(player, enemy))
        # Set the current level
        current_level_no = 0
        current_level = level_list[current_level_no]
     
        active_sprite_list = pygame.sprite.Group()
        player.level = current_level
        enemy.level = current_level
##########################################
        
 ###############################################           
        
        player.rect.x = 340
        player.rect.y = SCREEN_HEIGHT - player.rect.height
        active_sprite_list.add(player)

        enemy.rect.x = 200
        enemy.rect.y = SCREEN_HEIGHT - enemy.rect.height
        active_sprite_list.add(enemy)

     
        # Loop until the user clicks the close button.
        done = False
     
        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()
     
        # -------- Main Program Loop -----------
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
     
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT and player.change_x < 0:
                        player.stop()
                    if event.key == pygame.K_RIGHT and player.change_x > 0:
                        player.stop()

            pressed = pygame.key.get_pressed()
            if pressed[K_LEFT]:
                player.frame += 1
                player.go_left()
            if pressed[K_RIGHT]:
                player.frame += 1
                player.go_right()
            if pressed[K_UP]:
                player.jump()

#######################################################################                
     
            # Update the player.
            active_sprite_list.update()
     
            # Update items in the level
            current_level.update()
     
            # If the player gets near the right side, shift the world left (-x)
            if player.rect.right >= 500:
                diff = player.rect.right - 500
                player.rect.right = 500
                current_level.shift_world(-diff)
     
            # If the player gets near the left side, shift the world right (+x)
            if player.rect.left <= 120:
                diff = 120 - player.rect.left
                player.rect.left = 120
                current_level.shift_world(diff)
     
            # If the player gets to the end of the level, go to the next level
            current_position = player.rect.x + current_level.world_shift
            if current_position < current_level.level_limit:
                player.rect.x = 120
                
                if current_level_no < len(level_list)-1:
                    current_level_no += 1
                    current_level = level_list[current_level_no]
                    player.level = current_level

     
            # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
            current_level.draw(screen)
            active_sprite_list.draw(screen)
     
            # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
     
            # Limit to 60 frames per second
            clock.tick(60)
     
            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
     
        # Be IDLE friendly. If you forget this line, the program will 'hang'
        # on exit
            
            if current_position < -1700:
                maze1()

        
        pygame.quit()
     
    if __name__ == "__main__":
        main()



def maze1():
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
            mainmenu()
        # Draw the scene
        mazebgscreen = pygame.image.load("Gravel.gif")
        screen.blit(mazebgscreen,(0,0))
        for wall in walls:
            pygame.draw.rect(screen, (220, 220,220), wall.rect)
        pygame.draw.rect(screen, (255, 0, 0), end_rect)
        pygame.draw.rect(screen, (124,252,0), player.rect)
        pygame.display.flip()
    pygame.quit()





mainmenu() 
backbuttonloop()
instructionspage()
