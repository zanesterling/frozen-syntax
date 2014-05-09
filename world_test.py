import world
import unit

w = world.World(2)
u = unit.Unit(0, 0, 0, 1, 1)
w.addUnit(u, 0, 0)
w.go(0, 0, 1, 2)
w.runStep()
