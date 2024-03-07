from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.task import Task
from panda3d.core import Vec3

class Planet(ShowBase):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

class Universe(ShowBase):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

class Drone(ShowBase):
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

class SpaceStation(ShowBase):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

class Spaceship(ShowBase):
    def __init__(self, loader: Loader, manager: Task, render: NodePath, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        self.taskManager = manager
        self.render = render
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

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