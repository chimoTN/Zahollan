import pygame 

from src.animation import Animation
from idlelib.idle_test.test_configdialog import dialog

class Entity(Animation):
    
    #CONSTRUCTEUR
    def __init__(self, name, x, y):
        super().__init__(name)
        self.image = self.get_image(0,0)
        self.image.set_colorkey([0,0,0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()
        
        #pv / degat
        self.pv = 100
        self.degat = 10
        self.defance = 5
        
        
    #POUR LA COLISION DU JOUEUR (genre ces que a ces pied)    
    def save_location(self):
        self.old_position = self.position.copy()
        
    
    #MODIFIE LA POSITION DU JOUEUER
    def move_right(self):
        self.change_animation("right")
        self.position[0] += self.speed
    
    def move_left(self):
        self.change_animation("left")
        self.position[0] -= self.speed
        
    def move_up(self):
        self.change_animation("up")
        self.position[1] -= self.speed
        
    def move_down(self):
        self.change_animation("down")
        self.position[1] += self.speed
        
    #position du joueeur
    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        
    #SI RECT EN CONTACT AVEC COLLITION ON REPLACE LE JOUEUR A LA POSITION AVANT
    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        
        
        
        
    
class Player(Entity):
    
    def __init__(self):
        super().__init__("player", 0, 0)
                
        self.box = pygame.image.load('../img/info_perso.png')
        self.box = pygame.transform.scale(self.box, (220,110))
        
        self.font = pygame.font.Font("../dialogs/dialog_font.ttf",18)
                                          
        
    
        #pv / degat
        self.pv = 100
        self.degat = 10
        self.defance = 5
        self.xp = 0
        self.coins = 0
        self.lvl = 1
        self.var = True
    #Affichage la bare de vie du joueur
    def health_screen(self):
        print("vie")
        
        
    #Affichage la bare xp du joueur
    def xp_screen(self):
        print("xp")
        
    #affiche le lvl
    def lvl_screen(self):
        print("lvl")
    
        
    #l'affichage
    def render(self, screen):
            
        #on applique le texte et l'imagez
        screen.blit(self.box,(0,0))
            
            
        #affiche les pv
        pv = str(self.pv)
        text1 = self.font.render(pv, False, (0,0,0))
        screen.blit(text1,(120, 0))
        
        #affiche les xp
        xp = str(self.xp)
        text2 = self.font.render(xp, False, (0,0,0))
        screen.blit(text2,(120, 30))
        
        #affiche le lvl
        lvl = str(self.lvl)
        text2 = self.font.render(lvl, False, (0,0,0))
        screen.blit(text2,(20, 30))
        
        #affiche les cion   
        coin = str(self.coins) 
        text3 = self.font.render(coin, False, (0,0,0))
        screen.blit(text3,(50, 70))
            
    def pause(self,screen,var):
        
        #pour afficher pausse
        if var:
            
            text = self.font.render("PAUSE", False, (0,0,0))
            screen.blit(text,(520, 0))
           
            print("pausse")
    
    
    
    
class NPC(Entity):
    
    def __init__(self, name, nb_points,dialog):
        super().__init__(name, 0, 0)
        self.nb_points = nb_points
        self.dialog = dialog
        self.points = []
        self.name = name
        self.speed = 1
        self.current_point = 0
    
    def move(self):
        current_point = self.current_point
        target_point = self.current_point + 1
        
        if target_point >= self.nb_points:
            target_point = 0
        
        current_rect = self.points[current_point]
        target_rect = self.points[target_point]
        
        if(current_rect.y < target_rect.y and abs(current_rect.x - target_rect.x ) < 3):
            self.move_down()
            
        elif (current_rect.y > target_rect.y and abs(current_rect.x - target_rect.x ) < 3):
            self.move_up()
            
        elif(current_rect.x > target_rect.x and abs(current_rect.y - target_rect.y ) < 3):
            self.move_left()
    
        elif(current_rect.x < target_rect.x and abs(current_rect.y - target_rect.y ) < 3):
            self.move_right()
            
        
        if self.rect.colliderect(target_rect):
            self.current_point = target_point
         
            
    def teleport_spawn(self):
        location = self.points[self.current_point]
        self.position[0] = location.x
        self.position[1] = location.y
        self.save_location()
    
    def load_points(self, tmx_data):
        for num in range(1, self.nb_points + 1):
            point = tmx_data.get_object_by_name(f"{self.name}_{num}")
            rect = pygame.Rect(point.x, point.y, point.width, point.height)
            self.points.append(rect)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
 