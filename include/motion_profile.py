import numpy as np


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
            segments.append({"t_start": t_start, "dur": dur, "p0": p0, "v0": v0, "a0": a0, "jerk": jrk})
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
        p, _, _ = self.advance(seg["p0"], seg["v0"], seg["a0"], seg["jerk"], tl)

        return p 
    
    def velocity(self, t):
        if t < 0 or t >= self.total_time or self.total_time == 0:
            return 0.0
        
        seg, tl = self.segment_at(t)
        _, v, _ = self.advance(seg["p0"], seg["v0"], seg["a0"], seg["jerk"], tl)

        return v 
    
    def acceleration(self, t):
        if t < 0 or t >= self.total_time or self.total_time == 0:
            return 0.0
        
        seg, tl = self.segment_at(t)
        _, _, a = self.advance(seg["p0"], seg["v0"], seg["a0"], seg["jerk"], tl)

        return a

    def jerk(self, t):
         if t < 0 or t >= self.total_time or self.total_time == 0:
            return 0.0
         
         seg, _ = self.segment_at(t)
         return seg["jerk"]