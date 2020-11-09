from vpython import *


g = 9.8


def main():
    length = float(input("Enter length>>"))
    theta = float(input("Enter theta>>"))
    theta_dot = float(input("Enter theta_dot>>"))
    dt = float(input("Enter dt>>"))
    radius = float(input("Enter radius>>"))
    viscosity = float(input("Enter viscosity>>"))
    mu = 6 * pi * viscosity * radius

    # display(width=600, height=600, center=vector(0, 12, 0), background=color.white)
    scene.width = scene.height = 600
    scene.center = vector(0, 12, 0)

    bob = sphere(pos=vector(5, 40, 0), radius=radius*10, color=color.blue)
    pivot = vector(0, 20, 0)
    rod = cylinder(pos=pivot, axis=bob.pos-pivot, radius=0.1, color=color.red)

    time = 0

    while(True):
        theta_double_dot = -g/length*sin(radians(theta)) - mu*theta_dot*dt
        theta_dot += theta_double_dot*dt
        theta += theta_dot*dt

        rate(int(1/dt))
        bob.pos = vector(length*10*sin(radians(theta)), pivot.y-length*10*cos(radians(theta)),
                         0)  # calculating position
        rod.axis = bob.pos-rod.pos  # updating other end of rod of pendulum'

        time += dt


main()
