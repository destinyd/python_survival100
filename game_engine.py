WINDOW_SIZE = WIDTH , HEIGHT =  800,600
import pygame,os
from sys import exit
from plane import *
from bomb import *

FPS = 60.0
class GameEngine:
  def __init__(self ,window_size ,title):
    pygame.init()
    self.screen = pygame.display.set_mode(window_size, DOUBLEBUF ,32)
    pygame.display.set_caption(title)
    self.background = pygame.Surface(self.screen.get_size())
    self.background = self.background.convert()
    self.background.fill((10, 10, 10))

    self.screen.blit(self.background, (0, 0))
    pygame.display.flip()
    self.clock = pygame.time.Clock()
    self.update = self.empty_update


  def run(self):
    self.start()
    while 1:
      self.clock.tick(FPS)
      self.get_control()
      self.update()
      pygame.display.flip()

  def get_control(self):
    raise SystemExit,"no rewrite get_control"


  def quit(self):
    pygame.quit()
    raise SystemExit,""
    exit()


  def update(self):
    raise SystemExit,"no rewrite update"

  def empty_update(self):
    None

  def load_image(self,name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

