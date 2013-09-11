import libtcodpy as libtcod
from config import *

class TextScreen:
	foreColor=None
	clearColor=None
	text=None
	
	console=None
	
	def __init__(self,text,foreColor,clearColor):
		self.console=libtcod.console_new(cfg.SCREEN_WIDTH,cfg.SCREEN_HEIGHT)
		self.text=text
		self.foreColor=foreColor
		self.clearColor=clearColor
	
	def render(self):
		libtcod.console_set_default_background(self.console,self.clearColor)
		libtcod.console_set_default_foreground(self.console,self.foreColor)
		libtcod.console_clear(self.console)
		libtcod.console_print_ex(self.console, cfg.SCREEN_WIDTH/2, cfg.SCREEN_HEIGHT/3, libtcod.BKGND_NONE, libtcod.CENTER, self.text)
		libtcod.console_blit(self.console,0,0,cfg.SCREEN_WIDTH,cfg.SCREEN_HEIGHT,0,0,0)
			
class ScreenHandler:
	base=None
	cut=None
	queue=[]
	
	console=None
	
	def __init__(self,base):
		self.base=base
		
	def tick(self):
		if self.cut:
			self.cut.render()
		else:
			self.base.render()
			
			
	def addTextCut(self,text,forecol,backcol):
		self.cut=TextScreen(text,forecol,backcol)
	
	def clearCut(self):
		self.cut=None