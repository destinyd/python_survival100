WINDOW_SIZE = WIDTH , HEIGHT =  800,600
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
FPS = 60.0
ADD_BOMB_TIME = 300

class GameEngine:
  state = INIT
  global WINDOW_SIZE

  def __init__(self):
    global screen,background
    pygame.init()
    if pygame.font:
      self.font = pygame.font.Font(None, 36)
      self.little_font = pygame.font.Font(None, 18)
    screen = pygame.display.set_mode(WINDOW_SIZE, DOUBLEBUF ,32)
    pygame.display.set_caption("alive 100")
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((10, 10, 10))

    screen.blit(background, (0, 0))
    pygame.display.flip()

    self.clock = pygame.time.Clock()

    self.bomb_image = self.load_image('bomp.bmp',-1)

  def init(self):
    self.plane = Plane(self.load_image('plane.bmp', -1),(WIDTH / 2, HEIGHT / 2))
    self.bomb_group = pygame.sprite.Group()
    self.allsprites = pygame.sprite.Group() #RenderPlain([self.plane])

    self.plane.add(self.allsprites)
    self.record_time = False
    self.frame_total = 1
    self.bomb_max =  START_BOMB_NUM
    self.bomb_total = 0


  def run(self):
    self.start()
    while 1:
      self.clock.tick(FPS)
      self.get_input()
      self.update()
      pygame.display.flip()

  def start(self):
    self.init()
    self.state = START
    self.update = self.start_update

  def quit(self):
    pygame.quit()
    raise SystemExit,""
    exit()

  def play(self):
    self.state = PLAY
    self.record_time = True
    self.update = self.play_update

  def pause(self):
    self.state = PAUSE
    self.update = self.empty_update

  def game_over(self):
    self.state = GAME_OVER
    self.game_over_update()
    self.update = self.empty_update

  def get_input(self):
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


  def update(self):
    raise SystemExit,"no rewrite update"

  def empty_update(self):
    None

  def play_update(self):
      screen.blit(background, (0, 0))
      self.frame_total += 1
      if self.frame_total % ADD_BOMB_TIME == 0:
        self.bomb_max += 1
      self._fill_bomb()
      self.allsprites.update()
      self.allsprites.draw(screen)
      alive_time = self.frame_total / FPS
      text = self.little_font.render("alive %.2f sec" % (alive_time), 1, (250, 250, 250))
      textpos = text.get_rect(left= 10,top = 10)
      screen.blit(text, textpos)
      text = self.little_font.render("total bomb: %i" % (self.bomb_max), 1, (250, 250, 250))
      textpos = text.get_rect(right= 750,top = 10)
      screen.blit(text, textpos)
      for bomb_sprite in self.bomb_group.sprites():
        if self.plane.hit(bomb_sprite):
          self.game_over()


  def game_over_update(self):
      alive_time = self.frame_total / 60.0
      text = self.font.render("YOU ALIVE %.2f SECOND" % (alive_time), 1, (250, 250, 250))
      textpos = text.get_rect(centerx=background.get_width()/2, centery= background.get_height() /2)
      screen.blit(background, (0, 0))
      screen.blit(text, textpos)

  def start_update(self):
      text = self.font.render("PRESS ENTER TO START THE GAME", 1, (250, 250, 250))
      textpos = text.get_rect(centerx=background.get_width()/2, centery= background.get_height() /2)
      screen.blit(background, (0, 0))
      screen.blit(text, textpos)

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

  def _fill_bomb(self):
      if self.bomb_total < self.bomb_max:
        for x in range(0, self.bomb_max - self.bomb_total):
          bomb = Bomb(self.bomb_image,self.plane)
          self.allsprites.add(bomb)
          self.bomb_group.add(bomb)
          self.bomb_total += 1


