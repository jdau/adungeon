import math

class Config:
	SCREEN_WIDTH = 40
	SCREEN_HEIGHT = 30
	FPS=5
	
	OW_WIDTH=200
	OW_HEIGHT=130
	OW_TREE_THRES=0.2
	
	DUNGEONS=10
	
	WID2=0
	HGT2=0
	def __init__(self):
		self.WID2 = int(math.floor(self.SCREEN_WIDTH/2))
		self.HGT2 = int(math.floor(self.SCREEN_HEIGHT/2))
	
cfg=Config()