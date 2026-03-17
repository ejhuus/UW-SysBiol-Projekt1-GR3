# individual.py

import numpy as np

class Individual:
    """
    Klasa opisująca pojedynczego osobnika.
    Przechowuje wektor fenotypu w n-wymiarowej przestrzeni.
    """
    def __init__(self, phenotype, sex=None, tail=None):
        self.phenotype = phenotype
        self.sex = sex
        self.tail = tail

    def get_phenotype(self):
        return self.phenotype
    
    def get_effective_phenotype(self):
        if self.is_diploid():
            return self.phenotype.mean(axis=0)
        return self.phenotype
    
    def get_sex(self):
        return self.sex
    
    def get_tail(self):
        return self.tail

    def set_phenotype(self, new_phenotype):
        self.phenotype = new_phenotype
    
    def set_tail(self, new_tail):
        self.tail = new_tail

    def is_diploid(self):
        return isinstance(self.phenotype, np.ndarray) and self.phenotype.ndim == 2
