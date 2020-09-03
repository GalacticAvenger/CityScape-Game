import sys, pygame, random, itertools
from pygame.locals import *


global gameover

pygame.init()
screen_height = 800
screen_width = 1200
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Lunar Lander")
FPS = 30
screen_rect = screen.get_rect()

gray = (128, 128, 128)
black = (0, 0, 0)
orange = (255, 140, 0)

spaceship = pygame.image.load("/Users/samuelmeddin/Documents/Lunar Lander/lunar_lander.bmp")
spaceship_rect = spaceship.get_rect()
spaceship_rect.center = (200, 100)

y_gravity = 10
x_gravity = 80
vertical_speed = 80
horizontal_speed = 0
angle = 0
move_up = False
rotate_right = False
rotate_left = False
x_coord = 0
y_coord = 0
x_moves = 0
y_moves = 0

space_ship_rect_test = pygame.Rect(x_coord, y_coord, 35, 35)

SMALL_FONT = pygame.font.Font('freesansbold.ttf', 24)
FONT = pygame.font.Font('freesansbold.ttf', 32)
BIG_FONT = pygame.font.Font('freesansbold.ttf', 144)

gameover_text = BIG_FONT.render('GAME OVER', True, (255, 0, 0))
gameover_text_rect = gameover_text.get_rect()
gameover_text_rect.centerx = screen_rect.centerx
gameover_text_rect.centery = screen_rect.centery

restart_text = FONT.render('Hit R to Play Again', True, (255, 255, 255))
restart_text_rect = restart_text.get_rect()
restart_text_rect.top = gameover_text_rect.bottom
restart_text_rect.centerx = screen_rect.centerx

#pygame.draw.line(screen, color, (start coords), (end coords), thickness)
platform_x = [0, 25, 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400, 425, 450, 475, 500, 525, 550, 575, 600, 625, 650, 675, 700, 725, 750, 775, 800, 825, 850, 875, 900, 925, 950, 975, 1000, 1025, 1050, 1075, 1100, 1125, 1150, 1175, 1200]
platform_y = []
platforms = []
upwards_lines = []

deduct_fuel = False
fuel = 1000
score = 0
restart = False
start = True
gameover = False

class Line():
	def __init__(self, x, y, index):
		self.index = index
		self.y = y
		if self.y > platform_y[self.index + 1]:
			self.line = pygame.Rect((x,platform_y[self.index + 1]), (1, abs(self.y-platform_y[self.index + 1])))
		else:
			self.line = pygame.Rect((x, self.y), (1, abs(self.y-platform_y[self.index + 1])))
	
	def make_upwards_line(self):
		pygame.draw.rect(screen, gray, (self.line))


class Platform():
	def __init__(self, x, y, index):
		self.index = index
		if x == choice1 or x == choice2:
			self.platform = pygame.Rect(x, y, 75, 5)
		else:
			self.platform = pygame.Rect(x, y, 25, 1)

	def draw_platform(self):
		if self.platform.x == choice1 or self.platform.x == choice2:
			pygame.draw.line(screen, orange, (self.platform.x - 25, self.platform.y), (self.platform.x + 50, self.platform.y), 5)
		else:
			pygame.draw.line(screen, gray, (self.platform.x, self.platform.y), (self.platform.x + 25, self.platform.y))

	def draw_upwards_line(self):
		if self.platform.x == choice1 or self.platform.x == choice2:
			if self.platform.x == screen_width - 25:
				pass
			else:
				upwards_lines.append(Line(self.platform.x + 50, self.platform.y, self.index))
		else:
			upwards_lines.append(Line(self.platform.x + 25, self.platform.y, self.index))	

while True:
	FPSCLOCK = pygame.time.Clock()
	screen.fill(black)

	if gameover == False and restart == False:
		x_coord = float(spaceship_rect.centerx) + (vertical_speed / 100)
		y_coord = float(spaceship_rect.centery) + (horizontal_speed / 100)

		space_ship_rect_test = pygame.Rect(x_coord, y_coord, 35, 35)

		if start == True:
			for x in platform_x:
				platform_y.append(random.randint(int((screen_height)/2), int(screen_height) - 15))

			choice1 = random.choice(platform_x)
			while choice1 == 0 or choice1 == screen_width:
				choice1 = random.choice(platform_x)
			#platform_x.remove(choice1 + 50)
			platform_x.remove(choice1 + 25)
			platform_x.remove(choice1 - 25)
			#platform_y.pop(platform_x.index(choice1) + 2)
			platform_y.pop(platform_x.index(choice1) + 1)
			platform_y.pop(platform_x.index(choice1) - 1)

			choice2 = random.choice(platform_x)

			while choice2 == 0 or choice2 == screen_width or choice2 == choice1 or abs(platform_x.index(choice1) - platform_x.index(choice2)) == 1 or abs(platform_x.index(choice2) - platform_x.index(choice1)) == 1:
				choice2 = random.choice(platform_x)

			#platform_x.remove(choice2 + 50)
			platform_x.remove(choice2 + 25)
			platform_x.remove(choice2 - 25)
			#platform_y.pop(platform_x.index(choice2) + 2)
			platform_y.pop(platform_x.index(choice2) + 1)
			platform_y.pop(platform_x.index(choice2) - 1)
			start = False
			for x, y in zip(platform_x, platform_y):
				platforms.append(Platform(x, y, platform_x.index(x)))

			for platform in platforms:
				if platform.platform.x != screen_width:
					platform.draw_upwards_line()


		x_speed = SMALL_FONT.render('Horizontal Velocity  ' + str(int(x_gravity)), True, gray)
		screen.blit(x_speed, (screen_width - 300, 50))
		y_speed = SMALL_FONT.render('Vertical Velocity       ' + str(int(y_gravity/2)), True, gray)
		screen.blit(y_speed, (screen_width - 300, 100))
		score_text = SMALL_FONT.render('Score   ' + str(score), True, gray)
		screen.blit(score_text, (40, 50))
		fuel_text = SMALL_FONT.render('Fuel     ' + str(fuel), True, gray)
		screen.blit(fuel_text, (40, 100))



		screen.blit(pygame.transform.rotate(spaceship, angle),(space_ship_rect_test))
		horizontal_speed += y_gravity
		vertical_speed += x_gravity

		for platform in platforms:
			platform.draw_platform()
			#if ((platform.index % 25)/platforms.index(platform)) == 1:
			if platform.platform.colliderect(space_ship_rect_test):
				if platform.platform.x != choice1 and platform.platform.x != choice2:
					restart = True
				elif int(y_gravity/2) > 21 or abs(angle) > 5:
					restart = True
				elif int(y_gravity/2) < 21:
					'''x_coord = 0
					y_coord = 0
					x_gravity = 0
					y_gravity = 0'''
					space_ship_rect_test.bottom = platform.platform.top
					pygame.time.wait(2000)
					score += 100
					restart = True
					break

		for line in upwards_lines:
			line.make_upwards_line()
			if line.line.colliderect(space_ship_rect_test):
				restart = True

		if space_ship_rect_test.right > screen_width or space_ship_rect_test.left < 0 or space_ship_rect_test.top < 0 or space_ship_rect_test.bottom > screen_height:
			restart = True


		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			if event.type == KEYDOWN:
				if event.key == K_UP:
					if fuel <= 0:
						pass
					else:
						move_up = True
						spaceship = pygame.image.load('/Users/samuelmeddin/Documents/Lunar Lander/lunar_lander_fire.bmp')
						deduct_fuel = True
				if event.key == K_LEFT:
					rotate_left = True
				if event.key == K_RIGHT:
					rotate_right = True

			if event.type == KEYUP:
				if event.key == K_UP:
					move_up = False
					spaceship = pygame.image.load('/Users/samuelmeddin/Documents/Lunar Lander/lunar_lander.bmp')
					deduct_fuel = False
				if event.key == K_LEFT:
					rotate_left = False
				if event.key == K_RIGHT:
					rotate_right = False

		if deduct_fuel == True:
			if fuel > 0:
				fuel -= 1

		if fuel < 0:
			move_up = False
			spaceship = pygame.image.load('lunar_lander.bmp')
			deduct_fuel = False


		if rotate_left == True and angle < 90:
			angle += 3
		if rotate_right == True and angle > -90:
			angle -= 3
		if move_up == True:
			if fuel > 0:
				if angle >= 0:
					#Move leftward
					y_moves = float((90 - angle) / 90)
					x_moves = float(angle / -90)

				if angle < 0:
					y_moves = float((90 + angle) / 90)
					x_moves = float(-angle / 90)
				x_gravity += x_moves
				y_gravity -= y_moves
				x_moves = 0
				y_moves = 0
			else:
				move_up = False

		if move_up == False:
			y_gravity += .5

	elif restart == True:
		if fuel > 0:
			y_gravity = 10
			x_gravity = 80
			vertical_speed = 80
			horizontal_speed = 0
			angle = 0
			move_up = False
			rotate_right = False
			rotate_left = False
			x_coord = 0
			y_coord = 0
			x_moves = 0
			y_moves = 0
			upwards_lines.clear()
			platforms.clear()
			platform_y.clear()
			platform_x = [0, 25, 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400, 425, 450, 475, 500, 525, 550, 575, 600, 625, 650, 675, 700, 725, 750, 775, 800, 825, 850, 875, 900, 925, 950, 975, 1000, 1025, 1050, 1075, 1100, 1125, 1150, 1175, 1200]
			restart = False
			spaceship_rect.center = (200, 100)
			deduct_fuel = False
			start = True
			spaceship = pygame.image.load('lunar_lander.bmp')
		else:
			restart = False
			gameover = True


	elif gameover == True:
		screen.fill((0,0,0))
		screen.blit(gameover_text, gameover_text_rect)
		screen.blit(restart_text, restart_text_rect)

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			if event.type == KEYDOWN:
				if event.key == K_r:
					fuel = 1000
					deduct_fuel = False
					y_gravity = 10
					x_gravity = 80
					vertical_speed = 80
					horizontal_speed = 0
					angle = 0
					move_up = False
					rotate_right = False
					rotate_left = False
					x_coord = 0
					y_coord = 0
					x_moves = 0
					y_moves = 0
					upwards_lines.clear()
					platforms.clear()
					platform_y.clear()
					platform_x = [0, 25, 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400, 425, 450, 475, 500, 525, 550, 575, 600, 625, 650, 675, 700, 725, 750, 775, 800, 825, 850, 875, 900, 925, 950, 975, 1000, 1025, 1050, 1075, 1100, 1125, 1150, 1175, 1200]
					gameover = False
					spaceship_rect.center = (200, 100)
					start = True
					spaceship = pygame.image.load('lunar_lander.bmp')


	pygame.display.update()
	FPSCLOCK.tick(FPS)
