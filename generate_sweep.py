import json
import os
import numpy as np

base_config = {
    "N": 1000, "n": 10, "xi": 0.05, "mu": 0.1, "mu_c": 0.5, "sigma": 0.2, 
    "c": 0.01, "init_scale": 0.1, "init_scale_tail": 0.15, "threshold": 0.05,
    "init_sex_ratio": 0.5, "bias": 0.01, "tail_c": 0.15, "tail_cost": 0.6, "temperature": 0.8,
    "n_replicates": 20, "reproduction": "sexual",
    "seeds": [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19],
    "max_generations": 200, "plateau_chance": 0.25,
    "amplitude_low": 0, "period": 40, "phase_low": -0.5, "phase_high": 0.5, "amplitude_high": 0.35,
    "delta_low": 0, "delta_high": 0.035
}

plateu_length = [2, 5, 15]

output_dir = "experiments/param_sweep_test3"
os.makedirs(output_dir, exist_ok=True)

for plateu in plateu_length:
    config = base_config.copy()
    
    # Ustawiamy parametry sweepu
    config['mean_plateau_length'] = plateu

    # Generujemy unikalną nazwę i opis
    name = f"PLATEU_{plateu}"
    config["name"] = name

    
    # Zapis do pliku
    with open(f"{output_dir}/{name}.json", "w") as f:
        json.dump(config, f, indent=4)