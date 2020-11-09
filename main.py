from vpython import *

# display(width=600, height=600, center=vector(0, 12, 0), background=color.white)
scene.width = scene.height = 600

data = []
last = 0
dt = 0
i = 0

with open("result.txt", "r") as f:
    for l in f.readlines():
        a = l.split("\t")
        if a[0] == "time":
            continue
        data.append(float(a[1]))
        dt = float(a[0]) - last
        last = float(a[0])

bob = sphere(pos=vector(5, 40, 0), radius=0.5, color=color.blue)
pivot = vector(0, 20, 0)
rod = cylinder(pos=pivot, axis=bob.pos-pivot, radius=0.1, color=color.red)
t = 0  # time
l = mag(bob.pos-pivot)  # length of pendulum
cs = (pivot.y-bob.pos.y)/l  # calculation of cos(theta)
theta = acos(cs)  # angle with vertical direction
for d in data:
    rate(int(1/dt))
    theta = radians(d)  # updating of angular position
    bob.pos = vector(l*sin(theta), pivot.y-l*cos(theta),
                     0)  # calculating position
    rod.axis = bob.pos-rod.pos  # updating other end of rod of pendulum
