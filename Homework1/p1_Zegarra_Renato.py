import math
import matplotlib.pyplot as plt


def main():
    while True:
        a_input = input("Enter a: ")

        if a_input == "":
            break

        a = float(a_input)
        b = float(input("Enter b: "))
        c = float(input("Enter c: "))

        d = b ** 2 - 4 * a * c

        if d < 0:
            print("no real solutions")

            xopt = -b / (2 * a)
            xmin = xopt - 5
            xmax = xopt + 5

        elif d == 0:
            x1 = -b / (2 * a)

            print("one solution: {:.5f}".format(x1))

            xmin = x1 - 5
            xmax = x1 + 5

        else:
            x1 = (-b - math.sqrt(d)) / (2 * a)
            x2 = (-b + math.sqrt(d)) / (2 * a)

            print("two solutions: x1={:.5f} x2={:.5f}".format(x1, x2))

            xmin = x1 - 2
            xmax = x2 + 2

            if x1 > x2:
                xmin = x2 - 2
                xmax = x1 + 2

        xs = []
        ys = []

        step = (xmax - xmin) / 149

        for i in range(150):
            x = xmin + i * step
            y = a * x ** 2 + b * x + c

            xs.append(x)
            ys.append(y)

        plt.plot(xs, ys)
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title("Quadratic Function")
        plt.show()


if __name__ == "__main__":
    main()