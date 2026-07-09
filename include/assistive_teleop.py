from utils import clamp


class SlewLimiter:
    def __init__(self, dt, accel, decel):
        self.dt = dt * 1000 # Miliseconds
        self.accel = accel
        self.decel = decel
        self.prev_velocity = 0

    def update(self, input_value):
        delta = input_value - self.prev_velocity

        sameDirection = input_value * self.prev_velocity >= 0
        increasingMagnitude = abs(input_value) > abs(self.prev_velocity)

        limit = self.accel if sameDirection and increasingMagnitude else self.decel

        delta = clamp(delta, -limit * self.dt, limit * self.dt)

        self.prev_velocity = self.prev_velocity + delta
        return self.prev_velocity


class JerkSlewLimiter:
    def __init__(self, dt, max_accel, max_decel, max_jerk):
        self.dt = dt * 1000
        self.max_accel = max_accel
        self.max_decel = max_decel
        self.max_jerk = max_jerk
        self.velocity = 0
        self.accel = 0

    def update(self, target_velocity):
        desired_accel = (target_velocity - self.velocity) / self.dt

        sameDirection = target_velocity * self.velocity >= 0
        increasingMagnitude = abs(target_velocity) > abs(self.velocity)
        accel_limit = self.max_accel if sameDirection and increasingMagnitude else self.max_decel

        desired_accel = clamp(desired_accel, -accel_limit, accel_limit)

        max_delta_accel = self.max_jerk * self.dt
        accel_delta = clamp(desired_accel - self.accel, -max_delta_accel, max_delta_accel)
        self.accel += accel_delta

        self.velocity += self.accel * self.dt
        return self.velocity