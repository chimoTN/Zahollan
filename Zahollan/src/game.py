import pygame
import pytmx
import pyscroll

from src.player import Player
from src.map import MapManager
from src.dialogue import DialogBox
from src.time import Time
from src.shaders import Shaders
from src.mecanique import Meca

class Game:
    
    #CONSTRUCTEUR
    def __init__(self):
        
        #la fenetre de jeu
        self.screen = pygame.display.set_mode((900,700))
        pygame.display.set_caption("Zahollan")
        
        #generer notre joueur
        self.player = Player()
        self.map_manager = MapManager(self.screen, self.player)
        
        #box de dialogue
        self.dialog_box = DialogBox()
        
        #affichage du temp
        self.time = Time(self.screen)
        self.shaders = Shaders(self.screen)
        
        #pour le temp d'action FPS(quand le perso bouge)
        self.clock = pygame.time.Clock()
        
        #jeu en pause = true
        self.pausse = False
        
        self.meca = Meca(self.screen)
        
        
    #POUR SAVOIR QU'ELLE TOUCHE ET ACTIONNER    
    def handle_input(self):
        pressed = pygame.key.get_pressed()
        
        if pressed[pygame.K_UP]:
            self.player.move_up()
            
        if pressed[pygame.K_DOWN]:
            self.player.move_down()
            
        if pressed[pygame.K_LEFT]:
            self.player.move_left()
            
        if pressed[pygame.K_RIGHT]:
            self.player.move_right()
            
        
        
    #intervient des les collision
    def update(self):
        self.map_manager.update()
      
    def pause(self):
        
        #True = pause 
        if self.pausse == False : 
            self.pausse = True
            self.player.pause(self.screen, self.pausse)

            
        else:
            self.pausse = False
            

        
    #BOUCLE DU JEU
    def run(self):

 
        #boucle du jeu
        play = True 
        
        while play:
            
            #pour enregistrer ca location
            self.player.save_location()
            #appelle la methode de deplacement
            self.handle_input()
            #appelle la methode update
            self.update()
            
            #va desiner autoure du perso (centrage)
            self.map_manager.draw()

            #les box de discution
            self.dialog_box.render(self.screen)
            
            #le temp de la map ET les info joueur
            self.time.render(self.screen)
            self.player.render(self.screen)
            #les filtre de la map (nuit, brouillard)
            #self.shaders.render(self.screen)
            
            pygame.display.flip()
            
            #detection de tapage de touche
            for event in pygame.event.get():
                #Si tu click sur la croix rouge
                if event.type == pygame.QUIT:
                    play = False
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.map_manager.check_npc_collisions(self.dialog_box)
                
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        self.pause()
                    
            self.screen.fill(4)
            
            #False = pause
            if self.pausse == False : 
                self.clock.tick(60)
            
            else:
                self.clock.tick(1)
                
        pygame.quit()
    
    