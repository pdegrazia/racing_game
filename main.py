import itertools
import pygame

from models import Runner
from managers import GameManager, ScreenManager, MusicManager

WIDTH, HEIGHT = 1200, 800

runners_sprites = ['santa', 'dog', 'cat', 'dino']

runners_sprites_iter = itertools.chain(runners_sprites)


winner = None


runners = [Runner(runner_type, ) for runner_type in runners_sprites_iter]
groups = [pygame.sprite.Group(runner) for runner in runners]

race_is_over = False


screen_manager = ScreenManager(WIDTH, HEIGHT)

music_manager = MusicManager()

screen = screen_manager.get_screen()

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                race_is_over = False
                for runner in runners:
                    runner.is_running = True
                    music_manager.play_march()
            if event.key == pygame.K_RETURN:
                race_is_over = False
                winner = None
                GameManager.reset_all(runners)

    if not race_is_over:
        screen.fill([255, 255, 255])
        screen_manager.draw_grid()

        GameManager.update_runners_speed(runners)
        screen_manager.update_runners(groups)
        screen_manager.draw_runners(groups)
        winner = GameManager.find_winner(runners)

        if winner is not None:
            race_is_over = True

    else:
        winner = GameManager.find_winner(runners)
        screen.fill([255, 0, 0])
        print('Winner is {}'.format(winner.name))
        winner.rect.x = screen_manager.width / 2
        screen_manager.draw_winner(winner)

    screen_manager.update_screen()