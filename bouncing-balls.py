import pygame
import random
import math
from time import sleep

pygame.init()

display_width = 800
display_height = 600

black = (0,0,0)
white = (255,255,255)
red = (255, 0, 0)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Avoid the bouncing balls for as long as you can!")

clock = pygame.time.Clock()

smile = pygame.image.load("./assets/smile.png") # smile.png from https://textfac.es
smile_size = smile.get_rect().size # creates rectangle around image and returns (width, height)
ball_radius = 30

scores_file = "./assets/scores.txt"

#-----Function definitions for ball physics, creation, etc.-----

def smilePosUpdate(x,y):
	gameDisplay.blit(smile, (x,y))
	
def randSpdCalc():
	speedx = random.randint(5,10)
	speedy = random.randint(5,10)
	if random.randint(1,2) == 1:
		speedx *= -1
	if random.randint(1,2) == 1:
		speedy *= -1
	return [speedx, speedy]

def updateBouncyBall(ballx, bally, speed_of_ball, colour_of_ball):
	if ballx > display_width:
		speed_of_ball[0] = -1*speed_of_ball[0]
	if ballx < 0:
		speed_of_ball[0] = -1*speed_of_ball[0]
	if bally > display_height:
		speed_of_ball[1] = -1*speed_of_ball[1]
	if bally < 0:
		speed_of_ball[1] = -1*speed_of_ball[1]
	ballx += speed_of_ball[0]
	bally += speed_of_ball[1]
	pygame.draw.circle(gameDisplay, colour_of_ball, (ballx, bally), ball_radius)
	return [ballx, bally, speed_of_ball] 
	
def addBouncyBall(time):
	global ball1_data
	global ball2_data
	global ball3_data
	global ball4_data
	global ball5_data
	global ball6_data
	global ball_list
	
	ball_list = []
	
	if time > 0:
		ball1_data = updateBouncyBall(ball1_data[0], ball1_data[1], ball1_data[2], white)
		ball_list.append(ball1_data)
	if time >= 3:
		ball2_data = updateBouncyBall(ball2_data[0], ball2_data[1], ball2_data[2], white)
		ball_list.append(ball2_data)
	if time >= 6:
		ball3_data = updateBouncyBall(ball3_data[0], ball3_data[1], ball3_data[2], white)
		ball_list.append(ball3_data)
	if time >= 10:
		ball4_data = updateBouncyBall(ball4_data[0], ball4_data[1], ball4_data[2], white)
		ball_list.append(ball4_data)
	if time >= 16:
		ball5_data = updateBouncyBall(ball5_data[0], ball5_data[1], ball5_data[2], white)
		ball_list.append(ball5_data)
	if time >= 25:
		ball6_data = updateBouncyBall(ball6_data[0], ball6_data[1], ball6_data[2], white)
		ball_list.append(ball6_data)
	
def collisionDetection(ball_data, smile_x, smile_y):
	ball_x = ball_data[0]
	ball_y = ball_data[1]
	smile_radius = smile_size[0]
	distance = math.sqrt((ball_x - smile_x)**2 + (ball_y - smile_y)**2)
	if distance <= (smile_radius + ball_radius):
		return True

def gameOverText():
	font = pygame.font.Font(None, 100)
	text_surf = font.render("Game Over!", True, red)
	gameDisplay.blit(text_surf, (220, 250))
	
def displayScoreText(time, high_or_current):
	if high_or_current == "current":
		text_str = "Score: " + str(time)
		position = (display_width - 125, 20)
	elif high_or_current == "high":
		text_str = "Highscore: " + highScoreComputer()
		position = (40, 20)
	font = pygame.font.Font(None, 30)
	text_surf = font.render(text_str, True, white)
	gameDisplay.blit(text_surf, position)

#-----Function definitions for highscore related things-----

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
	
#-----Creating and initializing balls, should be replaced with python objects in the future-----

ball1_data = [0, 0, randSpdCalc()]
ball2_data = [0, 0, randSpdCalc()]
ball3_data = [0, 0, randSpdCalc()]
ball4_data = [0, 0, randSpdCalc()]
ball5_data = [0, 0, randSpdCalc()]
ball6_data = [0, 0, randSpdCalc()]

highscore_str = highScoreComputer()

#-----Main function-----

def main():

	mouseX = 0
	mouseY = 0
	mouseXnew = 0
	mouseYnew = 0
	mouseXchange = 0
	mouseYchange = 0

	global time

	done = False

	while not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			elif event.type == pygame.MOUSEMOTION:
				(mouseXnew, mouseYnew) = pygame.mouse.get_pos()
				mouseXchange = mouseXnew - mouseX - smile_size[0]/2
				mouseYchange = mouseYnew - mouseY - smile_size[1]/2
		gameDisplay.fill(black)
		
		smilePosUpdate(mouseXchange, mouseYchange)
		
		time = pygame.time.get_ticks()/1000

		displayScoreText(time, "current")
		displayScoreText(highscore_str, "high")
		
		addBouncyBall(time)	
		
		pygame.display.update()
			
		for ball in ball_list:
			if collisionDetection(ball, mouseXnew, mouseYnew) == True:
				gameOverText()
				pygame.display.update()
				scoreAppender(time, scores_file)
				done = True

		clock.tick(60)

#-----Calling main and quitting pygame-----

main()

pygame.quit()
quit()
