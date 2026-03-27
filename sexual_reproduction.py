# sexual_reproduction.py

import copy
import numpy as np
from strategies import ReproductionStrategy
from individual import Individual

from heapq import heappop, heappush, heapify
import random

class SexualReproduction(ReproductionStrategy):
    """
    Reprodukcja płciowa z uwzględnieniem doboru płciowego:
    Samiec losuje partnereki, aby uzyskać dokładnie target_size osobników nowego pokolenia.
    Ilość partnerek jest proporcjonalna do długości ogona, każda samica rodzi dwóch potomków, żeby
    populacja nie wymarła i podtrzymany był target_size.
    """

    def __init__(self):
        self._last_counts: np.ndarray = np.array([])

    def create_male_hierarchy(self, males: list) -> tuple:
        
        # konwersja na ujemne wartości ogona, bo heapq to kopiec minimalny - chcemy mieć największe ogony na górze
        males_neg_tails = [(-male.get_tail(), male) for male in males]

        # tworzenie kopca priorytetowego z posortowanej listy samców - nasza kolejka priorytetowa po samice
        heapify(males_neg_tails)

        # należy dodać głębokość kopca i przypisać do tupli, by obliczyć ilość samic przypadającą na danego samca 
        final_heap = []

        for i, (neg_tail, male) in enumerate(males_neg_tails):
            depth = (i + 1).bit_length() - 1 # obliczenie głębokości w pełnym drzewie binarnym na podstawie indeksu
            final_heap.append((neg_tail, male, depth))

        return (final_heap, len(final_heap).bit_length() ) # zwracamy kopiec i jego ilość warstw

    def sexual_selection(self, male_hierarchy: tuple, females: list) -> dict:

        # kreacja słownika samców według ich pozycji w hierarchii (kopcu)
        hierarchy_dict = {}
        for male in male_hierarchy[0]:
            if male[2] not in hierarchy_dict:
                hierarchy_dict[male[2]] = [male[1]]
            else:
                hierarchy_dict[male[2]].append(male[1])

        # inicjalizacja słownika z partnerkami dla każdego samca
        breeding_dict = {male[1]: [] for male in male_hierarchy[0]}

        # ważne metryki do doboru płciowego
        fem_amount = len(females)

        for depth in hierarchy_dict.keys():
            fems_per_layer = fem_amount // male_hierarchy[1] # ilość samic przypadająca na każdą warstwę kopca

            while fems_per_layer > 0:
                for male in hierarchy_dict[depth]: # iteracja po samcach na danej głębokości
                    breeding_dict[male].append(females[-1])
                    females.pop()
                    fems_per_layer -= 1

        return breeding_dict
        


    def reproduce(self, survivors: list, target_size: int) -> list:

        # losowość jest inherentną cechą natury
        males = [ind for ind in survivors if ind.get_sex() == "M"]
        males = random.shuffle(males)

        females = [ind for ind in survivors if ind.get_sex() == "F"]
        females = random.shuffle(females)

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



def sexual_reproduction(survivors: list, N: int) -> list:
    return SexualReproduction().reproduce(survivors, N)