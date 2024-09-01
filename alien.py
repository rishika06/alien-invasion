import pygame
from pygame.sprite import Sprite

#__ A CLASS TO REPRESENT A SINGLE ALIEN IN THE FLEET

class Alien(Sprite):
    def __init__(self, ai_game):
        #__ INITIALIZE THE ALIEN AND SET ITS STARTING POINT
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        #__ LOAD THE ALIEN IMAGE AND SET ITS RECT ATTRIBUTE
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        #__ START EACH NEW ALEIN AT THE TOP LEFT OF THE SCREEN
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #__STORE THE ALIENS EACT HORIZONTAL POSITON
        self.x = float(self.rect.x)
    
    #__MOVE THE ALIEN TO THE RIGHT OR LEFT
    def update(self):
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x
    
    #__RETURN TRUE IF ALIEN IS AT THE EDGE
    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
        