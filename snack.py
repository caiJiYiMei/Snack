#import the required modles
import pygame
from pygame.locals import *
import random
import sys

#some costant about color
#            R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)

#some constant about WIDTH and HEIGHT
FPS    = 15
BOXLEN = 20
WINWID = 640	#the width of the window
WINHEI = 480	#the height of the window
BOXWID = int(WINWID/BOXLEN)
BOXHEI = int(WINHEI/BOXLEN)

#Define the direction
UP    = 'up'
DOWN  = 'down'
LEFT  = 'left'
RIGHT = 'right'



#The main loop of the game
def main():
	pygame.init()
	global CANVAS, CLOCK, BEEATED, SCORE
	#Initialize the direction and surface
	CANVAS = pygame.display.set_mode((WINWID, WINHEI))
	CLOCK  = pygame.time.Clock()
	BEEATED = False
	SCORE = 0
	pygame.display.set_caption('WARMY1.0')

	#initial a snack which is 3 rect length, and it's direction
	snack = createSnack()
	direction = RIGHT
	head = snack[0]
	apple = creatApple()

	gameBeginOver(('Game', 'Begin'))
	#The main loop of the game
	while True:
		#listening the users controll demanding
		for event in pygame.event.get():
			if event.type == QUIT:
				crash()
			elif event.type == KEYDOWN:
				if event.key == K_LEFT and direction != RIGHT:
					direction = LEFT
				elif event.key == K_RIGHT and direction != LEFT:
					direction = RIGHT
				elif event.key == K_UP and direction != DOWN:
					direction = UP
				elif event.key == K_DOWN and direction != UP:
					direction = DOWN
				elif event.key == K_ESCAPE:
					crash()
		CANVAS.fill(BLACK)
		drawGrid()
		if touchBound(snack) != None:
			snack, apple, SCORE, BEEATED, direction = touchBound(snack)
		if BEEATED:
			apple = creatApple()
		drawApple(apple[0], apple[1])
		snack = eatApple(snack, apple)
		drawScore()
		snack = move(snack, direction)
		drawSnack(snack)
		pygame.display.update()
		CLOCK.tick(FPS)

#Examine if the sanck has out of the bound
def touchBound(snack):
	x, y = snack[0]
	if x == -1 or x == BOXWID or y == -1 or y == BOXHEI:
		return gameBeginOver(('Game', 'Over'))
	for body_x, body_y in snack[1:]:
		if body_x == x and body_y == y:
			return gameBeginOver(('Game', 'Over'))

#Move the snack
def move(snack, direction):
	head_x, head_y = snack[0]
	if direction == UP:
		snack.insert(0, (head_x, head_y - 1))
	elif direction == DOWN:
		snack.insert(0, (head_x, head_y + 1))
	elif direction == RIGHT:
		snack.insert(0, (head_x + 1, head_y))
	elif direction == LEFT:
		snack.insert(0, (head_x - 1, head_y))
	return snack

#eat an apple
def eatApple(snack, apple):
	global BEEATED, SCORE
	x, y = snack[0]
	apple_x, apple_y = apple
	if x == apple_x and y == apple_y:
		snack.insert(0, (apple_x, apple_y))
		BEEATED = True
		SCORE += 1
	else:
		del snack[len(snack) - 1]
		BEEATED = False
	return snack

#creat an apple
def creatApple():
	apple_x = random.randint(0, BOXWID)
	apple_y = random.randint(0, BOXHEI)
	return (apple_x, apple_y)

#If touch the bound the crash the programe
def crash():
	pygame.quit()
	sys.exit()

#Create a new snack when initial the game
def createSnack():
	start_x = random.randint(7, BOXWID - 7)
	start_y = random.randint(7, BOXHEI - 7)
	return [(start_x, start_y), (start_x - 1, start_y), (start_x -2, start_y) ]
#Drawing the grid of the surface
def drawGrid():
	for x in range(0, WINWID, BOXLEN):
		pygame.draw.line(CANVAS, DARKGRAY, (x, 0), (x, WINHEI))
	for y in range(0, WINHEI, BOXLEN):
		pygame.draw.line(CANVAS, DARKGRAY, (0, y), (WINWID, y))

#Drawing apple on the canvas
def drawApple(Top_x, Top_y):
	rectangle = pygame.Rect(Top_x * BOXLEN, Top_y * BOXLEN, BOXLEN, BOXLEN)
	pygame.draw.rect(CANVAS, RED, rectangle)

#Drawing sanck on the canvas
def drawSnack(snack):
	for (x, y) in snack:
		rectangle0 = pygame.Rect(x * BOXLEN, y * BOXLEN, BOXLEN, BOXLEN)
		pygame.draw.rect(CANVAS, GREEN, rectangle0)
		rectangle1 = pygame.Rect(x * BOXLEN + 3, y * BOXLEN + 3, BOXLEN - 6, BOXLEN - 6)
		pygame.draw.rect(CANVAS, DARKGRAY, rectangle1)

#Draw the score of the game
def drawScore():
	global SCORE
	font = pygame.font.Font('freesansbold.ttf', 18)
	scoreSurf = font.render('SCORE: %s' % (SCORE), True, WHITE)
	scoreRect = scoreSurf.get_rect()
	scoreRect.topleft = (WINWID - 120, 10)
	CANVAS.blit(scoreSurf, scoreRect)

#Draw the press key message for the player
def drawPress():
	font = pygame.font.Font('freesansbold.ttf', 18)
	pressSurf = font.render('Press a key t play', True, GREEN)
	pressRect = pressSurf.get_rect()
	pressRect.topleft = (WINWID - 200, WINHEI - 30)
	CANVAS.blit(pressSurf, pressRect)

#Drawing the gameover picture
def gameBeginOver(font):
	font0, font1 = font
	gameFont = pygame.font.Font('freesansbold.ttf', 150)
	font0Surf = gameFont.render(font0, True, WHITE)
	font1Surf = gameFont.render(font1, True, WHITE)
	font0Rect = font0Surf.get_rect()
	font1Rect = font1Surf.get_rect()
	font0Rect.midtop = (WINWID / 2, 10)
	font1Rect.midtop = (WINWID / 2, font0Rect.height + 10 + 45)

	CANVAS.blit(font0Surf, font0Rect)
	CANVAS.blit(font1Surf, font1Rect)
	drawPress()
	drawScore()
	pygame.display.update()
	pygame.time.wait(500)
	checkKeyPress()

	while True:
		if checkKeyPress():
			pygame.event.get()
			return createSnack(), creatApple(), 0, False, RIGHT

#check if there is a key press
def checkKeyPress():
	if len(pygame.event.get(QUIT)) > 0:
		crash()
	up = pygame.event.get(KEYUP)
	if len(up) == 0:
		return None
	elif up[0].key == K_ESCAPE:
		crash()
	return up[0].key

#Start the programe
if __name__ == '__main__':
	main()


