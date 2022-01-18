
class GameStats():
    """Track statistics for Alien Invasion"""

    def __init__(self, ai_game):
        """Initialize statistics"""
        self.settings = ai_game.settings
        self.reset_stats()

        #Startet das Spiel im inaktiven Zustand.
        self.game_active = False

        #Der Highscore darf nie zurückgesetzt werden.
        self.high_score = 0

        #Startet Alien Invasion im aktiven Zustand
        #self.game_active = True


    def reset_stats(self):
        """Initalize statistics that can change during the game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1



