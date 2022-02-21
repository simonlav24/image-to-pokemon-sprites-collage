from math import fabs, sqrt, cos, sin, pi, floor, ceil
from random import uniform, randint, choice
import pygame, os, argparse

def colorCompare(color1, color2):
  rmean = ( color1[0] + color2[0] ) // 2
  r = color1[0] - color2[0]
  g = color1[1] - color2[1]
  b = color1[2] - color2[2]
  return sqrt((((512+rmean)*r*r)>>8) + 4*g*g + (((767-rmean)*b*b)>>8))

def getSprite(color):
	closestColors = []
	for key in colorToSprite:
		closestColors.append((colorCompare(key, color), colorToSprite[key]))
	closestColors.sort()
	closestColors = closestColors[:3]
	return sprites[int(choice(closestColors)[1])][0]

def testColor():
	win.blit(image, (0,0))
	colorAtMouse = win.get_at(pygame.mouse.get_pos())
	chosen = getSprite(colorAtMouse)
	win.blit(chosen, pygame.mouse.get_pos())

def makeImage():
	if not MakeImage._single:
		MakeImage()
	
	if not MakeImage._single.done:
		MakeImage._single.step()

class MakeImage:
	_single = None
	def __init__(self):
		MakeImage._single = self
		self.used = pygame.Surface((winWidth, winHeight))
		self.used.fill((0,0,0))
		self.result = pygame.Surface((winWidth, winHeight))
		self.result.fill((255,255,255))
		self.pos = [0,0]
		self.done = False
		self.timesBetweenDraws = 0
		self.method = "random"
	def advance(self):
		if self.method == "ordered":
			self.timesBetweenDraws += 1
			if self.timesBetweenDraws > 150:
				self.timesBetweenDraws = 0
				self.pos[1] += 10
				self.pos[0] = 0
				return
			self.pos[0] += 1
			if self.pos[0] >= winWidth:
				self.pos[1] += 5
				self.pos[0] = 0
			if self.pos[1] >= winHeight:
				self.done = True
		elif self.method == "random":
			self.pos[0] = randint(0, winWidth-1)
			self.pos[1] = randint(0, winHeight-1)
			return
			mousePos = pygame.mouse.get_pos()
			self.pos[0] = mousePos[0] + randint(-100, 100)
			# clamp to win width
			if self.pos[0] < 0:
				self.pos[0] = 0
			if self.pos[0] >= winWidth:
				self.pos[0] = winWidth - 1
			self.pos[1] = mousePos[1] + randint(-100, 100)
			# clamp to win height
			if self.pos[1] < 0:
				self.pos[1] = 0
			if self.pos[1] >= winHeight:
				self.pos[1] = winHeight - 1

	def step(self):
		# print(self.pos)
		if self.used.get_at(self.pos) == (255,0,0):
			self.advance()
			return
		
		# print(self.timesBetweenDraws)

		draw = True

		radius = 20
		for i in range(10):
			checkX = int(self.pos[0] + radius * cos(2*pi*i/10))
			checkY = int(self.pos[1] + radius * sin(2*pi*i/10))
			
			if checkX < 0 or checkX >= winWidth or checkY < 0 or checkY >= winHeight:
				continue
			
			if self.used.get_at((checkX, checkY)) == (255,0,0):
				draw = False
				break
				
		if not draw:
			self.advance()
			return
		
		currentCol = image.get_at(self.pos)
		spr = getSprite(currentCol)
			
		radius = min([spr.get_width()//2, spr.get_height()//2])
		
		for i in range(10):
			checkX = int(self.pos[0] + radius * cos(2*pi*i/10))
			checkY = int(self.pos[1] + radius * sin(2*pi*i/10))
			
			if checkX < 0 or checkX >= winWidth or checkY < 0 or checkY >= winHeight:
				continue
			
			if self.used.get_at((checkX, checkY)) == (255,0,0):
				draw = False
				break
		
		if not draw:
			self.advance()
			return

		if draw:
			self.timesBetweenDraws = 0
			self.result.blit(spr, (self.pos[0] - spr.get_width()//2, self.pos[1] - spr.get_height()//2))
			usedRadius = radius
			if self.method == "random":
				usedRadius *= 0.4
			pygame.draw.circle(self.used, (255,0,0), self.pos, usedRadius)
			
			# win.blit(self.used, (0,0))
			win.blit(self.result, (0,0))

# load color dictionary
spriteToColor = {}
with open('colorPicker.txt', 'r') as f:
    spriteToColor = eval(f.read())

# reverse the color dictionary
colorToSprite = {}
for key in spriteToColor:
    colorToSprite[spriteToColor[key]] = key

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--image', type=str, default='', help='image path')
# scale factor - int
parser.add_argument('-s', '--scale', type=int, default=1, help='scale factor')
args = parser.parse_args()

pygame.init()

image = pygame.image.load(args.image)
scaleFactor = args.scale
image = pygame.transform.scale(image, (image.get_width()*scaleFactor, image.get_height()*scaleFactor))

winWidth = image.get_width()
winHeight = image.get_height()
win = pygame.Surface((winWidth, winHeight))
screen = pygame.display.set_mode((1280, 720))

# load all sprites to list as sprite name
sprites = []
for f in os.listdir('sprites'):
	if os.path.isfile(os.path.join('sprites', f)):
		sprites.append((pygame.image.load('sprites/' + f), f))

################################################################################ Main Loop
interval = 50
time = 0
run = True
while run:
	time += 1
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		
		if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
			pygame.image.save(win, 'result.png')
	keys = pygame.key.get_pressed()
	if keys[pygame.K_ESCAPE]:
		run = False
		
	# testColor()
	makeImage()
	
	if time % interval == 0:
		screen.blit(pygame.transform.scale(win, (720 * (winWidth / winHeight), 720)), (0,0))
		pygame.display.update()
pygame.quit()














