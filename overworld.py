import libtcodpy as libtcod
import math,random,copy
from config import *

from util import *

class OverworldTile:

	char='.'
	x=0
	y=0
	blocked=False
	
	foreColor=None
	backColor=None
	
	def __init__(self,x,y):
		self.x=x
		self.y=y
		
	def setChar(self,char): 
		self.char=char
		
	def setColors(self,fore,back):
		self.foreColor=fore
		self.backColor=back
		
	def setBlocked(self,blocked): 
		self.blocked=blocked
		
	def isBlocked(self): return self.blocked
		
	def draw(self,console):
		libtcod.console_put_char_ex( console, self.x, self.y, self.char, self.foreColor, self.backColor)
		
		
class OverworldTileEntity:

	char='#'
	x=0
	y=0
	
	foreColor=None
	backColor=None
	
	def __init__(self,x,y):
		self.x=x
		self.y=y
		
	def setChar(self,char): 
		self.char=char
		
	def setColors(self,fore,back):
		self.foreColor=fore
		self.backColor=back
		
	def position(self): return (self.x,self.y)
		
	def draw(self,console):
		libtcod.console_put_char_ex( console, self.x, self.y, self.char, self.foreColor, self.backColor)

class Overworld:
	
	level=None
	console=None
	
	width=0
	height=0
	
	pathable=[]
	
	tile_entity=[]
	
	def render(self):
		c=self.console
		wx=cfg.SCREEN_WIDTH
		wy=cfg.SCREEN_HEIGHT
		for y in xrange(wy):
			for x in xrange(wx):
				self.level[x][y].draw(c)
				
		for entity in self.tile_entity:
			entity.draw(c)
				
		libtcod.console_blit(self.console,0,0,wx,wy,0,0,0)
		
	def create(self):
		w=self.width=cfg.OW_WIDTH
		h=self.height=cfg.OW_HEIGHT
		th=cfg.OW_TREE_THRES
		
		self.level=[[OverworldTile(j,i) for i in xrange(h)] for j in xrange(w)]
		self.console=libtcod.console_new(w,h)

		backColor=libtcod.Color(0, 0, 0)
		
		noise2d = libtcod.noise_new(2)
		
		for x in xrange(w):
			for y in xrange(h):
				#f = [noise_zoom * x / (2*SAMPLE_SCREEN_WIDTH) + noise_dx,
				#	noise_zoom * y / (2*SAMPLE_SCREEN_HEIGHT) + noise_dy]
				zoom=0.09
				f = [zoom * x,
                    zoom * y]
				val = -(libtcod.noise_get(noise2d,f))
				c=60+int(((val+1)/2)*90)
				c1=int((((val*-1)+1)/2)*30)
				c2=10+int(((val+1)/2)*20)
				
				if val>th:				
					self.level[x][y].setChar('!')
					self.level[x][y].setColors(libtcod.Color(0, c, 0),libtcod.Color(0, c2, 0))
					self.level[x][y].setBlocked(True)
				else:
					self.level[x][y].setChar(176)
					self.level[x][y].setColors(libtcod.Color(0, c1, 0),libtcod.Color(0, c2, 0))
		
		# Determine all pathable coords
		start=(random.randint(1,w-1),random.randint(1,h-1))
		while self.level[start[0]][start[1]].blocked: start=(random.randint(1,w-1),random.randint(1,h-1))
		
		openlist=[]
		openlist.append(start)
		self.pathable.append(start)
		
		rels=((1,1),(1,-1),(-1,1),(-1,-1))
		
		while len(openlist):
			newlist=copy.copy(openlist)
			for coord in openlist:
				for rel in rels:
					crd=(coord[0]+rel[0],coord[1]+rel[1])
					if crd[0]<0 or crd[0]>=w or crd[1]<0 or crd[1]>=h: break
					if self.level[crd[0]][crd[1]].blocked: break
					
					if crd not in self.pathable:
						newlist.append(crd)
						self.pathable.append(crd)
				newlist.remove(coord)
				
			openlist=copy.copy(newlist)
			print len(self.pathable)
			
		# Place town
		
		town_pos=random.choice(self.pathable)
		town=OverworldTileEntity(town_pos[0],town_pos[1])
		town.setColors(libtcod.Color(0, 100, 150),libtcod.Color(40, 40, 0))
		self.tile_entity.append(town)
		
		# Place dungeons
		
		for i in xrange(5):
		
			validLocation=False
			pos=None
			while not validLocation:
				validLocation=True
				pos=random.choice(self.pathable)
				for entity in self.tile_entity:
					if entity.position()==pos:
						validLocation=False
				
			dungeon=OverworldTileEntity(pos[0],pos[1])
			dungeon.setColors(libtcod.Color(200, 0, 0),libtcod.Color(40, 0, 0))
			self.tile_entity.append(dungeon)