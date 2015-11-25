import pygame
import random
import math
from time import sleep

pygame.init()

pygame.display.set_caption("Avoid the bouncing balls for as long as you can!")
clock = pygame.time.Clock()

smile = pygame.image.load("./assets/smile.png") # smile.png from https://textfac.es
scores_file = "./assets/scores.txt"

#-----Constants-----

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255, 0, 0)

SMILE_SIZE = smile.get_rect().size # creates rectangle around image and returns (width, height)
BALL_RADIUS = 30

#-----Classes-----
class Ball():
	def __init__(self):
		self.posx = 0
		self.posy = 0
		self.speedx = randSpdCalc()
		self.speedy = randSpdCalc()

	def update(self):
		# if the ball is past the sreen, it reverses direction
		if self.posx > DISPLAY_WIDTH or self.posx < 0:
			self.speedx = self.speedx * (-1)
		if self.posy > DISPLAY_HEIGHT or self.posy < 0:
			self.speedy = self.speedy * (-1)
		# updating positions with speed
		self.posx += self.speedx
		self.posy += self.speedy
		#drawing ball after update
		pygame.draw.circle(gameDisplay, WHITE, (self.posx, self.posy), BALL_RADIUS)

	def removeFromScreen(self):
		# moves ball off screen
		self.posx = DISPLAY_WIDTH + 100
		self.posy = DISPLAY_HEIGHT + 100
		pygame.draw.circle(gameDisplay, WHITE, (self.posx, self.posy), BALL_RADIUS)

	def getPos(self):
		return [self.posx, self.posy]

class BallList():
	def __init__(self):
		self.numRuns = 0
		self.ball_list = []

	def addBall(self, _time):
		if (_time % 3 == 0 or _time == 0) and self.numRuns == 0:
			self.numRuns += 1
			self.ball_list.append(Ball())
		elif _time % 3 != 0 and self.numRuns == 1:
			self.numRuns = 0

	def getBallList(self):
		return self.ball_list

class Time():
	def __init__(self):
		self.time = pygame.time.get_ticks()/1000

	def update(self):
		self.time = pygame.time.get_ticks()/1000

	def getTime(self):
		return self.time

#-----Functions for game related things-----
def randSpdCalc():
		speed = random.randint(7,17)
		if random.randint(1,2) == 1:
			speed *= -1
		return speed

def smilePosUpdate(x,y):
	gameDisplay.blit(smile, (x,y))

def collisionDetection(ball_data, smile_x, smile_y):
	ball_x = ball_data[0]
	ball_y = ball_data[1]
	smile_radius = SMILE_SIZE[0]
	distance = math.sqrt((ball_x - smile_x)**2 + (ball_y - smile_y)**2)
	if distance <= (smile_radius + BALL_RADIUS):
		return True

def gameOverText():
	font = pygame.font.Font(None, 100)
	text_surf = font.render("Game Over!", True, RED)
	gameDisplay.blit(text_surf, (220, 250))
	
def displayScoreText(time, high_or_current):
	if high_or_current == "current":
		text_str = "Score: " + str(time)
		position = (DISPLAY_WIDTH - 125, 20)
	elif high_or_current == "high":
		text_str = "Highscore: " + highScoreComputer()
		position = (40, 20)
	font = pygame.font.Font(None, 30)
	text_surf = font.render(text_str, True, WHITE)
	gameDisplay.blit(text_surf, position)

#-----Functions for highscore related things-----
def scoreFileParser(data_file):
	data_file_read = open(data_file, "r")
	score_dic = {}
	for line in data_file_read:
		line = line[:-1]
		line_list = line.split(" ")
		score_dic.update({line_list[0]: line_list[1]})
	
	data_file_read.close()
	return score_dic
	
def highScoreComputer():
	score_dic = scoreFileParser(scores_file)
	highscore = 0
	highscore_key = ""
	for key in score_dic:
		value = int(score_dic[key])
		if value > highscore:
			highscore = value
			highscore_key = key
	highscore_str = str(highscore) + " by " + highscore_key
	return highscore_str
	
def scoreAppender(time, data_file):
	player_name = raw_input("Enter your name (one word): ")
	data_file_write = open(data_file, "a")
	data_file_write.write(player_name + " " + str(time) + "\n")
	data_file_write.close()
	print "Your score of ~~" + str(time) + "~~ has been added successfully!"
	
#-----Main function-----

def main():
	mouseX = 0
	mouseY = 0
	mouseXnew = 0
	mouseYnew = 0
	mouseXchange = 0
	mouseYchange = 0

	highscore_str = highScoreComputer()
	ballData = BallList()
	timeObject = Time()

	done = False
	while not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			elif event.type == pygame.MOUSEMOTION:
				(mouseXnew, mouseYnew) = pygame.mouse.get_pos()
				mouseXchange = mouseXnew - mouseX - SMILE_SIZE[0]/2
				mouseYchange = mouseYnew - mouseY - SMILE_SIZE[1]/2

		timeObject.update()
		time = timeObject.getTime()

		ballData.addBall(time)

		gameDisplay.fill(BLACK)
		smilePosUpdate(mouseXchange, mouseYchange)
		displayScoreText(time, "current")
		displayScoreText(highscore_str, "high")
			
		for ball in ballData.getBallList():
			if collisionDetection(ball.getPos(), mouseXnew, mouseYnew) == True:
				#-----Game over-----
				gameDisplay.fill(BLACK)
				gameOverText()
				displayScoreText(time, "current")
				displayScoreText(highscore_str, "high")
				pygame.display.update()
				scoreAppender(time, scores_file)
				done = True
				break
			else:
				ball.update()

		pygame.display.update()
		clock.tick(60)

#-----Calling main and quitting pygame-----
main()

pygame.quit()
quit()
