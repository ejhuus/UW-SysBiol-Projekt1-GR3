# Geometric Fisher Model — Evolutionary Simulation Framework

Fisher's Geometric Model (FGM) is one of the most influential theoretical
frameworks in evolutionary biology. It treats adaptation as a geometric
problem: a population occupies a cloud of points in an *n*-dimensional
phenotype space and must track a moving fitness optimum. This codebase
implements the model as a clean, extensible simulation that you can run,
inspect, and extend without modifying the core engine.

---

## PDF raportu

[Raport do projektu](RAPORT/Biologia_system_w_1_projekt.pdf)

## 📚 Documentation

| Guide | Contents |
|---|---|
| **[Mathematical background](docs/mathematical_background.md)** | Full formal specification — state spaces, fitness function, all four operators with probability distributions, statistics, Markov chain formulation, references |
| **[Running experiments](docs/running-experiments.md)** | Config file format, `run_experiment.py`, `run_many_experiments.py`, batch options, loading results in Python |
| **[Interactive viewer](docs/viewer.md)** | All four Streamlit pages — Overview, Single run, Compare, Parameter sweep, on-demand GIF generation |

---

## The model

Every individual carries a phenotype vector **p** ∈ ℝⁿ. The environment
defines an optimal phenotype **α**(t) at each generation. Fitness is a
Gaussian function of phenotypic distance from that optimum:

$$\varphi(\mathbf{p}, \boldsymbol{\alpha}) = \exp\!\left(-\frac{\|\mathbf{p} - \boldsymbol{\alpha}\|^2}{2\sigma^2}\right)$$

A perfect match gives φ = 1; fitness decays exponentially with distance.
The width σ controls how strict the environment is — smaller σ means only
near-perfect phenotypes survive.

### Baseline scenario — "global warming"

The optimum drifts steadily in a fixed direction with small stochastic
fluctuations:

$$\boldsymbol{\alpha}(t+1) = \boldsymbol{\alpha}(t) + \mathcal{N}(\mathbf{c},\, \delta^2 \mathbf{I})$$

where **c** is the mean drift per generation and δ adds noise. The population
must continuously adapt or go extinct. Above a critical drift speed ‖**c**‖
no population can keep up — this *critical drift threshold* is one of the key
quantities the model predicts.

### The evolutionary loop

Each generation runs four steps in order:

| Step | Operation | Implementation |
|------|-----------|----------------|
| 1 | **Mutation** — each trait *i* shifts by N(0, ξ²) with probability μ_c; whole individual mutates with probability μ | `IsotropicMutation` |
| 2 | **Selection** — individuals below a fitness threshold are removed; survivors are resampled proportionally to fitness up to N | `TwoStageSelection` |
| 3 | **Reproduction** — survivors are drawn with replacement to restore population size N | `AsexualReproduction`, `ProbabilitySexualReproduction`, `HierarchySexualReproduction` |
| 4 | **Environment update** — α shifts by **c** + N(0, δ²**I**) | `LinearShiftEnvironment`, `PeriodicEnvironment` |

> Mutation happens **before** selection, so new variation is exposed to
> selection within the same generation — matching the standard FGM formulation.

### Fisher's dimensionality effect

A key prediction of FGM is that adaptation becomes harder as n grows. In
high-dimensional spaces almost any random mutation is maladaptive, because
most directions in ℝⁿ move the phenotype *away* from the optimum. This is
why the mutation step size ξ must be tuned carefully: too large and all
mutations are harmful; too small and the population cannot keep pace with
the moving optimum.

---

## Quick start

```bash
pip install -r requirements.txt
python main.py
```

This runs 200 generations, saves PNG frames to `frames/`, assembles
`simulation.gif`, and opens a six-panel summary plot. All parameters live in
`config.py` — no other file needs to be touched for the baseline scenario.

### Example output

![Simulation GIF — baseline scenario (n=4, N=100, 200 generations)](simulation.gif)

*Baseline scenario: n = 4 trait dimensions, N = 100 individuals, 200 generations.
The fitness aura (green gradient) tracks the moving optimum (gold star).
Individuals are coloured from red (low fitness) to green (high fitness).
The fading white trail and arrow show the recent trajectory and predicted
next position of the optimum.*

---

## Key parameters (`config.py`)

| Parameter | Default | Meaning |
|-----------|---------|---------|
| `n` | 10 | Phenotype space dimensionality |
| `N` | 1000 | Population size |
| `sigma` | 0.2 | Selection tolerance (smaller = stricter) |
| `xi` | 0.05 | Per-trait mutation step size |
| `mu` / `mu_c` | 0.1 / 0.5 | Mutation probabilities (per individual / per trait) |
| `delta` | 0.01 | Stochastic noise added to drift |
| `threshold` | 0.01 | Minimum fitness for survival (stage 1 of selection) |
| `init_scale` | 0.1 | Spread of initial phenotypes around α₀ |
| `init_scale_tail` | 0.15 | Spread of initial tail size |
| `init_sex_ratio` | 0.5 | Ratio of men population in proportion to female population. |
| `seed` | 42 | RNG seed (`None` = different result each run) |
| `bias` | 0.02 | Directional mutation of tail size (after inheriting tail this scalar is added) |
| `tail_cost` | 0.6 | The cost of maintating a tail - decreases fitness |
| `temperature` | 0.5 | Parameter controlling how much much the tail increases sexual selection. (smaller = more strict) |
| `amplitude_low`, `amplitude_high` | 0/0.52 | Controlling the amplitude of the sinus wave |
| `phase_low`, `phase_high` | -0.5/0.5 | Vector of phases of sinusoid |
| `delta_low`, `delta_high` | 0/0.1 | Random fluctuations of the sinusoid |
| `plateu_chance` | 0.2 | Probability of a plateu occuring |
| `mean_plateu_length` | 8 | Mean length of a plateu |


> `alpha0` and `c` are derived from `n` automatically — changing `n` is
> safe; no manual vector resizing needed.

---

## Repository structure

| File / directory | Role |
|------------------|------|
| `config.py` | All simulation parameters — **start here** |
| `strategies.py` | Abstract base classes for the four extension interfaces |
| `main.py` | `run_simulation()` loop and GIF assembly |
| `individual.py` | `Individual` — single phenotype vector |
| `population.py` | `Population` — container with initialisation logic |
| `mutation.py` | `IsotropicMutation` |
| `selection.py` | `TwoStageSelection`, `ThresholdSelection`, `ProportionalSelection` |
| `reproduction.py` | `AsexualReproduction` |
| `environment.py` | `LinearShiftEnvironment` |
| `periodic_environment.py` | `PeriodicEnvironment` |
| `probability_sexual_reproduction.py` | `ProbabilitySexualReproduction` |
| `hierarchy_sexual_reproduction.py` | `HierarchySexualReproduction` |
| `stats.py` | `SimulationStats` — per-generation metrics, numpy array properties |
| `visualization.py` | GIF frame generation and summary plots |
| `run_experiment.py` | Single-experiment parallel runner |
| `run_many_experiments.py` | Batch runner — directories, globs, prefixes |
| `viewer.py` | Streamlit interactive explorer |
| `experiments/` | JSON experiment configs (one file = one reproducible condition) |
| `results/` | Generated output — **not committed**, lives only locally |
| `docs/` | Detailed documentation (see links at the top) |

---

## Extending the framework

All four evolutionary steps are **pluggable**. To add a new mechanism:

1. **Subclass** the appropriate ABC from `strategies.py`:
   `MutationStrategy`, `SelectionStrategy`, `ReproductionStrategy`, or
   `EnvironmentDynamics`
2. **Implement** the required method(s) — Python raises `TypeError`
   immediately if any abstract method is missing
3. **Pass** your instance to `run_simulation()` in `main.py`

Nothing else needs to change. Each extension lives in its own file.

### Adding a new statistic

Write into the `extra` dict on each `GenerationRecord`, then read it back:

```python
# inside your simulation (e.g. in a SimulationStats subclass):
stats.records[-1].extra['my_metric'] = some_value

# read back as a numpy time series:
series = np.array([r.extra.get('my_metric', np.nan) for r in stats.records])
```

For a cleaner solution, subclass `SimulationStats` and override `record()`.
The docstring in `stats.py` shows the exact pattern.
