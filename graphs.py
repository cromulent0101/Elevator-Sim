import matplotlib
import matplotlib.pyplot as plt
import random
from io import BytesIO
from typing import List, Dict

matplotlib.use("agg")  # used to allow savefig to work

# can we cache inputs to prevent excessive storage of graphs?
def generate_histogram(data: List) -> str:
    name = abs(int(str(hash(str(data)))[0:10]))
    plt.clf()
    plt.hist(data)
    plt.xlabel("Travel times")
    plt.ylabel("Number of Riders")
    plt.savefig(f"../graphs/{name}.png")  # needs should be async
    return name
