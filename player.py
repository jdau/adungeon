import libtcodpy as libtcod
import random,copy,math,time
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
	
	pathMap=None
	
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
		e2=int(edge/2)
		if idx==1: # top
			cx=px-e2+iter
			cy=py-distance
		elif idx==2: # right
			cx=px+distance
			cy=py-e2+iter
		elif idx==3: # bottom
			cx=px-e2+iter
			cy=py+distance
		elif idx==4: # left
			cx=px-distance
			cy=py-e2+iter
			
		return(cx,cy)
		
	def cornerCalc(self,idx,d,px,py):
		if idx==1: return (px-d,py-d)
		elif idx==2: return (px+d,py-d)
		elif idx==3: return (px-d,py+d)
		elif idx==4: return (px+d,py+d)
		
	def findExplorePoint(self,world):
		if self.explored: return (False,False) #expecting a list
		t0 = time.time()
		
		px=self.x
		py=self.y
		
		ww=world.getWidth()
		wh=world.getHeight()
		
		# Scan in expanding circle outwards
		distance=1
		edge=1
		searchEffort=150
		pathEffort=4
		
		potentials=[]
		edges=[1,2,3,4]
		goodPath=False
		
		while not goodPath:
			while len(potentials)<=searchEffort:
				# scan edges
				for i in edges:
					for j in xrange(edge):
						[cx,cy]=self.edgeCalc(i,j,edge,distance)
						if cx<0 or cx>=ww: continue
						if cy<0 or cy>=wh: continue
						if world.isBlocked(cx,cy) or world.isSeen(cx,cy): continue
						if world.isPathable(cx,cy):
							potentials.append((cx,cy))
							#world.putThing(cx,cy)
							
				# and corners
				for i in edges:
					[cx,cy]=self.cornerCalc(i,distance,px,py)
					if cx<0 or cx>=ww: continue
					if cy<0 or cy>=wh: continue
					if world.isBlocked(cx,cy) or world.isSeen(cx,cy): continue
					if world.isPathable(cx,cy):
						potentials.append((cx,cy))
						#world.putThing(cx,cy)
						
				distance=distance+1
				edge=edge+2
				
				if distance>max(ww,wh):
					self.explored=True
					return (False,False)
			
			# now pop random for effort amount and pick shortest path
			distRank={}
			for cd in potentials:
				dst=abs(px-cd[0])+abs(py-cd[1])
				while dst in distRank: dst=dst+1
				distRank[dst]=cd
			
			potentials=[]
			dkKeys=sorted(distRank)
			for i in xrange(int(searchEffort/2)):
				potentials.append(distRank[dkKeys[i]])
				#world.putThing(potentials[i][0],potentials[i][1])
				
			pselect=random.sample(potentials,pathEffort)
			distRank={}
			if not self.pathMap: self.pathMap=world.getBlockedMap()
			for cd in pselect:
				#world.putThing(cd[0],cd[1],"*")
				path=libtcod.path_new_using_map(self.pathMap,0)
				libtcod.path_compute(path,self.x,self.y,cd[0],cd[1])
				ps=libtcod.path_size(path)
				distRank[ps]=(cd,path)
			
			# get closest path len - if it is very high compared to distance, reject and expand search
			dkKeys=sorted(distRank)
			if dkKeys[0] < distance*4:
				ret=distRank[dkKeys[0]]
				goodPath=True
				print "Successful search at pl",dkKeys[0],"distance",distance,"took",int(math.floor((time.time()-t0)*1000)),"ms"
			else:
				print "Rejected search at pl",dkKeys[0],"distance",distance,"took",int(math.floor((time.time()-t0)*1000)),"ms"
		
		return ret
	
	def tick(self,world):
		if self.explored: return
		if not self.goal:
			[self.goal,self.path] = self.findExplorePoint(world)
			if not self.goal:
				self.explored=True
				print "All done"
				return
			self.path_progress=0
		
		[next_x,next_y]=libtcod.path_get(self.path, self.path_progress)
		self.x=next_x
		self.y=next_y
		self.path_progress=self.path_progress+1
		if libtcod.path_size(self.path)==self.path_progress:
			self.goal=None
			self.path=None