import json
import os
import numpy as np

base_config = {
    "N": 1000, "n": 10, "xi": 0.05, "mu": 0.1, "mu_c": 0.5,
    "c": 0.01, "init_scale": 0.1, "init_scale_tail": 0.15,
    "init_sex_ratio": 0.5, "bias": 0.02, "tail_c": 0.15, "tail_cost": 0.6, "temperature": 0.5,
    "n_replicates": 20, 
    "seeds": [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19],
    "reproduction": "asexual",
    "max_generations": 200, "plateau_chance": 0.2, "mean_plateau_length": 8
}

reproduction = ["sexual","asexual"]
sigmas = [0.2, 0.1]
thresholds = [0.01, 0.2]

output_dir = "experiments/param_sweep"
os.makedirs(output_dir, exist_ok=True)

for repro in reproduction:
    for sigma in sigmas:
        for thresh in thresholds:
            config = base_config.copy()
            
            # Ustawiamy parametry sweepu
            config['reproduction'] = repro
            config["sigma"] = sigma
            config["threshold"] = thresh
            
            # Generujemy unikalną nazwę i opis
            name = f"{repro}_sigma_{sigma}_threshold_{thresh}"
            config["name"] = name

            
            # Zapis do pliku
            with open(f"{output_dir}/{name}.json", "w") as f:
                json.dump(config, f, indent=4)