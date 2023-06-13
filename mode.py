import pygame

class mode_fighter():
  def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps):
    self.player = player
    self.size = data[0]
    self.mode_scale = data[1]
    self.mode_offset = data[2]
    self.action = 0
    self.frame_index = 0
    self.animation_list = self.mode_player(sprite_sheet, animation_steps)
    self.image = self.animation_list[self.action][self.frame_index]
    self.update_time = pygame.time.get_ticks()
    self.flip = flip
    self.rect = pygame.Rect(x, y, 80, 180)
    self.vel_y = 0 
    self.jump = False
    self.attack_typer = 0
    self.attacking = False
    self.blood = 100
    self.running = False
    self.hit = False
    self.alive = True

  def mode_player(self, sprite_sheet, animation_steps):
    animation_list = []
    for y, animation in enumerate(animation_steps):
      temp_image_list = []
      for x in range(animation):
        temp_image = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
        temp_image_list.append(pygame.transform.scale(temp_image, (self.size * self.mode_scale, self.size * self.mode_scale)))
      animation_list.append(temp_image_list)
    print("game debut by chien")
    return animation_list


  def mode_controls_player(self, screen_x, screen_y, surface, target):
    speed = 5
    dx = dy = 0
    gravity = 2
    self.running = False

    key_controls = pygame.key.get_pressed()
    if self.attacking == False:
      if self.player == 1:

        if key_controls[pygame.K_a]:
          dx = -speed
          self.running = True
        if key_controls[pygame.K_d]:
          dx = speed
          self.running = True

        # attack 
        if key_controls[pygame.K_f] or key_controls[pygame.K_g]:
          self.mode_attack(surface, target)
          if key_controls[pygame.K_f]:
            self.attack_typer = 1
          if key_controls[pygame.K_g]:
            self.attack_typer = 2

        if key_controls[pygame.K_SPACE] and self.jump == False:
          self.vel_y = -30
          self.jump = True


      if self.player == 2:

        if key_controls[pygame.K_LEFT]:
          dx = -speed
          self.running = True
        if key_controls[pygame.K_RIGHT]:
          dx = speed
          self.running = True

        # attack 
        if key_controls[pygame.K_KP1] or key_controls[pygame.K_KP2]:
          self.mode_attack(surface, target)
          if key_controls[pygame.K_KP1]:
            self.attack_typer = 1
          if key_controls[pygame.K_KP2]:
            self.attack_typer = 2

        if key_controls[pygame.K_KP0] and self.jump == False:
          self.vel_y = -30
          self.jump = True

    self.vel_y += gravity
    dy += self.vel_y

    if self.rect.left + dx < 0:
      dx = 0 - self.rect.left

    if self.rect.right + dx > screen_x:
      dx = screen_x - self.rect.right

    if self.rect.bottom + dy > screen_y - 70:
      self.vel_y = 0
      self.jump = False
      dy = screen_y - 70 - self.rect.bottom

    if target.rect.centerx < self.rect.centerx:
      self.flip = True
    else:
      self.flip = False


    self.rect.x += dx
    self.rect.y += dy

  def mode_update(self):
    if self.blood <= 0:
      self.blood = 0 
      self.alive = False
      self.mode_action(6)

    elif self.hit == True:
      self.mode_action(5)

    elif self.attacking == True:
      if self.attack_typer == 1:
        self.mode_action(4)
      elif self.attack_typer == 2:
        self.mode_action(3)

    elif self.jump == True:
      self.mode_action(2)

    elif self.running == True:
      self.mode_action(1)
    else:
      self.mode_action(0)

    animation_cooldown = 60
    self.image = self.animation_list[self.action][self.frame_index]

    if pygame.time.get_ticks() - self.update_time > animation_cooldown:
      self.frame_index += 1 
      self.update_time = pygame.time.get_ticks()

    if self.frame_index >= len(self.animation_list[self.action]):
      if self.alive == False:
        self.frame_index = len(self.animation_list[self.action]) - 1
      else:
        self.frame_index = 0

        if self.action == 3 or self.action == 4:
          self.attacking = False

        if self.action == 5:
          self.attacking = False
          self.hit = False
          self.update_time = pygame.time.get_ticks()


  def mode_attack(self, surface, target):
    self.attacking = True 
    attack_rects = pygame.Rect(self.rect.centerx - (4 * self.rect.width * self.flip), self.rect.y, 4 * self.rect.width, self.rect.height)
    if attack_rects.colliderect(target.rect):
      target.blood -= 0.5
      target.hit = True
      print("hit player")

    

  def mode_action(self, new_action):
    if new_action != self.action:
      self.action = new_action
      self.frame_index = 0
      self.update_time = pygame.time.get_ticks()


  def mode_body(self, surface):
    img_flip = pygame.transform.flip(self.image, self.flip, False)
   
    surface.blit(img_flip, (self.rect.centerx - (self.mode_offset[0] * self.mode_scale), self.rect.y - (self.mode_offset[1] * self.mode_scale)))
