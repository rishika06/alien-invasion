class Settings:

    def __init__(self):
        
        #__ SCREEN SETTINGS
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.ship_speed = 1.5
        self.ship_limit = 3

        #__BULLET SETTINGS
        self.bullet_speed = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        #__ ALIEN SETTINGS
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        #__FLEET DIRECTION OF 1 REPRESENTS RIGHT AND -1 REPRESENTS LEFT
        self.fleet_direction = 1

        #__HOW QUICKLY THE GAME SPEEDS UP
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()
    
    #__INITIALIZE SETTINGS THAT CHANGE THROUGHOUT THE GAME
    def initialize_dynamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0
        self.fleet_direction = 1
        self.alien_points = 50
    
    #__INCREASE SPEED SETTINGS
    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)

