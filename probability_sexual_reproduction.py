import numpy as np
import random
from strategies import ReproductionStrategy
from individual import Individual

class ProbabilitySexualReproduction(ReproductionStrategy):
    """
    Reprodukcja płciowa z probabilistycznym doborem płciowym.
    Szansa na partnerkę zależy wykładniczo od długości ogona.
    """

    def __init__(self, temperature: float, tail_c: float, bias: float):
        self._last_counts: np.ndarray = np.array([])
        self.temperature = temperature
        self.tail_c = tail_c
        self.bias = bias

    def sexual_selection(self, males: list, females: list) -> dict:
        if not males or not females:
            return {}

        # 1. Pobieramy długości ogonów
        tails = np.array([m.get_tail() for m in males], dtype=float)
        
        # 2. Skalowanie wykładnicze (np.exp). 
        exp_tails = np.exp(tails / self.temperature)
        
        # 3. Normalizacja do prawdopodobieństw
        probs = exp_tails / np.sum(exp_tails)

        # Inicjalizacja słownika par
        breeding_dict = {m: [] for m in males}

        # 4. Każda samica "wybiera" samca na podstawie wag
        # Używamy np.random.choice, aby wylosować indeksy samców
        male_indices = np.arange(len(males))
        chosen_indices = np.random.choice(male_indices, size=len(females), p=probs)

        for f_idx, m_idx in enumerate(chosen_indices):
            breeding_dict[males[m_idx]].append(females[f_idx])

        return breeding_dict

    def reproduce(self, survivors: list, target_size: int) -> list:
        # Podział na płcie i losowe przemieszanie (dla równego startu)
        males = [ind for ind in survivors if ind.get_sex() == "M"]
        females = [ind for ind in survivors if ind.get_sex() == "F"]
        random.shuffle(males)
        random.shuffle(females)

        if not males or not females:
            self._last_counts = np.array([])
            return []
        
        # Generujemy pary (jeden samiec może mieć wiele samic, lub zero)
        breeding_dict = self.sexual_selection(males, females)
        
        # Przygotowujemy listę par do produkcji potomstwa
        all_pairs = []
        for male, partnerki in breeding_dict.items():
            for female in partnerki:
                all_pairs.append((male, female))

        if not all_pairs:
            return []

        offspring = []
        # Tablica do statystyk (indeksujemy tak jak listę 'males')
        male_to_idx = {male: i for i, male in enumerate(males)}
        male_counts = np.zeros(len(males), dtype=int)

        # Tworzymy potomstwo aż do osiągnięcia target_size
        # Używamy itertools.cycle lub prostej pętli, by "sprawiedliwie" brać po 1 dziecku od każdej pary
        pair_idx = 0
        while len(offspring) < target_size:
            father, mother = all_pairs[pair_idx % len(all_pairs)]
            
            # Losowanie genotypu (1 chromosom od ojca, 1 od matki)
            father_pheno = father.get_phenotype()
            chrom_father = father_pheno[np.random.randint(2)]

            mother_pheno = mother.get_phenotype()
            chrom_mother = mother_pheno[np.random.randint(2)]

            child_pheno = np.stack([chrom_father, chrom_mother])

            # Losowanie płci dziecka
            sex = np.random.choice(["M", "F"])

            # Dziedziczenie ogona (uproszczone: tylko samce mają ogon w fenotypie)
            if sex == "M":
                father_tail = father.get_tail()
                mutation_noise = np.random.normal(0, self.tail_c) 
                new_tail = father_tail + self.bias + mutation_noise
                tail = np.clip(new_tail, 0.0, 1.0)
            else:
                tail = 0.0

            child = Individual(
                phenotype=child_pheno,
                sex=sex,
                tail=tail
            )

            offspring.append(child)
            male_counts[male_to_idx[father]] += 1
            
            pair_idx += 1

        self._last_counts = male_counts
        return offspring

    def get_reproduction_stats(self) -> dict:
        if len(self._last_counts) == 0:
            return {'n_parents': 0, 'median_offspring': 0.0, 'max_offspring': 0}
        
        reproducing = self._last_counts[self._last_counts > 0]
        return {
            'n_parents':        int(len(reproducing)),
            'median_offspring': float(np.median(reproducing)) if len(reproducing) > 0 else 0.0,
            'max_offspring':    int(self._last_counts.max()),
        }

def sexual_reproduction(survivors: list, N: int) -> list:
    return ProbabilitySexualReproduction().reproduce(survivors, N)