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
    def __init__(self, accel, decel):
        self.accel = accel
        self.decel = decel
        self.prev_velocity = 0

    def update(self, input_value):
        delta = input_value - self.prev_velocity

        sameDirection = input_value * self.prev_velocity >= 0
        increasingMagnitude = abs(input_value) > abs(self.prev_velocity)

        limit = self.accel if sameDirection and increasingMagnitude else self.decel

        delta = clamp(delta, -limit * LOOP_DELAY / 1000, limit * LOOP_DELAY / 1000)

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
    def __init__(self, shot_rate=0.5, shot_duration=0.1, shot_torque=5.0, rng=None):
        self.shot_rate = shot_rate        # avg shots per second
        self.shot_duration = shot_duration
        self.shot_torque = shot_torque
        self.rng = rng if rng is not None else np.random.default_rng()
        self._timer = 0.0

    def update(self, dt):
        if self._timer <= 0.0 and self.rng.random() < self.shot_rate * dt:
            self._timer = self.shot_duration

        if self._timer > 0.0:
            self._timer -= dt
            return self.shot_torque
        return 0.0
    
class HalfSineDisturbance:
    def __init__(self, shot_rate=0.5, shot_duration=0.1, shot_torque=5.0, rng=None):
        self.shot_rate = shot_rate
        self.shot_duration = shot_duration
        self.shot_torque = shot_torque
        self.rng = rng if rng is not None else np.random.default_rng()
        self._timer = 0.0
        self._elapsed = 0.0

    def update(self, dt):
        if self._timer <= 0.0 and self.rng.random() < self.shot_rate * dt:
            self._timer = self.shot_duration
            self._elapsed = 0.0

        if self._timer > 0.0:
            phase = np.pi * self._elapsed / self.shot_duration
            torque = self.shot_torque * np.sin(phase)
            self._timer -= dt
            self._elapsed += dt
            return torque
        return 0.0



