import pygame
import random
import yaml # For importing config settings


## Import Game Settings

# Make accessible via settings['setting_name']
settings_file = open('settings.yml')
settings = yaml.load(settings_file)



## Sprites

class Sprite:
	"""Class for initializing and rendering the sprites."""
	def __init__(self, xpos, ypos, filename):
		self.x = xpos
		self.y = ypos
		self.image = pygame.image.load(filename)
		# Game cheat - detect if it is set
		if 'enemymissile' in filename:
			self.image = pygame.transform.rotozoom(self.image, 0, settings['enemy_missile_size'])
		# Game cheat - detect if it is set
		if 'playermissile' in filename:
				self.image = pygame.transform.rotozoom(self.image, 0, settings['player_missile_size'])
		# Game cheat - detect if it is set
		if 'explosion' in filename:
			# If the player_missile has a larger size than default, double the size of the explosion
			self.image = pygame.transform.rotozoom(self.image, 0, settings['player_missile_size'])
		# Set "black" as the color to make transparent
		self.image.set_colorkey((0, 0, 0))

	def set_position(self, xpos, ypos):
		"""Figure out where we want to put the sprite."""
		self.x = xpos
		self.y = ypos

	def render(self): # Render the sprite
		screen.blit(self.image, (self.x, self.y))



def intersect(s1_x, s1_y, s2_x, s2_y):
	"""Setup collision detection."""
	if (s1_x > s2_x - 32) and (s1_x < s2_x + 32) and(s1_y > s2_y - 32) and (s1_y < s2_y + 32):
		return 1
	else:
		return 0


# Initialize
pygame.init()
# Set the window size (HARDCODED at 640xsettings['window_height'])
screen = pygame.display.set_mode((settings['window_width'], settings['window_height']))
# Set the keyboard repeating increment to be very fast
pygame.key.set_repeat(1, 1)
# Set the window title
pygame.display.set_caption('PyInvaders')
# Set the backdrop image
backdrop = pygame.image.load('data/backdrop.png')


### Load all sprites
#### Load the enemies

# Keep track of our total number of enemies
enemy_quantity = 0
# Initialize the "enemies_row1" list [NOTE: "Row1" = The TOP-most row]
enemies_row1 = []
# Initialize the "enemies_row2" list [NOTE: "Row2" = the second row from the TOP]
enemies_row2 = []
x = 0
for count in range(10): # For each enemy in this row, load a sprite for each of them (and space them 50px apart)
	enemies_row1.append(Sprite(50 * x + 50, 50, 'data/enemy.png'))
	x += 1
	enemy_quantity += 1 # Keep track of our total number of enemies
x = 0
for count in range(10): # For each enemy in this row, load a sprite for each of them (and space them 50px apart)
	enemies_row2.append(Sprite(50 * x + 50, 85, 'data/enemy.png')) # NOTE: '85' is '35' pixels below row1
	x += 1
	enemy_quantity += 1 # Keep track of our total number of enemies

#### Load the rest

# Load the player sprite
player = Sprite(20, 400, 'data/player.png')
# Load the player's missile sprite
player_missile = Sprite(0, settings['window_height'], 'data/player_missile.png')
# Load enemy_row1s' missile sprite
enemy_row1_missile = Sprite(0, settings['window_height'], 'data/enemy_missile.png')
# Load enemy_row2s' missile sprite
enemy_row2_missile = Sprite(0, settings['window_height'], 'data/enemy_missile.png')


## Begin Gameplay

# If quit == 1 (true) then the game ends
quit = 0

# So long as quit == 0 the game shall go on
while quit == 0:
	# Position the backdrop image, starting at the top-left
	screen.blit(backdrop, (0,0))

	### Setup the enemies and their directions
	for count in range(len(enemies_row1)): # For every enemy...
		enemies_row1[count].x += settings['enemy_speed'] # ...start moving
		enemies_row1[count].render() # Render the enemy
	for count in range(len(enemies_row2)): # For every enemy_row2...
		enemies_row2[count].x += settings['enemy_speed'] # ...start moving
		enemies_row2[count].render() # Render the enemy



	## Change Enemy Direction / New Line

	### Row1
	if len(enemies_row1) != 0:
		# Left
		if enemies_row1[len(enemies_row1)-1].x > 590: # When the right-most enemy hits the right-hand side of the screen...
			settings['enemy_speed'] = -(abs(settings['enemy_speed'])) # ...convert their speed to a negative number, forcing them to head to the left
			for count in range(len(enemies_row1)): # For every enemy...
				enemies_row1[count].y += settings['enemy_reverse_direction_drop_height'] # ...force them down 5px
		# Right
		if enemies_row1[0].x < 10: # When the left-most enemy hits the left-hand side of the screen...
			settings['enemy_speed'] = abs(settings['enemy_speed']) # ...convert their speed to a positive number, forcing them to head to the right
			for count in range(len(enemies_row1)): # For every enemy...
				enemies_row1[count].y += settings['enemy_reverse_direction_drop_height'] # ...force them down 5px
	### Row2
	if len(enemies_row2) != 0:
		# Left
		if enemies_row2[len(enemies_row2)-1].x > 590: # When the right-most enemy hits the right-hand side of the screen...
			settings['enemy_speed'] = -(abs(settings['enemy_speed'])) # ...convert their speed to a negative number, forcing them to head to the left
			for count in range(len(enemies_row2)): # For every enemy...
				enemies_row2[count].y += settings['enemy_reverse_direction_drop_height'] # ...force them down 5px
		# Right
		if enemies_row2[0].x < 10: # When the left-most enemy hits the left-hand side of the screen...
			settings['enemy_speed'] = abs(settings['enemy_speed']) # ...convert their speed to a positive number, forcing them to head to the right
			for count in range(len(enemies_row2)): # For every enemy...
				enemies_row2[count].y += settings['enemy_reverse_direction_drop_height'] # ...force them down 5px



	## Missile Management

	### player missile
	if player_missile.y < (settings['window_height'] - 1) and player_missile.y > 0: # If the player's missile is on the screen (i.e. 'in play')...
		player_missile.render() # ...show the missile...
		player_missile.y += -(abs(settings['player_missile_speed'])) # ...and change its coordinates at settings['player_missile_speed'] to give the appearance of motion (negative y-position makes it go up)
	else:
		player_missile.y = settings['window_height']

	### Enemy missiles

	# Row1
	if enemy_row1_missile.y >= settings['window_height'] and len(enemies_row1) > 0: # If there is no enemy missile on the screen (i.e. 'in play')...
		enemy_row1_missile.x = enemies_row1[random.randint(0, len(enemies_row1) - 1)].x # ...create a new one from a random choice of enemy...
		enemy_row1_missile.y = enemies_row1[0].y # ...set the position to wherever the chosen enemy is
	# Row2
	if enemy_row2_missile.y >= settings['window_height'] and len(enemies_row2) > 0: # If there is no enemy missile on the screen (i.e. 'in play')...
		enemy_row2_missile.x = enemies_row2[random.randint(0, len(enemies_row2) - 1)].x # ...create a new one from a random choice of enemy...
		enemy_row2_missile.y = enemies_row2[0].y # ...set the position to wherever the chosen enemy is
	# Enemy missile movement
	enemy_row1_missile.render() # Render the enemy missile...
	enemy_row1_missile.y += settings['enemy_missile_speed'] # ...and make it move down the screen
	enemy_row2_missile.render() # Render the enemy_row2 missile...
	enemy_row2_missile.y += settings['enemy_missile_speed'] # ...and make it move down the screen

	### Missile collision

	#### row1_missile
	if intersect(player_missile.x, player_missile.y, enemy_row1_missile.x, enemy_row1_missile.y): # If the player's missile collides with the enemy_row1_missile...
		# Explode!
		explosion = Sprite(player_missile.x, player_missile.y, 'data/explosion.png') # Set explosion coordinates
		explosion.render() # Render explosion
		# Reset missiles
		(player_missile.x, player_missile.y) = (0, settings['window_height']) # ...reset our missile
		(enemy_row1_missile.x, enemy_row1_missile.y) = (0, settings['window_height']) # ...reset row1's missile
	#### row2 missile
	if intersect(player_missile.x, player_missile.y, enemy_row2_missile.x, enemy_row2_missile.y): # If the player's missile collides with the enemy_row2_missile...
		# Explode!
		explosion = Sprite(player_missile.x, player_missile.y, 'data/explosion.png') # Set explosion coordinates
		explosion.render() # Render explosion
		# Reset missiles
		(player_missile.x, player_missile.y) = (0, settings['window_height']) # ...reset our missile
		(enemy_row2_missile.x, enemy_row2_missile.y) = (0, settings['window_height']) # ...reset row2's missile



	## Destroy enemy

	### enemies_row1
	for count in range(0, len(enemies_row1)): # If the player's missile hits one of the enemy ships...
		if intersect(player_missile.x, player_missile.y, enemies_row1[count].x, enemies_row1[count].y):
			# Game cheat setting
			if settings['piercing_missiles'] == 0:
				# Reset player missile (only one baddie per missile!)
				(player_missile.x, player_missile.y) = (0, settings['window_height'])
			# Explode!
			explosion = Sprite(enemies_row1[count].x, enemies_row1[count].y, 'data/explosion.png') # Set explosion coordinates
			explosion.render() # Render explosion
			# ...delete that enemy (enemy destroyed)
			del enemies_row1[count]
			settings['score'] += 1 # settings['score'] incrementer
			break
	### enemies_row2
	for count in range(0, len(enemies_row2)): # If the player's missile hits one of the enemy ships...
		if intersect(player_missile.x, player_missile.y, enemies_row2[count].x, enemies_row2[count].y):
			# Game cheat setting
			if settings['piercing_missiles'] == 0:
				# Reset player missile (only one baddie per missile!)
				(player_missile.x, player_missile.y) = (0, settings['window_height'])
			# Explode!
			explosion = Sprite(enemies_row2[count].x, enemies_row2[count].y, 'data/explosion.png') # Set explosion coordinates
			explosion.render() # Render explosion
			# ...delete that enemy (enemy destroyed)
			del enemies_row2[count]
			settings['score'] += 1 # settings['score'] incrementer
			break



	## Game Ending Events
	### Player destroyed

	# Player is hit by row1_missile
	if intersect(player.x, player.y, enemy_row1_missile.x, enemy_row1_missile.y): # If the player gets hit by an enemy missile...
		# Explode!
		explosion = Sprite(player.x, player.y, 'data/explosion.png') # Set explosion coordinates
		explosion.render() # Render explosion
		# Reset the player's location offscreen (we need to do this so that we can see the explosion -- otherwise the player overlaps it)
		(player.x, player.y) = (0, settings['window_height']) # ...reset our player
		print 'Game Over!'
		quit = 1
	# Player is hit by row2_missile
	if intersect(player.x, player.y, enemy_row2_missile.x, enemy_row2_missile.y): # If the player gets hit by an enemy missile...
		# Explode!
		explosion = Sprite(player.x, player.y, 'data/explosion.png') # Set explosion coordinates
		explosion.render() # Render explosion
		# Reset the player's location offscreen (we need to do this so that we can see the explosion -- otherwise the player overlaps it)
		(player.x, player.y) = (0, settings['window_height']) # ...reset our player
		print 'Game Over!'
		quit = 1
	# Player hits enemy_row1 ship
	for count in range(0, len(enemies_row1)): # For every enemy...
		if intersect(player.x, player.y, enemies_row1[count].x, enemies_row1[count].y): # ...check if the player has hit that enemy's ship
			# Explode!
			explosion = Sprite(player.x, player.y, 'data/explosion.png') # Set explosion coordinates
			explosion.render() # Render explosion
			# Reset the player's location offscreen (we need to do this so that we can see the explosion -- otherwise the player overlaps it)
			(player.x, player.y) = (0, settings['window_height']) # ...reset our player
			print 'Game Over!'
			quit = 1
	# Player hits enemy_row2 ship
	for count in range(0, len(enemies_row2)): # For every enemy...
		if intersect(player.x, player.y, enemies_row2[count].x, enemies_row2[count].y): # ...check if the player has hit that enemy's ship
			# Explode!
			explosion = Sprite(player.x, player.y, 'data/explosion.png') # Set explosion coordinates
			explosion.render() # Render explosion
			# Reset the player's location offscreen (we need to do this so that we can see the explosion -- otherwise the player overlaps it)
			(player.x, player.y) = (0, settings['window_height']) # ...reset our player
			print 'Game Over!'
			quit = 1
	# Enemy_row1 reaches bottom of screen
	for count in range(0, len(enemies_row1)): # For every enemy...
		if enemies_row1[count].y >= settings['window_height']: # ...check if any ships from enemy_row1 have reached the bottom of the screen
			print 'Game Over!'
			quit = 1
			break # This prevents having "Game Over!" display once per ship on that row (by default: 10 times -- because they all reach the bottom at the same time)
	# Enemy_row2 reaches bottom of screen
	for count in range(0, len(enemies_row2)): # For every enemy...
		if enemies_row2[count].y >= settings['window_height']: # ...check if any ships from enemy_row2 have reached the bottom of the screen
			print 'Game Over!'
			quit = 1
			break # This prevents having "Game Over!" display once per ship on that row (by default: 10 times -- because they all reach the bottom at the same time)

	### All enemies destroyed

	if (len(enemies_row1) + len(enemies_row2)) == 0: # If there are no enemies left (sum of all rows == 0)...
		print 'Victory!'
		quit = 1 # Player Wins!



	### Live settings['score'] Counter

	# The below two lines are commented out because the way we access the settings variables
	# settings['score']_font = pygame.font.Font(None, 50) # (Font-family, font-size)
	# settings['score']_text = pygame.font.Font(None, 50).render('settings['score']: ' + str(settings['score']) + ' / ' + str(enemy_quantity), True, (255,255,255)) # Set the settings['score'] string
	screen.blit(pygame.font.Font(None, 50).render('Score: ' + str(settings['score']) + ' / ' + str(enemy_quantity), True, (255,255,255)), (5, 5)) # Display the settings['score'] to the player | (5,5) is the x,y coordinates



	## Keyboard Navigation
	### Capture events for quitting

	# Check for player events
	for our_event in pygame.event.get():
		# If the player closes the window, quit
		if our_event.type == pygame.QUIT:
			quit = 1
		# If the player presses a key...
		if our_event.type == pygame.KEYDOWN:
			# ...if it's the escape key...
			if our_event.key == pygame.K_ESCAPE:
				# ...end the game
				quit = 1
			### Enable multi-key usage (more than a single key at once -- e.g. firing and moving simultaneously)
			
			# Obtain the state of all keys on the keyboard
			keys = pygame.key.get_pressed()
			if keys[pygame.K_RIGHT] and player.x < 590: # ...if it's the right key and we won't move off the screen...
				player = Sprite(player.x, player.y, 'data/player-right.png')
				player.render()
				player.x += settings['player_speed'] # ...move right
			if keys[pygame.K_LEFT] and player.x > 10: # ...if it's the left key and we won't move off the screen...
				player = Sprite(player.x, player.y, 'data/player-left.png')
				player.render()
				player.x -= settings['player_speed'] # ...move left
			if keys[pygame.K_SPACE]: # ...if it's the space key...
				if settings['missile_override_option'] == 0: # If missile is already in play, player must wait until it is destroyed to launch another
					if player_missile.y >= settings['window_height']: # ...if the player's missile is not in play...
						player_missile.x = player.x #...set missile's x coordinate to player.x...
						player_missile.y = player.y # ...and set missile's y coordinate to player.y
				elif settings['missile_override_option'] == 1: # If missile is already in play, it will disappear and a new one will be launched
					player_missile.x = player.x #...set missile's x coordinate to player.x...
					player_missile.y = player.y # ...and set missile's y coordinate to player.y
		if our_event.type == pygame.KEYUP:
			if our_event.key == pygame.K_RIGHT:
				player = Sprite(player.x, player.y, 'data/player.png')
				player.render()
			if our_event.key == pygame.K_LEFT:
				player = Sprite(player.x, player.y, 'data/player.png')
				player.render()



	
	# Render the player (at the bottom because it has to happen AFTER all of the keyboard inputs are captured and acted upon)
	player.render()

	# Update the display to show all the action that has occured this turn
	pygame.display.update()
	# Set gameplay speed. Lower number == faster gameplay
	pygame.time.delay(settings['game_speed'])


# Print the player's settings['score'] when the game is over (quit == 1), thus we break out of the while loop
print 'You scored: ' + str(settings['score']) + ' / ' + str(enemy_quantity)