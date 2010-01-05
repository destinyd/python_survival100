import random,pygame,time,math

BOMB_SPEED_CHOICE = [1,2]
MAX_SPEED = 1.0
class Bomb(pygame.sprite.Sprite):
  def __init__(self,load_image,target):
    pygame.sprite.Sprite.__init__(self)
    self.image, self.rect = load_image#_load_image('plane.bmp', -1)
    screen = pygame.display.get_surface()
    self.area = screen.get_rect()
    self.target = target
    self.init()
   

  def init(self):
    self.target_center = self.target.rect.center
    self.rect.center = self.init_pos() 
    self.pos = [float(self.rect.centerx), float(self.rect.centery)]
    self.move = self.init_move()

  def update(self):
    self.pos[0] += self.move[0]
    self.pos[1] += self.move[1]
    self.rect.center = int(self.pos[0]),int(self.pos[1])
    self.rect = self.rect.move(0,0)
    if self.out():
      self.init()

  def out(self):
    if self.rect.centerx < self.area.left - 1 or \
      self.rect.centerx > self.area.right + 1 or \
      self.rect.centery < self.area.top -1 or \
      self.rect.centery > self.area.bottom +1 :
      return True
    return False

  def init_move(self):
    self.speed = random.random() + MAX_SPEED #choice(BOMB_SPEED_CHOICE)
    self.center = self.rect.center[0],self.rect.center[1]
    self.range = self.target_center[0] - self.center[0] , self.target_center[1] - self.center[1]
    self.angle = math.atan2(self.range[1],self.range[0])
    return self.speed * math.cos(self.angle), self.speed * math.sin(self.angle)

  def init_pos(self):
    random.seed(int(time.time() * 1000000))
    if random.random() < 0.5:
      self.rand_num = random.randint(0,self.area.right * 2)
      if self.rand_num <= self.area.right:
        return self.rand_num , self.area.top
      else:
        return self.rand_num - self.area.right, self.area.bottom
    else:
      self.rand_num = random.randint(0,self.area.bottom * 2)
      if self.rand_num <= self.area.bottom:
        return self.area.left, self.rand_num
      else:
        return self.area.right, self.rand_num - self.area.bottom
      #    self.rand_num = random.randint(0,self.area.bottom * 2 + self.area.right * 2 - 1)
#    if self.rand_num < self.area.right:
      #      #      return self.rand_num,self.area.top
#    elif self.rand_num < self.area.right + self.area.bottom:
      #      return self.area.right, self.rand_num - self.area.right
#    elif self.rand_num < self.area.right * 2 + self.area.bottom:
      #      return self.rand_num - self.area.right - self.area.bottom, self.area.bottom
#    elif self.rand_num < self.area.bottom * 2 + self.area.right * 2 -1:
      #      return self.area.left,self.rand_num - self.area.right * 2 - self.area.bottom
#    else:
      #      return self.init_pos()
