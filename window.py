﻿# -*- coding: utf-8 -*-
#Basic window, timer, speech, menu handling
#Copyright (C) 2019 Yukio Nozawa <personal@nyanchangames.com>

from copy import copy
import pygame
import accessible_output2.outputs.auto
from pygame.locals import *
from dialog import *
class singletonWindow():
	"""Just a pygame window wrapper. As the name implies, you mustn't create multiple singletonWindow's in your game. """
	def __init__(self):
		pass#I want to avoid doing initialization at constructor as much as possible, just my liking
	def __del__(self):
		pygame.quit()

	def initialize(self,x,y,ttl):
		"""Initializes the game window. Returns True on success or False for failure. """
		pygame.init()
		self.clock=pygame.time.Clock()
		self.screen = pygame.display.set_mode((x, y))
		pygame.display.set_caption(ttl)
		self.keys=[0]*255
		self.previousKeys=[0]*255
		self.speech=accessible_output2.outputs.auto.Auto()
		return True

	def frameUpdate(self):
		"""A function that must be called once per frame. Calling this function will keep the 60fps speed. Returns True while the game is running and returns False when the process should exit. When returning false, you can immediately exit the game without caring about pygame termination because it's done automatically at the destructor. """
		self.clock.tick(60)
		self.screen.fill((255,63,10,))
		pygame.display.update()
		self.previousKeys=copy(self.keys)
		self.keys=pygame.key.get_pressed()
		if self.keys[K_LALT] and self.keys[K_F4]: return False
		for event in pygame.event.get():
			if event.type == QUIT: return False
		#end event
	#end frameUpdate

	def keyPressed(self,key):
		"""Retrieves if the specified key has changed to "pressed" from "not pressed" at the last frame. Doesn't cause key repeats.  """
		return self.keys[key] and not self.previousKeys[key]

	def keyPressing(self,key):
		"""Retrieves if the specified key is being pressed. Key repeats at 60rp/sec. """
		return self.keys[key]

	def wait(self,msec):
		"""waits for a specified period of milliseconds while keeping the window looping. Same as frameUpdate(), you should exit your game when this function returned false. """
		t=Timer()
		while t.elapsed<msec:
			if self.frameUpdate() is False: return False
		#end loop
		return True
	#end wait

	def say(self,str):
		"""tts speech"""
		self.speech.speak(str)

#end class singletonWindow


class Timer:
	def __init__(self):
		self.restart()

	def restart(self):
		self.startTick=pygame.time.get_ticks()

	@property
	def elapsed(self):
		return pygame.time.get_ticks()-self.startTick
#end class Timer

class menu:
	def __init__(self):
		pass
	def __del__(self):
		pass
	def initialize(self,wnd,ttl="no title", items=""):
		"""Initializes the menu with window instance, title and initial menu items. Requires a singletonWindow instance for this menu to work. Menu items should be a sequence of strings (not an array). the "#" character is used as the menu delimitor. """
		self.wnd=wnd
		self.title=ttl
		self.items=[]
		if items!="": self.items=items.split("#")
		self.cursor=0

	def add(self,str):
		"""Adds one or multiple menu items. # is used as the delimitor. """
		lst=str.split("#")
		for elem in lst:
			self.items.append(elem)

	def open(self):
		"""Starts the menu. You should call frameUpdate() to keep the menu operate after this. """
		if len(self.items)==0: return
		self.wnd.say("%s, %s" % (self.title, self.items[self.cursor]))

	def frameUpdate(self):
		"""The frame updating function for this menu. You should call your window's frameUpdate prior to call this function. Returns None for no action, -1 for cancellation and 0-based index for being selected. """
		if self.wnd.keyPressed(K_UP) and self.cursor!=0: self.moveTo(self.cursor-1)
		if self.wnd.keyPressed(K_DOWN) and self.cursor!=len(self.items)-1: self.moveTo(self.cursor+1)
		if self.wnd.keyPressed(K_HOME) and self.cursor!=0: self.moveTo(0)
		if self.wnd.keyPressed(K_END) and self.cursor!=len(self.items): self.moveTo(len(self.items)-1)
		if self.wnd.keyPressed(K_SPACE): self.moveTo(self.cursor)
		if self.wnd.keyPressed(K_ESCAPE):
			self.cancel()
			return -1
		#end cancel
		if self.wnd.keyPressed(K_RETURN):
			self.enter()
			return self.cursor
		#end enter
		return None
	#end frameUpdate

	def cancel(self):
		"""Internal function which is triggered when canceling the menu. """
		pass#if you wanna do something, write here instead

	def enter(self):
		"""Internal function which is triggered when selecting an option. """
		pass

	def moveTo(self,c):
		"""Moves the menu cursor to the specified position and reads out the cursor. """
		self.cursor=c
		self.wnd.say(self.items[self.cursor])
#end class menu
