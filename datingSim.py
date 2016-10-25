#!/usr/bin/env python

#
#   PyGame Boilerplate v 0.1 Feb 2014
#
#   Copyright (C) 2014 Rob Dudley
#
#   web   : http://www.rcwd.me/
#   email : rob@rcwd.me
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.


import sys  # Import the sys module (for exit handling)
import time, os
import pygame  # Import the PyGame Module
from pygame.locals import *  # Globalise all the PyGame local methods

basePath = os.path.dirname(__file__)
courier = os.path.join(basePath, "Fonts\\cour.ttf")

toRender = []

DELAY = 1/30

FONT_PATH = courier
FONT_SIZE = 10
#WIDTH, HEIGHT = 960, 720
WIDTH, HEIGHT = 240, 180

LETTER_WIDTH = 10 #guess and check baby
BOX_BUFFER = 3

COURIER_RELATIVE = "fonts\\cour.ttf"
BACKGROUND_RELATIVE = "images\\background.png"

courier = os.path.join(basePath, COURIER_RELATIVE)

class MovingText():
	def __init__(self, font, size):
		self.pygamefont = pygame.font.Font(font, size)
		self.lineFont = []
		self.lines = 1
	def getHeight(self):
		return self.pygamefont.get_height()
	def startNewSequence(self, text, delay): #text to render, fraction of second per character (do not exceed 1/(set FPS)), maximum x coord to render at
		self.text = text
		self.delay = delay
		self.t0 = time.clock()
		self.counter = 0
	def render(self, antialiasing, color, pos, maxPos):
		dt = time.clock() - self.t0
		if(dt > self.delay):
			self.counter += 1
			self.t0 = time.clock()
		
		text = self.text[:self.counter]
		textPos = 1
		toRender = []
		while(len(text) != 0):
			if(self.pygamefont.size(text[:textPos])[0] + pos[0] > maxPos[0] or len(text)-1 < textPos):
				textTR = text[:textPos].lstrip()
				toRender.append(self.pygamefont.render(textTR, antialiasing, color))
				text = text[textPos:]
				textPos = 1
			textPos += 1
			print(textPos)
		#toRender.append(self.pygamefont.render(self.text[:self.counter], antialiasing, color))
		return toRender
	def changeSpeed(self, newDelay):
		self.delay = newDelay
		
class MyGame():  # Game Class

	def main(self):  # Main Method (always takes the object as 1st arg)

		pygame.init()  # Initialise the PyGame Framework

		text = MovingText(FONT_PATH, FONT_SIZE)
		
		background = pygame.image.load(os.path.join(basePath, BACKGROUND_RELATIVE))

		screen = pygame.display.set_mode((WIDTH*3, HEIGHT*3))  # Create your screen / window
		staging = pygame.Surface((WIDTH, HEIGHT))
		# You can also pass an optional fullscreen arg
		# screen = pygame.display.set_mode(size, FULLSCREEN)

		clock = pygame.time.Clock()  # Set up the game clock

		pygame.display.set_caption('A War of Nutrition')  # Set the titlebar text

		staging.fill((255, 255, 255))  # Fill the screen with white (RGB)
		text.startNewSequence("Scrolling text is now working at fancy delays, and longer so we can test the effects of sped up text. This is a continuation to see what it looks like", DELAY)
		while True:  # The Game Loop

			clock.tick(60)  # 60 frames per second

			# process key presses
			for event in pygame.event.get():
				if event.type == pygame.QUIT:  # Handle Quit Event
					sys.exit()  # Clean Exit
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_k:
						text.changeSpeed(DELAY/4)
				if event.type == pygame.KEYUP:
					if event.key == pygame.K_k:
						text.changeSpeed(DELAY)

			#
			# Your Game Code Goes Here
			#
			
			staging.blit(background, (0,0), None)
			for idx, val in enumerate(text.render(False, (0,0,0), (5 + BOX_BUFFER, 124), (235 - LETTER_WIDTH, 175))):
				staging.blit(val, (5 + BOX_BUFFER, int(idx*text.getHeight()) + 125), None)
			#staging.blit(text.render(False, (0,0,0), (0,0), (WIDTH, HEIGHT)), (0,0), None)
			pygame.transform.scale(staging, (WIDTH*3, HEIGHT*3), screen)
			#screen.blit(pygame.transform.scale(staging, (int(640*1.5), int(480*1.5))), (0,0), None)
			
			pygame.display.update()  # Update the screen


if __name__ == '__main__':
	game = MyGame()  # Instantiate the Game class
	game.main()  # Call the main method
