import libtcodpy as libtcod
from config import *

from game import *
		
adungeon=Game()
adungeon.init_graphics()
adungeon.game_loop()