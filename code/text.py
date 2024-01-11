from tiles import StaticTile, AnimatedInfo
import pygame


class Introduction:
    def __init__(self):
        self.text_sprites = pygame.sprite.Group()
        sprite = StaticTile(0, 100, 150, pygame.image.load('../graphics/decoration/text/welcome.png').convert_alpha())
        self.text_sprites.add(sprite)

    def draw(self, surface, shift):
        self.text_sprites.update(shift)
        self.text_sprites.draw(surface)


class Conclusion:
    def __init__(self):
        self.text_sprites = pygame.sprite.Group()
        sprite = StaticTile(0, 100, 75, pygame.image.load('../graphics/decoration/text/thanks.png').convert_alpha())
        self.text_sprites.add(sprite)

    def draw(self, surface, shift):
        self.text_sprites.update(shift)
        self.text_sprites.draw(surface)


class Map_Info:
    def __init__(self):
        self.text_sprites = pygame.sprite.Group()
        sprite = AnimatedInfo(0, 100, 25, '/Users/Serena/PycharmProjects/GApp/graphics/info/maps/full')
        self.text_sprites.add(sprite)

    def draw(self, surface, shift):
        self.text_sprites.update(shift)
        self.text_sprites.draw(surface)


class Gem_Info:
    def __init__(self):
        self.text_sprites = pygame.sprite.Group()
        sprite = AnimatedInfo(0, 700, 360, '/Users/Serena/PycharmProjects/GApp/graphics/info/gems/skills')
        self.text_sprites.add(sprite)

    def draw(self, surface, shift):
        self.text_sprites.update(shift)
        self.text_sprites.draw(surface)


class Coin_Info:
    def __init__(self):
        self.text_sprites = pygame.sprite.Group()
        sprite = AnimatedInfo(0, 600, 360, '/Users/Serena/PycharmProjects/GApp/graphics/info/coins/coin')
        self.text_sprites.add(sprite)

    def draw(self, surface, shift):
        self.text_sprites.update(shift)
        self.text_sprites.draw(surface)
