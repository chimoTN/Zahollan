from dataclasses import dataclass
import pygame, pytmx, pyscroll
from src.player import NPC
from idlelib.idle_test.test_configdialog import dialog

@dataclass
class Portal:
    from_world: str 
    origin_point: str 
    target_world: str 
    teleport_point: str


@dataclass
class Map:
    
    name: str
    walls: list[pygame.Rect]
    groupe: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals: list[Portal]
    npcs: list[NPC]
    
class MapManager:
    
    def __init__(self,screen,player):
        self.maps = dict() # "house" -> Map("house", walls, group)
        self.screen = screen
        self.player = player
        self.current_map = "Fleurosia"
        
        self.register_map("Fleurosia", portals=[
            Portal(from_world = "Fleurosia" ,origin_point = "entree_1", target_world = "grand_chemun", teleport_point = "Spawn_1"),
            Portal(from_world = "Fleurosia" ,origin_point = "entree_2", target_world = "map2", teleport_point = "Spawn"),
        ], 
        npcs =[
            NPC("paul",nb_points=4, dialog=["fou moi la paix"]),
            NPC("robin",nb_points=2, dialog = ["comment tu va ?", "moi super bien"])
        ])
        
        self.register_map("map2", portals=[
            Portal(from_world = "map2" ,origin_point = "Sortie", target_world = "Fleurosia", teleport_point = "Spawn_2")
        ])
        
        self.register_map("grand_chemun", portals=[
            Portal(from_world = "grand_chemun" ,origin_point = "entree_1", target_world = "Fleurosia", teleport_point = "Spawn_1"),
            Portal(from_world = "grand_chemun" ,origin_point = "entree_2", target_world = "carte", teleport_point = "exit_fleurosia")
        ])
        
        self.register_map("Village", portals=[
            Portal(from_world = "Village" ,origin_point = "entree_un", target_world = "carte", teleport_point = "exit_zaholan"),
            Portal(from_world = "Village" ,origin_point = "enter_taverne", target_world = "Taverne", teleport_point = "Spawn"),
            Portal(from_world = "Village" ,origin_point = "enter_hdv", target_world = "Hotel_de_ville", teleport_point = "Spawn"),
            Portal(from_world = "Village" ,origin_point = "enter_magasin", target_world = "magasin", teleport_point = "Spawn"),
            Portal(from_world = "Village" ,origin_point = "enter_house", target_world = "maison", teleport_point = "Spawn_house")
        ])
        
        self.register_map("carte", portals=[
             Portal(from_world = "carte" ,origin_point = "entree_zaholan", target_world = "Village", teleport_point = "Spawn"),
             Portal(from_world = "carte" ,origin_point = "entree_fleurosia", target_world = "grand_chemun", teleport_point = "Spawn_2")
        ])
        
        
        #pour go a depuis un lieux interieur
        
        
        self.register_map("maison", portals=[
            Portal(from_world = "maison" ,origin_point = "exite_house", target_world = "Village", teleport_point = "exit_house")
        ])
        
        self.register_map("Taverne", portals=[
            Portal(from_world = "Taverne" ,origin_point = "Sortie", target_world = "Village", teleport_point = "exit_taverne")
        ])
        
        self.register_map("Hotel_de_ville", portals=[
           Portal(from_world = "Hotel_de_ville" ,origin_point = "Sortie", target_world = "Village", teleport_point = "exit_hdv")
        ])
                
        self.register_map("magasin", portals=[
            Portal(from_world = "magasin" ,origin_point = "Sortie", target_world = "Village", teleport_point = "exit_magasin")
        ])
        
        
        self.teleport_player("Spawn")
        self.teleport_npcs()
    
    
    def check_npc_collisions(self, dialog_box):
        for sprite in self.get_group().sprites():
            if sprite.feet.colliderect(self.player.rect) and type(sprite) is NPC:
                dialog_box.execute(sprite.dialog) 
    
    def check_collisions(self):
        #portail
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)
                
                if self.player.feet.colliderect(rect):
                    copy_portal = portal
                    self.current_map = portal.target_world
                    self.teleport_player(copy_portal.teleport_point)
                    
        #collision
        for sprite in self.get_group().sprites():
            
            #si on contact avec un pnj
            if type(sprite) is NPC:
                if sprite.feet.colliderect(self.player.rect):
                    sprite.speed = 0
                else:
                    sprite.speed = 1
                
            #si on contact avec un mur
            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()
    
    def teleport_player(self,name):
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()
        
    def register_map(self, name, portals=[], npcs=[]):
        
        #charger la carte (tmx)
        tmx_data = pytmx.util_pygame.load_pygame(f'../map/{name}.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2
        
        # Liste de rectangle de collisions
        walls = []
        
        for obj in tmx_data.objects:
            if obj.type == "collision":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        
        #dessiner le groupe de calques
        groupe = pyscroll.PyscrollGroup(map_layer = map_layer, default_layer = 9)
        groupe.add(self.player)
        
        #dessiner les pmj
        for npc in npcs:
            groupe.add(npc)
        
        #cree un object map
        self.maps[name] = Map(name, walls, groupe, tmx_data, portals, npcs)
        
    def get_map(self):
        return self.maps[self.current_map]
    
    def get_group(self):
        return self.get_map().groupe
    
    def get_walls(self):
        return self.get_map().walls
    
    def get_object(self,name):
        return self.get_map().tmx_data.get_object_by_name(name)
        
    def teleport_npcs(self):
        for map in self.maps:
            map_data = self.maps[map]
            npcs = map_data.npcs
    
            for npc in npcs:
                npc.load_points(map_data.tmx_data)
                npc.teleport_spawn()
    
    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)
        
    def update(self):
        self.get_group().update()
        self.check_collisions()
        
        for npc in self.get_map().npcs:
            npc.move()
        
        
        
        
        
        
        
        
        