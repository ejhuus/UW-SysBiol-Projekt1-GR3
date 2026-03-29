# config.py

import numpy as np

# -------------------
# PARAMETRY POPULACJI
# -------------------
N = 1000           # liczba osobników w populacji
n = 10             # wymiar przestrzeni fenotypowej

# Rozrzut początkowych fenotypów wokół optimum.
# Zbyt duży → większość osobników ma fitness ≈ 0 i wymiera w pierwszym pokoleniu.
#
# Wyprowadzenie: każda cecha startuje jako p_i ~ N(alpha0_i, init_scale²),
# więc ||p - alpha0||² ~ init_scale² * chi²(n),  E[||p-alpha0||²] = n * init_scale²
#
# Oczekiwane fitness w pokoleniu 0 (całka po rozkładzie chi²):
#
#   E[phi] = (1 + init_scale² / sigma²)^(-n/2)
#
# Stąd wzór na dobór init_scale dla zadanego minimalnego E[phi] = f_min:
#
#   init_scale <= sigma * sqrt( f_min^(-2/n) - 1 )
#
# Reguła praktyczna: init_scale = sigma / sqrt(n)
#   → E[phi] = (1 + 1/n)^(-n/2)  ≈  e^(-1/2) ≈ 0.61  (dla każdego dużego n)
#   → dla n=4: E[phi] = 1.25^(-2) ≈ 0.64  ✓  (populacja startuje zdrowo)
#
# Przykłady przy sigma=0.2, n=4:
#   init_scale = 0.10  →  E[phi] ≈ 0.64   ← obecna wartość, dobry start
#   init_scale = 0.30  →  E[phi] ≈ 0.24   ← populacja ledwo przeżywa selekcję
#   init_scale = 1.00  →  E[phi] ≈ 0.001  ← natychmiastowe wymarcie
init_scale = 0.1   # = sigma / sqrt(n) = 0.2 / 2 = 0.1
init_scale_tail = 0.15
init_sex_ratio = 0.5 # Ratio samców/samic - liczba to procent samców 

# --------------------
# PARAMETRY MUTACJI
# --------------------
mu = 0.3          # prawdopodobieństwo mutacji dla osobnika
mu_c = 0.5        # prawdopodobieństwo mutacji konkretnej cechy, jeśli osobnik mutuje
xi = 0.15         # odchylenie standardowe mutacji
                  # (mniejsze niż w 2D: w wyższych wymiarach duże kroki
                  #  są proporcjonalnie bardziej szkodliwe – tw. Fishera)

# --------------------
# PARAMETRY SELEKCJI
# --------------------
sigma = 0.3       # parametr w funkcji fitness (kontroluje siłę selekcji)
threshold = 0.01  # próg selekcji progowej
                  # (obniżony z 0.1 do 0.01: w 4D maksymalna tolerowana
                  #  odległość od optimum rośnie z 0.43 do 0.61)
tail_cost = 0.01

# --------------------
# PARAMETRY ŚRODOWISKA
# --------------------
# UWAGA: alpha0 i c są wyprowadzane z n.
# Wystarczy zmienić n powyżej – wektory środowiska dopasują się automatycznie.
zero_crossing = np.zeros(n)                            # punkt równowagi optymalnego fenotypu
amplitude = np.random.uniform(low=0, high=0.3,size =n) # Wektor amplitud, czyli największe możliwe odchylenie każdej z n cech fenotypu od punktu równowagi.
period = np.full(n, 40)                        # Wektor okresów sinusoidy w generacjach.
phase = np.random.uniform(low=-0.5, high=0.5,size = n)     # Wektor faz sinusoidy w generacjach.
delta = np.random.uniform(low=0, high=0.01,size = n)   # Wektor odchyleń std. losowych fluktuacji wokół funkcji (0 = brak szumu).
plateau_chance = 0.1                                   # Prawdopodobieństwo powstania równiny (zatrzymania się wszystkich wartości w wektorze na jakiś czas) w danej generacji.
mean_plateau_length = 8                                # Średnia długość równiny w rozkładzie geometrycznym.

max_generations = 200      # liczba pokoleń do zasymulowania

# ----------------------
# PARAMETRY REPRODUKCJI
# ----------------------
# W wersji bezpłciowej zakładamy klonowanie z uwzględnieniem mutacji.
# Jeśli chcemy modelować płciowo, trzeba dodać odpowiednie parametry.

# --------------------
# REPRODUKOWALNOŚĆ
# --------------------
# seed = None  →  inne wyniki przy każdym uruchomieniu
# seed = int   →  deterministyczne wyniki (do debugowania i raportów)
seed = 42
