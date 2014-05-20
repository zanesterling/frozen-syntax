import world
import unit
import math

w = world.World(2)
u = unit.Unit(0, 0, 0, 1, .1)
w.addUnit(u, 0, 0)
u = unit.Unit(20, 0, math.pi, 1, .1)
w.addUnit(u, 1, 0)
w.go(0, 0, 20, 0)
w.go(0, 1, 0, 0) #we set units 0 and 1 on a collision course with one another
for i in xrange(200):
    w.runStep()
