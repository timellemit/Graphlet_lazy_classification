#!/usr/bin/env python
"""
PyPov-0.0.1 Copyright (c) Simon Burton, 2003
See LICENSE file.
"""



import os, sys
from time import sleep
import pygame

from pygame.locals import *

#from pygame import image

pygame.init()
#screen = pygame.display.set_mode( (640,480) )
screen = pygame.display.set_mode( (1280,960), FULLSCREEN )
#screen = pygame.display.set_mode( (800,600), FULLSCREEN )
#screen = pygame.display.set_mode( (800,600) )
pygame.mouse.set_visible(0)

bg = pygame.Surface(screen.get_size())
bg = bg.convert()
bg.fill( (196,0,0) )
bg.fill( (255,255,255) )
bg.fill( (0,0,0) )
sz = bg.get_size()
#assert sz[0] == 800

def blit(im):
  w,h=im.get_size()
  x = (sz[0]-w)/2
  y = (sz[1]-h)/2
  screen.blit(im,(x,y))
  pygame.display.flip()

while 1:
  for name in sys.argv[1:]:
    try:
      blit(pygame.image.load(name))
      #sleep(0.1)
      print "blit",name
    except pygame.error, e:
      print 'doh!', e
    for e in pygame.event.get():
      if e.type == QUIT or \
        (e.type == KEYUP and e.key == K_ESCAPE):
        pygame.display.quit()
        sys.exit(0)
  #break


