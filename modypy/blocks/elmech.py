"""
A collection fo electro-mechanical blocks.
"""

import math

from modypy.model import Block, Port, State, SignalState, Signal


class DCMotor(Block):
    """
    A DC motor with external load.

    This model has the following inputs:

    ``voltage``
        representing the terminal voltage on the motor
    ``external_torque``
        representing the braking torque of the external load

    It has two outputs:

    ``speed_rps``
        representing the speed in RPS
    ``torque``
        representing the torque generated by the motor

    The parameters are:

    ``motor_constant``
        the motor constant in usually Vs/rad
    ``resistance``
        the internal resistance of the coil in Ohms
    ``inductance``
        the inductance of the coil in Henry
    ``moment_of_inertia``
        the moment of inertia of the rotor and the load in ``kg*m^2``

    The model expresses the following equations of motion::

        U(t)    = motor_constant*omega(t) + resistance*i(t) + inductance*di(t)/dt
        motor_constant*I(t) = moment_of_inertia*domega(t)/dt + tau_ext(t)
    """
    def __init__(self,
                 parent,
                 motor_constant,
                 resistance,
                 inductance,
                 moment_of_inertia,
                 initial_omega=0, initial_current=0):
        Block.__init__(self, parent)

        self.motor_constant = motor_constant
        self.resistance = resistance
        self.inductance = inductance
        self.moment_of_inertia = moment_of_inertia

        self.voltage = Port(self, shape=1)
        self.external_torque = Port(self, shape=1)

        self.omega = State(self,
                           shape=1,
                           derivative_function=self.omega_dot,
                           initial_condition=initial_omega)
        self.current = SignalState(self,
                                   shape=1,
                                   derivative_function=self.current_dot,
                                   initial_condition=initial_current)

        self.speed_rps = Signal(self, shape=1, value=self.speed_rps_output)
        self.torque = Signal(self, shape=1, value=self.torque_output)

    def omega_dot(self, data):
        """Calculates the derivative of the speed in rad/s^2"""
        current = data.states[self.current]
        tau_ext = data.signals[self.external_torque]
        return (self.motor_constant * current - tau_ext) / self.moment_of_inertia

    def current_dot(self, data):
        """Calculates the derivative of the current in A/s"""
        omega = data.states[self.omega]
        current = data.states[self.current]
        voltage = data.signals[self.voltage]

        return (voltage - self.motor_constant * omega - self.resistance * current) / self.inductance

    def speed_rps_output(self, data):
        """Calculates the current speed in RPS"""
        omega = data.states[self.omega]
        return omega/(2*math.pi)

    def torque_output(self, data):
        """Calculates the torque generated by the motor in kg*m/s^2"""
        current = data.states[self.current]
        return self.motor_constant * current
