import math
import random
timeStep=0.1
attractStrength=0
particleRadius=15
class mixparticle:
  def __init__(self, type, index, x, y, prevX, prevY, vx, vy, temp, polarity, mass):    
    self.type = type
    self.index=float(index)
    self.x=float(x)
    self.y=float(y)
    self.prevX=float(prevX)
    self.prevY=float(prevY)
    self.vx=float(vx)
    self.vy=float(vy)
    self.temp=float(temp)
    self.polarity=polarity
    self.mass=(mass)
  def newvelocity(self):
    theta= random.random()*2*math.pi
    magnitude= random.random()*self.temp
    self.vx=0.3*magnitude*math.cos(theta)+self.vx*0.8
    self.vy=0.3*magnitude*math.sin(theta)+self.vy*0.8
  def gpx(self):
    return self.prevX
  def gpy(self):
    return self.prevY
  def cpx(self):
    return self.x
  def cpy(self):
    return self.y
  def changepx(self, a):
    self.prevX=a
  def changepy(self, a):
    self.prevY=a

  def particleInteractions(self, otherParticles):
    
    #NOTE: Collision mechanics are not perfect yet because I am still learning how to solve the system of differential equations in 3 dimensional space.
    #NOTE: I will be imlementing more precise particle attraction and repulsion with the Lennard-Jones Potential.
    
    #print("For Particle Interactions"+str(otherParticles)+"\n")
    netForceX=0
    netForceY=0
    ForceX=0
    ForceY=0
    for j in range(len(otherParticles[0])):
      changePrevX=0
      changePrevY=0
      rad=otherParticles[2][j]
      thet=otherParticles[1][j]
      mag=math.sqrt(((self.x-self.prevX))**2+((self.y-self.prevY))**2)
      if(rad>0):
        if(rad<2*particleRadius):
          changePrevX=changePrevX+mag*(math.cos(thet))
          changePrevY=changePrevY+mag*(math.sin(thet))
          #print("Collision\n")
        else:
          ForceX= attractStrength*math.cos(thet)
          ForceY= attractStrength*math.sin(thet)

          #ForceX= attractStrength*math.cos(thet)/((rad))
          #ForceY= attractStrength*math.sin(thet)/((rad))
          if(otherParticles[0][j]==0 or self.polarity==0):
            ForceX=ForceX/10
            ForceY=ForceY/10
      netForceX=netForceX+ForceX
      netForceY=netForceY+ForceY
      #print("ForceX= "+str(netForceX)+"  ForceY= "+str(netForceY)+"\n\n")

      #update prevx and prevy to account for collisions
      if(changePrevY!=0 or changePrevX!=0):
        scaled=mag**2/(changePrevX**2+changePrevY**2)
        self.prevX=self.x+changePrevX/scaled
        # if(changePrevY!=self.y):
        self.prevY=self.y+changePrevY
    # netForceX=attractStrength*netForceX
    # netForceY=attractStrength*netForceY
    self.vx=0.7*self.vx+netForceX
    self.vy=0.7*self.vy+netForceY
    return((netForceX/self.mass, netForceY/self.mass))
      # theta= random.random()*2*math.pi
      # magnitude= random.random()*self.temp
      # netForceX+= magnitude*math.cos(theta)
      # netForceY+= magnitude*math.sin(theta)    
    
    # if(netForceX>15):
    #   netForceX=15
    # if(netForceY>15):
    #   netForceY=15
    # #print("Force:"+str(netForceX)+", "+str(netForceY)+"\n")

    # print(str(self.vx)+", "+str(self.vy)+"\n")
    # self.vx=10*math.sqrt(abs(netForceX/self.mass))*abs(netForceX)/netForceX
    # self.vy=10*math.sqrt(abs(netForceY/self.mass))*abs(netForceY)/netForceY
    
    #print(str(netForceX/self.mass)+""+str(netForceY/self.mass)+"\n")

  def getMass(self):
    return self.mass

  def newposition(self, accX, accY):
    #saving current Pos
    currentPosX=self.x
    currentPosY=self.y

    #implementing Velert Integration
    x=2*self.x-self.prevX+accX*timeStep**2
    y=2*self.y-self.prevY+accY*timeStep**2

    # update current pos to be old pos
    self.prevX=currentPosX
    self.prevY=currentPosY

    if(x<0):
      self.x= abs(x-self.x)-self.x
      self.prevX=self.x-abs(x-currentPosX)
    elif(x>500):
      self.x=500-((x-self.x)-(500-self.x))
      self.prevX=self.x+abs(x-currentPosX)
      #print("bounced right")
    else:
      self.x=x
    if(y<0):
      self.y= abs(y-self.y)-self.y
      self.prevY=self.y-abs(y-currentPosY)
    elif(y>500):
      self.y=500-((y-self.y)-(500-self.y))
      self.prevY=self.y+abs(y-currentPosY)
      #print("bounced top")
    else:
      self.y=y

    # error management
    if(self.y>=500):
      self.y=499.9999
    if(self.y<=0):
      self.y=0.0001
    if(self.x>=500):
      self.x=499.9999
    if(self.x<=0):
      self.x=0.0001

   

  def printing(self):
    print(str(self.x)+" "+str(self.y)+"\n")  
  def getpos(self):
    b=[]
    b.append(self.x)
    b.append(self.y)
    return b
  def gettype(self):
    return(self.type)
  def getPolarity(self):
    return(self.polarity)
  def getVelocity(self):
    return ([self.vx, self.vy])
