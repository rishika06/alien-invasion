import pygame
from pygame.sprite import Sprite

#__ A CLASS TO MANAGE THE SHIP
class Ship(Sprite):

    def __init__(self, ai_game):
        #__ INITIALIZE THE SHIP AND SET ITS STARTING POSITION
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        #__ LOAD THE SHIP IMAGE AND GET ITS RECT
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        #__ START EACH NEW SHIP AT THE BOTTOM CENTER OF THE SCREEN
        self.rect.midbottom = self.screen_rect.midbottom

        #__ STORE A DECIMAL VALUE FOR THE SHIP'S HORIZONTAL POSITION
        self.x = float(self.rect.x)

        #__ MOVEMENT FLAG
        self.moving_right = False
        self.moving_left = False

    def update(self):
        #__ UPDATE THE SHIP'S POSITION BASED ON THE MOVEMENT FLAG
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        
        self.rect.x = self.x
    
    def blitme(self):
        #__ DRAW THE SHIP AT ITS CURRENT LOCATION
        self.screen.blit(self.image, self.rect)

    #__CENTER THE SHIP ON THE SCREEN
    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)