import libtcodpy as libtcod
import random,copy
from config import *

class AIPlayer:
	x=0
	y=0
	
	foreColor=None
	backColor=None
	
	goal=None
	path=None
	path_progress=None
	
	map=None
	
	doing=0
	
	def whatDoing(self):
		# 0 = nothing
		# 1 = moving
		return self.doing
	
	def __init__(self):
		self.foreColor=libtcod.Color(0, 200, 0)
		self.backColor=libtcod.Color(0, 0, 0)
		
	def draw(self,console,offset_x,offset_y):
		libtcod.console_put_char_ex( console, self.x-offset_x, self.y-offset_y, "@", self.foreColor, self.backColor)
	
	def setPosition(self,x,y):
		self.x=x
		self.y=y
	
	def position(self): return (self.x,self.y)
	
	def newLevel(self,world):
		self.map=copy.deepcopy(world.getPathable())
		
	def setSeen(self,x,y):
		try:
			self.map.remove((x,y))
		except:
			pass
	
	def tick(self,world):
		
		if not self.goal:
			self.goal=random.choice(self.map)
			self.doing=0
			print "goal"
			return
			
		if not self.path:
			map=world.getBlockedMap()
			self.path=libtcod.path_new_using_map(map,0)
			libtcod.path_compute(self.path,self.x,self.y,self.goal[0],self.goal[1])
			self.path_progress=0
			self.doing=0
			print "path"
			return
			
		[next_x,next_y]=libtcod.path_get(self.path, self.path_progress)
		self.x=next_x
		self.y=next_y
		self.path_progress=self.path_progress+1
		if libtcod.path_size(self.path)==self.path_progress:
			self.goal=None
			self.path=None
			print "path done"