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


class JerkLimitedSlew:
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
        
class SCurveProfile:
    def __init__(self, start_pos, end_pos, max_vel, max_accel, max_jerk):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.max_vel = max_vel
        self.max_accel = max_accel
        self.max_jerk = max_jerk

        self.distance = abs(end_pos - start_pos)
        self.direction = 1 if (end_pos > start_pos) else -1

        j, a, v, d = max_jerk, max_accel, max_vel, self.distance 

        if d == 0:
            self.tj = self.ta = self.t_cruise = 0.0
            self.a_peak = 0.0
            self.v_peak = 0.0
            self.total_time = 0.0
            self.segments = []
            return
        
        tj_full = a / j

        if a * tj_full > v:
            tj = np.sqrt(v / j)
            ta = 0.0
            self.a_peak = j * tj 
        else:
            tj = tj_full
            ta = v / a - tj
            a_peak = a 

        v_peak = v
        t_ramp = 2 * tj + ta
        d_ramp = v_peak * t_ramp 

        if d_ramp <= d:
            t_cruise = (d - d_ramp) / v_peak

        # Never reaches max velocity    
        else: 
            t_cruise = 0.0
            B = a * tj_full
            v_candidate = (-B + np.sqrt(B^2 + 4 * a * d)) / 2

            # Lower max velocity with quicker max acceleration phase
            if v_candidate >= a * tj_full:
                v_peak = v_candidate
                tj = tj_full
                ta = v_peak / a - tj
                a_peak = a

            # Does not reach max acceleration phase
            else:
                v_peak = (d * np.sqrt(j) / 2) ** (2 / 3)
                tj = np.sqrt(v_peak / j)
                ta = 0.0
                a_peak = j * tj 

        self.tj = tj
        self.ta = ta
        self.t_cruise = t_cruise
        self.a_peak = a_peak # pyright: ignore[reportPossiblyUnboundVariable]
        self.v_peak = v_peak

        self.max_accel = a_peak # pyright: ignore[reportPossiblyUnboundVariable]
        self.max_vel = v_peak

        self.total_time = 4*tj + 2*ta + self.t_cruise

        self.build_segments()

    def build_segments(self):
        j = self.max_jerk * self.direction
        durations = [self.tj, self.ta, self.tj, self.t_cruise, self.tj, self.ta, self.tj]
        jerks = [j, 0.0, -j, 0.0, -j, 0.0, j]

        segments = []
        t_start = 0.0
        p0, v0, a0 = self.start_pos, 0.0, 0.0

        for dur, jrk in zip(durations, jerks):
            segments.append({"t_start": t_start, "dur": dur, "p0": p0, "v0": v0, "a0": a0, "jrk": jrk})
            p0, v0, a0 = self.advance(p0, v0, a0, jrk, dur)
            t_start += dur

        self.segments = segments

    @staticmethod
    def advance(p0, v0, a0, jerk, t):
        a1 = a0 + jerk * t
        v1 = v0 + a0 * t + jerk * 0.5 * t**2
        p1 = p0 + v0 * t + a0 * 0.5 * t**2 + jerk * (1/6) * t**3
        return p1, v1, a1 
    
    def segment_at(self, t):
        for seg in self.segments:
            if t < seg["t_start"] + seg["dur"]:
                return seg, t - seg["t_start"]
        last = self.segments[-1]
        return last, last["dur"]
    
    def position(self, t):
        if t < 0 or self.total_time == 0:
            return self.start_pos
        if t >= self.total_time:
            return self.end_pos
        
        seg, tl = self.segment_at(t)
        p, _, _ = self.advance(seg["p0"], seg["v0"], seg["a0"], seg["jerk"], seg["time"])

        return p 
    
    def velocity(self, t):
        if t < 0 or t >= self.total_time or self.total_time == 0:
            return 0.0
        
        seg, tl = self.segment_at(t)
        _, v, _ = self.advance(seg["p0"], seg["v0"], seg["a0"], seg["jerk"], seg["time"])

        return v 
    
    def acceleration(self, t):
        if t < 0 or t >= self.total_time or self.total_time == 0:
            return 0.0
        
        seg, tl = self.segment_at(t)
        _, _, a = self.advance(seg["p0"], seg["v0"], seg["a0"], seg["jerk"], seg["time"])

        return a

    def jerk(self, t):
         if t < 0 or t >= self.total_time or self.total_time == 0:
            return 0.0
         
         seg, _ = self.segment_at(t)
         return seg["jerk"]


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
