# reproduction.py

import copy
import numpy as np
from strategies import ReproductionStrategy
from individual import Individual


class AsexualReproduction(ReproductionStrategy):
    """
    Reprodukcja bezpłciowa (klonowanie):
    Losowo wybiera rodziców spośród ocalałych (z powtórzeniami) i klonuje ich,
    aby uzyskać dokładnie target_size osobników nowego pokolenia.

    Każdy ocalały ma równe szanse na bycie rodzicem – selekcja już uwzględniła fitness.
    Po każdym wywołaniu reproduce() dostępne są statystyki przez get_reproduction_stats().
    """

    def __init__(self):
        self._last_counts: np.ndarray = np.array([])

    def reproduce(self, survivors: list, target_size: int) -> list:
        if not survivors:
            self._last_counts = np.array([])
            return []
        indices = np.random.randint(0, len(survivors), size=target_size)
        # bincount[i] = liczba potomków osobnika i
        self._last_counts = np.bincount(indices, minlength=len(survivors))
        return [copy.deepcopy(survivors[i]) for i in indices]

    def get_reproduction_stats(self) -> dict:
        """
        Zwraca statystyki z ostatniego reproduce():
        n_parents       – ilu osobników miało ≥1 potomka ("ewolucyjny sukces")
        median_offspring – mediana potomków wśród reprodukujących się osobników
        max_offspring   – maksymalna płodność (najlepiej przystosowany osobnik)
        """
        if len(self._last_counts) == 0:
            return {'n_parents': 0, 'median_offspring': 0.0, 'max_offspring': 0}
        reproducing = self._last_counts[self._last_counts > 0]
        return {
            'n_parents':        int(len(reproducing)),
            'median_offspring': float(np.median(reproducing)) if len(reproducing) else 0.0,
            'max_offspring':    int(self._last_counts.max()),
        }

class SexualReproduction(ReproductionStrategy):
    """
    Reprodukcja płciowa z uwzględnieniem doboru płciowego:
    Samiec losuje partnereki, aby uzyskać dokładnie target_size osobników nowego pokolenia.
    Ilość partnerek jest proporcjonalna do długości ogona, każda samica rodzi dwóch potomków, żeby
    populacja nie wymarła i podtrzymany był target_size.
    """

    def __init__(self):
        self._last_counts: np.ndarray = np.array([])

    def reproduce(self, survivors: list, target_size: int) -> list:
        males = [ind for ind in survivors if ind.get_sex() == "M"]
        females = [ind for ind in survivors if ind.get_sex() == "F"]

        if not males or not females:
            self._last_counts = np.array([])
            return []
        
        offspring = []

        male_counts = np.zeros(len(males), dtype=int)

        for _ in range(target_size):
            # obecnie zwykłe losowanie partnera - PAWEŁ dodaj dobór płciowy.
            father_idx = np.random.randint(len(males))
            mother_idx = np.random.randint(len(females))

            father = males[father_idx]
            mother = females[mother_idx]

            male_counts[father_idx] += 1

            # losowanie chromosomu ojca
            father_pheno = father.get_phenotype()
            chrom_father = father_pheno[np.random.randint(2)]

            # losowanie chromosomu matki
            mother_pheno = mother.get_phenotype()
            chrom_mother = mother_pheno[np.random.randint(2)]

            child_pheno = np.stack([chrom_father, chrom_mother])

            # losowanie płci
            sex = np.random.choice(["M", "F"])

            # dziedziczenie ogona
            if sex == "M":
                tail = father.get_tail()
            else:
                tail = 0.0

            child = Individual(
                phenotype=child_pheno,
                sex=sex,
                tail=tail
            )

            offspring.append(child)

        self._last_counts = male_counts
        return offspring


    def get_reproduction_stats(self) -> dict:
        """
        Zwraca statystyki z ostatniego reproduce():
        n_parents       – ilu osobników miało ≥1 potomka ("ewolucyjny sukces")
        median_offspring – mediana potomków wśród reprodukujących się osobników
        max_offspring   – maksymalna płodność (najlepiej przystosowany osobnik)
        """
        if len(self._last_counts) == 0:
            return {'n_parents': 0, 'median_offspring': 0.0, 'max_offspring': 0}
        reproducing = self._last_counts[self._last_counts > 0]
        return {
            'n_parents':        int(len(reproducing)),
            'median_offspring': float(np.median(reproducing)) if len(reproducing) else 0.0,
            'max_offspring':    int(self._last_counts.max()),
        }


# Funkcja pomocnicza zachowana dla kompatybilności wstecznej
def asexual_reproduction(survivors: list, N: int) -> list:
    return AsexualReproduction().reproduce(survivors, N)

def sexual_reproduction(survivors: list, N: int) -> list:
    return SexualReproduction().reproduce(survivors, N)
