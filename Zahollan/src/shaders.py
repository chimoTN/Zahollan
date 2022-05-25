import pygame

class Shaders():
    
    def __init__(self,screen):
        self.current_moment_day = "day"
        
        self.screen = screen
        
        self.shader = pygame.image.load('../img/brouillard.png')
        self.shader = pygame.transform.scale(self.shader, (800,600))
        
        if self.current_moment_day == "night":
            self.shader.fill((75, 0, 130,150))
        else:
            self.shader.fill((175, 100, 130,150))
        
    def set_day(self):
        self.current_moment_day = "day"
        
        print("ces le jour")
        
        
    def set_night(self):
        self.current_moment_day = "night"
        
        print("in night ca mere")
        
    def set_crepuscule(self):
        self.current_moment_day = "crepuscule"
        
    def set_aurore(self):
        self.current_moment_day = "aurore"
        
        
    #l'affichage
    def render(self, screen):
        
        self.screen.blit(self.shader, (0, 0))