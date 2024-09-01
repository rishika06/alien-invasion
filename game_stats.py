
#__TRACK STATISTICS FOR ALIEN INVASION
class GameStats:
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        #__START ALEIN INVASION IN AN ACTIVE STATE
        self.game_active = False

        # __HIGH SCORE SHOULD NEVER BE RESET
        self.high_score = 0

    #__INITIALIZE STATISTICS THAT CAN CHANGE DURING THE GAME
    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1