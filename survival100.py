from game_engine import *
import pygame,os
from pygame.locals import *
from sys import exit
from plane import *
from bomb import *


INIT = 0
START = 1
PLAY = 2
PAUSE = 3
GAME_OVER = 4
QUIT = -1

START_BOMB_NUM = 100
ADD_BOMB_TIME = 300
WINDOW_SIZE = WIDTH , HEIGHT =  800,600
TITLE = "survival 100"

class Survival100(GameEngine):
  state = INIT
  bomb_group = pygame.sprite.Group()
  allsprites = pygame.sprite.Group()

  def __init__(self):
    GameEngine.__init__(self,WINDOW_SIZE,TITLE)
    if pygame.font:
      self.font = pygame.font.Font(None, 36)
      self.little_font = pygame.font.Font(None, 18)

    self.bomb_image = self.load_image('bomp.bmp',-1)
    self.plane_image = self.load_image('plane.bmp', -1)

  def init(self):
    self.plane = Plane(self.plane_image , (WIDTH / 2, HEIGHT / 2))
    self.bomb_group.empty()
    self.allsprites.empty()

    self.plane.add(self.allsprites)
    self.frame_total = 1
    self.bomb_max =  START_BOMB_NUM
    self.bomb_total = 0


  def start(self):
    self.init()
    self.state = START
    self.update = self.start_update


  def play(self):
    self.state = PLAY
    self.update = self.play_update

  def pause(self):
    self.state = PAUSE
    self.update = self.empty_update

  def game_over(self):
    self.state = GAME_OVER
    self.game_over_update()
    self.update = self.empty_update

  def get_control(self):
    for event in pygame.event.get():
      if event.type == QUIT:
        self.quit()
      elif event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          self.quit()
        elif self.state == START and event.key == K_RETURN:
          self.play()
        elif self.state == PLAY and event.key == K_RETURN:
          self.pause()
        elif self.state == PAUSE and event.key == K_RETURN:
          self.play()
        elif self.state == GAME_OVER and event.key == K_RETURN:
          self.start()


  def play_update(self):
      self.screen.blit(self.background, (0, 0))
      self.frame_total += 1
      if self.frame_total % ADD_BOMB_TIME == 0:
        self.bomb_max += 1
      self._fill_bomb()
      self.allsprites.update()
      self.allsprites.draw(self.screen)
      self.alive_time = self.frame_total / FPS

      text = self.little_font.render("survival %.2f sec" % (self.alive_time), 1, (250, 250, 250))
      textpos = text.get_rect(left= 10,top = 10)
      self.screen.blit(text, textpos)

      text = self.little_font.render("total bomb: %i" % (self.bomb_max), 1, (250, 250, 250))
      textpos = text.get_rect(right= 750,top = 10)
      self.screen.blit(text, textpos)
      for bomb_sprite in self.bomb_group.sprites():
        if self.plane.hit(bomb_sprite):
          self.game_over()


  def game_over_update(self):
      if self.alive_time < 100:
        text = self.font.render("YOU SURVIVAL %.2f SECOND" % (self.alive_time), 1, (250, 250, 250))
        textpos = text.get_rect(centerx=self.background.get_width()/2, centery= self.background.get_height() /2)
      else:
        text = self.font.render("YOU ARE SPRING MAN,SURVIVAL  %.2f SECOND" % (alive_time), 1, (250, 0, 0))
        textpos = text.get_rect(centerx=self.background.get_width()/2, centery= self.background.get_height() /2)

      self.screen.blit(self.background, (0, 0))
      self.screen.blit(text, textpos)

  def start_update(self):
      text = self.font.render("PRESS ENTER TO START THE GAME", 1, (250, 250, 250))
      textpos = text.get_rect(centerx=self.background.get_width()/2, centery= self.background.get_height() /2)
      self.screen.blit(self.background, (0, 0))
      self.screen.blit(text, textpos)

  def _fill_bomb(self):
      if self.bomb_total < self.bomb_max:
        for x in range(0, self.bomb_max - self.bomb_total):
          bomb = Bomb(self.bomb_image,self.plane)
          self.allsprites.add(bomb)
          self.bomb_group.add(bomb)
          self.bomb_total += 1

 
