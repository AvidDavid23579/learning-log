import numpy as np


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