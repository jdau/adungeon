import libtcodpy as libtcod
import math,random,copy
from config import *

from util import *

# a lot could be merged and abstracted between dungeon and overworld, right now i am keeping it all seperate until i know what each needs to do

class DungeonTile:

	char='#'
	x=0
	y=0
	blocked=True
	
	foreColor=None
	backColor=None
	
	seen=False
	
	def __init__(self,x,y):
		self.x=x
		self.y=y
		self.foreColor=libtcod.Color(102, 69, 51)
		self.backColor=libtcod.Color(0, 0, 0)
		
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
		
		
class DungeonTileEntity:

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

class Dungeon:
	
	level=None
	console=None
	
	width=0
	height=0
	
	pathable=[]
	blockedMap=[]
	
	player=None
	tile_entity=[]
	entry=None
	
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
		ePos=self.entry.position()
		self.player.setPosition(ePos[0],ePos[1])
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
		
	def findPathable(self):
		self.pathable=[]
		w=self.width
		h=self.height
		start=(random.randint(1,w-1),random.randint(1,h-1))
		while self.level[start[0]][start[1]].isBlocked(): start=(random.randint(1,w-1),random.randint(1,h-1))
		
		openlist=[]
		openlist.append(start)
		self.pathable.append(start)
		rels=((0,1),(0,-1),(-1,0),(1,0))
		
		while len(openlist):
			newlist=copy.copy(openlist)
			for coord in openlist:
				for rel in rels:
					crd=(coord[0]+rel[0],coord[1]+rel[1])
					if crd[0]<0 or crd[0]>=w or crd[1]<0 or crd[1]>=h: continue
					if self.level[crd[0]][crd[1]].isBlocked(): continue
					
					if crd not in self.pathable:
						newlist.append(crd)
						self.pathable.append(crd)
				newlist.remove(coord)
				
			openlist=copy.copy(newlist)
			
	def clearUnpathableAreas(self):
		w=self.width
		h=self.height
		for x in xrange(w):
			for y in xrange(h):
				if self.level[x][y].blocked: continue
				if not (x,y) in self.pathable:
					self.level[x][y].setBlocked(True)
					
	def digMap(self,x,y):
		self.level[x][y].setBlocked(False)
		self.level[x][y].setChar(176)
		self.level[x][y].setColors(libtcod.Color(99, 70, 54),libtcod.Color(0, 0, 0))
					
	def vline(self, x, y1, y2):
		if y1 > y2:
			y1,y2 = y2,y1
		for y in range(y1,y2+1):
			self.digMap(x,y);

	def vline_up(self, x, y):
		while y >= 0 and self.isBlocked(x,y):
			self.digMap(x,y);
			y -= 1

	def vline_down(self, x, y):
		while y < self.height and self.isBlocked(x,y):
			self.digMap(x,y);
			y += 1

	def hline(self, x1, y, x2):
		if x1 > x2:
			x1,x2 = x2,x1
		for x in range(x1,x2+1):
			self.digMap(x,y);

	def hline_left(self, x, y):
		while x >= 0 and self.isBlocked(x,y):
			self.digMap(x,y);
			x -= 1

	def hline_right(self, x, y):
		while x < self.width and self.isBlocked(x,y):
			self.digMap(x,y);
			x += 1
					
	def traverseNode(self,node,dat):
		bsp_random_room=True
		bsp_min_room_size=5
		if libtcod.bsp_is_leaf(node):
			# calculate the room size
			minx = node.x + 1
			maxx = node.x + node.w - 1
			miny = node.y + 1
			maxy = node.y + node.h - 1
			if minx > 1:
				minx -= 1
			if miny > 1:
				miny -=1
			if maxx == self.width - 1:
				maxx -= 1
			if maxy == self.height - 1:
				maxy -= 1
			if bsp_random_room:
				minx = libtcod.random_get_int(None, minx, maxx - bsp_min_room_size + 1)
				miny = libtcod.random_get_int(None, miny, maxy - bsp_min_room_size + 1)
				maxx = libtcod.random_get_int(None, minx + bsp_min_room_size - 1, maxx)
				maxy = libtcod.random_get_int(None, miny + bsp_min_room_size - 1, maxy)
			# resize the node to fit the room
			node.x = minx
			node.y = miny
			node.w = maxx-minx + 1
			node.h = maxy-miny + 1
			# dig the room
			for x in range(minx, maxx + 1):
				for y in range(miny, maxy + 1):
					self.digMap(x,y);
		else:
			# resize the node to fit its sons
			left = libtcod.bsp_left(node)
			right = libtcod.bsp_right(node)
			node.x = min(left.x, right.x)
			node.y = min(left.y, right.y)
			node.w = max(left.x + left.w, right.x + right.w) - node.x
			node.h = max(left.y + left.h, right.y + right.h) - node.y
			# create a corridor between the two lower nodes
			if node.horizontal:
				# vertical corridor
				if left.x + left.w - 1 < right.x or right.x + right.w - 1 < left.x:
					# no overlapping zone. we need a Z shaped corridor
					x1 = libtcod.random_get_int(None, left.x, left.x + left.w - 1)
					x2 = libtcod.random_get_int(None, right.x, right.x + right.w - 1)
					y = libtcod.random_get_int(None, left.y + left.h, right.y)
					self.vline_up(x1, y - 1)
					self.hline(x1, y, x2)
					self.vline_down(x2, y + 1)
				else:
					# straight vertical corridor
					minx = max(left.x, right.x)
					maxx = min(left.x + left.w - 1, right.x + right.w - 1)
					x = libtcod.random_get_int(None, minx, maxx)
					self.vline_down(x, right.y)
					self.vline_up(x, right.y - 1)
			else:
				# horizontal corridor
				if left.y + left.h - 1 < right.y or right.y + right.h - 1 < left.y:
					# no overlapping zone. we need a Z shaped corridor
					y1 = libtcod.random_get_int(None, left.y, left.y + left.h - 1)
					y2 = libtcod.random_get_int(None, right.y, right.y + right.h - 1)
					x = libtcod.random_get_int(None, left.x + left.w, right.x)
					self.hline_left(x - 1, y1)
					self.vline(x, y1, y2)
					self.hline_right(x + 1, y2)
				else:
					# straight horizontal corridor
					miny = max(left.y, right.y)
					maxy = min(left.y + left.h - 1, right.y + right.h - 1)
					y = libtcod.random_get_int(None, miny, maxy)
					self.hline_left(right.x - 1, y)
					self.hline_right(right.x, y)
					
		return True # required or the library shits itself
		
	def create(self):
		w=cfg.DNG_MINWIDTH+random.randint(0,cfg.DNG_SIZEVAR)
		h=cfg.DNG_MINHEIGHT+random.randint(0,cfg.DNG_SIZEVAR)
		self.width=w
		self.height=h
		
		self.level=[[DungeonTile(j,i) for i in xrange(h)] for j in xrange(w)]
		self.console=libtcod.console_new(w,h)

		backColor=libtcod.Color(0, 0, 0)
		
		# magic!
		bsp_depth=9
		bsp_min_room_size=5
		
		bsp = libtcod.bsp_new_with_size(0,0,w,h)
		libtcod.bsp_split_recursive(bsp, 0, bsp_depth,
                                            bsp_min_room_size,
                                            bsp_min_room_size, 1.5, 1.5)
		libtcod.bsp_traverse_inverted_level_order(bsp, self.traverseNode)
		
		self.findPathable()
		self.clearUnpathableAreas()
		
		# Place entrance
		
		e_pos=random.choice(self.pathable)
		entry=DungeonTileEntity(e_pos[0],e_pos[1])
		entry.setChar('>')
		entry.setColors(libtcod.Color(0, 100, 150),libtcod.Color(40, 40, 0))
		self.tile_entity.append(entry)
		self.entry=entry
			
		self.buildBlockedMap()