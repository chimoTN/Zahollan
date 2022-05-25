import pygame
from src.shaders import Shaders
class Time:
    
    X_POSITION = 730
    Y_POSITION = 30
        
    def __init__(self,screen):
        
        self.current_time = 12
        self.seconds = 0
        self.micro_sec = 0
        
        self.screen = screen
        self.time = Shaders(screen)
        
        self.box = pygame.image.load('../img/time.png')
        self.box = pygame.transform.scale(self.box, (100,70))
        self.font = pygame.font.Font("../dialogs/dialog_font.ttf",18)
        self.run = True
        
        
        
    #les seconde
    def tpm_sec(self):
        
        #si ca fait plus que 60 seconds
        self.micro_sec = self.micro_sec + 1
        
        
        if self.micro_sec >= 60:
            self.seconds = self.seconds + 1
            self.micro_sec = 0
            
            
        if self.seconds >= 60:
            self.tpm_heur()
            self.seconds = 0
            
            
    #les heur
    def tpm_heur(self):
    
        if self.current_time <= 22 :
            self.current_time = self.current_time + 1
            
        else:
            self.current_time = 0
        
    
    #regarde les changement de temp pour passer la nuit
    def save_moment_day(self):
        
        print("in def")
        
        #si ces le soir
        if self.current_time > 20:
            self.time.set_night()()
            print("go night")
            
        #le crepuscule
        elif self.current_time > 17:
            self.time.set_day()
        
        #le jour
        elif self.current_time > 9:
            self.time.set_day()
            
        #l'aurore
        elif self.current_time > 7:
            self.time.set_day()
        
        else:
            self.time.set_night()
            print("go day")
    
    #l'affichage
    def render(self, screen):
        
        if self.run:
            
            #pour avoir les effet de nuit
            #self.save_moment_day()
            
            #on apelle les seconde qui apelle les heur ..
            self.tpm_sec()
            
            #on construit la chaine pour l'heur
            sec = int(self.seconds)
            temps = str(self.current_time) + " : "+ str(sec)
            
            #on applique le texte et l'image
            screen.blit(self.box,(800,10))
                
            text = self.font.render(temps, False, (0,0,0))
            screen.blit(text,(self.X_POSITION + 85, self.Y_POSITION - 15 ))
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            