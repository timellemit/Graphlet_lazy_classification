#!/usr/bin/env python

"""
PyPov-0.0.2 Copyright (c) Simon Burton, 2003
See LICENSE file.
"""


from math import *
from random import *
from Povray import *

def test00():
  " mesh "
  file=File()
  Camera(location=(20,20,-50),look_at=(50,50,50)).write(file)
  LightSource((50,50,-50),(1,1,1)).write(file)
  textures = []
  for i in range(100):
    name = "t%s"%i
    file.declare(
      name, Texture(
        Finish(
          ambient = 0.2,
          diffuse = 0.7,
          reflection = 0.8,
          specular = 1
        ),
        Pigment( color=(random(),random(),random()) )
      )
    )
    textures.append(Texture(name))
  mesh=Mesh()
  for i in range(100):
    A = [ random()*100 for j in range(3) ]
    B = [ random()*100 for j in range(3) ]
    C = [ random()*100 for j in range(3) ]
    mesh.append( Triangle(A,B,C,textures[i]) )
    #mesh.append( Triangle(A,B,C) )
  mesh.append( 
    Texture(
      Finish(
        ambient = 0.2,
        diffuse = 0.7,
      ),
      Pigment(color=(0.9,0.9,0.9))
      #Pigment(ImageMap("me.jpg"),scale=(100,100,100))
  ))
  mesh.write(file)

def test01():
  " mesh "
  file=File()
  Camera(location=(20,20,-50),look_at=(50,50,50)).write(file)
  LightSource((50,50,-50),(1,1,1)).write(file)
  textures = []
  for i in range(100):
    name = "t%s"%i
    file.declare(
      name, Texture(
        Finish(
          ambient = 0.2,
          diffuse = 0.7,
          reflection = 0.8,
          specular = 1
        ),
        Pigment(color=(random(),random(),random()))))
    textures.append(Texture(name))
  mesh=Mesh()
  for i in range(100):
    A = [ random()*100 for j in range(3) ]
    B = [ a + random()*32 for a in A ]
    C = [ b + random()*32 for b in B ]
    mesh.append( Triangle(A,B,C,textures[i]) )
  mesh.append( 
    Texture(
      Finish(
        ambient = 0.2,
        diffuse = 0.7,
      ),
      Pigment(color=(0.9,0.9,0.9))
  ))
  mesh.write(file)

def test02():
  " mesh "
  file=File()
  Camera(location=(0,-64,-192),look_at=(0,0,0)).write(file)
  textures = []
  N = 32
  for i in range(N):
    name = "t%s"%i
    file.declare(
      name, Texture(
        Finish(
          ambient = 0.2,
          diffuse = 0.7,
          reflection = 0.8,
          specular = 1
        ),
        Pigment(color=(random(),random(),random()))))
    textures.append(Texture(name))
  theta = 0.0
  dtheta = 2*pi/N
  R = 50
  r = 128
  LR = R+r
  LightSource((LR,LR,LR),(1,1,1)).write(file)
  LightSource((0,LR,LR),(1,1,1)).write(file)
  LightSource((LR,0,LR),(1,1,1)).write(file)
  LightSource((0,0,LR),(1,1,1)).write(file)
  LightSource((LR,0,0),(1,1,1)).write(file)
  mesh=Mesh()
  for i in range(N):
    X = (R*sin(theta),R*cos(theta),0)
    _R =R+random()*2*r-r
    Y = (_R*sin(theta),_R*cos(theta),random()*2*r-r)
    _R =R+random()*2*r-r
    Z = (_R*sin(theta),_R*cos(theta),random()*2*r-r)
    #A = [ x + random()*2*r - r for x in X ]
    A = [ x for x in X ]
    B = [ a + random()*2*r - r for a in A ]
    C = [ b + random()*2*r - r for b in B ]
    #mesh.append( Triangle(A,B,C,textures[i]) )
    mesh.append( Triangle(X,Y,Z,textures[i]) )
    theta+=dtheta
  mesh.append( 
    Texture(
      Finish(
        ambient = 0.2,
        diffuse = 0.7,
      ),
      Pigment(color=(0.9,0.9,0.9))
  ))
  mesh.write(file)

#
##############################################################
#

def test03():
  file=File()
  Camera(
    location=(N/2,N/2,-N),
    direction=(0,0,1),
    sky=(0,0,-1)
  ).write(file)
  LightSource((0,0,-256),(0,0.3,0)).write(file)
  LightSource((N,0,-256),(0.3,0,0)).write(file)
  LightSource((0,N,-256),(0,0,1)).write(file)
  LightSource((N,N,-256),(0.1,0.3,0)).write(file)
  mkmesh(file,h=3.0,N=32)

def mkmesh(file,theta=0.0,omega=6.0,h=3.0,N=192):
  file.declare( "water",
    Texture(
      Finish(
        ambient = 0.2,
        diffuse = 0.3,
        reflection = 0.8,
        specular = 0.3
      ), Pigment(color=(0.4,0.4,1))))
  def field(x,y,h=h):
    _x = (float(x)/N)-0.5
    _y = (float(y)/N)-0.5
    return h * sin( theta + omega*sqrt(_x*_x+_y*_y)*2*pi )
  mesh = Mesh(file=file) # write as we go
  for x in range(N):
    for y in range(N):
      A,B,C = ((x,y,field(x,y)),
        (x+1,y,field(x+1,y)),
        (x,y+1,field(x,y+1)))
      #mesh.append( Triangle(A,B,C,textures[(x,y)]) )
      mesh.append( Triangle(A,B,C,Texture("water")) )
      A,B,C = ((x+1,y+1,field(x+1,y+1)),
        (x+1,y,field(x+1,y)),
        (x,y+1,field(x,y+1)))
      mesh.append( Triangle(A,B,C,Texture("water")) )
  mesh.append( 
    Texture(
      Finish(
        ambient = 0.2,
        diffuse = 0.7,
      ),
      Pigment(color=(0.9,0.9,0.9))
  ))
  mesh.write(file)
  # much easier to use a height field!

#
##############################################################
#

def mkv(r):
  return Vector((random()-0.5)*r,(random()-0.5)*r,(random()-0.5)*r)

def mkortho(r):
  v1, v2 = mkv(r), mkv(r)
  #print v1,v2,v1.dot(v2)
  rv2 = v2.norm()
  # gram-schmidt 
  r = (v1/v1.norm()).dot(v2)
  #print r, v1, v2
  #print v2 - r*v1
  v2 -= r*(v1/v1.norm())
  #v2 *= rv2 / v2.norm() # restore norm
  #print v1,v2,v1.dot(v2)
  #print v1.norm(),v2.norm()
  assert abs(v1.dot(v2)) < 0.001 
  return v1,v2

def test10():
  " moving triangles "
  nframes = 256
  N = 16
  textures = []
  texture_file = File("textures.inc")
  for i in range(N):
    name = "t%s"%i
    texture_file.declare(
      name, Texture(
        Finish( ambient = 0.2, diffuse = 0.7, reflection = 0.8,
          specular = 1),
        Pigment(color=(random(),random(),random()))))
    textures.append(Texture(name))
  #cam = Camera(location=(20,20,-50),look_at=(50,50,50))
  cam = Camera(location=(20,20,-100),look_at=(0,0,0))
  #light = LightSource((50,50,-50),(1,1,1))
  light = LightSource((100,100,-100),(1,1,1))

  orthos = [ (mkortho(100),mkortho(100),mkortho(100))
    for i in range(N) ]
  thetas = [ random()*2*pi for i in range(N) ]
  dtheta = 2*pi / nframes
  for frame in range(nframes):
    file = File("tri/tri.%.2d.pov"%frame,"textures.inc",cam,light)
    mesh=Mesh()
    for i in range(N):
      theta = thetas[i]
      ortho = orthos[i]
      v1 = ortho[0][0]*sin(theta) + ortho[0][1]*cos(theta)
      v2 = ortho[1][0]*sin(theta) + ortho[1][1]*cos(theta)
      v3 = ortho[2][0]*sin(theta) + ortho[2][1]*cos(theta)
      mesh.append( Triangle(v1,v2,v3,textures[i]) )
      thetas[i] += dtheta
    mesh.append( 
      Texture(
        Finish(
          ambient = 0.2,
          diffuse = 0.7,
        ),
        Pigment(color=(0.9,0.9,0.9))
    ))
    mesh.write(file)

def test11():
  " fewly coloured triangles "
  file=File()
  Camera(location=(20,20,-50),look_at=(50,50,50)).write(file)
  LightSource((50,50,-50),(1,1,1)).write(file)
  textures = []
  for i in range(16):
    name = "t%s"%i
    file.declare(
      name, Texture(
        Finish(
          ambient = 0.2,
          diffuse = 0.7,
          reflection = 0.8,
          specular = 1
        ),
        Pigment(color=(random(),random(),random()))))
    textures.append(Texture(name))
  mesh=Mesh()
  for i in range(100):
    A = [ random()*100 for j in range(3) ]
    B = [ random()*100 for j in range(3) ]
    C = [ random()*100 for j in range(3) ]
    mesh.append( Triangle(A,B,C,textures[i%len(textures)]) )
  mesh.append( 
    Texture(
      Finish(
        ambient = 0.2,
        diffuse = 0.7,
      ),
      Pigment(color=(0.9,0.9,0.9))
  ))
  mesh.write(file)

def test12():
  " fewly normalized coloured triangles "
  file=File()
  Camera(location=(20,20,-50),look_at=(50,50,50)).write(file)
  LightSource((50,50,-50),(1,1,1)).write(file)
  textures = []
  def mkcol():
    c = (random(),random(),random())
    norm = sqrt( c[0]*c[0]+c[1]*c[1]+c[2]*c[2] )
    return c[0]/norm,c[1]/norm,c[2]/norm
  for i in range(16):
    name = "t%s"%i
    file.declare(
      name, Texture(
        Finish(
          ambient = 0.2,
          diffuse = 0.7,
          reflection = 0.8,
          specular = 1
        ),
        #Pigment(color=(random(),random(),random()))))
        Pigment(color=mkcol())))
    textures.append(Texture(name))
  mesh=Mesh()
  for i in range(100):
    A = [ random()*100 for j in range(3) ]
    B = [ random()*100 for j in range(3) ]
    C = [ random()*100 for j in range(3) ]
    mesh.append( Triangle(A,B,C,textures[i%len(textures)]) )
  mesh.append( 
    Texture(
      Finish(
        ambient = 0.2,
        diffuse = 0.7,
      ),
      Pigment(color=(0.9,0.9,0.9))
  ))
  mesh.write(file)

def test13():
  " r g or b coloured triangles "
  file=File("out.pov","metals.inc","textures.inc")
  Background( (0,0,0,0) )
  Camera(location=(20,20,-75),look_at=(50,50,50)).write(file)
  LightSource((50,50,-50),(1,1,1)).write(file)
  textures = []
  def mkcol():
    #return choice( [(1,0,0), (0,1,0), (0,0,1) ])
    return choice( [(1,0,0,0), (0,1,0,0), (0,0,1,0) ])
  #for i in range(16):
    #name = "t%s"%i
    #file.declare(
      #name, Texture(
        #Finish(
          #ambient = 0.2,
          #diffuse = 0.7,
          #reflection = 0.8,
          #specular = 1
        #),
        ##Pigment(color=(random(),random(),random()))))
        #Pigment(color=mkcol())))
    #textures.append(Texture(name))
  textures = []
  for i in range(16):
    name = "t%s"%i
    file.declare(
      name, Texture(
        Finish("F_MetalC"),
        Normal(bumps=0.1,scale=0.0002),
        #Pigment(color=(random(),random(),random()))))
        Pigment(color=mkcol())))
    textures.append(Texture(name))
  #file.declare( "metal",
    #Texture(
      #Normal(bumps=0.1,scale=0.0002),
      #Pigment(color=mkcol()),
      #Finish("F_MetalC"),
    #)
  #)
  #textures = [Texture("metal")]
  #textures = [
    #Texture("Brushed_Aluminum")
  #]
  mesh=Mesh()
  for i in range(10):
    A = [ random()*100 for j in range(3) ]
    B = [ random()*100 for j in range(3) ]
    C = [ random()*100 for j in range(3) ]
    mesh.append( Triangle(A,B,C,textures[i%len(textures)]) )
  mesh.append( 
    Texture(
      Finish(
        ambient = 0.2,
        diffuse = 0.7,
      ),
      Pigment(color=(0.9,0.9,0.9))
  ))
  mesh.write(file)

def test130():
  " blue coloured triangles "
  file=File("out.pov","metals.inc","textures.inc")
  Background( (0,0,0,0) )
  Camera(location=(20,20,-75),look_at=(50,50,50)).write(file)
  LightSource((50,50,-50),(1,1,1)).write(file)
  textures = []
  def mkcol():
    #return choice( [(1,0,0), (0,1,0), (0,0,1) ])
    #return choice( [(1,0,0,0), (0,1,0,0), (0,0,1,0) ])
    return (0.1*random(),0.1*random(),random())
  textures = []
  for i in range(16):
    name = "t%s"%i
    file.declare(
      name, Texture(
        Finish("F_MetalC"),
        Normal(bumps=0.1,scale=0.0002),
        #Pigment(color=(random(),random(),random()))))
        Pigment(color=mkcol())))
    textures.append(Texture(name))
  mesh=Mesh()
  for i in range(10):
    A = [ random()*100 for j in range(3) ]
    B = [ random()*100 for j in range(3) ]
    C = [ random()*100 for j in range(3) ]
    mesh.append( Triangle(A,B,C,textures[i%len(textures)]) )
  mesh.append( 
    Texture(
      Finish(
        ambient = 0.2,
        diffuse = 0.7,
      ),
      Pigment(color=(0.9,0.9,0.9))
  ))
  mesh.write(file)

def test14():
  " me coloured triangles "
  file=File()
  Camera(location=(20,20,-50),look_at=(50,50,50)).write(file)
  LightSource((50,50,-50),(1,1,1)).write(file)
  textures = []
  for i in range(100):
    name = "t%s"%i
    file.declare(
      name, Texture(
        Finish(
          ambient = 0.2,
          diffuse = 0.7,
          reflection = 0.8,
          specular = 1
        ),
        Pigment( color=(random(),random(),random()) )
      )
    )
    textures.append(Texture(name))
  mesh=Mesh()
  for i in range(100):
    A = [ random()*100 for j in range(3) ]
    B = [ random()*100 for j in range(3) ]
    C = [ random()*100 for j in range(3) ]
    #mesh.append( Triangle(A,B,C,textures[i]) )
    mesh.append( Triangle(A,B,C) )
  mesh.append( 
    Texture(
      Finish(
        ambient = 0.2,
        diffuse = 0.7,
      ),
      #Pigment(color=(0.9,0.9,0.9))
      Pigment(ImageMap("me.jpg"),scale=(100,100,100))
  ))
  mesh.write(file)

def bigger(v1,v2):
  if v1[0]>v2[0] and v1[1]>v2[1] and v1[2]>v2[2]:
    return True

def volume(v1,v2):
  assert bigger(v2,v1)
  return (v2[0]-v1[0])*(v2[1]-v1[1])*(v2[2]-v1[2])

def mkgrid(xs,ys,zs):
  grid = []
  for x in xs:
    for y in ys:
      for z in zs:
        grid.append( (x,y,z) )
  return grid

def mkpairs(grid):
  pairs = []
  pmap = {}
  for v in grid:
    pmap[v] = []
  for v1 in grid:
    for v2 in grid:
      if bigger(v2,v1):
        pmap[v1].append(v2)
  for v1 in grid:
    vs = pmap[v1]
    if vs:
      # find minimum v in vs
      mv = vs[0]
      for v2 in vs[1:]:
        if bigger(mv,v2):
          mv=v2
      pairs.append( (v1,mv) )
  return pairs

def mkbox(file):
  R = 36
  wR, hR, dR = R,R,R
  r = 4
  file.include("colors.inc","woods.inc")
  texture = Texture("T_Wood1",scale=16)
  grid = mkgrid(
    (-wR,-wR+r,wR-r,wR), (-hR,-hR+r,hR-r,hR), (-hR,-hR+r,0))
  pairs = mkpairs( grid )
  #Box( (-wR,-hR,-dR), (wR,hR,0),
    #texture, rotate = Vector(1,1,0)*45 ).write(file)
  maxi  = 0
  maxvol = volume(*pairs[maxi])
  for i in range(len(pairs)):
    if volume(*pairs[i]) > maxvol:
      maxvol = volume(*pairs[i])
      maxi = i
  pairs.pop(maxi)
  i = 1
  for v1,v2 in pairs:
    assert bigger(v2,v1)
    texture = Texture("T_Wood%d"%i,scale=16)
    i = i + 1
    Box( v1, v2,
      texture, rotate = Vector(1,0,0.1)*(-120) ).write(file)

def test15():
  " illuminating triangles "
  N = 0
  file=File()
  Camera(location=(0,0,-120),look_at=(0,0,0)).write(file)
  mkbox(file)
  LightSource((0,0,0),(1,1,1)).write(file)
  LightSource((-0,0,-92),(1,1,1)).write(file)
  Plane( (0,0,1), 512, 
    Texture(
      Finish(
        ambient = 0.2,
        diffuse = 0.2,
        reflection = 0.2,
        specular = 0.2
      ),
      Pigment( color=(0.1,0.1,0.1) )
    ),
    "hollow"
  ).write(file)
  textures = []
  for i in range(N):
    name = "t%s"%i
    file.declare(
      name, Texture(
        Finish(
          ambient = 0.2,
          diffuse = 0.7,
          reflection = 0.8,
          specular = 1
        ),
        Pigment( color=(random(),random(),random()) )
      )
    )
    textures.append(Texture(name))
  ts = []
  for i in range(N/2):
    A = ( randint(-32,32), randint(-32,32), randint(-32,0) )
    B = ( randint(-32,32), randint(-32,32), randint(-32,64) )
    C = ( randint(-32,32), randint(-32,32), randint(-32,64) )
    ts.append( Triangle(A,B,C,textures[i]) )
  for i in range(N/2):
    A = ( randint(-32,32), randint(-32,32), 0 )
    B = ( randint(-48,48), randint(-48,48), randint(0,64) )
    C = ( randint(-48,48), randint(-48,48), randint(0,64) )
    ts.append( Triangle(A,B,C,textures[i]) )
  if ts:
    mesh = Mesh( None, *ts )
    mesh.rotate = Vector(1,0,0.1)*(-120)
    mesh.write(file)

if __name__=="__main__":
  try:
    n = int(sys.argv[1])
  except:
    n = 20
  eval ("test%.2d()"%n)

