# periodic_environment.py

import numpy as np
from strategies import EnvironmentDynamics

class PeriodicConstEnvironment(EnvironmentDynamics):
    """
    Scenariusz okresowo zmieniającego się środowiska.
    Każda cecha w optymalnym fenotypie przesuwa się niezależnie wzdłuż sinusoidy o zadanym punkcie
    równowagi, okresie, amplitudzie i fazie z opcjonalnymi losowymi "równinami" - przedziałami czasu,
    w którym wszystkie wartości wektora pozostają na stałym poziomie.
    Długość przerwy jest losowana z rozkładu geometrycznego z parametrem p = 1/średnia długość przerwy
    Możliwe też opcjonalne losowe fluktuacje w każdym pokoleniu.
    """

    def __init__(self, zero_crossing: np.ndarray,
                 amplitude: np.ndarray,
                 period:np.ndarray,
                 phase:np.ndarray,
                 delta: np.ndarray,
                 plateau_chance: float,
                 mean_plateau_length: float,
                 ):
        """
            :param zero_crossing: punk równowagi, czyli wartość, wokół której oscyluje optimum.
            :param delta: Wektor odchyleń std. losowych fluktuacji wokół funkcji (0 = brak szumu).
            :param amplitude: Wektor amplitud funkcji, czyli największe możliwe odchylenie od punktu równowagi.
            :param period: Wektor okresów sinusoidy w generacjach.
            :param phase: Wektor faz sinusoidy w generacjach.
            :plateau_chance: Prawdopodobieństwo powstania równiny (zatrzymania się wszystkich wartości w wektorze na jakiś czas)
             w danej generacji.
            :param mean_plateau_length: Średnia długość równiny (1/P(równina skończy się w danej generacji)) w rozkładzie geometrycznym.

        """
        # wave parameters
        self.zero_crossing = np.array(zero_crossing, dtype=float)
        self.amplitude = np.array(amplitude, dtype=float)
        self.period =np.array(period, dtype=float)
        self.phase = np.array(phase, dtype=float)
        self.delta = np.array(delta, dtype=float)

        #stability parameters
        self.plateau_chance = float(plateau_chance)
        self.mean_plateau_length = float(mean_plateau_length)

        # setting initial time to 0
        self.tick_amount = 0
        self.remaining_plateau_ticks = 0

    def update(self) -> None:
        # If function already is in stable state
        if self.remaining_plateau_ticks > 0:
            self.remaining_plateau_ticks -= 1
        else:
            #Chanse to enter stability
            if np.random.random() < self.plateau_chance:
                # Generate the plateau length using a geometric distribution
                self.remaining_plateau_ticks = np.random.geometric(1/self.mean_plateau_length)
            else:
                self.tick_amount += 1

    def get_optimal_phenotype(self):
        n = len(self.zero_crossing)
        random_shift = np.random.normal(loc=0, scale=self.delta, size=n)
        return self.zero_crossing + self.amplitude * np.sin(self.tick_amount * 2 * np.pi / self.period + self.phase) + random_shift

    def set_current_generation(self, tick: int):
        self.tick_amount = tick