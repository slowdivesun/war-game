# Importing the pygame module
import pygame
from pygame.locals import *

# Import randint method random module
from random import randint

# Initiate pygame and give permission
# to use pygame's functionality
pygame.init()

# Create a display surface object
# of specific dimension
window = pygame.display.set_mode((600, 600))

# Creating a new clock object to
# track the amount of time
clock = pygame.time.Clock()

# Creating a variable for direction
direction = 1

# Creating a new rect for player
player_rect = Rect(100, 100, 50, 50)

# Starting speed
speed_x = 5
speed_y = 4

# Creating a boolean variable that
# we will use to run the while loop
run = True

# Creating an infinite loop
# to run our game
while run:

	# Setting the framerate to 60fps
	clock.tick(60)

	# Changing the direction and x,y coordinate
	# of the object if the coordinate of left
	# side is less than equal to 20 or right side coordinate
	# is greater than equal to 580
	if player_rect.left <= 20 or player_rect.right >= 580:
		direction *= -1
		speed_x = randint(0, 8) * direction
		speed_y = randint(0, 8) * direction

		# Changing the value if speed_x
		# and speed_y both are zero
		if speed_x == 0 and speed_y == 0:
			speed_x = randint(2, 8) * direction
			speed_y = randint(2, 8) * direction

	# Changing the direction and x,y coordinate
	# of the object if the coordinate of top
	# side is less than equal to 20 or bottom side coordinate
	# is greater than equal to 580
	if player_rect.top <= 20 or player_rect.bottom >= 580:
		direction *= -1
		speed_x = randint(0, 8) * direction
		speed_y = randint(0, 8) * direction

		# Changing the value if speed_x
		# and speed_y both are zero
		if speed_x == 0 and speed_y == 0:
			speed_x = randint(2, 8) * direction
			speed_y = randint(2, 8) * direction

	# Adding speed_x and speed_y
	# in left and top coordinates of object
	player_rect.left += speed_x
	player_rect.top += speed_y

	# Drawing player rect
	pygame.draw.rect(window, (0, 255, 0), player_rect)

	# Updating the display surface
	pygame.display.update()

	# Filling the window with white color
	window.fill((255, 255, 255))
