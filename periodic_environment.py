# periodic_environment.py

import numpy as np
from strategies import EnvironmentDynamics

class PeriodicConstEnvironment(EnvironmentDynamics):

    def __init__(self, zero_crossing: np.ndarray, amplitude: np.ndarray, period:np.ndarray, phase:np.ndarray, delta: float = 0.0):
        """
            :param zero_crossing: punk zerowy, czyli wartość wokół której "waha się" optimum.
            :param delta: odch. std. losowych fluktuacji wokół c (0 = brak szumu)
            :param amplitude: amplituda funkcji, czyli największe możliwe odchylenie od punktu zerowego
            :param period: okres sinusoidy w generacjach
            :param phase: # TODO opisac to

        """
        # setting parameters
        self.zero_crossing = np.array(zero_crossing, dtype=float)
        self.amplitude = amplitude
        self.period = period
        self.phase = phase
        self.delta = float(delta)

        # set initial time to 0
        self.tick_amount = 0
        

    def update(self) -> None:
        self.tick_amount += 1

    def get_optimal_phenotype(self):
        n = len(self.zero_crossing)
        random_shift = np.random.normal(loc=0, scale=self.delta, size=n)
        return self.zero_crossing + self.amplitude * np.sin(self.tick_amount * 2 * np.pi / self.period + self.phase) + random_shift

    def set_current_generation(self, tick: int):
        self.tick_amount = tick