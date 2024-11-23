#NOTE: equations used are simplifications of true equations. They still convey the general principles underlying particle dynamics
#be cool to add a temperature gradient and have heat transfer with this

#Furthermore, units are arbitrary, as the simulation is not precise enough for units to be sensical. The simulation is intended to demonstrate the fact that certain macroscopic properties emerge from fundamental mechanical principles. not to perfectly follow reality (no simulation perfectly follows reality, but they are still useful).

import math
import random
import time
from mixingparticle import*
import pygame
import numpy as np

polA=0
massA=0
polB=0
massB=0
Aparticles=[]
Bparticles=[]
temp=10
numpartA= 150
numpartB= 150
Gravity=10
title = ""
currentTime=0 
#default 10 by 10 grid
gridLength=50
if(2*particleRadius>gridLength):
  gridLength=2*particleRadius
gridSize=math.ceil(500/gridLength)

type= int(input("Enter 1 for polar-polar with equal density. Enter 2 for polar-polar with greater density at bottom. Enter 3 for Nonpolar-Polar with equal density\n"))
if (type==1):
  polA=1
  polB=1
  massA=1
  massB=1
  title= "polar-polar with equal density"
if(type==2):
  polA=1
  polB=1
  massA=1
  massB=5
  title= "polar-polar with greater density at bottom"
if(type==3 or type==4):
  polA=0
  polB=1
  massA=1
  massB=1
  title = "Nonpolar-Polar with equal density"
if(type==4):
  title= "Evaporation "
for i in range(numpartA):
  xRand=random.random()*500
  yRand=random.random()*250
  Aparticles.append(mixparticle("A", i, xRand, yRand, xRand+(2*random.random()-1)*temp, yRand+(2*random.random()-1)*temp, float(temp)*(random.random()-0.5), float(temp)*(random.random()-0.5),temp, polA, massA))

for i in range(numpartB):
  xRand=random.random()*500
  yRand=250+random.random()*250
  Bparticles.append(mixparticle("B", i, xRand, yRand, xRand+(2*random.random()-1)*temp, yRand+(2*random.random()-1)*temp, float(temp)*(random.random()-0.5), float(temp)*(random.random()-0.5),temp, polB, massB))
#initial kinetic energy
kineticEnergy=0
for particle in Bparticles:
  kineticEnergy+=0.5*particle.getMass()*((particle.gpx()-particle.cpx())**2+(particle.gpy()-particle.cpy())**2)
for particle in Aparticles:
  kineticEnergy+=0.5*particle.getMass()*((particle.gpx()-particle.cpx())**2+(particle.gpy()-particle.cpy())**2)
kineticEnergy=numpartA*(temp+10*attractStrength+Gravity*50)

def grouping(particleSet1):
  
  sizing = np.zeros((gridSize,gridSize))
  max=0
  for i in range(len(particleSet1)):
    x=math.floor((particleSet1[i].getpos()[0])/gridLength)
    y=math.floor((particleSet1[i].getpos()[1])/gridLength)

    # if(x>19 or x<-19):
    #   blah=particleSet2[i].getVelocity()
    #   print("xbounds. x="+str(x)+" xVel:"+str(blah[0])+" yVel:"+str(blah[1])+" xPos:"+str(particleSet2[i].getpos()[0])+" yPos:"+str(particleSet2[i].getpos()[1]))
    # if(y>19 or y<-19):
    #   blah=particleSet2[i].getVelocity()
    #   print("ybounds. y="+str(y)+ " xVel:"+str(blah[0])+" yVel:"+str(blah[1])+" xPos:"+str(particleSet2[i].getpos()[0])+" yPos:"+str(particleSet2[i].getpos()[1]))

    sizing[x][y]=sizing[x][y]+1

# Unecessary because using only one particle set
  # for i in range(len(particleSet2)):
  #   x=math.floor((particleSet2[i].getpos()[0])/25)
  #   y=math.floor((particleSet2[i].getpos()[1])/25)

    # if(x>19 or x<-19):
    #   blah=particleSet2[i].getVelocity()
    #   print("x bounds. x="+str(x)+" xVel:"+str(blah[0])+" yVel:"+str(blah[1])+" xPos:"+str(particleSet2[i].getpos()[0])+" yPos:"+str(particleSet2[i].getpos()[1]))
    # if(y>19 or y<-19):
    #   blah=particleSet2[i].getVelocity()
    #   print("y bounds. y="+str(y)+"xVel:"+str(blah[0])+" yVel:"+str(blah[1])+" xPos:"+str(particleSet2[i].getpos()[0])+" yPos:"+str(particleSet2[i].getpos()[1]))


  for i in range(gridSize):
    for j in range(gridSize):
      if(sizing[i][j]>max):
        max=sizing[i][j]

  tensor = np.zeros((gridSize, gridSize, int(max)), dtype=object)
  counter = np.zeros((gridSize,gridSize))
  for i in range(len(particleSet1)):
    x=math.floor(particleSet1[i].getpos()[0]/gridLength)
    y=math.floor(particleSet1[i].getpos()[1]/gridLength)
    z=int(counter[x][y])
    tensor[x][y][z]=particleSet1[i]
    counter[x][y]=counter[x][y]+1

# uneccesary because only one particle set
  # for i in range(len(particleSet2)):
  #   x=math.floor(particleSet2[i].getpos()[0]/25)
  #   y=math.floor(particleSet2[i].getpos()[1]/25)
  #   z=int(counter[x][y])
  #   tensor[x][y][z]=particleSet2[i]
  #   counter[x][y]=counter[x][y]+1
  return tensor
  

def findNeighbors(particle, particleSet):
   #print("For Find Neighbors"+str(particleSet)+"\n")
   Position= particle.getpos()
   x = Position[0]
   y = Position[1]
   polar=[]
   thetaSet=[]
   radiusSet=[]
   for i in range(len(particleSet[0])):
      do=False
      #print("Particle Set of i is: "+str(particleSet[0])+"\n")
      #print("Particle Set of i is: "+str(particleSet[0][i])+"\n")
        
      try:
        otherPart = particleSet[0][i].getpos()
        xdiff= otherPart[0]-x
        ydiff= otherPart[1]-y
        radius = math.sqrt(xdiff**2+ydiff**2)
        if(radius<gridLength or radius<2*particleRadius):
          if(xdiff!=0):
            theta=math.atan(ydiff/xdiff)
          else:
            theta=3.14159/2
            if(ydiff<0):
              theta=-3.14159/2
          if(xdiff<0):
            theta=theta+math.pi

          polar.append(particleSet[0][i].getPolarity())
          thetaSet.append(theta)
          radiusSet.append(radius)
          do=True
      except:
        if(do==False):
          polar.append(-1)
          thetaSet.append(-1)
          radiusSet.append(-1)
   # unknown bug correction- every once in a while polar has an extra -1 at index 1
   while(len(polar)>len(thetaSet)):
     del polar[1]       
            
   returnMat=[polar,thetaSet, radiusSet]
   #print("Radii"+ str(radiusSet))
   #print("returnMat:" + str(returnMat))
   return returnMat

pygame.init()
clock = pygame.time.Clock()
pause = False

#Screen
screen_width=500
screen_height=500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(title)
time=0
keepRunning=True
pause= False
while keepRunning:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      keepRunning = False
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_p:  # Press 'P' to toggle pause
        pause = not pause
     
  if (not pause):    
    # Set up fonts
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 15)
    time=time+1
    # Render text
    text_surface = font.render(title+" Time="+str(time)+", Temp= "+str(math.floor(temp)), True, (255, 255, 255))
    time=time+1

    #Clear Screen
    screen.fill((0,0,0))
    
    #check for updating
    #print("Updating")
    
    # Grouping Particles
    bothParticles=Bparticles
    if(type!=4):
      bothParticles.extend(Aparticles)
    groupsTensor= grouping(bothParticles)
    
    XaccB=0
    XaccA=0
    YaccB=0
    YaccA=0
    for i in range(numpartA):
        if(type!=4):
          b=Aparticles[i].getpos()
          x=b[0]
          y=b[1]
          Color1= pygame.Color(0,0,100)
          pos=(x,y)
          pygame.draw.circle(screen, Color1,pos, particleRadius)
          # Aparticles[i].newvelocity()
          e= math.floor(((Aparticles[i].getpos())[0])/gridLength)
          #print(str(e))
          f= math.floor(((Aparticles[i].getpos())[1])/gridLength)
          #print(str(f))
          foundNeighbors=[groupsTensor[e,f,:]] 
          # for i in range(3):
          #   for j in range(3):
          #     i1 = i -1
          #     j1 = j -1
          #     if(e+i1>-1 and e+i1<20 and f+j1>-1 and f+j1<20):
          #       foundNeighbors.append( groupsTensor[e+i1, f+j1, :])
          interactionsMat=findNeighbors(Aparticles[i], foundNeighbors)
          forces=Aparticles[i].particleInteractions(interactionsMat)
          XaccA=forces[0]/Aparticles[i].getMass()
          YaccA=forces[1]/Aparticles[i].getMass()
          #pygame.draw.line(screen,Color1,pos,(int(math.floor(pos[0]+forces[0])), int(math.floor(pos[1]+forces[1]))),width=1 )
          


        b=Bparticles[i].getpos()
        x=b[0]
        y=b[1]
        pos=(x,y)
        Color1= pygame.Color(100,0,0)
        # Bparticles[i].newvelocity()
        x= math.floor(Bparticles[i].getpos()[0]/gridLength)
        y= math.floor(Bparticles[i].getpos()[1]/gridLength)
        foundNeighbors=[groupsTensor[x,y,:]] 
        # for i in range(3):
        #   for j in range(3):
        #     i1 = i -1
        #     j1 = j -1
        #     if(x+i1>-1 and x+i1<20 and y+j1>-1 and y+j1<20):
        #       foundNeighbors.append( groupsTensor[x+i1, y+j1, :])
        interactionsMat=findNeighbors(Bparticles[i], foundNeighbors)
        forces=Bparticles[i].particleInteractions(interactionsMat)
        XaccB=forces[0]/Bparticles[i].getMass()
        YaccB=forces[1]/Bparticles[i].getMass()
        if(False):
          endx=int(pos[0]+20*(Xacc))
          endy=int(pos[1]+20*(Yacc))
          pygame.draw.line(screen,Color1,pos,(endx,endy),width=3 )
          width=2
          pygame.draw.polygon(screen, "white", [[endx-width, endy], [endx+width, endy], [endx, endy+width]], 5)
        pygame.draw.circle(screen, Color1,pos, particleRadius)
    for i in range(numpartA):
      if(type!=4):
        Aparticles[i].newposition(XaccA,YaccA+Gravity)
      Bparticles[i].newposition(XaccB,YaccB+Gravity)
    
    
    #modify velocities so kinetic energy stays constant
    CkineticEnergy=0
    for particle in Bparticles:
      CkineticEnergy+=0.5*particle.getMass()*((particle.gpx()-particle.cpx())**2+(particle.gpy()-particle.cpy())**2)
    for particle in Aparticles:
      CkineticEnergy+=0.5*particle.getMass()*((particle.gpx()-particle.cpx())**2+(particle.gpy()-particle.cpy())**2)
    numactivepart=numpartB
    if(type!=4):
      numactivepart+=numpartA
    temp=CkineticEnergy/(numactivepart)

    #For some reason particle energy is increasing over time even though verlet integration generally prevents this from happening
    # Trying to utilize this to scale down particle velocity, but there is currently a bug.
    if(False):
      for particle in Bparticles:
        xdiff=particle.gpx()-particle.cpx()
        ydiff=particle.gpy()-particle.cpy()
        radius=math.sqrt((xdiff)**2+(ydiff)**2)
        thetadiff=math.pi/2
        if(ydiff<0):
          thetadiff=-thetadiff
        if(xdiff!=0):
          thetadiff= math.atan((ydiff)/(xdiff))
        if(xdiff<0):
          thetadiff+=math.pi
        newpx=particle.cpx()+radius*math.sqrt(kineticEnergy/CkineticEnergy)*math.cos(thetadiff)
        print("x:kin="+str(kineticEnergy)+"kin/Ckin= "+str(kineticEnergy/CkineticEnergy)+" Curren: "+str(particle.cpx())+"Old Past: " +str(particle.gpx())+"\n"+". New Past: "+str(newpx)+"\n\n")
        particle.changepx(newpx)
        newpy=particle.cpy()+radius*math.sqrt(kineticEnergy/CkineticEnergy)*math.sin(thetadiff)
        print("y:kin="+str(kineticEnergy)+"kin/Ckin= "+str(kineticEnergy/CkineticEnergy)+" Curren: "+str(particle.cpy())+"Old Past: " +str(particle.gpy())+"\n"+". New Past: "+str(newpy)+"\n\n")
        particle.changepx(newpy)
      for particle in Aparticles:
        xdiff=particle.gpx()-particle.cpx()
        ydiff=particle.gpy()-particle.cpy()
        radius=math.sqrt((xdiff)**2+(ydiff)**2)
        thetadiff=math.pi/2
        if(ydiff<0):
          thetadiff=-thetadiff
        if(xdiff!=0):
          thetadiff= math.atan((ydiff)/(xdiff))
        if(xdiff<0):
          thetadiff+=math.pi
        newpx=particle.cpx()+radius*math.sqrt(CkineticEnergy/CkineticEnergy)*math.cos(thetadiff)
        print("radius: "+str(radius)+"thetadiff: " +str(thetadiff)+"x:kin="+str(kineticEnergy)+"kin/Ckin= "+str(kineticEnergy/CkineticEnergy)+" Curren: "+str(particle.cpx())+"Old Past: " +str(particle.gpx())+"\n"+". New Past: "+str(newpx)+"\n\n")
        particle.changepx(newpx)
        newpy=particle.cpy()+radius*math.sqrt(CkineticEnergy/CkineticEnergy)*math.sin(thetadiff)
        print("radius: "+str(radius)+"thetadiff: "+str(thetadiff)+"y:kin="+str(kineticEnergy)+"kin/Ckin= "+str(kineticEnergy/CkineticEnergy)+" Curren: "+str(particle.cpy())+"Old Past: " +str(particle.gpy())+"\n"+". New Past: "+str(newpy)+"\n\n")
        particle.changepx(newpy) 
        #Bparticles[i].effectOfGravity()
    
        
    # for i in range(numpartA):
    #     Bparticles[i].newposition()
    #     Aparticles[i].newposition()
    # Blit the text surface onto the screen
    screen.blit(text_surface, (10, 10))
    if(False):
      for i in range(25):
        textThing = font.render(str(i*20), True, (255, 255, 255))
        screen.blit(textThing, (10,i*20))
    currentTime=currentTime+1
    pygame.display.flip()
    clock.tick(100)
    # while(True):
#   win= GraphWin("Diffusion",500,500)
#   for i in range(numpartA):
#       b=Aparticles[i].getpos()
#       pt=Point(b[0], b[1])
#       cir=Circle(pt, 5)
#       cir.setFill("red")
#       cir.draw(win)
#       Aparticles[i].newvelocity()
#       Aparticles[i].newposition()
 
#       b=Bparticles[i].getpos()
#       pt=Point(b[0], b[1])
#       cir=Circle(pt, 5)
#       cir.setFill("blue")
#       cir.draw(win)
#       Bparticles[i].newvelocity()
#       Bparticles[i].newposition()
#   win.getMouse()  
#   win.close()
