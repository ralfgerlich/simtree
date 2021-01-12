"""
A planet orbiting a sun.
"""
import numpy as np
import numpy.linalg as linalg
import matplotlib.pyplot as plt

from modypy.model import System, State
from modypy.simulation import Simulator

# Define the system parameters
G = 6.67E-11*(24*60*60)**2
SUN_MASS = 1.989E30
PLANET_ORBIT = 149.6E09
PLANET_ORBIT_TIME = 365.256

# Define the initial state
PLANET_VELOCITY = 2 * np.pi * PLANET_ORBIT / PLANET_ORBIT_TIME
X_0 = np.c_[PLANET_ORBIT, 0]
V_0 = 0.9*PLANET_VELOCITY * np.c_[np.sin(np.deg2rad(20)), np.cos(np.deg2rad(20))]

# Create the system
system = System()


# Define the derivatives
def position_dt(data):
    return data.states[velocity]


def velocity_dt(data):
    x = data.states[position]
    r = linalg.norm(x)
    return -G * SUN_MASS/(r**3) * x


# Create the states
position = State(system,
                 shape=2,
                 derivative_function=position_dt,
                 initial_condition=X_0)

velocity = State(system,
                 shape=2,
                 derivative_function=velocity_dt,
                 initial_condition=V_0)


# Run a simulation
simulator = Simulator(system,
                      start_time=0.0,
                      integrator_options={
                          'rtol': 1E-6
                      })
msg = simulator.run_until(time_boundary=PLANET_ORBIT_TIME)

if msg is not None:
    print("Simulation failed with message '%s'" % msg)
else:
    # Plot the result
    trajectory = simulator.result.state[:, position.state_slice]
    plt.plot(trajectory[:, 0], trajectory[:, 1])
    plt.title("Planet Orbit")
    plt.savefig("03_planet_orbit_simulation.png")
    plt.show()