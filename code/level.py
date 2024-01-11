import pygame 
from support import import_csv_layout, import_cut_graphics
from settings import tile_size, screen_height, screen_width
from tiles import Tile, StaticTile, Chest, Collectible, Tree, Crate
from enemy import Enemy
from decoration import Sky, Water, Clouds, Ground, TreeDark, TreeMid, TreeTop, TreeLight, TreeBack
from text import Introduction, Conclusion, Map_Info, Gem_Info, Coin_Info
from player import Player
from particles import ParticleEffect
from game_data import levels

class Level:
	def __init__(self,current_level,surface,create_overworld,change_health):
		# general setup
		self.display_surface = surface
		self.world_shift = 0
		self.current_x = None

		# audio
		self.coin_sound = pygame.mixer.Sound('/Users/Serena/PycharmProjects/GApp/audio/effects/coin.wav')
		self.stomp_sound = pygame.mixer.Sound('/Users/Serena/PycharmProjects/GApp/audio/effects/stomp.wav')

		# overworld connection 
		self.create_overworld = create_overworld
		self.current_level = current_level
		level_data = levels[self.current_level]
		self.new_max_level = level_data['unlock']

		# player 
		player_layout = import_csv_layout(level_data['player'])
		self.player = pygame.sprite.GroupSingle()
		self.goal = pygame.sprite.GroupSingle()
		self.player_setup(player_layout,change_health)

		# # user interface
		# self.change_coins = change_coins

		# dust 
		self.dust_sprite = pygame.sprite.GroupSingle()
		self.player_on_ground = False

		# explosion particles
		self.explosion_sprites = pygame.sprite.Group()

		# terrain setup
		terrain_layout = import_csv_layout(level_data['terrain'])
		self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')

		# grass setup 
		grass_layout = import_csv_layout(level_data['grass'])
		self.grass_sprites = self.create_tile_group(grass_layout,'grass')

		# spikes setup
		spikes_layout = import_csv_layout(level_data['spikes'])
		self.spikes_sprites = self.create_tile_group(spikes_layout, 'spikes')

		# crates
		crate_layout = import_csv_layout(level_data['crates'])
		self.crate_sprites = self.create_tile_group(crate_layout,'crates')

		# platforms
		platforms_layout = import_csv_layout(level_data['platforms'])
		self.platforms_sprites = self.create_tile_group(platforms_layout, 'platforms')

		# map
		map_layout = import_csv_layout(level_data['maps'])
		self.map_sprites = self.create_tile_group(map_layout,'maps')

		# gems
		gems_layout = import_csv_layout(level_data['gems'])
		self.gems_sprites = self.create_tile_group(gems_layout, 'gems')

		# coins
		coins_layout = import_csv_layout(level_data['coins'])
		self.coins_sprites = self.create_tile_group(coins_layout, 'coins')

		# # foreground palms
		# fg_palm_layout = import_csv_layout(level_data['fg palms'])
		# self.fg_palm_sprites = self.create_tile_group(fg_palm_layout,'fg palms')
		#
		# background palms
		trees_layout = import_csv_layout(level_data['trees'])
		self.trees_sprites = self.create_tile_group(trees_layout,'trees')

		# enemy
		enemy_layout = import_csv_layout(level_data['enemy'])
		self.enemy_sprites = self.create_tile_group(enemy_layout,'enemy')

		# constraint
		constraints_layout = import_csv_layout(level_data['constraints'])
		self.constraints_sprites = self.create_tile_group(constraints_layout,'constraints')

		self.sky = Sky(20,self.current_level,'level')
		level_width = len(terrain_layout[0]) * tile_size
		self.water = Water(screen_height - 200,level_width,self.current_level)

		if self.current_level == 0:
			self.intro = Introduction()

		if self.current_level == 4:
			self.concl = Conclusion()

		if self.current_level == 1 or self.current_level == 0 or self.current_level == 4:
			self.clouds = Clouds(550,level_width,35)

		if self.current_level == 3:
			self.ground = Ground(level_width,5)
			self.tree_dark = TreeDark(level_width,5)
			self.tree_mid = TreeMid(level_width, 5)
			self.tree_top = TreeTop(level_width, 5)
			self.tree_light = TreeLight(level_width, 5)
			self.tree_back = TreeBack(level_width, 5)

		if current_level == 1:
			self.map_info = Map_Info()

		if current_level == 2:
			self.gem_info = Gem_Info()

		if current_level == 3:
			self.coin_info = Coin_Info()

		self.map_collided = False
		self.map_collision_timer = 0

		self.gem_collided = False
		self.gem_collision_timer = 0

		self.coin_collided = False
		self.coin_collision_timer = 0

	def create_tile_group(self,layout,type):
		sprite_group = pygame.sprite.Group()

		for row_index, row in enumerate(layout):
			for col_index,val in enumerate(row):
				if val != '-1':
					x = col_index * tile_size
					y = row_index * tile_size

					if type == 'terrain':
						terrain_tile_list = import_cut_graphics('../graphics/terrain/terrain_tiles.png')
						tile_surface = terrain_tile_list[int(val)]
						sprite = StaticTile(tile_size,x,y,tile_surface)

					if type == 'platforms':
						platform_tile_list = import_cut_graphics('../graphics/terrain/platforms.png')
						tile_surface = platform_tile_list[int(val)]
						sprite = StaticTile(tile_size, x, y, tile_surface)
						
					if type == 'grass':
						grass_tile_list = import_cut_graphics('../graphics/decoration/grass/grass.png')
						tile_surface = grass_tile_list[int(val)]
						sprite = StaticTile(tile_size,x,y,tile_surface)

					if type == 'spikes':
						spikes_tile_list = import_cut_graphics('../graphics/spikes/spikes.png')
						tile_surface = spikes_tile_list[int(val)]
						sprite = StaticTile(tile_size,x,y,tile_surface)

					if type == 'crates':
						sprite = Crate(tile_size,x,y)

					if type == 'maps':
						sprite = Collectible(tile_size, x, y, '../graphics/maps')

					if type == 'gems':
						sprite = Collectible(tile_size, x, y, '../graphics/gems')

					if type == 'coins':
						sprite = Collectible(tile_size, x, y, '../graphics/coins/silver')

					# if type == 'fg palms':
					# 	if val == '0': sprite = Palm(tile_size,x,y,'../graphics/terrain/palm_small',38)
					# 	if val == '1': sprite = Palm(tile_size,x,y,'../graphics/terrain/palm_large',64)
					#
					if type == 'trees':
						if val == '19': sprite = Tree(tile_size, x, y, '../graphics/trees/left', 20)
						if val == '18': sprite = Tree(tile_size,x,y,'../graphics/trees/regular',20)
						if val == '17': sprite = Tree(tile_size, x, y, '../graphics/trees/right', 10)

					if type == 'enemy':
						sprite = Enemy(tile_size,x,y)

					if type == 'constraints':
						sprite = Tile(tile_size,x,y)

					sprite_group.add(sprite)
		
		return sprite_group

	def player_setup(self,layout,change_health):
		for row_index, row in enumerate(layout):
			for col_index,val in enumerate(row):
				x = col_index * tile_size
				y = row_index * tile_size
				if val == '1':
					sprite = Player((x,y),self.display_surface,self.create_jump_particles,change_health)
					self.player.add(sprite)
				if val == '0':
					sprite = Chest(tile_size,x,y,'../graphics/character/chest')
					self.goal.add(sprite)
				if val == '2':
					sprite = Chest(tile_size,x,y,'../graphics/character/chest')
					self.goal.add(sprite)
				if val == '3':
					sprite = Chest(tile_size,x,y,'../graphics/character/chest')
					self.goal.add(sprite)

	def enemy_collision_reverse(self):
		for enemy in self.enemy_sprites.sprites():
			if pygame.sprite.spritecollide(enemy,self.constraints_sprites,False):
				enemy.reverse()

	def create_jump_particles(self,pos):
		if self.player.sprite.facing_right:
			pos -= pygame.math.Vector2(10,5)
		else:
			pos += pygame.math.Vector2(10,-5)
		jump_particle_sprite = ParticleEffect(pos,'jump')
		self.dust_sprite.add(jump_particle_sprite)

	def horizontal_movement_collision(self):
		player = self.player.sprite
		player.collision_rect.x += player.direction.x * player.speed
		collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() # + self.fg_palm_sprites.sprites()
		for sprite in collidable_sprites:
			if sprite.rect.colliderect(player.collision_rect):
				if player.direction.x < 0: 
					player.collision_rect.left = sprite.rect.right
					player.on_left = True
					self.current_x = player.rect.left
				elif player.direction.x > 0:
					player.collision_rect.right = sprite.rect.left
					player.on_right = True
					self.current_x = player.rect.right

		# if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
		# 	player.on_left = False
		# if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
		# 	player.on_right = False

	def vertical_movement_collision(self):
		player = self.player.sprite
		player.apply_gravity()
		collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.platforms_sprites.sprites()

		for sprite in collidable_sprites:
			if sprite.rect.colliderect(player.collision_rect):
				if player.direction.y > 0: 
					player.collision_rect.bottom = sprite.rect.top
					player.direction.y = 0
					player.on_ground = True
				elif player.direction.y < 0:
					player.collision_rect.top = sprite.rect.bottom
					player.direction.y = 0
					player.on_ceiling = True

		if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
			player.on_ground = False
		# if player.on_ceiling and player.direction.y > 0.1:
		# 	player.on_ceiling = False

	def scroll_x(self):
		player = self.player.sprite
		player_x = player.rect.centerx
		direction_x = player.direction.x

		if player_x < screen_width / 4 and direction_x < 0:
			self.world_shift = 8
			player.speed = 0
		elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
			self.world_shift = -8
			player.speed = 0
		else:
			self.world_shift = 0
			player.speed = 8

	def get_player_on_ground(self):
		if self.player.sprite.on_ground:
			self.player_on_ground = True
		else:
			self.player_on_ground = False

	def create_landing_dust(self):
		if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
			if self.player.sprite.facing_right:
				offset = pygame.math.Vector2(10,15)
			else:
				offset = pygame.math.Vector2(-10,15)
			fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset,'land')
			self.dust_sprite.add(fall_dust_particle)

	def check_death(self):
		if self.player.sprite.rect.top > screen_height:
			self.create_overworld(self.current_level,0)

	def check_win(self):
		if pygame.sprite.spritecollide(self.player.sprite,self.goal,False):
			self.create_overworld(self.current_level,self.new_max_level)

	def check_map_collisions(self):
		collided_maps = pygame.sprite.spritecollide(self.player.sprite,self.map_sprites,True)
		if collided_maps:
			self.coin_sound.play()
			self.map_collided = True
			self.map_collision_timer = pygame.time.get_ticks()

	def check_gem_collisions(self):
		collided_gems = pygame.sprite.spritecollide(self.player.sprite,self.gems_sprites,True)
		if collided_gems:
			self.coin_sound.play()
			self.gem_collided = True
			self.gem_collision_timer = pygame.time.get_ticks()
	def check_coin_collisions(self):
		collided_coins = pygame.sprite.spritecollide(self.player.sprite,self.coins_sprites,True)
		if collided_coins:
			self.coin_sound.play()
			self.coin_collided = True
			self.coin_collision_timer = pygame.time.get_ticks()
		# if collided_maps:
		# 	for map in collided_maps:
		# 		self.change_coins(map.value)

	def check_enemy_collisions(self):
		enemy_collisions = pygame.sprite.spritecollide(self.player.sprite,self.enemy_sprites,False)

		if enemy_collisions:
			for enemy in enemy_collisions:
				enemy_center = enemy.rect.centery
				enemy_top = enemy.rect.top
				player_bottom = self.player.sprite.rect.bottom
				if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
					self.stomp_sound.play()
					self.player.sprite.direction.y = -15
					explosion_sprite = ParticleEffect(enemy.rect.center,'explosion')
					self.explosion_sprites.add(explosion_sprite)
					enemy.kill()
				else:
					self.player.sprite.get_damage()

	def check_spikes_collisions(self):
		spikes_collisions = pygame.sprite.spritecollide(self.player.sprite,self.spikes_sprites,False)

		if spikes_collisions:
			for spikes in spikes_collisions:
				self.player.sprite.get_damage()

	def run(self):
		# run the entire game / level 
		
		# sky 
		self.sky.draw(self.display_surface)
		if self.current_level == 1 or self.current_level == 0 or self.current_level == 4:
			self.clouds.draw(self.display_surface,self.world_shift)

		if self.current_level == 3:
			self.tree_back.draw(self.display_surface, self.world_shift)
			# self.tree_light.draw(self.display_surface, self.world_shift)
			# self.tree_mid.draw(self.display_surface, self.world_shift)
			self.tree_dark.draw(self.display_surface,self.world_shift)
			self.tree_top.draw(self.display_surface, self.world_shift)
			self.ground.draw(self.display_surface, self.world_shift)

		if self.current_level == 0:
			self.intro.draw(self.display_surface,self.world_shift)

		if self.current_level == 4:
			self.concl.draw(self.display_surface,self.world_shift)

		# water
		if self.current_level == 1 or self.current_level == 2:
			self.water.draw(self.display_surface, self.world_shift)

		# trees
		self.trees_sprites.update(self.world_shift)
		self.trees_sprites.draw(self.display_surface)

		# dust particles
		self.dust_sprite.update(self.world_shift)
		self.dust_sprite.draw(self.display_surface)

		# terrain
		self.terrain_sprites.update(self.world_shift)
		self.terrain_sprites.draw(self.display_surface)

		# platforms
		self.platforms_sprites.update(self.world_shift)
		self.platforms_sprites.draw(self.display_surface)

		# spikes
		self.spikes_sprites.update(self.world_shift)
		self.spikes_sprites.draw(self.display_surface)
		
		# enemy 
		self.enemy_sprites.update(self.world_shift)
		self.constraints_sprites.update(self.world_shift)
		self.enemy_collision_reverse()
		self.enemy_sprites.draw(self.display_surface)
		self.explosion_sprites.update(self.world_shift)
		self.explosion_sprites.draw(self.display_surface)

		# crate
		self.crate_sprites.update(self.world_shift)
		self.crate_sprites.draw(self.display_surface)

		# grass
		self.grass_sprites.update(self.world_shift)
		self.grass_sprites.draw(self.display_surface)

		# maps
		self.map_sprites.update(self.world_shift)
		self.map_sprites.draw(self.display_surface)

		# gems
		self.gems_sprites.update(self.world_shift)
		self.gems_sprites.draw(self.display_surface)

		# coins
		self.coins_sprites.update(self.world_shift)
		self.coins_sprites.draw(self.display_surface)

		# # foreground palms
		# self.fg_palm_sprites.update(self.world_shift)
		# self.fg_palm_sprites.draw(self.display_surface)

		# player sprites
		self.player.update()
		self.horizontal_movement_collision()
		
		self.get_player_on_ground()
		self.vertical_movement_collision()
		self.create_landing_dust()
		
		self.scroll_x()
		self.player.draw(self.display_surface)
		self.goal.update(self.world_shift)
		self.goal.draw(self.display_surface)

		self.check_death()
		self.check_win()

		# checking collisions w/ collectibles
		self.check_map_collisions()
		self.check_gem_collisions()
		self.check_coin_collisions()
		self.check_spikes_collisions()
		self.check_enemy_collisions()

		# opening popups
		if self.map_collided:
			if pygame.time.get_ticks() - self.map_collision_timer < 7000:
				self.map_info.draw(self.display_surface, self.world_shift)
			else:
				self.map_collided = False

		if self.gem_collided:
			if pygame.time.get_ticks() - self.gem_collision_timer < 3600:
				self.gem_info.draw(self.display_surface, self.world_shift)
			else:
				self.gem_collided = False

		if self.coin_collided:
			if pygame.time.get_ticks() - self.coin_collision_timer < 4600:
				self.coin_info.draw(self.display_surface, self.world_shift)
			else:
				self.coin_collided = False







