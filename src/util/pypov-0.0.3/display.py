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
#screen = pygame.display.set_mode( (1024,768), FULLSCREEN )
#screen = pygame.display.set_mode( (800,600), FULLSCREEN )
screen = pygame.display.set_mode( (800,600) )
pygame.mouse.set_visible(0)

bg = pygame.Surface(screen.get_size())
bg = bg.convert()
bg.fill( (196,0,0) )
bg.fill( (255,255,255) )
bg.fill( (0,0,0) )
sz = bg.get_size()
#assert sz[0] == 800

def aspect(sz):
  return float(sz[0])/sz[1]

def blit(im): 
  imsz = im.get_size()
  mul = min( float(sz[0])/imsz[0], float(sz[1])/imsz[1] )
  #mul *= 0.7
  tgtsz = ( imsz[0]*mul, imsz[1]*mul )
  #im = pygame.transform.scale( im, tgtsz )
  x = max(0, (sz[0]-tgtsz[0])/2)
  y = max(0, (sz[1]-tgtsz[1])/2)
  #im = im.get_alpha()
  #im = im.convert()
  screen.blit(bg, (0,0) )
  screen.blit(im, (x,y) )
  pygame.display.flip()

def blit(im):
  screen.blit(im,(0,0))
  pygame.display.flip()

ims = [ pygame.image.load(name).convert()
  for name in sys.argv[1:] ]

while 1:
  for im in ims:
    try:
      blit(im)
      sleep(0.1)
    except pygame.error, e:
      print 'doh!', e
    for e in pygame.event.get():
      if e.type == QUIT or \
        (e.type == KEYUP and e.key == K_ESCAPE):
        pygame.display.quit()
        sys.exit(0)


