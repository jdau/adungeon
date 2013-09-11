import libtcodpy as libtcod
import random,math
from config import *

class gameColor:
	r_lower=0
	g_lower=0
	b_lower=0
	
	r_upper=0
	g_upper=0
	b_upper=0
	
	init=False
	
	def generate(self):
		return libtcod.Color(random.randint(self.r_lower,self.r_upper), random.randint(self.g_lower,self.g_upper), random.randint(self.b_lower,self.b_upper))
	
	def setColor(self,r_l,r_u,g_l,g_u,b_l,b_u):
		self.init=True
		self.r_lower=r_l
		self.g_lower=g_l
		self.b_lower=b_l
		
		self.r_upper=r_u
		self.g_upper=g_u
		self.b_upper=b_u
		
	def setColVariance(self,r,r_var,g,g_var,b,b_var):
		self.init=True
		[self.r_lower,self.r_upper]=self.genVariance(r,r_var)
		[self.g_lower,self.g_upper]=self.genVariance(g,g_var)
		[self.b_lower,self.b_upper]=self.genVariance(b,b_var)
		
		print self.r_lower,self.r_upper
		
	def genVariance(self,b,var):
		return [int(b-math.floor(float(var)/2.0)),int(b+math.ceil(float(var)/2.0))]