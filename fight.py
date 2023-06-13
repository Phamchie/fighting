import pygame
from mode import mode_fighter

pygame.init()

screen_x = 1000
screen_y = 600
screen = pygame.display.set_mode((screen_x, screen_y))

fighter1_size = 162
fighter1_scale = 5
fighter1_offset = [72, 56]
fighter1_data = [fighter1_size, fighter1_scale, fighter1_offset]

fighter2_size = 250
fighter2_scale = 4
fighter2_offset = [112, 107]
fighter2_data = [fighter2_size, fighter2_scale, fighter2_offset]

# setup caption and logo
pygame.display.set_caption("Game Debut By Chien")
screen_logo = pygame.image.load("code/logo.png").convert_alpha()
screen_logo = pygame.transform.scale(screen_logo, (100, 100))
pygame.display.set_icon(screen_logo)

clock = pygame.time.Clock()
FPS = 60

fighter1_sheet = pygame.image.load("code/son/warrior.png").convert_alpha()
fighter2_sheet = pygame.image.load("code/son/wizard.png").convert_alpha()
fighter1_animation_steps = [10, 8, 1, 7, 7, 3, 7]
fighter2_animation_steps = [8, 8, 2, 8, 8, 3, 7]

sys_cursor = pygame.image.load("code/sys.png").convert_alpha()
sys_cursor = pygame.transform.scale(sys_cursor, (140, 120))
pygame.mouse.set_visible(False)

background = pygame.image.load("code/japen.gif").convert_alpha()

def draw_background():
  background_scale = pygame.transform.scale(background, (screen_x, screen_y))
  screen.blit(background_scale, (0, 0))

def draw_health(blood, x, y):
  health = blood / 100
  pygame.draw.rect(screen, ('yellow'), (x - 5, y - 5, 310, 40))
  pygame.draw.rect(screen, ('red'), (x, y, 300, 30))
  pygame.draw.rect(screen, ('green'), (x, y, 300 * health, 30))

fighter1 = mode_fighter(1, 200, 310, False, fighter1_data, fighter1_sheet, fighter1_animation_steps)
fighter2 = mode_fighter(2, 700, 310, True, fighter2_data, fighter2_sheet, fighter2_animation_steps)


run = True
while run:
  draw_background()

  draw_health(fighter1.blood, 20, 20)
  draw_health(fighter2.blood, 680, 20)

  fighter1.mode_update()
  fighter2.mode_update()

  fighter1.mode_controls_player(screen_x, screen_y, screen, fighter2)
  fighter2.mode_controls_player(screen_x, screen_y, screen, fighter1)

  fighter1.mode_body(screen)
  fighter2.mode_body(screen)
      
  pos = pygame.mouse.get_pos()

  screen.blit(sys_cursor, pos)

  clock.tick(FPS)

  pygame.display.flip()

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

    pygame.display.update()

pygame.quit()
