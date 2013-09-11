import libtcodpy as libtcod
from config import *

class AIPlayer:
	x=0
	y=0
	
	foreColor=None
	backColor=None
	
	def __init__(self):
		self.foreColor=libtcod.Color(0, 200, 0)
		self.backColor=libtcod.Color(0, 0, 0)
		
	def draw(self,console,offset_x,offset_y):
		libtcod.console_put_char_ex( console, self.x-offset_x, self.y-offset_y, "@", self.foreColor, self.backColor)
	
	def setPosition(self,x,y):
		self.x=x
		self.y=y
	
	def position(self): return (self.x,self.y)