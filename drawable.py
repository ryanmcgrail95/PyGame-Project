import sys
import os
import pygame
import math
import time
import random
from pygame.locals	import *
from math2		import *
from sprite 		import Sprite


class Drawable(object):
	def __init__(self, gameSpace, x,y, fileName, frameNumX, frameNumY):
		self.gs = gameSpace

		self.x = x
		self.y = y
				
		# Load Sprite
		self.sprite = Sprite(fileName, frameNumX, frameNumY);
		self.spriteIndex = 0
		self.spriteSpeed = 1
		self.spriteAngle = 0
		self.spriteScale = 1
		self.spriteLoop = True

		self.vx = 0
		self.vy = 0

		
	def destroy(self):
		self.gs.instanceRemove(self)
		
	def tick(self, input):
		# Move (x,y) based on velocity
		self.x += self.vx
		self.y += self.vy
		
		# Animate image, and loop if necessary
		self.spriteIndex += self.spriteSpeed
		if self.spriteLoop:
			self.spriteIndex %= self.sprite.frameNum
		
	def draw(self, screen):		
		self.sprite.draw(screen, self.x, self.y, self.spriteIndex, self.spriteAngle, self.spriteScale);