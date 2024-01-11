from settings import vertical_tile_number, tile_size, screen_width
import pygame
from tiles import AnimatedTile, StaticTile
from support import import_folder
from random import choice, randint

class Sky:
	def __init__(self,horizon,current_level,style = 'level'):

		if current_level == 0:
			self.top = pygame.image.load('../graphics/decoration/sky/sky_lightlight.png').convert()
			self.bottom = pygame.image.load('../graphics/decoration/sky/sky_lightlight.png').convert()
			self.middle = pygame.image.load('../graphics/decoration/sky/sky_lightlight.png').convert()
			self.horizon = horizon

		elif current_level == 1:
			self.top = pygame.image.load('../graphics/decoration/sky/sky_yellow.png').convert()
			self.bottom = pygame.image.load('../graphics/decoration/sky/sky_blue.png').convert()
			self.middle = pygame.image.load('../graphics/decoration/sky/sky_pinkyellow.png').convert()
			self.horizon = horizon

		elif current_level == 2:
			self.top = pygame.image.load('../graphics/decoration/sky/sky_lightblue.png').convert()
			self.bottom = pygame.image.load('../graphics/decoration/sky/sky_darkblue.png').convert()
			self.middle = pygame.image.load('../graphics/decoration/sky/sky_mediumblue.png').convert()
			self.horizon = horizon

		elif current_level == 3:
			self.top = pygame.image.load('../graphics/decoration/sky/forest_blue.png').convert()
			self.bottom = pygame.image.load('../graphics/decoration/sky/forest_dark.png').convert()
			self.middle = pygame.image.load('../graphics/decoration/sky/forest_med.png').convert()
			self.horizon = horizon

		else:
			self.top = pygame.image.load('../graphics/decoration/sky/sky_lightlight.png').convert()
			self.bottom = pygame.image.load('../graphics/decoration/sky/sky_lightlight.png').convert()
			self.middle = pygame.image.load('../graphics/decoration/sky/sky_lightlight.png').convert()
			self.horizon = horizon - 200

		# stretch
		self.top = pygame.transform.scale(self.top,(screen_width,tile_size))
		self.bottom = pygame.transform.scale(self.bottom,(screen_width,tile_size))
		self.middle = pygame.transform.scale(self.middle,(screen_width,tile_size))

		self.style = style

	def draw(self,surface):
		for row in range(vertical_tile_number):
			y = row * tile_size
			if row < self.horizon:
				surface.blit(self.top,(0,y))
			elif row == self.horizon:
				surface.blit(self.middle,(0,y))
			else:
				surface.blit(self.bottom,(0,y))

		if self.style == 'overworld':
			for palm in self.palms:
				surface.blit(palm[0],palm[1])
			for cloud in self.clouds:
				surface.blit(cloud[0],cloud[1])

class Water:
	def __init__(self,top,level_width,current_level):
		water_start = -screen_width
		water_tile_width = 192
		tile_x_amount = int((level_width + screen_width * 2) / water_tile_width)
		self.water_sprites = pygame.sprite.Group()

		for tile in range(tile_x_amount):
			x = tile * water_tile_width + water_start
			y = top
			if current_level == 1:
				sprite = AnimatedTile(230, x, y-75, '../graphics/decoration/water')
			else:
				sprite = AnimatedTile(192, x, y+150, '../graphics/decoration/water2')
			self.water_sprites.add(sprite)

	def draw(self,surface,shift):
		self.water_sprites.update(shift)
		self.water_sprites.draw(surface)

class Clouds:
	def __init__(self,horizon,level_width,cloud_number):
		cloud_surf_list = import_folder('../graphics/decoration/clouds')
		min_x = -screen_width
		max_x = level_width + screen_width
		min_y = 0
		max_y = horizon
		self.cloud_sprites = pygame.sprite.Group()

		for cloud in range(cloud_number):
			cloud = choice(cloud_surf_list)
			x = randint(min_x,max_x)
			y = randint(min_y,max_y)
			sprite = StaticTile(0,x,y,cloud)
			self.cloud_sprites.add(sprite)

	def draw(self,surface,shift):
		self.cloud_sprites.update(shift)
		self.cloud_sprites.draw(surface)


class Ground:
	def __init__(self,level_width,image_number):
		image_surf_list = import_folder('../graphics/decoration/lvl3/layer0')
		min_x = -screen_width
		self.image_sprites = pygame.sprite.Group()

		for image in range(image_number):
			image = choice(image_surf_list)
			x = min_x
			y = 180
			sprite = StaticTile(0,x,y,image)
			self.image_sprites.add(sprite)
			min_x += 900

	def draw(self,surface,shift):
		self.image_sprites.update(shift)
		self.image_sprites.draw(surface)


class TreeTop:
	def __init__(self,level_width,image_number):
		image_surf_list = import_folder('../graphics/decoration/lvl3/layer2')
		min_x = -screen_width
		self.image_sprites = pygame.sprite.Group()

		for image in range(image_number):
			image = choice(image_surf_list)
			x = min_x
			y = 200
			sprite = StaticTile(0,x,y,image)
			self.image_sprites.add(sprite)
			min_x += 900

	def draw(self,surface,shift):
		self.image_sprites.update(shift)
		self.image_sprites.draw(surface)

class TreeDark:
	def __init__(self,level_width,image_number):
		image_surf_list = import_folder('../graphics/decoration/lvl3/layer3')
		min_x = -screen_width
		max_x = level_width + screen_width
		self.image_sprites = pygame.sprite.Group()

		for image in range(image_number):
			image = choice(image_surf_list)
			x = min_x
			y = 200
			sprite = StaticTile(0,x,y,image)
			self.image_sprites.add(sprite)
			min_x += 900

	def draw(self,surface,shift):
		self.image_sprites.update(shift)
		self.image_sprites.draw(surface)

class TreeMid:
	def __init__(self,level_width,image_number):
		image_surf_list = import_folder('../graphics/decoration/lvl3/layer5')
		min_x = -screen_width
		max_x = level_width + screen_width
		self.image_sprites = pygame.sprite.Group()

		for image in range(image_number):
			image = choice(image_surf_list)
			x = min_x
			y = 200
			sprite = StaticTile(0,x,y,image)
			self.image_sprites.add(sprite)
			min_x += 900

	def draw(self,surface,shift):
		self.image_sprites.update(shift)
		self.image_sprites.draw(surface)

class TreeLight:
	def __init__(self,level_width,image_number):
		image_surf_list = import_folder('../graphics/decoration/lvl3/layer6')
		min_x = -screen_width
		max_x = level_width + screen_width
		self.image_sprites = pygame.sprite.Group()

		for image in range(image_number):
			image = choice(image_surf_list)
			x = min_x
			y = 200
			sprite = StaticTile(0,x,y,image)
			self.image_sprites.add(sprite)
			min_x += 900

	def draw(self,surface,shift):
		self.image_sprites.update(shift)
		self.image_sprites.draw(surface)

class TreeBack:
	def __init__(self,level_width,image_number):
		image_surf_list = import_folder('../graphics/decoration/lvl3/layer9')
		min_x = -screen_width
		max_x = level_width + screen_width
		self.image_sprites = pygame.sprite.Group()

		for image in range(image_number):
			image = choice(image_surf_list)
			x = min_x
			y = 200
			sprite = StaticTile(0,x,y,image)
			self.image_sprites.add(sprite)
			min_x += 900

	def draw(self,surface,shift):
		self.image_sprites.update(shift)
		self.image_sprites.draw(surface)



