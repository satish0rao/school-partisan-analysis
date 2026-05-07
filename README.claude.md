# File-by-file reference

Grouped by role. Files not directly read are described from filename + how the drivers use them.

## Drivers (orchestrators)

- **`driver.py`** — oldest driver. Builds a `tests` list (hispanic/asian variants), shells out to `split_by_demo.py` → `join_precinct_school_method2.py`, then runs `quick_test.py` for every pair of outputs. Python 2 prints. Largely superseded.
- **`driver-one-table.py`** — README's stated entry point. Same pipeline as `driver.py`, but builds two big tables: (a) `vote_achievement_correlations.csv` (cross-pair `diff`-vs-vote correlations) and (b) `covariates_achievement_correlations.csv` (same cross-pairs ✕ every numeric SEDA covariate, joined via NCES↔SEDA on `LEAID`).
- **`driver-big-correlates.py`** — newest driver. Same orchestration, but the second phase runs `statsmodels.OLS` regressions of `diff` on selected SEDA covariates (`paredVblkwht`, `perblk`, `occsales_fem`, etc.) and on `vote_x`, plus a random-noise control regression. The `tests` variable is reassigned multiple times (lines 16-34) — only the last uncommented assignment wins.

## Workers

- **`join_precinct_school.py`** — Method 1: match school zipcode → precincts with same zipcode. Earlier, simpler version.
- **`join_precinct_school_method2.py`** — Method 2: nearest-zipcode geometric match via the `geom_lookup` coarse-grid scan. This is what the drivers actually call. Caches school↔precinct mapping to `school_to_precinct.csv`. Tags precincts urban/non-urban based on which shapefile they came from. Writes `kahuna.csv`.
- **`school-data/split_by_demo.py`** — Filters the giant CDE score file by `Subgroup ID` in chunked reads (chunksize 10⁵). Writes `school-data/<prefix>.<year>.txt`.

## Params

- **`params.py`** — overwritten on every driver run by `cp <chosen>.py params.py`. Don't hand-edit.
- **`params_all.py`** — both `include_urban()` and `include_non_urban()` return True.
- **`params_urban.py`** — urban only.
- **`params_non_urban.py`** — non-urban only.
- **`params_only_urban.py`** — same idea, urban-only variant. Possibly redundant with `params_urban.py`.

## Ad-hoc / utility scripts

- **`quick_test.py`** — takes two `kahuna.*.csv` files, merges on `School Code`, prints `diff`-correlation and `describe()`. Used by `driver.py`.
- **`test.py`** — sanity check that `scipy.stats.linregress`, `np.corrcoef`, `np.linalg.lstsq`, `pandas.corr()`, and `statsmodels.OLS` agree on a hand-coded X/Y. Not a unit test.
- **`get_covariates.py`** — three-line snippet that joins NCES↔SEDA on `LEAID` and pulls `[LEAID, ST_LEAID]`. Looks like an interactive scratch.

## Build / config

- **`Makefile`** — `make init` creates virtualenv, `make env` installs requirements, `make data` wgets URLs from `data.txt` into `seda/`.
- **`requirements.txt`** — pandas, pyshp, scipy, statsmodels.
- **`data.txt`** — two SEDA URLs for `make data`.
- **`README.md`** — short usage note + data source pointers.
- **`.gitignore`** — `*.txt`, `*.zip`, `*.csv`, the election-data clone dir.

## Data directories

- **`school-data/`** — CDE STAR (2013) + CAASPP Smarter Balanced (2017) score files; `ca2012entities_csv.txt` is the school↔district↔county directory. `README` has source URLs. Score files arrive as zips and must be unzipped.
- **`election-data/`** — `california-2016-election-precinct-maps/` (datadesk repo: shapefiles + `final-results/all_precinct_results.csv`). `harvard/` likely an alternate dataset.
- **`zipcodes/`** — `US Zip Codes from 2013 Government Data`: ZIP↔lat/lng table used to geolocate schools.
- **`seda/`** — Stanford SEDA `SEDA_cov_geodist_pool_v20.csv` district covariates.
- **`nces/`** — `ccd_lea_052_1516_w_1a_011717.csv`: NCES district directory; bridges SEDA `leaidC` ↔ NCES `ST_LEAID`.
- **`edfacts/`** — `math-achievement-lea-sy2015-16.csv`. Not referenced by any driver/worker I read; appears unused.
- **`stupid-scripts/`** — one-off shell-rename scripts (`mv-econ`, `mv-not-to-econ-ok.py`). Author-named "stupid" for a reason.

## Output directories

- **`kahuna-files/`** — outputs when both urban and non-urban schools are included.
- **`urban-kahuna-files/`** — urban-only outputs.
- **`non-urban-kahuna-files/`** — non-urban-only outputs.

## Cached / generated artifacts at repo root

- **`school_to_precinct.csv`** — ~11 MB cache of school↔precinct mapping. Expensive to regenerate; `join_precinct_school_method2.py` reuses it if present.
- **`precincts_zipcodes.csv`** — older method-1 cache (precinct → zip+lat/lng).
- **`vote_achievement_correlations.csv`** — output of `driver-one-table.py` / `driver-big-correlates.py` first phase.
- **`covariates_achievement_correlations.csv`** — output of `driver-one-table.py` covariate phase. The `.non-urban.csv` variant is the non-urban run.
- **`kahuna.afam.2.csv`, `kahuna.white.csv`, `kahuna.hispanic.csv`, `afam_kahuna.csv`, `sorted_schools_by_difff.csv`, `tmp.csv`** — stray outputs from earlier runs that escaped the move-to-`<root>/` step. Not authoritative.

## Editor cruft (ignore, don't commit)

- **`#file#`** — Emacs auto-save buffers (`#README.md#`, `#driver-big-correlates.py#`, etc.).
- **`.#file`** — Emacs lock symlinks pointing to a long-dead PID/host.
- **`file~`** — Emacs backup-on-save files (`driver.py~`, `params.py~`, etc.).
- **`junk`, `mv-ok-to`, `mv-econ~`, `mv-not-to-econ-ok.py~`** — scratch/leftovers.
- **`params.pyc`** — Python 2 bytecode cache.
