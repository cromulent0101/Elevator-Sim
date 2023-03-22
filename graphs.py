import matplotlib
import matplotlib.pyplot as plt
import random
from io import BytesIO
from typing import List, Dict

matplotlib.use("agg")  # used to allow savefig to work

# can we cache inputs to prevent excessive storage of graphs?
def generate_histogram(data: List) -> str:
    name = str(hash(str(data)))[
        0:10
    ]  # ok this won't work because Python changes the seed each time
    plt.clf()
    plt.hist(data)
    plt.savefig(f"../graphs/{abs(int(name))}.png")  # needs to go somewhere else async
    return abs(int(name))
