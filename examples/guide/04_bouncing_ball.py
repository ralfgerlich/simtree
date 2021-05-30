"""
A bouncing ball
"""
import matplotlib.pyplot as plt

from modypy.blocks.linear import integrator
from modypy.model import System, State, ZeroCrossEventSource
from modypy.simulation import Simulator, SimulationResult

# The system parameters
DELTA = 0.7
G = 9.81

# The initial conditions
INITIAL_HEIGHT = 10.0
INITIAL_VELOCITY = 0.0

# The system
system = System()


# The system states
def velocity_dt(_system_state):
    """Calculate the derivative of the vertical speed"""
    return -G


velocity = State(system,
                 derivative_function=velocity_dt,
                 initial_condition=INITIAL_VELOCITY)
height = integrator(system,
                    input_signal=velocity,
                    initial_condition=INITIAL_HEIGHT)


# Define the zero-crossing-event
def bounce_event_function(system_state):
    """Define the value of the event function for detecting bounces"""
    return height(system_state)


bounce_event = ZeroCrossEventSource(system,
                                    event_function=bounce_event_function,
                                    direction=-1)


# Define the event-handler
def bounce_event_handler(data):
    """Reverse the direction of motion after a bounce"""
    velocity.set_value(data, -DELTA*velocity(data))


# Register it with the bounce event
bounce_event.register_listener(bounce_event_handler)

# Run a simulation
simulator = Simulator(system,
                      start_time=0.0,
                      max_step=0.1)
result = SimulationResult(system,
                          simulator.run_until(time_boundary=8))

# Plot the result
plt.plot(result.time, height(result))
plt.title("Bouncing Ball")
plt.xlabel("Time")
plt.savefig("04_bouncing_ball_simulation.png")
plt.show()
