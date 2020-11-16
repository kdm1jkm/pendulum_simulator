from elastic_pendulum import ElasticPendulum
from simple_pendulum import SimplePendulum


def main():
    b = True
    print("1: Simple Pendulum")
    print("2: Elastic Pendulum")
    sort: int = 0
    while b:
        sort = int(input("Enter>>"))
        b = sort not in [1, 2]
    if sort == 1:
        obj = SimplePendulum()
    elif sort == 2:
        obj = ElasticPendulum()
    print("1. Graph")
    print("2. Simulate")
    b = True
    while b:
        sort = int(input("Enter>>"))
        b = sort not in [1, 2]
    if sort == 1:
        obj.run_with_input()
    elif sort == 2:
        obj.simulate_with_input()


if __name__ == '__main__':
    main()
