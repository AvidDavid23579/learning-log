import numpy as np

LOOP_DELAY = 20


def clamp(val, min_val, max_val):
    if val < min_val:
        return min_val
    elif val > max_val:
        return max_val
    else:
        return val


class SlewLimiter:
    def __init__(self, dt, accel, decel):
        self.dt = dt # Miliseconds
        self.accel = accel
        self.decel = decel
        self.prev_velocity = 0

    def update(self, input_value):
        delta = input_value - self.prev_velocity

        sameDirection = input_value * self.prev_velocity >= 0
        increasingMagnitude = abs(input_value) > abs(self.prev_velocity)

        limit = self.accel if sameDirection and increasingMagnitude else self.decel

        delta = clamp(delta, -limit * self.dt / 1000, limit * self.dt / 1000)

        self.prev_velocity = self.prev_velocity + delta
        return self.prev_velocity


class BangBang:
    def __init__(self, setpoint, deadband, u_max, u_min):
        self.setpoint = setpoint
        self.deadband = deadband
        self.u_max = u_max
        self.u_min = u_min

    def control(self, current_value):
        error = self.setpoint - current_value

        if error > self.deadband:
            return self.u_max
        elif error < -self.deadband:
            return self.u_min
        else:
            return 0


class Hysteresis:
    def __init__(self, setpoint, deadband, u_max, u_min):
        self.setpoint = setpoint
        self.deadband = deadband
        self.u_max = u_max
        self.u_min = u_min
        self.previous_output = 0

    def control(self, current_value):
        error = self.setpoint - current_value

        if error > self.deadband:
            self.previous_output = self.u_max
        elif error < -self.deadband:
            self.previous_output = self.u_min

        return self.previous_output


class PID:
    def __init__(self, Kp, Ki, Kd, alpha, u_max, u_min, setpoint=0.0):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.u_max = u_max
        self.u_min = u_min

        # Exponential moving average coefficient
        # alpha = 0 -> no filtering
        # alpha -> 1 -> more filtering
        self.alpha = alpha

        self.setpoint = setpoint

        self.integral = 0.0
        self.filtered_derivative = 0.0

    def control(self, current_value, current_velocity, dt, setpoint=None, setpoint_velocity=0):
        # Allow updating the setpoint each call
        if setpoint is not None:
            self.setpoint = setpoint

        error = self.setpoint - current_value

        # Integral
        self.integral += error * dt

        # de/dt = d(target)/dt - d(measurement)/dt
        raw_derivative = setpoint_velocity - current_velocity

        # EMA filter
        self.filtered_derivative = self.alpha * self.filtered_derivative + (1 - self.alpha) * raw_derivative

        output = self.Kp * error + self.Ki * self.integral + self.Kd * self.filtered_derivative

        output = clamp(output, self.u_min, self.u_max)

        return output


class SquareWaveDisturbance:
    def __init__(self, shot_rate=0.5, shot_duration=0.1, shot_torque=5.0, bidirectional=False, rng=None):
        self.shot_rate = shot_rate
        self.shot_duration = shot_duration
        self.shot_torque = shot_torque
        self.bidirectional = bidirectional
        self.rng = rng if rng is not None else np.random.default_rng()
        self._timer = 0.0
        self._sign = 1.0

    def update(self, dt):
        if self._timer <= 0.0 and self.rng.random() < self.shot_rate * dt:
            self._timer = self.shot_duration
            self._sign = self.rng.choice([-1.0, 1.0]) if self.bidirectional else 1.0

        if self._timer > 0.0:
            self._timer -= dt
            return self._sign * self.shot_torque
        return 0.0

    @property
    def active(self):
        return self._timer > 0.0


class HalfSineDisturbance:
    def __init__(self, shot_rate=0.5, shot_duration=0.1, shot_torque=5.0, bidirectional=False, rng=None):
        self.shot_rate = shot_rate
        self.shot_duration = shot_duration
        self.shot_torque = shot_torque
        self.bidirectional = bidirectional
        self.rng = rng if rng is not None else np.random.default_rng()
        self._timer = 0.0
        self._elapsed = 0.0
        self._sign = 1.0

    def update(self, dt):
        if self._timer <= 0.0 and self.rng.random() < self.shot_rate * dt:
            self._timer = self.shot_duration
            self._elapsed = 0.0
            self._sign = self.rng.choice([-1.0, 1.0]) if self.bidirectional else 1.0

        if self._timer > 0.0:
            phase = np.pi * self._elapsed / self.shot_duration
            torque = self._sign * self.shot_torque * np.sin(phase)
            self._timer -= dt
            self._elapsed += dt
            return torque
        return 0.0

    @property
    def active(self):
        return self._timer > 0.0


class TrapezoidalProfile:
    def __init__(self, start_pos, end_pos, max_vel, max_accel):

        # Initialize the trapezoidal motion profile parameters
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.max_vel = max_vel
        self.max_accel = max_accel

        self.distance = abs(end_pos - start_pos)
        self.direction = 1 if end_pos > start_pos else -1

        # Calculate the time to reach max velocity
        self.t_accel = max_vel / max_accel
        self.d_accel = 0.5 * max_accel * self.t_accel**2

        # Triangle profile (never reaches max velocity)
        if 2 * self.d_accel > self.distance:
            self.t_accel = np.sqrt(self.distance / max_accel)
            self.t_flat = 0
            self.d_flat = 0
            self.d_accel = 0.5 * max_accel * self.t_accel**2
            self.max_vel = self.max_accel * self.t_accel

        # Full trapezoidal profile
        else:
            self.d_flat = self.distance - 2 * self.d_accel
            self.t_flat = self.d_flat / max_vel

        # Total time for the motion
        self.total_time = 2 * self.t_accel + self.t_flat

    def position(self, t):
        if t < 0:
            return self.start_pos
        elif t < self.t_accel:
            # Acceleration phase
            return self.start_pos + 0.5 * self.max_accel * t**2 * self.direction
        elif t < (self.t_accel + self.t_flat):
            # Constant velocity phase
            return self.start_pos + (self.d_accel + (t - self.t_accel) * self.max_vel) * self.direction
        elif t < (self.total_time):
            # Deceleration phase
            x_dec_start = self.start_pos + (self.d_accel + self.d_flat) * self.direction
            t_dec = t - (self.t_accel + self.t_flat)
            return x_dec_start + self.direction * (self.max_vel * t_dec - 0.5 * self.max_accel * t_dec**2)
        else:
            return self.end_pos

    def velocity(self, t):
        if t < 0:
            return 0
        elif t < self.t_accel:
            # Acceleration phase
            return self.max_accel * t * self.direction
        elif t < (self.t_accel + self.t_flat):
            # Constant velocity phase
            return self.max_vel * self.direction
        elif t < (self.total_time):
            # Deceleration phase
            t_dec = t - (self.t_accel + self.t_flat)
            return (self.max_vel - self.max_accel * t_dec) * self.direction
        else:
            return 0

    def acceleration(self, t):
        if t < 0:
            return 0

        elif t < self.t_accel:
            return self.max_accel * self.direction

        elif t < self.t_accel + self.t_flat:
            return 0

        elif t <= self.total_time:
            return -self.max_accel * self.direction

        else:
            return 0

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