import sys
import os
import pygame
import math
import time
import random
from drawable import *
from pygame.locals	import *
from math2			import *
import gfx2d
from pygame			import *

class Hud(Drawable):	
	def __init__(self, gameSpace):
		super(Hud, self).__init__(gameSpace, 0,0,0, 0,0,1, 0,1,0)
	
		self.imgStatic = Sprite("static.png", 2,1)
		self.imgFlynn = Sprite("flynn.png", 3,1)
		self.ind = 0
		
		self.staticTime = 100
		
		self.scaredTime = 50
		
		self.talkInd = 0
		self.text = "Do a barrel roll!\n\nTry a somersault!\n\nPress V to brake!"
				
		self.imgTalkBar = Surface((640-15-126,96)).convert_alpha()
		self.imgTalkBar.fill((0,0,0,128))

	def tick(self, input):
		self.ind = (self.ind + .3) % 2
		
		if self.staticTime > 0:
			self.staticTime -= 1
		elif self.scaredTime > 0:
			self.scaredTime -= 1
		else:
			if self.talkInd < len(self.text):
				self.talkInd += .25
			else:
				self.ind = 0

	def draw(self, screen):
		pass
		
	def blitToScreen(self, screen):
		if self.staticTime > 0:
			self.imgStatic.draw(screen, 15+48, 480-48-15, frame=self.ind, scale=.75)	
		elif self.scaredTime > 0:
			self.imgFlynn.draw(screen, 15+48, 480-48-15, frame=2, scale=.75)
		else:
			self.imgFlynn.draw(screen, 15+48, 480-48-15, frame=self.ind, scale=.75)
		
		xTB = 15+96+15
		yTB = 480-15-96
		screen.blit(self.imgTalkBar, (xTB, yTB))
		
		gfx2d.drawText(screen, self.text[:(int)(self.talkInd)], xTB+15,yTB+15)
	
		if self.gs.isConnected:
			gfx2d.drawText(screen, "Successfully connected!", 0,0)
		else:
			dotStr = "." * (3 - self.gs.connectTimer/self.gs.connectDiv % 4)
			gfx2d.drawText(screen, "Attempting to connect" + dotStr, 0,0)