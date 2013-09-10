import libtcodpy as libtcod
from config import *

class Game:

	shutdown=False

	def init_graphics(self):
		libtcod.console_init_root(80, 50, 'libtcod', False)
		libtcod.sys_set_fps(cfg.FPS)
	
	def handle_keys(self):
		key = libtcod.console_wait_for_keypress(True)
		if key.vk == libtcod.KEY_ESCAPE:
			self.shutdown=True
	
	def game_loop(self):
	
		while not libtcod.console_is_window_closed(): 
			
			self.handle_keys()
			if self.shutdown: break
			
			libtcod.console_flush()