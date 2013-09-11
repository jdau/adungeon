import libtcodpy as libtcod
from config import *

class Screen:
	ref=None
	entity_ref=None
	
	scroll=False
	tick=False
	
	x_dim=0
	y_dim=0
	
	def __init__(self,x,y):
		self.x_dim=x
		self.y_dim=y
	
	def render(self,console):
		# Todo: Improve error handling
		if not scroll: return
		
		for x in xrange(self.x_dim):
			for y in xrange(self.y_dim):
				self.ref[x][y].draw(console)
				
		for entity in self.entity_ref:
			entity.draw(console)
			
class ScreenHandler:
	base=None
	cut=None
	queue=[]
	
	console=None
	
	def __init__(self,base):
		self.base=base
		
	def tick(self):
		self.base.render()
			