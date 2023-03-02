import matplotlib.pyplot as plt
from io import BytesIO
from typing import List, Dict


def generate_histogram(data: List) -> None:
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [4, 5, 6])

    # Save the graph to a BytesIO object
    buffer = BytesIO()
    fig.savefig(buffer, format="png")
    buffer.seek(0)


if __name__ == "__main__":

    # Generate your Matplotlib graph

    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [4, 5, 6])
    plt.show()

    # Save the graph to a BytesIO object
    # buffer = BytesIO()
