import pygame

class Meca:
    
    def __init__(self,screen):
        self.screen = screen 
        self.font = pygame.font.Font("../dialogs/dialog_font.ttf",50)
        self.var = True
    
    #methode qui va calculer les point de vie en fonction des degat et le renvoie a la methode player qui affiche la bare
    def health(self):
        print("coucou")
        
    #calcule les xp gagnier et renvoie a player qui le desinne
    def xp(self):
        print("couou")
    
    #calcule les piece et le renvoie  a player qui l'affiche 
    def coin(self):
        print("je sais pas si on en as besoin")
        
        
    def render(self,var):
        
        
        #self.box = pygame.image.load('../img/info_perso.png')
        #self.screen.blit(self.box,(0,0))
        
        #pour afficher pausse
        if self.var:
            
            text = self.font.render("PAUSE", False, (0,0,0))
            self.screen.blit(text,(520, 0))
           
            print("pausse")
            

        
        
        
    #prochainement ca sera un inventaire
        