import libtcodpy as libtcod
import random,copy,math
from config import *

class AIPlayer:
	x=0
	y=0
	
	foreColor=None
	backColor=None
	
	goal=None
	path=None
	path_progress=None
	
	explored=False
	
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
		
	def setSeen(self,x,y): pass
			
	def edgeCalc(self,idx,iter,edge,distance):
		px=self.x
		py=self.y
		
		if idx==1: # top
			cx=px-int(math.floor(edge/2))+iter
			cy=py-distance
		elif idx==2: # right
			cx=px+distance
			cy=py-int(math.floor(edge/2))+iter
		elif idx==3: # bottom
			cx=px-int(math.floor(edge/2))+iter
			cy=py+distance
		elif idx==4: # left
			cx=px-distance
			cy=py-int(math.floor(edge/2))+iter
			
		return(cx,cy)
		
	def cornerCalc(self,idx,d,px,py):
		if idx==1: return (px-d,px-d)
		elif idx==2: return (px+d,px-d)
		elif idx==3: return (px-d,px+d)
		elif idx==4: return (px+d,px+d)
		
	def findExplorePoint(self,world):
		if self.explored: return (False,False) #expecting a list
		px=self.x
		py=self.y
		
		ww=world.getWidth()
		wh=world.getHeight()
		
		# Scan in expanding circle outwards
		distance=1
		edge=1
		potentials=[]
		effort=7
		while len(potentials)<effort:
			# scan edges in a random priority
			edges=range(1,4)
			random.shuffle(edges)
			for i in edges:
				for j in xrange(edge):
					[cx,cy]=self.edgeCalc(i,j,edge,distance)
					if cx<0 or cx>=ww: break
					if cy<0 or cy>=wh: break
					if not world.isBlocked(cx,cy) and not world.isSeen(cx,cy):
						potentials.append((cx,cy))
						#world.putThing(cx,cy)
						
			# and corners in same random priority
			for i in edges:
				[cx,cy]=self.cornerCalc(i,distance,px,py)
				if cx<0 or cx>=ww: break
				if cy<0 or cy>=wh: break
				if not world.isBlocked(cx,cy) and not world.isSeen(cx,cy):
					potentials.append((cx,cy))
					#world.putThing(cx,cy)
					
			distance=distance+1
			edge=edge+2
			
			if distance>max(ww,wh):
				self.explored=True
				return (False,False)
		
		# now pop random for effort amount and pick shortest path
		random.shuffle(potentials)
		map=world.getBlockedMap()
		self.path=libtcod.path_new_using_map(map,0)
		libtcod.path_compute(self.path,self.x,self.y,potentials[0][0],potentials[0][1])
		self.goal=potentials[0]
	
	def tick(self,world):
		if not self.goal:
			self.findExplorePoint(world)
			if not self.goal: return #nop
			self.path_progress=0
		
		[next_x,next_y]=libtcod.path_get(self.path, self.path_progress)
		self.x=next_x
		self.y=next_y
		self.path_progress=self.path_progress+1
		if libtcod.path_size(self.path)==self.path_progress:
			self.goal=None
			self.path=None
			print "path done"