import math
import matplotlib.pyplot as plt


def plot_function(fun_str, domain, ns):
    """Display a table and plot a mathematical function."""
    xmin = domain[0]
    xmax = domain[1]

    xs = []
    ys = []

    step = (xmax - xmin) / (ns - 1)

    for i in range(ns):
        x = xmin + i * step
        y = eval(fun_str)

        xs.append(x)
        ys.append(y)

    print("{:>10} {:>10}".format("x", "y"))
    print("----------------------")

    for i in range(ns):
        print("{:+10.4f} {:+10.4f}".format(xs[i], ys[i]))

    plt.plot(xs, ys)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(fun_str)
    plt.show()


def main():
    fun_str = input("Enter function with variable x: ")
    ns = int(input("Enter number of samples: "))
    xmin = float(input("Enter xmin: "))
    xmax = float(input("Enter xmax: "))

    domain = (xmin, xmax)

    plot_function(fun_str, domain, ns)


if __name__ == "__main__":
    main()