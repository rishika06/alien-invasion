import pygame
from pygame.sprite import Sprite

#__ A CLASS TO MANAGE THE BULLETS FIRED FROM THE SHIP
class Bullet(Sprite):
 
#__ CREATE A BULLET OBJECT AT THE SHIP'S CURRENT POSITION
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color
        #__ CREATE A BULLET AT RECT(0,0)
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        #__ STORE THE BULLET'S POSITION AS A DECIMAL VALUE
        self.y = float(self.rect.y)
    
    #__ MOVE THE BULLET UP THE SCREEN
    def update(self):
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    #__ DRAW THE BULLET ON THE SCREEN
    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
