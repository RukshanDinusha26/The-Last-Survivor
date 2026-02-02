import pgzero, pgzrun, pygame
import math, sys, random
from enum import Enum
from game import Game
from constants import *

if sys.version_info < (3,5):
    print("This game requires at least version 3.5 of Python. Please download it from www.python.org")
    sys.exit()

pgzero_version = [int(s) if s.isnumeric() else s for s in pgzero.__version__.split('.')]
if pgzero_version < [1,2]:
    print("This game requires at least version 1.2 of Pygame Zero. You have version {0}. Please upgrade using the command 'pip3 install --upgrade pgzero'".format(pgzero.__version__))
    sys.exit()


game = Game()

def draw():
    screen.clear()
    game.draw(screen)

def update():
    game.update()
    game.clock.tick(game.fps)

def on_key_down(key):
    if game.state == 'menu':
        if key == keys.RETURN:
            game.start_game()
        elif key == keys.ESCAPE:
            sys.exit()
    elif game.state == 'playing':
        if key == keys.ESCAPE:
            game.state = 'pause'
    elif game.state == 'pause':
        if key == keys.ESCAPE:
            game.state = 'playing'


def on_mouse_down(pos):
    if game.state == 'menu':
        if game.start_button_rect.collidepoint(pos):
            game.start_game()
        elif game.quit_button_rect.collidepoint(pos):
            sys.exit()
    elif game.state == 'pause':
        if game.resume_button_rect.collidepoint(pos):
            game.state = 'playing'
        elif game.restart_button_rect.collidepoint(pos):
            game.start_game()
            game.state = 'playing'
        elif game.main_menu_button_rect.collidepoint(pos):
            game.state = 'menu'
        elif game.quit_pause_button_rect.collidepoint(pos):
            sys.exit()
    elif game.state == 'game_over':
        if game.restart_button_rect.collidepoint(pos):
            game.start_game()
            game.state = 'playing'
        elif game.main_menu_button_rect.collidepoint(pos):
            game.state = 'menu'
        elif game.quit_pause_button_rect.collidepoint(pos):
            sys.exit()

pgzrun.go()
