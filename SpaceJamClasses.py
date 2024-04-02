from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.task import Task
from panda3d.core import Vec3
from CollideObjectBase import *
from SpaceJamClasses import Missile
from direct.gui.OnscreenImage import OnscreenImage
from direct.task.Task import TaskManager
import DefensePaths as defensePaths

class Planet(SphereCollideObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

class Universe(InverseSphereCollideObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(Universe, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 0.9)
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

class Drone(SphereCollideObject):
    # Variable we use to keep track of how many drones have been spawned.
    droneCount = 0

    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

class SpaceStation(CapsuleCollidableObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(SpaceStation, self).__init__(loader, modelPath, parentNode, nodeName, 1, -1, 5, 1, -1, -5, 10)
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

class Spaceship(SphereCollideObject):
    def __init__(self, loader: Loader, manager: Task, render: NodePath, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(Spaceship, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 0.9)
        self.taskManager = manager
        self.render = render
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)
        self.taskMgr.add(self.CheckIntervals, 'checkMissiles', 34)

        self.SetKeyBindings()

    def SetKeyBindings(self):
        # All of our key bindings for our spaceship's movement.
        self.accept('space', self.Thrust, [1])
        self.accept('space-up', self.Thrust, [0])
        self.accept('arrow_left', self.LeftTurn, [1])
        self.accept('arrow_left-up', self.LeftTurn, [0])
        self.accept('arrow_right', self.RightTurn, [1])
        self.accept('arrow_right-up', self.RightTurn, [0])
        self.accept('arrow_up', self.PitchBack, [1])
        self.accept('arrow_up-up', self.PitchBack, [0])
        self.accept('arrow_down', self.PitchForward, [1])
        self.accept('arrow_down-up', self.PitchForward, [0])
        self.accept('q', self.RollLeft, [1])
        self.accept('q-up', self.RollLeft, [0])
        self.accept('e', self.RollRight, [1])
        self.accept('e-up', self.RollRight, [0])
        self.accept('f', self.Fire)


    def Thrust(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyThrust, 'forward-thrust')

        else:
            self.taskManager.remove('forward-thrust')

    def ApplyThrust(self, task):
        rate = 5
        # getRelativeVector is from our render library.
        # Vec3.forward() gets the forward-facing direction of our modelNode.
        trajectory = self.render.getRelativeVector(self.modelNode, Vec3.forward())
        # If you are going to manipulate a vector, always normalize it first so the length of the vector is 1.
        trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * rate)
        return Task.cont

    def LeftTurn(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyLeftTurn, 'left-turn')

        else:
            self.taskManager.remove('left-turn')

    def ApplyLeftTurn(self, task):
        # Half a degree every frame.
        rate = .5
        self.modelNode.setH(self.modelNode.getH() + rate)
        return Task.cont

    def RightTurn(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyRightTurn, 'right-turn')

        else:
            self.taskManager.remove('right-turn')

    def ApplyRightTurn(self, task):
        # Half a degree every frame.
        rate = .5
        self.modelNode.setH(self.modelNode.getH() - rate)
        return Task.cont
    
    def PitchForward(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyPitchForward, 'pitch-forward')

        else:
            self.taskManager.remove('pitch-forward')

    def ApplyPitchForward(self, task):
        rate = .5
        self.modelNode.setP(self.modelNode.getP() + rate)
        return Task.cont

    def PitchBack(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyPitchBackward, 'pitch-backward')

        else:
            self.taskManager.remove('pitch-backward')

    def ApplyPitchBackward(self, task):
        rate = .5
        self.modelNode.setP(self.modelNode.getP() - rate)
        return Task.cont
    
    def RollLeft(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyRollLeft, 'roll-left')

        else:
            self.taskManager.remove('roll-left')

    def ApplyRollLeft(self, task):
        rate = .5
        self.modelNode.setR(self.modelNode.getR() - rate)
        return Task.cont
    
    def RollRight(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyRollRight, 'roll-right')

        else:
            self.taskManager.remove('roll-right')

    def ApplyRollRight(self, task):
        rate = .5
        self.modelNode.setR(self.modelNode.getR() + rate)
        return Task.cont
    
class Missile(SphereCollideObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)
    
        self.reloadTime = .25
        self.missileDistance = 4000 # Until the missile explodes
        self.missileBay = 1 # Only one missile in the missile bay to be launched.
        
    def Fire(self):
        if self.missileBay:
            travRate = self.missileDistance
            aim = self.render.getRelativeVector(self.modelNode, Vec3.forward()) # The direction the spaceship is facing.
            # Normalizing a vector makes it consistant all the time.
            aim.normalize()
            fireSolution = aim * travRate
            inFront = aim * 150
            travVec = fireSolution + self.modelNode.getPos()
            self.missileBay -= 1
            tag = 'missile' + str(Missile.missileCount)
            posVec = self.modelNode.getPos() + inFront # Spawn the missile in front of te nose of the ship
            # Create our missile
            currentMissile = Missile(self.loader, './Assets/Phaser/phaser.egg', self.render, tag, posVec, 4.0)
            fireModels = {}
            cNodes = {}
            collisionSolids = {}
            Intervals = {}
            missileCount = 0
            Missile.Intervals[tag] = currentMissile.modelName.posInterval(2.0, travVec, startPos = posVec, fluid = 1)
            Missile.Intervals[tag].start()
        else:
            # If we aren't reloading, we want to start reloading.
            if not self.taskMgr.hasTaskNamed('reload'):
                print('Initializing reload...')
                # Call the reload method on no delay.
                self.taskmgr.doMethodLater(0, self.Reload, 'reload')
                return Task.cont
            
    def Reload(self, task):
        if task.time > self.reloadTime:
            self.missileBay += 1
            if self.missileBay > 1:
                self.missileBay = 1
                print("Reload complete.")
                return Task.done
            elif task.time <= self.reloadTime:
                print("Reload proceeding...")
                return Task.cont
            
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, posVec: Vec3, scaleVec: float = 1.0):
        super(Missile, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 3.0)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setPos(posVec)
        Missile.missileCount += 1
        Missile.fireModels[nodeName] = self.modelNode
        Missile.cNodes[nodeName] = self.collisionNode
        # We retrieve the solid for our collisionNode
        Missile.collisionSolids[nodeName] = self.collisionNode.node().getSolid(0)
        Missile.cNodes[nodeName].show()
        print("Fire torpedo #" + str(Missile.missileCount))
        
    def CheckIntervals(self, task):
        for i in Missile.Intervals:
            if not Missile.Intervals[i].isPlaying():
                Missile.cNodes[i].detachNode()
                Missile.fireModels[i].detachNode()
                del Missile.Intervals[i]
                del Missile.fireModels[i]
                del Missile.cNodes[i]
                del Missile.collisionSolids[i]
                print(i + ' had reached the end of its fire solution.')
                break
        return Task.cont
    
    def EnableHUD(self):
        self.Hud = OnscreenImage(image = "./Assets/Hud/ReticleIV.png", pos = Vec3(0, 0, 0), scale = 0.1)
        self.Hud.SetTransparency(TransparencyAttrib.MAlpha)
        self.EnableHUB()
        
class Orbiter(SphereCollideObject):
    numOrbits = 0
    velocity = 0.005
    cloudTimer = 240
    
    def __init__(self, loader: Loader, taskMgr: TaskManager, modelPath: str, parentNode: NodePath, nodeName: str, scaleVec: Vec3, texPath: str, centralObject: PlacedObject, orbitRadius: float, orbitType: str, staringAt: Vec3):
        super(Orbiter, self,).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 3.2)
        self.taskMgr = taskMgr
        self.OrbitType = orbitType
        self.modelNode.setScale(scaleVec)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)
        self.orbitObject = centralObject
        self.orbitRadius = orbitRadius
        self.staringAt = staringAt
        Orbiter.numOrbits += 1
        
        self.cloudClock = 0
        
        self.taskFlag = "Traveler-" + str(Orbiter.numOrbits)
        taskMgr.add(self.Orbit, self.taskFlag)
        
    def Orbit(self, task):
        if self.orbitType == "MLB":
            positionVec = defensePaths.BaseballSeams(task.time * Orbiter.velocity, self.numOrbits, 2.0)
            self.modelNode.setPos(positionVec * self.orbitRadius + self.orbitObject.modelNode.getPos())
            
        elif self.orbitType == "cloud":
            if self.cloudClock < Orbiter.cloudTimer:
                self.cloudClock += 1
                
            else:
                self.cloudClock = 0
                positionVec = defensePaths.Cloud()
                self.modelNode.setPos(positionVec * self.orbitRadius + self.orbitObject.modelNode.getPos())
                
        self.modelNode.lookAt(self.staringAt.modelNode)
        return task.cont
