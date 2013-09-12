import libtcodpy as libtcod
from config import *


from overworld import *
from screen import *
from player import *

class Game:

	shutdown=False

	def init_graphics(self):
		libtcod.console_set_custom_font("annchrome.png",libtcod.FONT_LAYOUT_ASCII_INROW)
		libtcod.console_init_root(cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT, 'libtcod', False)
		libtcod.sys_set_fps(cfg.FPS)
	
	def handle_keys(self):
		#key = libtcod.console_wait_for_keypress(True)
		key = libtcod.console_check_for_keypress()
		if key.vk == libtcod.KEY_ESCAPE:
			self.shutdown=True
	
	def game_loop(self):
		
		world=Overworld()
		screens=ScreenHandler(world)
		screens.addTextCut("Generating world...",libtcod.green,libtcod.black)
		
		screens.tick()
		self.handle_keys()
		libtcod.console_flush()
		
		world.create()
		
		player=AIPlayer()
		world.playerStart(player)
		
		screens.clearCut()
		cycles=0
	
		while not libtcod.console_is_window_closed(): 
			
			screens.tick()
			player.tick(world)
			self.handle_keys()
			if self.shutdown: break
			
			libtcod.console_flush()