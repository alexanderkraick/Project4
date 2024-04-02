from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.task import *
from panda3d.core import CollisionTraverser, CollisionHandlerPusher
from CollideObjectBase import PlacedObject

import DefensePaths as defensePaths
import SpaceJamClasses as spaceJamClasses
import CollideObjectBase as CollideObjectBase
import math

class SpaceJam(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        # It's very important to get rid of code bloat as much as possible. We got rid of many lines in this script just by using classes.
        self.Universe = spaceJamClasses.Universe(self.loader, "./Assets/Universe/Universe.x", self.render, 'Universe', "Assets/Universe/Universe.jpg", (0, 0, 0), 10000)
        self.Planet1 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, 'Planet1', "./Assets/Planets/Planet1.jpg", (-6000, -3000, -800), 250)
        self.Planet2 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, 'Planet2', "./Assets/Planets/Planet2.jpg", (0, 6000, 0), 300)
        self.Planet3 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, 'Planet3', "./Assets/Planets/Planet3.jpg", (500, -5000, 200), 500)
        self.Planet4 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, 'Planet4', "./Assets/Planets/Planet4.jpg", (300, 6000, 500), 150)
        self.Planet5 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, 'Planet5', "./Assets/Planets/Planet5.jpg", (700, -2000, 100), 500)
        self.Planet6 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, 'Planet6', "./Assets/Planets/Planet6.jpg", (0, -900, -1400), 700)
        self.SpaceStation1 = spaceJamClasses.SpaceStation(self.loader, "./Assets/Space Station/spaceStation.egg", self.render, 'Space Station', "./Assets/Space Station/SpaceStation1_Dif2.png", (1500, 1000, -100), 40)
        self.Hero = spaceJamClasses.Spaceship(self.loader, self.taskMgr, self.render, "./Assets/Dumbledore/Dumbledore.egg", self.render, 'Hero', "./Assets/Dumbledore/spacejet_C.png", Vec3(1000, 1200, -50), 50)
        self.Sentinal1 = spaceJamClasses.Orbiter(self.loader, self.taskMgr, self.rootAssetFolder + "/DroneDefender/DroneDefender.obj", self.render, "Drone", 6.0, self.rootAssetFolder + "/DroneDefender/octoad1_auv.png", self.Planet5, 900, "MLB", self.Hero)
        self.Sentinal2 = spaceJamClasses.Orbiter(self.loader, self.taskMgr, self.rootAssetFolder + "/DroneDefender/DroneDefender.obj", self.render, "Drone", 6.0, self.rootAssetFolder + "/DroneDefender/octoad1_auv.png", self.Planet2, 500, "Cloud", self.Hero)

        self.SetCamera()

        fullCycle = 60

        for j in range(fullCycle):
            spaceJamClasses.Drone.droneCount += 1
            nickName = "Drone" + str(spaceJamClasses.Drone.droneCount)

            self.DrawCloudDefense(self.Planet1, nickName)
            self.DrawBaseballSeams(self.SpaceStation1, nickName, j, fullCycle, 2)
            
        self.DrawCircleXYDefense()
        self.DrawCircleXZDefense()
        self.DrawCircleYZDefense()
        
        self.cTrav = CollisionTraverser()
        self.cTrav.traverse(self.render)
        self.pusher = CollisionHandlerPusher()
        self.pusher.addCollider(self.Hero.collisionNode, self.Hero.modelNode)
        self.cTrav.addCollider(self.Hero.collisionNode, self.pusher)
        self.cTrav.showCollisions(self.render)

    def DrawCircleXYDefense(self):
        self.parent = self.loader.loadModel('./Assets/DroneDefender/DroneDefender.obj')
        self.parent.setScale(0.25)
        a = 0.0
        aInc = 0.2
        R = 50.0

        for i in range(30):
            posVec = (R * math.cos(a), R * math.sin(a), 0)
            self.placeholder = self.render.attachNewNode("Placeholder")
            self.placeholder.setPos(posVec)
            self.placeholder.setColor(255, 0, 0, 1)
            self.parent.instanceTo(self.placeholder)
            a += aInc

    def DrawCircleXZDefense(self):
        self.parent = self.loader.loadModel('./Assets/DroneDefender/DroneDefender.obj')
        self.parent.setScale(0.25)
        a = 0.0
        aInc = 0.2
        R = 50.0

        for i in range(30):
            posVec = (R * math.cos(a), 0, R * math.sin(a))
            self.placeholder = self.render.attachNewNode("Placeholder")
            self.placeholder.setPos(posVec)
            self.placeholder.setColor(0, 255, 0, 1)
            self.parent.instanceTo(self.placeholder)
            a += aInc

    def DrawCircleYZDefense(self):
        self.parent = self.loader.loadModel('./Assets/DroneDefender/DroneDefender.obj')
        self.parent.setScale(0.25)
        a = 0.0
        aInc = 0.2
        R = 50.0

        for i in range(30):
            posVec = (0, R * math.cos(a), R * math.sin(a))
            self.placeholder = self.render.attachNewNode("Placeholder")
            self.placeholder.setPos(posVec)
            self.placeholder.setColor(0, 0, 255, 1)
            self.parent.instanceTo(self.placeholder)
            a += aInc 
             
    def DrawBaseballSeams(self, centralObject, droneName, step, numSeams, radius = 1):
            unitVec = defensePaths.BaseballSeams(step, numSeams, B = 0.4)
            unitVec.normalize()
            position = unitVec * radius * 250 + centralObject.modelNode.getPos()
            spaceJamClasses.Drone(self.loader, "./Assets/DroneDefender/DroneDefender.obj", self.render, droneName, "./Assets/DroneDefender/octotoad1_auv.png", position, 5)

    def DrawCloudDefense(self, centralObject, droneName):
        unitVec = defensePaths.Cloud()
        unitVec.normalize()
        position = unitVec * 500 + centralObject.modelNode.getPos()
        spaceJamClasses.Drone(self.loader, "./Assets/DroneDefender/DroneDefender.obj", self.render, droneName, "./Assets/DroneDefender/octotoad1_auv.png", position, 10)

    def SetCamera(self):
        self.disableMouse()
        self.camera.reparentTo(self.Hero.modelNode)
        self.camera.setFluidPos(0, 1, 0)

app = SpaceJam()
app.run()
