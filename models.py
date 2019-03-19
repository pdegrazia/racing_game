import random
import glob
import pygame

#I have to find a way to remove this
width, height = 1200, 800


class Runner(pygame.sprite.Sprite):
    starting_height = height/8 - 20

    def __init__(self, type):
        super(Runner, self).__init__()
        self.images = []
        self.name = type
        self._create_sprites(type)
        self.y_pos = self.starting_height
        Runner.starting_height += height/4
        self.x_pos = 0
        self.is_running = False
        self.speed = 0
        self.width = 100
        self.height = 100
        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self.is_winner = False

    def _create_sprites(self, type):
        sprites = glob.glob('images/'+type+'/*.*')
        for sprite in sprites:
            self.images.append(pygame.image.load(sprite))

    def update(self):
        if self.is_running:
            self.rect.x += self.speed
            # when the update method is called, we will increment the index
            self.index += 1
        else:
            self.speed = 0

        # if the index is larger than the total images
        if self.index >= len(self.images):
            # we will make the index to 0 again
            self.index = 0

        # finally we will update the image that will be displayed
        self.image = self.images[self.index]

    def reset(self):
        self.x_pos = 0
        self.is_running = False
        self.speed = 0
        self.is_winner = False
        self.rect.x = 0

    def change_speed(self):
        self.speed = random.randint(1, 10)

    def check_if_winner(self):
        #don't like this way of doing things
        #I am repeating return self
        if self.is_winner:
            return self
        elif self.rect.x >= width - 80:
            self.is_running = False
            pygame.mixer.music.stop()
            self.is_winner = True
            return self
