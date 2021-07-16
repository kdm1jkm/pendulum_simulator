from simple_pendulum import SimplePendulum, get_extreme_value
import numpy as np
from tqdm import tqdm
import matplotlib.pylab as plt
import math
from datetime import datetime
import os

if __name__ == '__main__':
    obj = SimplePendulum()
    th = []
    t = []
    o_cha = []
    g = 2 * math.pi * math.sqrt(1 / 9.8)
    for i in tqdm(np.arange(0, 180, 0.1)):
        obj.length = 1
        obj.dt = 0.001
        obj.time = 0
        obj.mass = 0.5
        obj.radius = 0.1
        obj.viscosity = 0

        obj.theta = math.radians(i)
        obj.theta_dot = 0

        times, thetas = obj.process(15, False)

        # plt.plot(times, thetas)

        local_min, local_max = get_extreme_value(thetas, False)

        if len(local_min) != 0:
            th.append(i)
            t.append(times[local_min[0]] * 2)
            o_cha.append((times[local_min[0]] * 2 - g) / g)
            # o_cha.append((times[local_min[0]] * 2 - g) / g)

    date = datetime.today().strftime("%Y%m%d-%H%M%S")
    os.makedirs("result/" + date)

    with open("result/" + date + "/result.csv", "w") as f:
        for i in range(len(t)):
            f.write(str(th[i]))
            f.write(", ")
            f.write(str(t[i]))
            f.write(', ')
            f.write(str(o_cha[i]))
            f.write("\n")

    plt.plot(np.array(th), np.array(o_cha) * 100)
    plt.show()
