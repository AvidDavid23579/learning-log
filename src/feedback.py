from utils import clamp


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

        # de/dt = d(target)/dt - d(measurement)/dt
        raw_derivative = setpoint_velocity - current_velocity

        # EMA filter
        self.filtered_derivative = self.alpha * self.filtered_derivative + (1 - self.alpha) * raw_derivative

        # Integral
        unclamped_output = self.Kp * error + self.Ki * self.integral + self.Kd * self.filtered_derivative
        saturated_high = unclamped_output > self.u_max
        saturated_low = unclamped_output < self.u_min
        if not ((saturated_high and error > 0) or (saturated_low and error < 0)):
            self.integral += error * dt

        output = self.Kp * error + self.Ki * self.integral + self.Kd * self.filtered_derivative

        output = clamp(output, self.u_min, self.u_max)

        return output
