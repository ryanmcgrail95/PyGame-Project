import sys
import os
import pygame
import math
import time
import random
from pygame.locals	import *
from math2			import *
from sprite 		import *
from drawable		import *
from mat			import *
from laser			import *
from explosion		import *
import canv3d


class Arwing(Drawable):
	hasLoaded = False

	MOD_ARWING = None
	
	TEX_JET = None
	TEX_JET_WIDTH = 128
	TEX_JET_HEIGHT = 128

	SND_ENGINE = None
	SND_SINGLE_SHOT = None
	SND_BOOST = None
	SND_BRAKE = None
	SND_DAMAGE = None
	
	SPD_BASE = 5
	SPD_MAX = 10
	SPD_MIN = 1

	def __init__(self, gameSpace, x,y,z):
		super(Arwing, self).__init__(gameSpace, x,y,z, x,y,z+1, 0,1,0)
		
		# If Arwing sounds/model not loaded yet, do so now!
		if not Arwing.hasLoaded:
			Arwing.MOD_ARWING = canv3d.loadObj("arwing.obj")
			Arwing.TEX_JET = pygame.surfarray.pixels2d(pygame.image.load("img/jet.png").convert_alpha())
			Arwing.SND_ENGINE = pygame.mixer.Sound("snd/engine.ogg")
			Arwing.SND_SINGLE_SHOT = pygame.mixer.Sound("snd/singleshot.ogg")
			Arwing.SND_BOOST = pygame.mixer.Sound("snd/boost.ogg")
			Arwing.SND_BRAKE = pygame.mixer.Sound("snd/brake.ogg")
			Arwing.SND_DAMAGE = pygame.mixer.Sound("snd/damage.ogg")

		# Get
		self.dpos = numpy.array([x, y, z, 1.])		
		self.dtoPos = numpy.array([x, y, z-1, 1.])		
		self.dupNorm = numpy.array([0,1,0,0.])

		self.speed = 0
		self.roll = 0
		self.pitch = 0
		self.yaw = 0
		
		self.drawHP = self.hp = 1
		
		self.hurtAnimation = -1
		
		self.drawPoints = self.points = 0;

	def respawn(self):
		self.ori[0] = 0;
		self.ori[1] = 0;
		self.ori[2] = 0;
		self.ori[3] = 0;
		self.ori[4] = 0;
		self.ori[5] = 1;
		self.ori[6] = 0;
		self.ori[7] = 1;
		self.ori[8] = 0;
		
		self.drawHP = self.hp = 1;
		self.drawPoints = self.points = 0;
		self.hurtAnimation = -1;
		

	def tick(self, input):
		if self.hp == 0:
			return
	
		super(Arwing, self).tick(input)
		
		if self.hurtAnimation > -1:
			self.hurtAnimation += .02
		
			if self.hurtAnimation > 1:
				self.hurtAnimation = -1
		
		# Smoothly move drawn values to true values
		self.drawHP += (self.hp - self.drawHP)/5
		if self.drawPoints > self.points:
			self.drawPoints -= 1
			if self.drawPoints < self.points:
				self.drawPoints = self.points

		if (input['respawn']):
			self.respawn();

			
	def hurt(self):
		if self.hp == 0:
			return

		Arwing.SND_DAMAGE.play()
		self.hurtAnimation = 0
		self.hp -= .1
		
	def addPoints(self, points):
		self.points += points;
	
	def explode(self):
		if self.hp == 0:
			return

		self.gs.instanceAppend( Explosion(self.gs, self.ori[0],self.ori[1],self.ori[2]) )
	
	def draw(self, screen):
		if self.hp == 0:
			return
			
		canv3d.setMatIdentity(MAT_T)
		canv3d.addMatTranslation(MAT_T, self.ori[0],self.ori[1],self.ori[2])

		spd = 8
		for i in range(0,3):
			self.dpos[i] += (self.ori[i] - self.dpos[i])/spd;
			self.dtoPos[i] += (self.ori[3+i] - self.dtoPos[i])/spd;
			self.dupNorm[i] += (self.ori[6+i] - self.dupNorm[i])/spd;
		
		nX = self.dtoPos[0]-self.dpos[0]
		nY = self.dtoPos[1]-self.dpos[1]
		nZ = self.dtoPos[2]-self.dpos[2]
		
		canv3d.addMatAntiLook(MAT_T, 0,0,0,		nX,nY,nZ,		self.dupNorm[0],self.dupNorm[1],self.dupNorm[2]);

		canv3d.addMatRotationX(MAT_T, self.pitch)
		canv3d.addMatRotationY(MAT_T, self.yaw)

		if self.hurtAnimation > -1:
			cR = 255
			cG = cB = int(255 * abs(cosd(720 * self.hurtAnimation)))
			canv3d.addMatRotationY(MAT_T, -45)
			canv3d.addMatRotationZ(MAT_T, 45 * cosd(360*4 * self.hurtAnimation) * (1 - self.hurtAnimation) )
			canv3d.addMatRotationY(MAT_T, 45)
		else:
			cR = cG = cB = 255

		# Further transform model
		canv3d.addMatRotationZ(MAT_T, self.roll)
		canv3d.addMatTranslation(MAT_T, 0,-20,0)		
		canv3d.addMatScale(MAT_T,.25,.25,.25);

		# Compile matrices into completeMat before drawing
		canv3d.compileMats()

		
		# Draw Arwing, modifying color if damage animation is playing
		canv3d.setRGB(cR,cG,cB)	
		canv3d.drawObj(Arwing.MOD_ARWING);
		canv3d.setRGB(255,255,255)
		
		# Draw exhaust behind ship
		xs = 50 * (1 + .5*rnd()) * (.25 + .75*self.speed / Arwing.SPD_BASE)
		ys = xs * .8
		up = 10
		back = -80
		canv3d.setTexture(Arwing.TEX_JET, Arwing.TEX_JET_WIDTH, Arwing.TEX_JET_HEIGHT)
		canv3d.draw3dFloor(-xs,up-ys,xs,up+ys,back);