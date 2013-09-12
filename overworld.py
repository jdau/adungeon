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
	
	seen=False
	
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
	def isSeen(self): return self.seen
	def gotSeen(self): self.seen=True
		
	def draw(self,console,offset_x,offset_y):
		if not self.seen: return
		libtcod.console_put_char_ex( console, self.x-offset_x, self.y-offset_y, self.char, self.foreColor, self.backColor)
		
		
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
		
	def draw(self,console,offset_x,offset_y):
		
		libtcod.console_put_char_ex( console, self.x-offset_x, self.y-offset_y, self.char, self.foreColor, self.backColor)

class Overworld:
	
	level=None
	console=None
	
	width=0
	height=0
	
	pathable=[]
	blockedMap=[]
	
	player=None
	tile_entity=[]
	town=None
	
	def halfScreenWidth(self): return int(math.floor(cfg.SCREEN_WIDTH/2))
	
	def render(self):
		c=self.console
		libtcod.console_clear(c)
		wx=cfg.SCREEN_WIDTH
		wy=cfg.SCREEN_HEIGHT
		
		self.playerReveal()
		offset_x=self.player.x-cfg.WID2
		if offset_x+wx > self.width: offset_x=self.width-wx
		if offset_x<0: offset_x=0
		
		offset_y=self.player.y-cfg.HGT2
		if offset_y+wy > self.height: offset_y=self.height-wy
		if offset_y<0: offset_y=0
		
		for x in xrange(wx):
			for y in xrange(wy):
				self.level[offset_x+x][offset_y+y].draw(c,offset_x,offset_y)
				
		for entity in self.tile_entity:
			pos=entity.position()
			#if self.level[pos[0]][pos[1]].seen: entity.draw(c,offset_x,offset_y)
			entity.draw(c,offset_x,offset_y)
				
		self.player.draw(c,offset_x,offset_y)
				
		libtcod.console_blit(self.console,0,0,wx,wy,0,0,0)
		
	def playerReveal(self):
		sight=15
		libtcod.map_compute_fov(self.blockedMap,self.player.x,self.player.y,sight,True)
		self.level[self.player.x][self.player.y].gotSeen()
		wx=cfg.WID2
		wy=cfg.HGT2
		for x in xrange(self.player.x-wx,self.player.x+wx):
			for y in xrange(self.player.y-wy,self.player.y+wy):
				if libtcod.map_is_in_fov(self.blockedMap, x, y):
					self.level[x][y].gotSeen()
	
	def playerStart(self,player):
		self.player=player
		townPos=self.town.position()
		self.player.setPosition(townPos[0],townPos[1])
		self.player.newLevel(self)
		
	def buildBlockedMap(self):
		bmap = libtcod.map_new(self.width,self.height)
		
		for x in xrange(self.width):
			for y in xrange(self.height):
				if self.level[x][y].blocked:
					libtcod.map_set_properties(bmap,x,y,False,False)
				else:
					libtcod.map_set_properties(bmap,x,y,True,True)
		
		self.blockedMap=bmap
		
	def getWidth(self): return self.width
	def getHeight(self): return self.height
	
	def getBlockedMap(self): return self.blockedMap
	def getPathable(self): return self.pathable
	def isPathable(self,x,y): return (x,y) in self.pathable
	def isSeen(self,x,y): return self.level[x][y].isSeen()
	def isBlocked(self,x,y): return self.level[x][y].isBlocked()
	
	def putThing(self,x,y,char="+"): #debug
		rlist=copy.copy(self.tile_entity)
		for e in rlist:
			if e.position()==(x,y):
				self.tile_entity.remove(e)
				
		thing=OverworldTileEntity(x,y)
		thing.setChar(char)
		thing.setColors(libtcod.Color(random.randint(0,255), random.randint(0,255), random.randint(0,255)),libtcod.Color(0, 0, 0))
		self.tile_entity.append(thing)
		
	def findPathable(self):
		w=self.width
		h=self.height
		start=(random.randint(1,w-1),random.randint(1,h-1))
		while self.level[start[0]][start[1]].isBlocked(): start=(random.randint(1,w-1),random.randint(1,h-1))
		
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
					if self.level[crd[0]][crd[1]].isBlocked(): break
					
					if crd not in self.pathable:
						newlist.append(crd)
						self.pathable.append(crd)
				newlist.remove(coord)
				
			openlist=copy.copy(newlist)
		
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
				zoom=0.09
				f = [zoom * x,zoom * y]
				val = libtcod.noise_get(noise2d,f)
				c=60+int(((val+1)/2)*90)
				c1=int((((val*-1)+1)/2)*30)
				c2=10+int(((val+1)/2)*20)
				
				if val>th:				
					self.level[x][y].setChar(23)
					self.level[x][y].setColors(libtcod.Color(0, c, 0),libtcod.Color(0, c2, 0))
					self.level[x][y].setBlocked(True)
				else:
					self.level[x][y].setChar(176)
					self.level[x][y].setColors(libtcod.Color(0, c1, 0),libtcod.Color(0, c2, 0))
		
		while len(self.pathable) < 200:
			self.findPathable()
			
		# Place town
		
		town_pos=random.choice(self.pathable)
		town=OverworldTileEntity(town_pos[0],town_pos[1])
		town.setColors(libtcod.Color(0, 100, 150),libtcod.Color(40, 40, 0))
		self.tile_entity.append(town)
		self.town=town
		
		# Place dungeons
		
		for i in xrange(5):
		
			validLocation=False
			pos=None
			while not validLocation:
				validLocation=True
				pos=random.choice(self.pathable)
				for entity in self.tile_entity:
					if entity.position()==pos:
						print "inval"
						validLocation=False
				
			dungeon=OverworldTileEntity(pos[0],pos[1])
			dungeon.setColors(libtcod.Color(200, 0, 0),libtcod.Color(40, 0, 0))
			self.tile_entity.append(dungeon)
			
		self.buildBlockedMap()