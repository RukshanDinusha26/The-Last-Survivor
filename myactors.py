from pgzero.builtins import Actor, keyboard, keys
import pygame, math, sys, random
from pygame.rect import Rect
from constants import *
class MyActor(Actor):
  def __init__(self,img,x,y,speed):
    self.myimg = img
    self.direction = "down"
    self.imgno = 1
    myimg = f'{self.myimg}_{self.direction}_{self.imgno}'
    super().__init__(myimg, (x,y))    
    self.vposx, self.vposy = x, y
    self.dx, self.dy = 0, 0
    self.speed = speed
    self.timer = 0    
    self.olddx = -100
    self.olddirection = -100

  def update(self):

    self.timer += 1

    if (self.dx < 0): 
      direction = "left"
    elif (self.dx == 0): 
      if (self.dy < 0):
        direction = "up"
      elif (self.dy >= 0):
        direction = "down"            
    else:
      direction = "right"

    if (self.olddirection != direction):
      self.imgno = 1
      self.direction = direction

    if (self.timer==10):
      self.timer = 0
      if (self.olddirection == direction):
        self.imgno +=1
        if self.imgno == 4:
          self.imgno = 1 

    self.image = f'{self.myimg}_{self.direction}_{self.imgno}'
    self.olddx = self.dx
    self.olddirection = direction


    # Return vector representing amount of movement that should occur
    self.dx = self.dx * self.speed
    self.dy = self.dy * self.speed

    self.vposx += self.dx
    self.vposx = max(0+PLAYER_W,min(self.vposx, LEVEL_W-PLAYER_W))    
    self.vposy += self.dy
    self.vposy = max(0+PLAYER_H,min(self.vposy, LEVEL_H-PLAYER_H))

  def draw(self, offset_x, offset_y):
    self.pos = (self.vposx - offset_x, self.vposy - offset_y)
    super().draw()

class Player(MyActor):
  def __init__(self, x, y,game):
    self.img = "warrior"
    self.health = 100
    self.max_health = 100
    self.game = game 
    super().__init__(self.img,x,y,5)
    self.is_attacking = False
    self.attack_frame = 0

  def update(self):
    # Return vector representing amount of movement that should occur
    self.dx, self.dy = 0, 0
    if keyboard.a:
        self.dx = -1
    elif keyboard.d:
        self.dx = 1
    if keyboard.w:
        self.dy = -1
    elif keyboard.s:
        self.dy = 1
    
    if keyboard.space:
            self.is_attacking = True

    if self.is_attacking:
        self.attack_frame += 1
        if self.attack_frame >= 7:
            self.is_attacking = False
            self.attack_frame = 0
            self.attack()

    super().update()
    
  def draw(self, offset_x, offset_y):
        if self.is_attacking:
            self.image = f"{self.img}_attack_{self.direction}_{self.attack_frame}"
        else:
            self.image = f"{self.img}_{self.direction}_{self.imgno}"
        super().draw(offset_x, offset_y)

  def hurt(self,damage):
    self.health -= damage
    if (self.health<=0):
      self.game.state = 'game_over'
      print("game over")
  
  def draw_health_bar(self, screen):
        health_bar_width = int((self.health / self.max_health) * 100)
        
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(9, 9, 102, 22))
        
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(10, 10, 100, 20))

        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(10, 10, health_bar_width, 20))

        font = pygame.font.Font("fonts/ARCADECLASSIC.ttf", 20)  # Choose font and size
        text_surface = font.render("Health", True, (0, 0, 0))  # Render text
        text_rect = text_surface.get_rect()
        text_rect.center = (60, 20)  # Position the text in the center
        screen.blit(text_surface, text_rect)  # Draw text on the screen
  

  def distance_to(self, other_actor):
        return self.pos.distance_to(other_actor.pos)
  
  def attack(self):
      attack_range = Rect(self.x - 50, self.y - 50, 100, 100)
        # Loop through all monsters in the game
      for monster in self.game.monster:
            # Check for collision between player and monster
          if monster.colliderect(attack_range):
                # Damage the monster
                monster.take_damage(100)
class Monster(MyActor):
  def __init__(self, img, posx, posy,spd):
    super().__init__(img, posx, posy, spd)
    self.alive = True
    self.health = 100
  
  def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.alive = False
    
  def update(self,player):
    # Return vector representing amount of movement that should occur    
    super().update()   
    if (self.colliderect(player)):
      player.hurt(10)
      self.alive = False
      

class Bat(Monster):
  def __init__(self, screencoords):

    LEFT = 0
    TOP = 1
    RIGHT = 2
    BOTTOM = 3

    side = random.randint(0,3)    
    
    if (side == LEFT):
      posx = max(screencoords[LEFT] - 50, 0)
      posy = random.randint(screencoords[TOP],screencoords[BOTTOM])      
    elif (side == TOP): 
      posx = random.randint(screencoords[LEFT],screencoords[RIGHT])
      posy = max(screencoords[TOP] - 50, 0)
    elif (side == RIGHT): 
      posx = min(screencoords[RIGHT] + 50, LEVEL_W)
      posy = random.randint(screencoords[TOP],screencoords[BOTTOM])
    elif (side == BOTTOM):
      posx = random.randint(screencoords[LEFT],screencoords[RIGHT])
      posy = min(screencoords[BOTTOM] + 50, LEVEL_H)

    super().__init__("bat", posx, posy, 1)
    
  def update(self,player): 

    if (self.vposx > player.vposx):
      self.dx = -1
    elif (self.vposx < player.vposx):
      self.dx = 1
    else:
        self.dx = 0
    if (self.vposy > player.vposy):
      self.dy = -0.5
    elif (self.vposx < player.vposy):
      self.dy = 0.5
    else:
      self.dy = 0

    super().update(player)   


   
