#!/usr/bin/env python

"""
PyPov-0.0.2 Copyright (c) Simon Burton, 2003
See LICENSE file.
"""


from math import *
from random import *

from Povray import *

def test00():
  file = File("out.pov","colors.inc")
  Camera(location=(0,2,-3),look_at=(0.5,0.5,0.5)).write(file)
  Box( (0,0,0), (1,1,1), white ).write(file)
  Sphere( (0,1,2), 2, Texture(Pigment(color="Yellow"))).write(file)

def test01():
  file = File("out.pov","colors.inc")
  Camera(location=(0,2,-3),look_at=(0.5,0.5,0.5)).write(file)
  LightSource((2,4,-3),color="White").write(file)
  for i in range(100):
    v = random(),random(),random()
    color = random(),random(),random()
    Sphere( v, random()*0.3+0.02, Pigment(color=color)).write(file)

def test02():
  file = File("out.pov","colors.inc")
  file.include( "metals.inc" )
  #Item("background",color="Gray50")
  Background("Gray50")
  Camera(
    location=(0,.1,-25),
    look_at=(0.0,0.0,0.0),
    angle=30 ).write(file)
  Torus(
    #4, 1, Pigment("Green"), rotate=-90*x
    4, 1,
    Texture(
      Finish("F_MetalA"),
      Pigment(color=(0.4,0.5,0.6)),
      Normal(bumps=0.4,scale=0.2)),
    rotate=-90*x
  ).write(file)
  LightSource((300,300,-1000),color="White").write(file)

def test03():
  N = 10
  bg = Background("Gray50")
  cam = Camera(
    location=(0,.1,-25),
    look_at=(0.0,0.0,0.0),
    angle=30 )
  light = LightSource((300,300,-1000),color="White")
  torus = Torus(
    4, 1,
    Texture(
      Finish("F_MetalA"),
      Pigment(color=(0.4,0.5,0.6)),
      Normal(bumps=0.4,scale=0.2)),
  )
  i = 0
  for angle in range(0,180,10):
    torus.rotate = -angle*x
    file = File(
      "out/out.%.4d.pov"%i,
      "colors.inc", "metals.inc",
      cam, bg, light, torus )
    i+=1

def test04():
  cam = Camera(
    location=(0,0,-10),
    look_at=(100.0,0.0,0.0),
    angle=30 )
  light = LightSource((300,300,-1000),color=(1,1,1))
  spheres = [ Sphere( (2*i,0,0), 1, Pigment(color=(1,1,1)) )
    for i in range(400) ]
  file = File( "spheres.pov", cam, light, *spheres )

def test10():
  file = File("out.pov","colors.inc")
  Camera(location=(0,2,-3),look_at=(0.5,0.5,0.5)).write(file)
  LightSource((2,4,-3),color="White").write(file)
  Intersection(
    Sphere( (0,0,0), 1, translate=-0.5*x ),
    Sphere( (0,0,0), 1, translate=0.5*x ),
    Pigment("Red") 
  ).write(file)

gamma = (sqrt(5)-1)/2
def test20():
  " fibonacci "
  file = File()
  Camera(location=(0,0,-128), look_at=(0,0,0)).write(file)
  LightSource((100,100,-100), color=(1,1,1)).write(file)
  LightSource((150,150,-100), color=(0,0,0.3)).write(file)
  LightSource((-150,150,-100), color=(0,0.3,0)).write(file)
  LightSource((150,-150,-100), color=(0.3,0,0)).write(file)
  theta = 0.0
  for i in range(200):
    r = i * 0.5
    color = 1,1,1
    v = [ r*sin(theta), r*cos(theta), 0 ]
    Sphere( v, 0.7*sqrt(i),
      Texture(
        Finish(
          ambient = 0.0,
          diffuse = 0.0,
          reflection = 0.85,
          specular = 1
        ),
        Pigment(color=color))
    ).write(file)
    theta += gamma * 2 * pi

def test21():
  " fibonacci "
  file = File()
  Camera(location=(0,0,-96), look_at=(0,0,0)).write(file)
  #LightSource((0,0,-100), color=(1,1,1)).write(file)
  LightSource((32,32,-100), color=(0,0,0.6)).write(file)
  LightSource((-32,32,-100), color=(0,0.6,0)).write(file)
  LightSource((32,-32,-100), color=(0.6,0,0)).write(file)
  #LightSource((-32,-32,-100), color=(0.1,0.1,0.3)).write(file)
  theta = 0.0
  N=400
  for i in range(N):
    v = [ 64*sin(theta), 64*cos(theta), 200-i ]
    Sphere( v, 15.0,
      Texture(
        Finish(
          ambient = 0.0,
          diffuse = 0.0,
          reflection = 0.85,
          specular = 1
        ),
        Pigment(color=(1,1,1)))
    ).write(file)
    theta += gamma * 2 * pi

def test22():
  " fibonacci "
  lights = [
    #LightSource((0,0,-200), color=(1,1,1)),
    LightSource((96,96,-312), color=(0,0,1)),
    LightSource((-96,96,-312), color=(0,1,0)),
    LightSource((96,-96,-312), color=(1,0,0)),
    LightSource((-96,-96,-312), color=(0.3,0.3,1))
  ]
  cam = Camera()
  cam.location=(0,0,-96)
  cam.look_at=(0,0,0)
  file = File( "out.pov", cam, *lights )
  theta = 0.0
  #N=400
  N=300
  for i in range(N):
    v = [ 64*sin(theta), 64*cos(theta), 200-i ]
    Sphere( v, 15.0,
      Texture(
        Finish(
          ambient = 0.0,
          diffuse = 0.0,
          reflection = 0.85,
          specular = 1
        ),
        Pigment(color=(1,1,1)))
    ).write(file)
    theta += gamma * 2 * pi

def test23():
  " fibonacci "
  lights = [
    #LightSource((0,0,-200), color=(1,1,1)),
    LightSource((96,96,-312), color=(0,0,1)),
    LightSource((-96,96,-312), color=(0,1,0)),
    LightSource((96,-96,-312), color=(1,0,0)),
    LightSource((-96,-96,-312), color=(0.3,0.3,1))
  ]
  cam = Camera()
  cam.look_at=(0,0,0)
  M = 16
  for j in range(M):
    cam.location=(-192+192*2*(float(j)/M),0,-96)
    file = File( "out.%.4d.pov"%j, cam, *lights )
    theta = 0.0
    #N=400
    N=300
    for i in range(N):
      v = [ 64*sin(theta), 64*cos(theta), 200-i ]
      Sphere( v, 15.0,
        Texture(
          Finish(
            ambient = 0.0,
            diffuse = 0.0,
            reflection = 0.85,
            specular = 1
          ),
          Pigment(color=(1,1,1)))
      ).write(file)
      theta += gamma * 2 * pi

def mkspheres( idxs, dtheta = gamma*2*pi ):
  theta = 0.0
  spheres = []
  for i in idxs:
    r = i * 0.5
    color = 1,1,1
    v = [ r*sin(theta), r*cos(theta), 0 ]
    spheres.append(
      Sphere( v, 0.2+0.3*sqrt(i),
        Texture(
          Finish(
            #ambient = 0.1,
            ambient = 0.0,
            #diffuse = 0.1,
            diffuse = 0.0,
            reflection = 0.8,
            specular = 1
          ),
          Pigment(color=color))
      ))
    theta += dtheta
  return spheres

def test30():
  " fibonacci "
  light = LightSource((100,100,-100), color=(1,1,1))
  #cam = Camera(location=(0,0,-128), look_at=(0,0,0))
  cam = Camera(look_at=(0,0,0))
  dtheta = gamma*2*pi
  i=0
  N = 512
  ddtheta = 2*pi / N
  for i in range(N):
  #while dtheta < 2*pi:
    cam.location = (0,32*sin(dtheta),-128*cos(dtheta))
    spheres = mkspheres( range(10,100), dtheta )
    file = File("out/out.%.4d.pov"%i, light, cam, *spheres)
    #dtheta += 0.0001*2*pi
    dtheta += ddtheta
    i+=1

def test31():
  " this is a big one "
  light = LightSource((100,100,-100), color=(1,1,1))
  #cam = Camera(location=(0,0,-128), look_at=(0,0,0))
  cam = Camera(look_at=(0,0,0))
  cam.location=(0,0,-64)
  dtheta = 0.0
  i=0
  N = 1024 * 4 
  ddtheta = 2*pi / N
  for i in range(N):
    cam.rotate = x*(180*dtheta/pi)
    spheres = mkspheres( range(10,100), dtheta )
    #spheres = mkspheres( range(10,100), gamma*2*pi )
    file = File("out/out.%.4d.pov"%i, light, cam, *spheres)
    dtheta += ddtheta
    i+=1

if __name__=="__main__":
  try:
    n = int(sys.argv[1])
  except:
    n = 20
  eval ("test%.2d()"%n)

