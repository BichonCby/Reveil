import sys
import os
import pygame
from pygame.locals import *
import logging
import signal
import RPi.GPIO as GPIO
from threading import Thread
import time

#definitions de l'OS
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'TSLIB')
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

#define
AFF = 5
CAP = 6

class  AfficheHeure(Thread):
	#Thread qui va afficher l'heure en permanance
	def __init__(self):
		Thread.__init__(self)
		print 'initHeure'
	def run(self):
		global NotFinished
		global current_hour,current_min,current_sec

		print 'premierrun'
		while NotFinished:
			print 'runHeure'
			self.heure = time.localtime()
			current_hour = self.heure.tm_hour
			current_min = self.heure.tm_min
			current_sec = self.heure.tm_sec
			time.sleep(1)


class ScreenThd(Thread):
	#Thread d'affichage sur l'ecran. Il gere les captures
	def __init__(self):
                global boutons
		Thread.__init__(self)
		print 'initScreen'
		self.stscr = 0
		# bouton  nom    x0,y0,w,h,txt,aff,push
		boutons={'base':[0,0,320,240,' ',0,0]}
		boutons['keyb0']=[45,200,30,35,'0',0,0]
		boutons['keyb1']=[10,160,30,35,'1',0,0]
		boutons['keyb2']=[45,160,30,35,'2',0,0]
		boutons['keyb3']=[80,160,30,35,'3',0,0]
		boutons['keyb4']=[10,120,30,35,'4',0,0]
		boutons['keyb5']=[45,120,30,35,'5',0,0]
		boutons['keyb6']=[80,120,30,35,'6',0,0]
		boutons['keyb7']=[10,80,30,35,'7',0,0]
		boutons['keyb8']=[45,80,30,35,'8',0,0]
		boutons['keyb9']=[80,80,30,35,'9',0,0]
		#boutons['keyb2']=[

	def run(self):
		global NotFinished
		print 'premierRunScreen'
		lcd.fill(BLACK)
		pygame.display.update()
		while NotFinished:
			print 'runScreen'
			self.catch()
			self.redraw()
			time.sleep(1)
	#recuperation des appuis sur l'ecran (et les boutons??)
	def catch(self):
		for event in pygame.event.get():
			#print (event.type)
			if (event.type == MOUSEBUTTONUP):
				#print('top')
				pos = pygame.mouse.get_pos()
				x,y = pos
				print(pos)
				for (k,v) in boutons.items():
					if x>v[0] and x<v[0]+v[2] and y>v[1] and y<v[1]+v[3]:
						v[CAP]=1
						print(k)
					else:
						v[CAP]=0
						# print(k)
				# return
	def redraw(self):
		global current_jour,current_min,current_sec
		lcd.fill(BLACK)
		#reinitialisation
		for (k,v) in boutons.items():
			v[AFF] = 0
		#machine etat
		if self.stscr == 0: #
			self.screen0()
		elif self.strscr == 10:
			self.screen10()
		#text_current_time = font1.render('%02d:%02d:%02d' % (current_hour,current_min,current_sec),True,WHITE)
		#lcd.blit(text_current_time,(100,100))
		pygame.display.update()

	def screen0(self):
                #print 'screen0'
                #activation des boutons a afficher
                boutons['keyb0'][AFF]=1
                boutons['keyb1'][AFF]=1
                boutons['keyb2'][AFF]=1
                boutons['keyb3'][AFF]=1
                boutons['keyb4'][AFF]=1
                boutons['keyb5'][AFF]=1
                boutons['keyb6'][AFF]=1
                boutons['keyb7'][AFF]=1
                boutons['keyb8'][AFF]=1
                boutons['keyb9'][5]=1
		for (k,v) in boutons.items():
                        if v[5] == 1:
                                rect= pygame.draw.rect(lcd,RED,(v[0]-5,v[1],v[2],v[3]))
                                text = font1.render(v[4],True,WHITE)
                                lcd.blit(text,(v[0],v[1]))
                        #print(v)
		text = font1.render('%02d:%02d' % (alarm_hour,alarm_min),True, WHITE)
		lcd.blit(text,(10,10))
	def screen10(self):
		text = font1.render('--:--',True,WHITE)
		lcd.blit(text,(10,10))
#Colors
WHITE = (255,255,255)
BLACK = (1,1,1)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

alarm_hour = 8
alarm_min = 1
current_hour = 9
current_min = 7
current_sec = 10

NotFinished = True

pygame.init()

lcd = pygame.display.set_mode((320,240))

pygame.mouse.set_visible(False)
font1 = pygame.font.Font(None,50)
Screen = ScreenThd()
Heure = AfficheHeure()
#Heure.deamon = True #dies with main thread
#Screen.deamon = True
Heure.start()
Screen.start()

def signal_handler(signal, frame):
	global NotFinished
	print 'You pressed Ctrl+C!'
	NotFinished = False
	#print 'Fermeture du process Screen'
	#time.sleep(1)
	#print 'Fermeture du process Heure'
	#time.sleep(1)
	print 'Au revoir'
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
time.sleep(5000) # A remplacer
