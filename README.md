# Elevator-Sim

## Overview

This project aims to simulate the passenger traffic between two types of elevators: Normal and [Destination-Control](https://en.wikipedia.org/wiki/Destination_dispatch) (DC).

A normal elevator is the one you're most familiar with: each floor of a building has either an up or a down button. Press the button, and an elevator will be dispatched to your floor. Once it arrives, you enter the elevator and select your destination floor from within the elevator.

In a DC elevator, passengers select their destination floor from outside the elevator, eliminating the need to press a traditional up or down button, which potentially optimizes passenger throughput, especially in office buildings with high elevator usage.

## Features

- Simulates traffic between the two different types of elevators.
- Ingests an external CSV file to define a passenger's name, starting floor, destination floor, and runs a simulation to estimate how long it takes for each passenger to reach their destination.
- (WIP) Basic web page GUI to track passenger and elevator movement using Django REST Framework.

## Installation

Clone the repository:

    git clone https://github.com/cromulent0101/Elevator-Sim.git

Navigate to the directory:

    cd Elevator-Sim

(Optional) Create a new virtual environment and activate it:

    python -m venv .venv
    source .venv/bin/activate


Install the required packages:

    pip install -r requirements.txt

Yes, I know `poetry` exists and is probably better than this method.

## Usage

Modify the SIMULATION_CSV in main.py to point to your desired simulation CSV.

Configure the elevator parameters like ELEVATOR_CAPACITY, NUM_ELEVATORS, TIME_STEP, and MAX_TIME in main.py to suit your needs.

Run the simulator:

    python main.py

This will run the simulation for both types of elevators and print the results such as wait times, total floors traversed, etc.

## Backend

The backend utilizes the Django REST Framework for API routes. Logic to run the simulation is embedded in the Serializer.

## (WIP) Frontend

The frontend provides histograms of each elevator’s wait times and other metrics. Users will eventually be able to discretely choose various simulation parameters using sliders.

## Metrics

Metrics available include:

- Total time spent by all passengers waiting on the starting floor.
- Total time spent by all passengers before reaching the destination floor.
- Total floors traversed by all passengers per unit time.
- Max time spent waiting on a floor by any given passenger.

## Notes

The simulation initially used the `sleep()` function for real-time simulations, and threading to simulate multiple elevators at once, but was later modified to a non-real-time approach using a simulated timesteps for scalability.

## Further Reading
[Disk Scheduling Algorithms](http://www.cs.iit.edu/~cs561/cs450/disksched/disksched.html)

[Understanding the Benefits and Limitations of Destination Control](https://peters-research.com/index.php/papers/understanding-the-benefits-and-limitations-of-destination-control/)

A few scholarly articles on practical elevator scheduling in real-world buildings: [1](https://merl.com/publications/docs/TR2003-61.pdf)
[2](https://elib.dlr.de/47190/1/strang-context-UCI07-32-CameraReadyVersion-PID360095.pdf)
[3](https://ieeexplore.ieee.org/abstract/document/4620746)

[Queueing Theory](https://github.com/joelparkerhenderson/queueing-theory)
