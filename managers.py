import pygame
FPS = 10


class GameManager:
    @staticmethod
    def update_runners_speed(runners):
        for runner in runners:
            if runner.is_running:
                runner.change_speed()

    @staticmethod
    def find_winner(runners):
        for runner in runners:
            winning_runner = runner.check_if_winner()
            if winning_runner:
                return winning_runner

    @staticmethod
    def reset_all(runners):
        for runner in runners:
            runner.reset()


class MusicManager:
    def __init__(self):
        pygame.mixer.init()

    def play_march(self):
        pygame.mixer.music.load('sounds/march.wav')
        pygame.mixer.music.play()


class ScreenManager:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()

    def update_screen(self):
        pygame.display.flip()
        self.clock.tick(FPS)

    def get_screen(self):
        return self.screen

    def draw_grid(self):
        # drawing lanes
        quarter = self.height / 4
        for y in range(1, 4):
            pygame.draw.rect(self.screen, (0, 0, 0), (0, y * quarter, self.width, 10))

        # drawing start and end lines
        pygame.draw.rect(self.screen, (0, 0, 0), (80, 0, 20, self.height))
        pygame.draw.rect(self.screen, (0, 0, 0), (self.width - 80, 0, 20, self.height))

    def draw_winner(self, winner):
        pygame.sprite.Group(winner).draw(self.screen)

    def draw_runners(self, groups):
        for group in groups:
            group.draw(self.screen)

    def update_runners(self, groups):
        for group in groups:
            group.update()
