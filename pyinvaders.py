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
		if 'enemy_missile' in filename:
			self.image = pygame.transform.rotozoom(self.image, 0, settings['enemy_missile_size'])
		# Game cheat - detect if it is set
		if 'player_missile' in filename:
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
	if (s1_x > s2_x - 32) and (s1_x < s2_x + 32) and (s1_y > s2_y - 32) and (s1_y < s2_y + 32):
		return 1
	else:
		return 0


# Initialize
pygame.init()
# Set the keyboard repeating increment to be very fast
pygame.key.set_repeat(1, 1)
# Set the window title
pygame.display.set_caption('PyInvaders')
# Set the window size
screen = pygame.display.set_mode((settings['window_width'], settings['window_height']))
# Set the backdrop image
backdrop = pygame.image.load('data/backdrop.png')


### Load all sprites
#### Load the enemies
# Keep track of our total number of enemies
enemy_quantity = 0
row_altitude = 50
enemies = {}
# For each row that we need to draw...
for row in range(settings['enemy_row_quantity']):
	x = 0 # Start every row at enemy #0
	# ...draw each enemy that we need to draw per row...
	enemies[row] = {}
	for enemy_number in range(settings['enemies_per_row']):
		# ...render a sprite at that enemy's location...
		enemies[row][enemy_number] = Sprite(50 * x + 50, row_altitude, 'data/enemy.png')
		x += 1 # ...increase the horizontal offset for the next enemy by 1 (so it is placed "1" ship-length over)...
		enemy_quantity += 1 # Keep track of our total number of enemies
	row_altitude += settings['enemy_vertical_spacing'] # ...set the altitude of the next row to be 35 pixels lower than the current row

#### Load the rest
# Load the player sprite
player = Sprite(20, 400, 'data/player.png')
# Load the player's missile sprite
player_missile = Sprite(0, settings['window_height'], 'data/player_missile.png')
# Load enemies' missile sprite
enemy_missiles = {}
for row in enemies:
	enemy_missiles[row] = Sprite(0, settings['window_height'], 'data/enemy_missile.png')


## Begin Gameplay
# If quit == 1 (true) then the game ends
quit = 0

# So long as quit == 0 the game shall go on
while quit == 0:
	# Position the backdrop image, starting at the top-left
	screen.blit(backdrop, (0,0))

	## Setup the enemies and their directions
	for row in enemies:
		for enemy_number in enemies[row]: # For every enemy...
			enemies[row][enemy_number].x += settings['enemy_speed'] # ...start moving
			enemies[row][enemy_number].render() # Render the enemy



	## Change Enemy Direction / New Line
	for row in enemies:
		if len(enemies[row]) != 0:
			# Left
			right_most_enemy = max(enemies[row]) # Find the right-most enemy ("max" key in)
			if enemies[row][right_most_enemy].x > 590: # When the right-most enemy hits the right-hand side of the screen...
				settings['enemy_speed'] = -(abs(settings['enemy_speed'])) # ...convert their speed to a negative number, forcing them to head to the left
				for enemy_number in enemies[row]: # For every enemy...
					enemies[row][enemy_number].y += settings['enemy_reverse_direction_drop_height'] # ...force them down 5px
			# Right
			left_most_enemy = min(enemies[row])
			if enemies[row][left_most_enemy].x < 10: # When the left-most enemy hits the left-hand side of the screen...
				settings['enemy_speed'] = abs(settings['enemy_speed']) # ...convert their speed to a positive number, forcing them to head to the right
				for enemy_number in enemies[row]: # For every enemy...
					enemies[row][enemy_number].y += settings['enemy_reverse_direction_drop_height'] # ...force them down 5px



	## Missile Management
	### Player missile
	if player_missile.y < (settings['window_height'] - 1) and player_missile.y > 0: # If the player's missile is on the screen (i.e. 'in play')...
		player_missile.render() # ...show the missile...
		player_missile.y += -(abs(settings['player_missile_speed'])) # ...and change its coordinates at settings['player_missile_speed'] to give the appearance of motion (negative y-position makes it go up)
	else:
		player_missile.y = settings['window_height']

	### Enemy missiles
	for row in enemy_missiles:
		# Create the missile
		if enemy_missiles[row].y >= settings['window_height'] and len(enemies[row]) > 0: # If there is no enemy missile on the screen (i.e. 'in play') and there are still enemies on this row...
			left_most_enemy = min(enemies[row])
			enemy_missiles[row].x = enemies[row][random.choice(enemies[row].keys())].x # ...create a new one from a random choice of enemy...
			enemy_missiles[row].y = enemies[row][left_most_enemy].y # ...set the position to wherever the chosen enemy is
		# Move the missile
		enemy_missiles[row].render() # Render the enemy missile...
		enemy_missiles[row].y += settings['enemy_missile_speed'] # ...and make it move down the screen

		### Missile collision
		if intersect(player_missile.x, player_missile.y, enemy_missiles[row].x, enemy_missiles[row].y): # If the player's missile collides with the enemy_missiles[row]...
			# Explode!
			explosion = Sprite(player_missile.x, player_missile.y, 'data/explosion.png') # Set explosion coordinates
			explosion.render() # Render explosion
			# Reset missiles
			(player_missile.x, player_missile.y) = (0, settings['window_height']) # ...reset our missile
			(enemy_missiles[row].x, enemy_missiles[row].y) = (0, settings['window_height']) # ...reset row1's missile



	## Destroy enemy
	for row in enemies:
		for enemy_number in enemies[row]:
			if intersect(player_missile.x, player_missile.y, enemies[row][enemy_number].x, enemies[row][enemy_number].y):
				# Game cheat setting
				if settings['piercing_missiles'] == 0:
					# Reset player missile (only one baddie per missile!)
					(player_missile.x, player_missile.y) = (0, settings['window_height'])
				# Explode!
				explosion = Sprite(enemies[row][enemy_number].x, enemies[row][enemy_number].y, 'data/explosion.png') # Set explosion coordinates
				explosion.render() # Render explosion
				# ...delete that enemy (enemy destroyed)
				del enemies[row][enemy_number]
				settings['score'] += 1 # settings['score'] incrementer
				break



	## Game Ending Events
	### Player events
	#### Player is hit by enemy missile
	for row in enemy_missiles:
		if intersect(player.x, player.y, enemy_missiles[row].x, enemy_missiles[row].y): # If the player gets hit by an enemy missile...
			# Explode!
			explosion = Sprite(player.x, player.y, 'data/explosion.png') # Set explosion coordinates
			explosion.render() # Render explosion
			# Reset the player's location offscreen (we need to do this so that we can see the explosion -- otherwise the player overlaps it)
			(player.x, player.y) = (0, settings['window_height']) # ...reset our player
			print 'Game Over!'
			quit = 1
	### Check enemy events
	total_enemies_remaining = 0 # For when we check if all enemies have been destroyed
	for row in enemies:
		for enemy_number in enemies[row]:
			# Player hits enemy ship
			if intersect(player.x, player.y, enemies[row][enemy_number].x, enemies[row][enemy_number].y): # ...check if the player has hit that enemy's ship
				# Explode!
				explosion = Sprite(player.x, player.y, 'data/explosion.png') # Set explosion coordinates
				explosion.render() # Render explosion
				# Reset the player's location offscreen (we need to do this so that we can see the explosion -- otherwise the player overlaps it)
				(player.x, player.y) = (0, settings['window_height']) # ...reset our player
				print 'Game Over!'
				quit = 1
			# Enemy reaches bottom of screen
			if enemies[row][enemy_number].y >= settings['window_height']: # ...check if any enemy ships have reached the bottom of the screen
				print 'Game Over!'
				quit = 1
				break # This prevents having "Game Over!" display once per ship on that row (by default: 10 times -- because they all reach the bottom at the same time)
			total_enemies_remaining += 1 # For when we check if all enemies have been destroyed		

	#### All enemies destroyed
	if total_enemies_remaining == 0: # If there are no enemies left (sum of all rows == 0)...
		print 'Victory!'
		quit = 1 # Player Wins!



	## Live settings['score'] Counter
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
				player = Sprite(player.x, player.y, 'data/player-right.png') # ...swap out the player's sprite...
				player.render() # ...render the new sprite...
				player.x += settings['player_speed'] # ...move right
			if keys[pygame.K_LEFT] and player.x > 10: # ...if it's the left key and we won't move off the screen...
				player = Sprite(player.x, player.y, 'data/player-left.png') # ...swap out the player's sprite...
				player.render() # ...render the new sprite...
				player.x -= settings['player_speed'] # ...move left
			if keys[pygame.K_SPACE]: # ...if it's the space key...
				if settings['missile_override_option'] == 0: # If missile is already in play, player must wait until it is destroyed to launch another
					if player_missile.y >= settings['window_height']: # ...if the player's missile is not in play...
						player_missile.x = player.x #...set missile's x coordinate to player.x...
						player_missile.y = player.y # ...and set missile's y coordinate to player.y
				elif settings['missile_override_option'] == 1: # If missile is already in play, it will disappear and a new one will be launched
					player_missile.x = player.x #...set missile's x coordinate to player.x...
					player_missile.y = player.y # ...and set missile's y coordinate to player.y
		# When the player releases a key...
		if our_event.type == pygame.KEYUP:
			if our_event.key == pygame.K_RIGHT: # ...if they're done moving right...
				player = Sprite(player.x, player.y, 'data/player.png') # ...return the player's sprite back to its original...
				player.render() # ...render the old sprite again
			if our_event.key == pygame.K_LEFT: # ...if they're done moving left...
				player = Sprite(player.x, player.y, 'data/player.png') # ...return the player's sprite back to its original...
				player.render() # ...render the old sprite again



	
	# Render the player (at the bottom because it has to happen AFTER all of the keyboard inputs are captured and acted upon)
	player.render()

	# Update the display to show all the action that has occured this turn
	pygame.display.update()
	# Set gameplay speed. Lower number == faster gameplay
	pygame.time.delay(settings['game_speed'])


# Print the player's settings['score'] when the game is over (quit == 1), thus we break out of the while loop
print 'You scored: ' + str(settings['score']) + ' / ' + str(enemy_quantity)