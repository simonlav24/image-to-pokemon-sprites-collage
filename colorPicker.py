from math import fabs, sqrt, cos, sin, pi, floor, ceil
from random import uniform, randint, choice
import pygame, os, ast
pygame.init()

pygame.font.init()
myfont = pygame.font.SysFont('Arial', 12)

winWidth = 1280
winHeight = 720
win = pygame.display.set_mode((winWidth,winHeight))


currentIndex = 0
currentSprite = None
imageCount = sum([1 for f in os.listdir('sprites') if os.path.isfile(os.path.join('sprites', f))])

colorByIndex = {}

def loadSprite(index):
	num = str(index).zfill(3)
	return pygame.image.load('sprites/' + num + '.png')

def saveIndices():
	with open('colorPicker.txt', 'w') as f:
		f.write(str(colorByIndex))

def loadIndices():
	global colorByIndex
	try:
		with open('colorPicker.txt', 'r') as f:
			colorByIndex = ast.literal_eval(f.read())
	except:
		colorByIndex = {}

loadIndices()
currentSprite = loadSprite(currentIndex)

run = True
while run:
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		# mouse click
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			color = win.get_at(event.pos)
			colorByIndex[currentIndex] = color

		if event.type == pygame.KEYDOWN:
			# if left arrow
			if event.key == pygame.K_LEFT:
				currentIndex = (currentIndex - 1) % imageCount
				currentSprite = loadSprite(currentIndex)
			if event.key == pygame.K_RIGHT:
				currentIndex = (currentIndex + 1) % imageCount
				currentSprite = loadSprite(currentIndex)
			if event.key == pygame.K_s:
				saveIndices()
	
	keys = pygame.key.get_pressed()
	if keys[pygame.K_ESCAPE]:
		run = False

	win.fill((255,255,255))
	# blit sprite all over screen in pattern
	for x in range(0, winWidth, currentSprite.get_width()):
		for y in range(0, winHeight, currentSprite.get_height()):
			win.blit(currentSprite, (x,y))
	# blit sprite in center of screen 6 times larger
	win.blit(pygame.transform.scale(currentSprite, (currentSprite.get_width() * 6, currentSprite.get_height() * 6)), (winWidth/2 - currentSprite.get_width() * 3, winHeight/2 - currentSprite.get_height() * 3))
	
	# blit current color if it exists
	num = str(currentIndex).zfill(3)
	if num in colorByIndex.keys():
		color = colorByIndex[num]
		pygame.draw.rect(win, color, (0,winHeight - 100, 100, 100))

	pygame.display.update()
pygame.quit()