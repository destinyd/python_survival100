import pygame
from pygame.locals import *

LINEAR = 10
SLASH_SPEED = 7
MOVE = (0,0), \
      (0,- LINEAR),(LINEAR,0),(SLASH_SPEED,- SLASH_SPEED),(0,LINEAR),(0,0), \
      (SLASH_SPEED,SLASH_SPEED),(LINEAR,0),(- LINEAR,0),(- SLASH_SPEED,- SLASH_SPEED),(0,0), \
      (0,- LINEAR),(- SLASH_SPEED,SLASH_SPEED),(- LINEAR,0),(0,LINEAR),(0,0)

class Plane(pygame.sprite.Sprite):
  def __init__(self,load_image,start_pos):
    pygame.sprite.Sprite.__init__(self)
    self.image, self.rect = load_image#_load_image('plane.bmp', -1)
    screen = pygame.display.get_surface()
    self.area = screen.get_rect()
    self.rect.center = start_pos
    self.move = 0,0
    self.direction = 0 #up 1 right 2 down 4 left 8

  def update(self):
    self.direction = 0
    self.move = 0,0
    self._get_input()
    self._walk()

  def _walk(self):
    #"move plane by input"
    self.move = MOVE[self.direction]
    newpos = self.rect.move(self.move)
    if newpos.left <= self.area.left or \
       newpos.right >= self.area.right :
         newpos.centerx = self.rect.centerx
    if newpos.top <= self.area.top or \
       newpos.bottom >= self.area.bottom :
         newpos.centery = self.rect.centery
    self.rect = newpos

  def _get_input(self):
        key = pygame.key.get_pressed()

        if key[K_UP]:
          self.direction += 1
        if key[K_RIGHT]:
          self.direction += 2
        if key[K_DOWN]:
          self.direction += 4
        if key[K_LEFT]:
          self.direction += 8

  def hit(self,target):
    hitbox = self.rect.inflate(-20,-20)
    return hitbox.colliderect(target.rect)
