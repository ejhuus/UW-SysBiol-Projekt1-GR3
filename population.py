# population.py

import numpy as np
from individual import Individual
import random

class Population:
    """
    Klasa przechowuje listę osobników (Individual)
    oraz pomaga w obsłudze różnych operacji na populacji.
    """
    def __init__(self, size, n_dim, is_diploid, init_sex_ratio, init_scale: float = 0.1,
                 init_scale_tail: float = 0.15, alpha_init=None):
        """
        Inicjalizuje populację losowymi fenotypami w n-wymiarach.
        :param size:       liczba osobników (N)
        :param n_dim:      wymiar fenotypu (n)
        :param init_scale: odchylenie std rozkładu startowego wokół optimum.
                           Zalecana reguła: sigma / sqrt(n).
                           Przy zbyt dużej wartości cała populacja ma fitness ≈ 0
                           i wymiera w pierwszym pokoleniu.
        :param alpha_init: centrum inicjalizacji – powinno być równe alpha0
                           ze środowiska. None → inicjalizacja wokół [0,...,0],
                           co powoduje wymarcie gdy alpha0 ≠ 0.
        """
        center = (np.array(alpha_init, dtype=float)
                  if alpha_init is not None else np.zeros(n_dim))
        self.individuals = []
        if is_diploid:
            males = int(init_sex_ratio * size)
            females = size - males
            for _ in range(males):
                chrom1 = np.random.normal(loc=center, scale=init_scale, size=n_dim)
                chrom2 = np.random.normal(loc=center, scale=init_scale, size=n_dim)
                phenotype = np.stack([chrom1, chrom2])
                tail = np.clip(np.random.normal(loc=0.5, scale=init_scale_tail), 0.0, 1.0)

                self.individuals.append(Individual(phenotype, 'M', tail))
            for _ in range(females):
                chrom1 = np.random.normal(loc=center, scale=init_scale, size=n_dim)
                chrom2 = np.random.normal(loc=center, scale=init_scale, size=n_dim)
                phenotype = np.stack([chrom1, chrom2])
                self.individuals.append(Individual(phenotype, 'F', 0.0))
        else:
            for _ in range(size):
                phenotype = np.random.normal(loc=center, scale=init_scale, size=n_dim)
                self.individuals.append(Individual(phenotype))

    def get_individuals(self):
        return self.individuals

    def set_individuals(self, new_individuals):
        self.individuals = new_individuals

    def __len__(self) -> int:
        return len(self.individuals)
