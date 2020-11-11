from vpython import *


g = 9.8


def main():
    dt = float(input("Enter dt>>"))
    r = int(1/dt)
    print(r)

    thetas = []
    lengths = []

    with open("elastic.txt") as f:
        for l in f.readlines():
            a = l.split("\t")
            thetas.append(float(a[1]))
            lengths.append(float(a[2]))

    l = lengths[0]

    # display(width=600, height=600, center=vector(0, 12, 0), background=color.white)
    scene.width = scene.height = 600
    scene.center = vector(0, 12, 0)

    bob = sphere(pos=vector(5, 40, 0), radius=l/10, color=color.blue)
    pivot = vector(0, 20, 0)
    rod = cylinder(pos=pivot, axis=bob.pos-pivot, radius=l/200, color=color.red)

    for i in range(len(thetas)):
        rate(r)
        bob.pos = vector(lengths[i]*sin(thetas[i]), pivot.y -
                         lengths[i]*cos(thetas[i]),  0)  # calculating position
        rod.axis = bob.pos-rod.pos  # updating other end of rod of pendulum'


main()
