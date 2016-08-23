import libtcodpy as libtcod
from config import *

# Test change

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
		
class ProgressScreen:
	foreColor=None
	clearColor=None
	text=None
	
	duration=0
	elapsed=0
	
	console=None
	def __init__(self,text,duration,foreColor,clearColor):
		self.text=text
		self.duration=duration*cfg.FPS
		self.foreColor=foreColor
		self.clearColor=clearColor
		
	def render(self):
		
		libtcod.console_set_default_background(self.console,self.clearColor)
		libtcod.console_set_default_foreground(self.console,self.foreColor)
		libtcod.console_clear(self.console)
		libtcod.console_print_ex(self.console, cfg.SCREEN_WIDTH/2, cfg.SCREEN_HEIGHT/3, libtcod.BKGND_NONE, libtcod.CENTER, self.text)
		
		barRange=int(float(self.elapsed)/float(self.duration)*cfg.SCREEN_WIDTH-4)
		for i in xrange(barRange):
			libtcod.console_print_ex(self.console, i+2, (cfg.SCREEN_HEIGHT/3)*2, libtcod.BKGND_NONE, libtcod.CENTER, "#")
		
		self.elapsed=self.elapsed+1
		if self.elapsed==self.duration: return False
		
		libtcod.console_blit(self.console,0,0,cfg.SCREEN_WIDTH,cfg.SCREEN_HEIGHT,0,0,0)
		return True
			
class ScreenHandler:
	base=None
	cut=None
	queue=[]
	
	console=None
	
	def __init__(self,base):
		self.base=base
		
	def tick(self):
		if self.cut:
			if not self.cut.render(): 
				self.cut=False # return False will stop cut
			return False
		else:
			self.base.render()
			return True
			
			
	def addTextCut(self,text,forecol,backcol):
		self.cut=TextScreen(text,forecol,backcol)
		
	def addProgressCut(self,text,duration,forecol,backcol):
		self.cut=ProgressScreen(text,duration,forecol,backcol)
	
	def clearCut(self):
		self.cut=None