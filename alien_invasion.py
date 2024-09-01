import sys
import pygame
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:

    def __init__(self):
        #__ INITIALIZE THE GAME AND CREATE GAME RESOURCES
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        #__CREATE AN INSTANCE TO STORE GAME STATISTICS AND SCOREBOARD
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        #__START ALIEN INVASION IN AN INACTIVE STATE
        self.game_active = False

        #__MAKE THE PLAY BUTTON
        self.play_button = Button(self, "Play")

    def run_game(self):
    #__ THIS IS THE MAIN LOOP FOR THE GAME
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                # self.bullets.update()
                self._update_bullets()
                self._update_aliens()
           
            self._update_screen()

    #__ KEYBOARD AND MOUSE EVENTS
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    #__START A NEW GAME WHEN THE PLAYER CLICKS PLAY
    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            
            #__RESET THE GAME STATISTICS
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            #__GET RID OF ANY REMAINING ALIENS OR BULLETS
            self.aliens.empty()
            self.bullets.empty()
            
            #__CREATE A NEW FLEET AND CENTER THE SHIP
            self._create_fleet()
            self.ship.center_ship()

            #__HIDE THE MOUSE CURSOR
            pygame.mouse.set_visible(False)
    
   #__ RESPOND TO KEYPRESSES
    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    #__ CREATE A NEW BULLET AND ADD IT TO THE BULETS GROUP
    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    #__ RESPOND TO KEY RELEASES
    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    #__ UPDATE POSITION OF BULLETS AND GET RID OF THE OLD BULLETS
    def _update_bullets(self):
        #__ UPDATE BULLET POSITIONS
        self.bullets.update()
        #__ GET RID OF BULLETS THAT HAVE DISAPPEARED
        for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()


    #__RESPOND TO BULLET ALIEN COLLISION
    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        
        #__DESTROY EXISTING BULLETS AND CREATE NEW FLEET
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # __INCREASE LEVEL
            self.stats.level += 1
            self.sb.prep_level()

    
     #__ CREATE THE FLEET OF ALIENS
    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        #__ DETERMINE THE NO OF ROWS OF ALIENS THAT FIT ON THE SCREEN
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -(3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        #__ CREATE THE FULL FLEET OF ALIENS
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

     #__CREATE THE FIRST ROW OF ALIENS
    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)
    
    #__ RESPOND AS NEEDED IF ANY ALIEN HAVE REACHED EDGE
    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    #__DROP THE ENTIRE FLEET AND CHANGE THE FLEET'S DIRECTION
    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    
    #__RESPOND TO THE SHIP BEING HIT BY AN ALIEN
    def _ship_hit(self):
        if self.stats.ships_left > 0:
            #__DECREMENT SHIPS_LEFT
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            #__GET RID OF ANY REMAINING ALIENS AND BULLETS
            self.aliens.empty()
            self.bullets.empty()
            #__CREATE A NEW FLEET AND CENTER THE SHIP
            self._create_fleet()
            self.ship.center_ship()
            #__PAUSE
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    #__CHECK IF ANY ALIENS HAVE REACHED THE BOTTOM OF THE SCREEN
    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #__TREAT THIS THE SAME AS IF THE SHIP GOT HIT
                self._ship_hit()
                break

    #__UPDATE THE POSITION OF ALL THE ALIENS IN THE FLEET
    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

        #__LOOK FOR ALIEN-SHIP COLLISION
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        #__LOOK FOR ALIENS HITTING THE BOTTOM OF THE SCREEN
        self._check_aliens_bottom()

    
    #__ UPDATE IMAGES ON SCREEN AND FLIP TO NEW SCREEN
    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # __DRAW THE SCORE INFORMATION
        self.sb.show_score() 

        #__DRAW THE PLAY BUTTON IF THE GAME IS INACTIVE
        if not self.stats.game_active:
            self.play_button.draw_button()

        #__ MAKES THE MOST RECENTLY DRAWN SCREEN VISISBLE
        pygame.display.flip()



if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()    