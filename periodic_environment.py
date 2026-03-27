# periodic_environment.py

import numpy as np
from strategies import EnvironmentDynamics
from math import sin

class PeriodicConstEnvironment(EnvironmentDynamics):
    current_generation = 0

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


    def update(self) -> None:
        self.current_generation += 1

    def get_optimal_phenotype(self):
        n = len(self.zero_crossing)
        return self.zero_crossing + self.amplitude * sin(np.full(n,self.current_generation) / self.period + self.phase)

    def set_current_generation(self, generation: int):
        self.current_generation = generation