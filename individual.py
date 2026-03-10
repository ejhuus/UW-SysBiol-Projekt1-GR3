# individual.py

import numpy as np

class Individual:
    """
    Klasa opisująca pojedynczego osobnika.
    Przechowuje wektor fenotypu w n-wymiarowej przestrzeni.
    """
    def __init__(self, phenotype, sex):
        self.phenotype = phenotype
        self.sex = sex

    def get_phenotype(self):
        return self.phenotype
    
    def get_sex(self):
        return self.sex

    def set_phenotype(self, new_phenotype):
        self.phenotype = new_phenotype
    
