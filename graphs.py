import matplotlib
import matplotlib.pyplot as plt
import random
from io import BytesIO
from typing import List, Dict

matplotlib.use("agg")


def generate_histogram(data: List) -> str:
    # can we cache inputs to prevent excessive storage of graphs?
    name = str(hash(str(data)))[
        0:10
    ]  # ok this won't work because Python changes the seed each time
    # fig, ax = plt.subplots(1, 1)
    plt.hist(data)
    # ax.plot([1, 2, 3])
    # ax.plot(data)
    # # Save the graph to a BytesIO object
    # buffer = BytesIO()
    plt.savefig(f"../graphs/{abs(int(name))}.png")
    # plt.show()
    # buffer.seek(0)
    return name


if __name__ == "__main__":
    data = [
        412341,
        3,
        2,
        1,
        1,
        43,
        14,
        3,
        14,
        5,
        1,
        23,
        14,
        13,
        1,
        3,
        1,
        31,
        34,
        1,
        34,
        1,
        1,
        323,
        2,
    ]

    # Generate your Matplotlib graph
    # for _ in range(1000):
    #     data.append(random.normalvariate(0,10))

    generate_histogram(data)
    # fig, ax = plt.subplots(1,1)
    # ax.hist(data)
    # plt.savefig('../graphs/test.png')
    # plt.show()

    # Save the graph to a BytesIO object
    # buffer = BytesIO()
