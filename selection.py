# selection.py

import numpy as np
from strategies import SelectionStrategy
from individual import Individual


# ---------------------------------------------------------------------------
# Funkcje pomocnicze (używane też w stats.py)
# ---------------------------------------------------------------------------

def fitness_function(individual: Individual, alpha: np.ndarray, sigma: float, tail_cost: float) -> float:
    """
    Gaussowska funkcja fitness:
        phi_alpha(p) = exp( -||p - alpha||^2 / (2 * sigma^2) )

    :param phenotype: fenotyp osobnika
    :param alpha: optymalny fenotyp środowiska
    :param sigma: parametr siły selekcji (większe sigma = słabsza selekcja)
    :return: wartość fitness w przedziale (0, 1]
    """
    phenotype = individual.get_effective_phenotype()
    diff = (phenotype - alpha)
    base_fitness = float(np.exp(-np.dot(diff, diff) / (2 * sigma ** 2)))
    tail = individual.get_tail() if individual.get_tail() is not None else 0.0
    # Jeżeli samica lub nie ma ogona to nie ma wpływu na dostosowanie.
    return base_fitness * (1 - tail * tail_cost)


def compute_fitnesses(individuals: list, alpha: np.ndarray, sigma: float, tail_cost: float) -> np.ndarray:
    """Oblicza fitness dla całej listy osobników. Zwraca tablicę numpy (N,)."""
    return np.array([fitness_function(ind, alpha, sigma, tail_cost)
                     for ind in individuals])


# ---------------------------------------------------------------------------
# Strategie selekcji
# ---------------------------------------------------------------------------

class ThresholdSelection(SelectionStrategy):
    """
    Selekcja progowa: eliminuje osobniki o fitness poniżej progu.
    Zwraca ocalałych – może ich być mniej niż N.
    Reprodukcja uzupełni populację do N w następnym kroku.
    """

    def __init__(self, sigma: float, threshold: float, tail_cost: float | None = None):
        self.sigma = sigma
        self.threshold = threshold
        self.tail_cost = tail_cost

    def select(self, individuals: list, alpha: np.ndarray) -> list:
        return [ind for ind in individuals
                if fitness_function(ind, alpha, self.sigma, self.tail_cost) >= self.threshold]


class ProportionalSelection(SelectionStrategy):
    """
    Selekcja proporcjonalna (ruletka / Wright-Fisher):
    losuje N osobników z powtórzeniami, proporcjonalnie do fitness.
    Zwraca dokładnie N osobników.
    """

    def __init__(self, sigma: float, N: int, tail_cost: float | None = None):
        self.sigma = sigma
        self.N = N
        self.tail_cost = tail_cost

    def select(self, individuals: list, alpha: np.ndarray) -> list:
        fitnesses = compute_fitnesses(individuals, alpha, self.sigma, self.tail_cost)
        total = fitnesses.sum()
        probs = fitnesses / total if total > 0 else np.ones(len(individuals)) / len(individuals)
        chosen = np.random.choice(len(individuals), size=self.N, replace=True, p=probs)
        return [individuals[i] for i in chosen]


class TwoStageSelection(SelectionStrategy):
    """
    Dwuetapowa selekcja (domyślna – zgodna z treścią zadania):
      Etap 1 – progowy: eliminuje osobniki z fitness < threshold
      Etap 2 – proporcjonalny: spośród ocalałych losuje N osobników
                               proporcjonalnie do fitness

    Zwraca dokładnie N osobników (lub pustą listę = wymarcie w etapie 1).
    """

    def __init__(self, sigma: float, threshold: float, N: int, tail_cost: float | None = None):
        self.sigma = sigma
        self.threshold = threshold
        self.N = N
        self.tail_cost = tail_cost

    def select(self, individuals: list, alpha: np.ndarray) -> list:
        # Etap 1: selekcja progowa
        survivors = [ind for ind in individuals
                     if fitness_function(ind, alpha, self.sigma, self.tail_cost) >= self.threshold]
        if not survivors:
            return []

        # Etap 2: selekcja proporcjonalna – wypełnia do N
        fitnesses = compute_fitnesses(survivors, alpha, self.sigma, self.tail_cost)
        total = fitnesses.sum()
        probs = fitnesses / total if total > 0 else np.ones(len(survivors)) / len(survivors)
        chosen = np.random.choice(len(survivors), size=self.N, replace=True, p=probs)
        return [survivors[i] for i in chosen]
