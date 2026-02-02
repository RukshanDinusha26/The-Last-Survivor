import pgzero, pgzrun, pygame
import math, sys, random
from myactors import Player, Monster, Bat
from constants import *
from pygame.math import Vector2

class Game:
    def __init__(self):
        self.state = 'menu'
        self.player = Player(HALF_LEVEL_W, HALF_LEVEL_H, self)
        self.monster = []
        self.timer = 0
        self.score = 0

        self.menu_background = pygame.image.load("images/menu-background.png")
        self.menu_background = pygame.transform.scale(self.menu_background, (800, 480))

        self.title_font = pygame.font.Font("fonts/ARCADECLASSIC.ttf", 48)
        self.button_font = pygame.font.Font("fonts/ARCADECLASSIC.ttf", 24)
        
        self.start_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 20, 200, 40)
        self.quit_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 40, 200, 40)
    
        self.resume_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 20, 200, 40)
        self.restart_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 40, 200, 40)
        self.main_menu_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 40)
        self.quit_pause_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 160, 200, 40)

        self.clock = pygame.time.Clock()
        self.fps = 30
        
    def start_game(self):
        self.player = Player(HALF_LEVEL_W, HALF_LEVEL_H,self)
        self.monster = []
        self.timer = 0
        self.state = 'playing'   
        self.score = 0
    
    def draw(self, screen):
      if self.state == 'menu':
          self.draw_menu(screen)
      elif self.state == 'playing':
          self.draw_game(screen)
          self.draw_score(screen)
          font = pygame.font.Font("fonts/ARCADECLASSIC.ttf", 24)  # Choose font and size
          score_text = font.render(f"Score {self.score}", True, (255, 255, 255))  # Render score text
          screen.blit(score_text, (WIDTH - 150, 20)) 
      elif self.state == 'pause':
            self.draw_pause(screen)
      elif self.state == 'game_over':
            self.draw_game_over(screen)
    
    def draw_menu(self, screen):
        screen.blit(self.menu_background, (0,-30))

        title_surf = self.title_font.render("THE  LAST SURVIVOR", True, (255, 255, 255))
        title_rect = title_surf.get_rect(topleft=(20,40))
        screen.blit(title_surf, title_rect)

        start_surf = self.button_font.render("Start Game", True, (255, 255, 255))
        start_rect = start_surf.get_rect(topleft=(40,120))
        screen.blit(start_surf, start_rect)
        
        quit_surf = self.button_font.render("Quit Game", True, (255, 255, 255))
        quit_rect = quit_surf.get_rect(topleft=(40,170))
        screen.blit(quit_surf, quit_rect)

        self.start_button_rect = start_rect
        self.quit_button_rect = quit_rect
        
        if self.start_button_rect.collidepoint(pygame.mouse.get_pos()) or self.quit_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    
    def draw_game(self,screen):
      offset_x = max(0, min(LEVEL_W - WIDTH, self.player.vposx - WIDTH / 2))
      offset_y = max(0, min(LEVEL_H - HEIGHT, self.player.vposy - HEIGHT / 2))
      offset = Vector2(offset_x, offset_y)

      screen.blit("pitch", (-offset_x, -offset_y))

      self.player.draw(offset_x, offset_y)
      for mob in self.monster:
        mob.draw(offset_x, offset_y)
        
      pygame_screen = pygame.display.get_surface()  
      
      self.player.draw_health_bar(pygame_screen)
      self.draw_score(screen)
    
    def draw_score(self, screen):
        font = pygame.font.Font("fonts/ARCADECLASSIC.ttf",24)  # Choose font and size
        score_text = font.render(f"Score  {self.score}", True, (255, 255, 255))  # Render score text
        screen.blit(score_text, (LEVEL_W - 150, 20))  # Draw score text on the screen 
      
        
    def draw_pause(self, screen):
        screen.blit(self.menu_background, (0,-30))

        title_surf = self.title_font.render("PAUSE", True, (255, 255, 255))
        title_rect = title_surf.get_rect(topleft=(20,40))
        screen.blit(title_surf, title_rect)

        resume_surf = self.button_font.render("Resume", True, (255, 255, 255))
        resume_rect = resume_surf.get_rect(topleft=(40,120))
        screen.blit(resume_surf, resume_rect)
        
        restart_surf = self.button_font.render("Restart", True, (255, 255, 255))
        restart_rect = restart_surf.get_rect(topleft=(40,170))
        screen.blit(restart_surf, restart_rect)
        
        main_menu_surf = self.button_font.render("Main Menu", True, (255, 255, 255))
        main_menu_rect = main_menu_surf.get_rect(topleft=(40,220))
        screen.blit(main_menu_surf, main_menu_rect)
        
        quit_pause_surf = self.button_font.render("Quit Game", True, (255, 255, 255))
        quit_pause_rect = quit_pause_surf.get_rect(topleft=(40,270))
        screen.blit(quit_pause_surf, quit_pause_rect)

        self.resume_button_rect = resume_rect
        self.restart_button_rect = restart_rect
        self.main_menu_button_rect = main_menu_rect
        self.quit_pause_button_rect = quit_pause_rect
        
        if (
        self.resume_button_rect.collidepoint(pygame.mouse.get_pos())
        or self.restart_button_rect.collidepoint(pygame.mouse.get_pos())
        or self.main_menu_button_rect.collidepoint(pygame.mouse.get_pos())
        or self.quit_pause_button_rect.collidepoint(pygame.mouse.get_pos())
        ):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def draw_game_over(self, screen):
        screen.blit(self.menu_background, (0,-30))
        
        title_surf = self.title_font.render(f"GAME OVER! Your score is {self.score}", True, (255, 255, 255))
        title_rect = title_surf.get_rect(topleft=(20,40))
        screen.blit(title_surf, title_rect)

        restart_surf = self.button_font.render("Restart", True, (255, 255, 255))
        restart_rect = restart_surf.get_rect(topleft=(40,170))
        screen.blit(restart_surf, restart_rect)
        
        main_menu_surf = self.button_font.render("Main Menu", True, (255, 255, 255))
        main_menu_rect = main_menu_surf.get_rect(topleft=(40,220))
        screen.blit(main_menu_surf, main_menu_rect)
        
        quit_pause_surf = self.button_font.render("Quit Game", True, (255, 255, 255))
        quit_pause_rect = quit_pause_surf.get_rect(topleft=(40,270))
        screen.blit(quit_pause_surf, quit_pause_rect)

        self.restart_button_rect = restart_rect
        self.main_menu_button_rect = main_menu_rect
        self.quit_pause_button_rect = quit_pause_rect
        
        if (
        self.restart_button_rect.collidepoint(pygame.mouse.get_pos())
        or self.main_menu_button_rect.collidepoint(pygame.mouse.get_pos())
        or self.quit_pause_button_rect.collidepoint(pygame.mouse.get_pos())
        ):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    
    def update(self):
        if self.state == 'playing':
            self.update_game()
            self.player.update()
            for monsterr in self.monster:
                monsterr.update(self.player)
                if not monsterr.alive:
                    self.score += 1  # Increase score by 1 for each killed monster
                    self.monster.remove(monsterr)
    
    
    def update_game(self):
      self.player.update()

      self.timer += 1
      if (self.timer == 20):
        self.timer = 0
        self.monster.append(Bat(self.screencoords()))

      for mob in self.monster:
        mob.update(self.player)
        if (not mob.alive):
           self.monster.remove(mob)

    def screencoords(self):
      left = int(max(0, min(LEVEL_W - WIDTH, self.player.vposx - WIDTH / 2)))
      top = int(max(0, min(LEVEL_H - HEIGHT, self.player.vposy - HEIGHT / 2)))
      right = int(max(0, min(LEVEL_W + WIDTH, self.player.vposx + WIDTH / 2)))
      bottom = int(max(0, min(LEVEL_H + HEIGHT, self.player.vposy + HEIGHT / 2)))
      coords = [left, top, right, bottom]          
      return coords

