import numpy as np


class ArmFeedforward:
    def __init__(self, mass, length, inertia, damping, gravity=9.81):
        self.m = mass
        self.l = length
        self.I = inertia
        self.b = damping
        self.g = gravity

    def calculate(self, theta_ref, omega_ref, alpha_ref):

        gravity = self.m * self.g * (self.l / 2) * np.cos(theta_ref)
        friction = self.b * omega_ref
        inertia = self.I * alpha_ref

        return gravity + friction + inertia