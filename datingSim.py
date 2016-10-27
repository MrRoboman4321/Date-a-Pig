import sys  # Import the sys module (for exit handling)
import time, os, pickle, textwrap
from enum import Enum
import pygame  # Import the PyGame Module
from pygame.locals import *  # Globalise all the PyGame local methods

basePath = os.path.dirname(__file__)

toRender = []

DELAY = 1/30

FONT_SIZE = 10
#WIDTH, HEIGHT = 960, 720
WIDTH, HEIGHT = 240, 180

LETTER_WIDTH = 10 #guess and check baby
BOX_BUFFER = 3
CHAR_PER_LINE = 37

DATA_LINES_RELATIVE = "gamedata\\lines.wlia" #Whose line is it anyway?

FONT_COURIER_RELATIVE = "fonts\\cour.ttf" #Monospaced font for conversations

IMG_BACKGROUND_RELATIVE = "images\\background.png" #Textbox and other various background items
IMG_LYMAN_RELATIVE = "images\\LymanCutlar.png" #Lyman Cutlar, the American (I think)

SFX_MANSPEAK_RELATIVE = "sounds\\WoodblockLow.wav" #Both Lyman and the other guy's speech sound

courier = os.path.join(basePath, FONT_COURIER_RELATIVE)
background = os.path.join(basePath, IMG_BACKGROUND_RELATIVE)
manspeak = os.path.join(basePath, SFX_MANSPEAK_RELATIVE)
lyman = os.path.join(basePath, IMG_LYMAN_RELATIVE)
lines = os.path.join(basePath, DATA_LINES_RELATIVE)

class Screen(Enum):
	menu = 0
	game = 1
	screen = 2

class MovingText():
	def __init__(self, fontPath, size, soundPath = None):
		self.pygamefont = pygame.font.Font(fontPath, size)
		self.lineFont = []
		self.lines = 1

		if(soundPath == None):
			self.hasSound = False
		else:
			self.hasSound = True
			self.sound = pygame.mixer.Sound(soundPath)
			self.channel = pygame.mixer.Channel(0)
	def getHeight(self):
		return self.pygamefont.get_height()
	def startNewSequence(self, text, delay): #text to render, fraction of second per character (do not exceed 1/(set FPS)), maximum x coord to render at
		self.text = text
		self.delay = delay
		self.t0 = time.clock()
		self.counter = 0
		self.channel.play(self.sound, loops=-1)
		self.paused = False
		self.finished = False
	def render(self, antialiasing, color, pos, maxPos, progressed):
		dt = time.clock() - self.t0
		if(self.paused):
			if(progressed):
				self.text = self.text[len(''.join(textwrap.wrap(self.text[:self.counter], CHAR_PER_LINE)[:4])):]
				self.counter = 0
				self.t0 = time.clock()
				self.channel.unpause()
				self.paused = False
		if(dt > self.delay and not self.paused):
			if(self.counter != max(len(self.text), 37)):
				self.counter += 1
			else:
				self.paused = True
				self.finished = True
				if(self.hasSound):
					self.channel.stop()
			print("Total character: " + str(len(self.text)) + ", counter at: " + str(self.counter))
			self.t0 = time.clock()

		if(self.text[:self.counter] == ""):
			text = "."
		else:
			text = self.text[:self.counter]
		if(self.counter == CHAR_PER_LINE*4):
			self.paused = True
			self.channel.stop()
		
		#toRenderText = [text[i:i+CHAR_PER_LINE] for i in range(0, len(text), CHAR_PER_LINE)]
		
		lineSplit = textwrap.wrap(text, CHAR_PER_LINE)
		
		toRender = [self.pygamefont.render(i, antialiasing, color) for i in lineSplit]
		print("To Render: ")
		print(toRender)
		
		#toRender.append(self.pygamefont.render(self.text[:self.counter], antialiasing, color))
		return toRender
	def changeSpeed(self, newDelay):
		self.delay = newDelay
	
	def isFinished(self):
		return self.finished
		
class MyGame():  # Game Class

	def main(self):  # Main Method (always takes the object as 1st arg)

		pygame.init()  # Initialise the PyGame Framework

		text = MovingText(courier, FONT_SIZE, manspeak)
		
		backgroundImg = pygame.image.load(background)
		lymanImg = pygame.image.load(lyman)
		
		linesList = pickle.load(open(lines, "rb"))
		curline = 0
		
		questionsStarted = False
		answers = []

		screen = pygame.display.set_mode((WIDTH*3, HEIGHT*3))  # Create your screen / window
		staging = pygame.Surface((WIDTH, HEIGHT))
		# You can also pass an optional fullscreen arg
		# screen = pygame.display.set_mode(size, FULLSCREEN)

		clock = pygame.time.Clock()  # Set up the game clock

		pygame.display.set_caption('A War of Nutrition')  # Set the titlebar text

		staging.fill((255, 255, 255))  # Fill the screen with white (RGB)
		text.startNewSequence(linesList[curline][5], DELAY)
		while True:  # The Game Loop
			progressed = False
			clock.tick(60)  # 60 frames per second

			# process key presses
			selection = 0
			for event in pygame.event.get():
				if event.type == pygame.QUIT:  # Handle Quit Event
					sys.exit()  # Clean Exit
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_k:
						text.changeSpeed(DELAY/4)
					elif event.key == pygame.K_RETURN:
						progressed = True
					elif event.key == K_1:
						selection = 1
					elif event.key == K_2:
						selection = 2
					elif event.key == K_3:
						selection = 3
					elif event.key == K_4:
						selection = 4
				elif event.type == pygame.KEYUP:
					if event.key == pygame.K_k:
						text.changeSpeed(DELAY)

			#
			# Your Game Code Goes Here
			#
			
			staging.blit(backgroundImg, (0,0), None)
			staging.blit(lymanImg, (0,0), None)
			if(text.isFinished() and (progressed or questionsStarted)):
				if(not questionsStarted):
					questionsStarted = True
					if(linesList[curline][8] == ''):
						questionsStarted = False
						curline = int(linesList[curline][6])-1
						text.startNewSequence(linesList[curline][5], DELAY)
					for i in range(3):
						if(linesList[curline][7+(2*i)] != ""):
							print("\nappending answers\n")
							answers.append(MovingText(courier, FONT_SIZE, manspeak))
							answers[-1].startNewSequence(str(i+1) + "." + linesList[curline][7+(2*i)], DELAY)
				if(linesList[curline][3+(2*selection)] != "" and selection != 0):
					curline = int(linesList[curline][4+(2*selection)])-1 #uh
					text.startNewSequence(linesList[curline][5], DELAY)
					questionsStarted = False
					answers = []
				for idx, val in enumerate(answers):
					print(answers) #send help please
					staging.blit(val.render(False, (0,0,0), (5 + BOX_BUFFER, 127 + idx*val.getHeight()), (235 - LETTER_WIDTH, 175), False)[0], (5 + BOX_BUFFER, 127 + idx*val.getHeight()), None)
			if(not questionsStarted):
				for idx, val in enumerate(text.render(False, (0,0,0), (5 + BOX_BUFFER, 124), (235 - LETTER_WIDTH, 175), progressed)):
					staging.blit(val, (5 + BOX_BUFFER, int(idx*text.getHeight()) + 125), None)
			pygame.transform.scale(staging, (WIDTH*3, HEIGHT*3), screen)
			#screen.blit(pygame.transform.scale(staging, (int(640*1.5), int(480*1.5))), (0,0), None)
			
			pygame.display.update()  # Update the screen


if __name__ == '__main__':
	game = MyGame()  # Instantiate the Game class
	game.main()  # Call the main method
