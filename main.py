import random
import glob
import itertools
import pygame

size = width, height = 1200, 800


runners_sprites = ['santa', 'dog', 'cat', 'dino']

runners_sprites_iter = itertools.chain(runners_sprites)

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
FPS = 10
pygame.mixer.init()

winner = None


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
        #not cool: I should handle this as an attribute rather than a global variable
        #then check which character is the winner in the main loop and display it in a square
        global winner
        if self.rect.x >= width - 80:
            self.is_running = False
            pygame.mixer.music.stop()
            if not winner:
                winner = self.name
                self.is_winner = True


def draw_grid():
    #drawing lanes
    quarter = height / 4
    for y in range(1, 4):
        pygame.draw.rect(screen, (0, 0, 0), (0, y * quarter, width, 10))

    #drawing start and end lines
    pygame.draw.rect(screen, (0, 0, 0), (80, 0, 20, height))
    pygame.draw.rect(screen, (0, 0, 0), (width - 80, 0, 20, height))


def draw_runners(groups):
    for group in groups:
        group.draw(screen)


def update_runners(groups):
    for group in groups:
        group.update()


def update_runners_speed(runners):
    for runner in runners:
        if runner.is_running:
            runner.change_speed()


def play_march():
    pygame.mixer.music.load('sounds/march.wav')
    pygame.mixer.music.play()


def find_winner(runners):
    for runner in runners:
        if runner.is_winner:
            return runner


def reset_all(runners):
    for runner in runners:
        runner.reset()


def draw_winner(winner):
    pygame.sprite.Group(winner).draw(screen)


runners = [Runner(type) for type in runners_sprites_iter]
groups = [pygame.sprite.Group(runner) for runner in runners]

race_is_over = False

while True:

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                race_is_over = False
                for runner in runners:
                    runner.is_running = True
                    play_march()
            if event.key == pygame.K_RETURN:
                race_is_over = False
                winner = None
                reset_all(runners)

    if not race_is_over:
        screen.fill([255, 255, 255])
        draw_grid()

        update_runners_speed(runners)
        update_runners(groups)
        draw_runners(groups)
        for runner in runners:
            runner.check_if_winner()

        if winner is not None:
            race_is_over = True

    else:
        screen.fill([255, 0, 0])
        winner = find_winner(runners)
        print('Winner is {}'.format(winner.name))
        winner.rect.x = width/2
        draw_winner(winner)


    pygame.display.flip()
    clock.tick(FPS)
