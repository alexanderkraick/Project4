from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.task import *
from panda3d.core import CollisionTraverser, CollisionHandlerPusher
from CollideObjectBase import PlacedObject

from panda3d.core import CollisionHandlerEvent
from direct.interval.LerpInterval import LerpFunc
from direct.particles.ParticleEffect import ParticleEffect
import re

import DefensePaths as defensePaths
import SpaceJamClasses as spaceJamClasses
import CollideObjectBase as CollideObjectBase
import math

def Player(self):
    
    self.cntExplode = 0
    self.explodeIntervals = {}

    self.traverser = traverser

    self.handler = CollisionHandlerEvent()
    
    self.handler.addInPattern('into')
    self.accept('into', self.HandleInto)
    
    self.traverser.addCollider(currentMissile.CollisionNode, self.handler)
    
def HandleInto(self, entry):
    fromNode = entry.getFromNodePath().getName()
    print("fromNode: " + fromNode)
    intoNode = entry.getIntoNodePath().getName()
    print("intoNode: " + intoNode)
    
    intoPosition = Vec3(entry.getSurfacePoint(self.render))
    
    tempVar = fromNode.split('_')
    shooter = tempVar[0]
    tempVar = intoNode.split[0]
    tempVar = intoNode.split[0]
    victim = tempVar[0]

    pattern = r'[0-9]'
    strippedString = re.sub(pattern, '', victim)
    if (strippedString == 'drone'):
        print(shooter + ' is DONE.')
        Missile.Intervals[shooter].finish()
        print(victim, ' hit at ', intoPosition)
        self.DroneDestroy(victim, intoPosition)
        
    else:
        Missile.Intervals[shooter].finish()
        
def DroneDestroy(self, hitID, hitPosition):
    nodeID = self.render.find(hitID)
    nodeID.detachNode()
    
    self.explodeNode.setPos(hitPosition)
    self.Explode(hitPosition)
    
def Explode(self, impactPoint):
    self.cntExplode += 1
    tag = 'particles-' + str(self.cntExplode)
    
    self.explodeIntervals[tag] = LerpFunc(self.ExplodeLight, fromData = 0, toData = 1, duration = 4.0, extraArgs = [impactPoint])
    self.explodeIntervals[tag].start()
    
def ExplodeLight(self, t, explosionPosition):
    if t == 1.0 and self.explodeEffect:
        self.explodeEffect.disable()
        
    elif t == 0:
        self.explodeEffect.start(self.explodeNode)
        
def SetParticles(self):
    base.enableParticles()
    self.explodeEffect = ParticleEffect()
    self.explodeEffect.loadConfig("./Assets/Part-fx/basic_xpld_efx.ptf")
    self.explodeEffect.setScale(20)
    self.explodeNode = self.render.attachNewNode('ExplosionEffects')
