import pygame.font

class Button:

    def __init__(self, ai_game, msg):
        
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        #__SET THE DIMENSIONS AND PROPERTIES OF THE BUTTON
        self.width, self.height = 200, 50
        self.button_color = (14, 132, 26)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        #__BUILD THE BUTTONS RECT OBJECT AND CENTER IT
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        #__THE BUTTON MSG NEEDS TO BE PREPED ONLY ONCE
        self._prep_msg(msg)

    #__TURN MSG INTO A RENDERED IMAGE AND CENTER TEXT ON THE BUTTON
    def _prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color,
        self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    #__DRAW BLANK BUTTON AND THEN DRAW MESSAGE
    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
