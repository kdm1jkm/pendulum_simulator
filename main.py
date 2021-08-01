from elastic_pendulum import ElasticPendulum
from simple_pendulum import SimplePendulum
from double_pendulum import DoublePendulum
from PendulumSimulator import PendulumSimulator


def main():
    print("1: Simple Pendulum")
    print("2: Elastic Pendulum")
    print("3: Double Pendulum")
    sort = None
    while sort not in ["1", "2", "3"]:
        sort = input("Enter>>")

    if sort == "1":
        obj = SimplePendulum()
    elif sort == "2":
        obj = ElasticPendulum()
    elif sort == "3":
        obj = DoublePendulum()

    print("1. Graph")
    print("2. Simulate")
    sort = None
    while sort not in ["1", "2"]:
        sort = input("Enter>>")
    if sort == "1":
        obj.run_with_input()
    elif sort == "2":
        obj.simulate_with_input()


if __name__ == '__main__':
    main()
