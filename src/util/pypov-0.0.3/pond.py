#!/usr/bin/env python

"""
PyPov-0.0.2 Copyright (c) Simon Burton, 2003
See LICENSE file.
"""


from math import *
from random import *

#import mkim
from Povray import *
#from FieldIm import *

class Pond(FieldIm):
  def __init__(self,phase=0.0,omega=6.0,N=256):
    self.phase=phase
    self.omega=omega
    FieldIm.__init__(self,None,N,N,self)
  def __call__(self,x,y):
    x-=0.5; y-=0.5;
    return (1.0+sin(self.phase+self.omega*sqrt(x*x+y*y)*2*pi))/2.0

def test00(nframes=1):
  cam = Camera(
    location=(0,20,-20),
    look_at=0,
    angle=30
  )
  lights = [ LightSource((0,0,-32),color=(0,0.3,0)),
    LightSource((256,0,-32),color=(0.3,0,0)),
    LightSource((0,256,-32),color=(0,0,1)),
    LightSource((256,256,-32),color=(0.1,0.3,0)) ]
  water = Texture(
      Finish(
        ambient = 0.2,
        diffuse = 0.3,
        reflection = 0.8,
        specular = 0.3
      ), Pigment(color=(0.4,0.4,1)))
  phase = 0.0
  dphase = -2*pi/nframes
  for i in range(nframes):
    hf = HeightField(
      #"field.png",
      Pond(phase).filename,
      "smooth",
      #Pigment(color=(0.4,0.4,1)),
      water,
      translate=(-0.5,-0.5,-0.5),
      #translate=(0.5,0.5,0),
      #scale=(N*10,N*10,3),
      scale=(24,1.75,24),
    )
    phase+=dphase
    file=File("pond/out.%.2d.pov"%i,cam,hf,*lights)

def test01(nframes=1):
  cam = Camera(
    location=(0,20,-20),
    look_at=0,
    angle=30
  )
  lights = [ LightSource((0,0,-32),color=(0,0.3,0)),
    LightSource((256,0,-32),color=(0.3,0,0)),
    LightSource((0,256,-32),color=(0,0,1)),
    LightSource((256,256,-32),color=(0.1,0.3,0)) ]
  water = Texture(
      Finish(
        ambient = 0.2,
        diffuse = 0.3,
        reflection = 0.8,
        specular = 0.3
      ), Pigment(color=(0.4,0.4,1)))
  phase = 0.0
  dphase = -2*pi/nframes
  def field(x,y):
    x-=0.5; y-=0.5;
    return (1.0+sin(6.0*sqrt(x*x+y*y)*2*pi))/2.0
  field_im = FieldIm("field.png",192,192,field)
  for i in range(nframes):
    hf = HeightField(
      "field.png",
      "smooth",
      #Pigment(color=(0.4,0.4,1)),
      water,
      translate=(-0.5,-0.5,-0.5),
      #translate=(0.5,0.5,0),
      #scale=(N*10,N*10,3),
      scale=(24,1.75,24),
    )
    phase+=dphase
    file=File("out.02.pov",cam,hf,*lights)

def test10(nframes=1):
  cam = Camera(
    location=(0,20,-20),
    look_at=0,
    angle=30
  )
  lights = [ LightSource((0,0,-32),color=(0,0.3,0)),
    LightSource((256,0,-32),color=(0.3,0,0)),
    LightSource((0,256,-32),color=(0,0,1)),
    LightSource((256,256,-32),color=(0.1,0.3,0)) ]
  water = Texture(
      Finish(
        ambient = 0.3,
        diffuse = 0.5,
        reflection = 0.8,
        specular = 0.3
      ),
      Pigment(
        #color=(0.4,0.4,1)
        ImageMap("me.jpg")
      )
    )
  phase = 0.0
  dphase = -2*pi/nframes
  for i in range(nframes):
    hf = HeightField(
      #"field.png",
      Pond(phase).filename,
      "smooth",
      #Pigment(color=(0.4,0.4,1)),
      water,
      translate=(-0.5,-0.5,-0.5),
      #translate=(0.5,0.5,0),
      #scale=(N*10,N*10,3),
      scale=(24,1.75,24),
    )
    phase+=dphase
    file=File("pond/out.%.2d.pov"%i,cam,hf,*lights)

if __name__=="__main__":
  try:
    n = int(sys.argv[1])
  except:
    n = 0
  eval ("test%.2d()"%n)

