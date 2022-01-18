class Settings():
    """A class to store all the games settings"""

    def __init__(self):

        #Bildschirmeinstellungen
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Schiffseinstellungen
        self.ship_speed = 1.5
        self.ship_limit = 2

        #Geschosseinstellugen
        self.bullet_speed = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 4

        #invasionsschiffseinstellungen
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # Der Wert 1 für fleet_direction bedeutet "nach rechts", -1 "nach links".
        self.fleet_direction = 1

        #Stärke der Beschleunigung des Spiels
        self.speedup_scale = 1.1

        #Stärke der Punktwerterhöhung bei Treffern
        self.score_scale = 1.5

        self.initialize_dynamic_settings()




    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game"""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        #Der Wert 1 für fleet_direction bedeutet "nach rechts", -1 "nach links"
        self.fleet_direction = 1

        #Punktwertung
        self.alien_points = 50


    def increase_speed(self):
        """increase speed settings and alien point values"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)




