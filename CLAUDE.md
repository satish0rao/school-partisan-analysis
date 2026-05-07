# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Language and runtime

Python 3. The drivers shell out to workers via `python3 ...` in `os.system` calls.

Dependencies: `pandas`, `pyshp` (imported as `shapefile`), `scipy`, `statsmodels`, `numpy`.

## Setup and common commands

```bash
make init                              # virtualenv env
make env                               # env/bin/pip install -r requirements.txt
make data                              # wget SEDA covariate CSVs from data.txt into seda/
```

Before running anything, unzip the score files inside `school-data/` (e.g. `ca2013_all_csv_v3.zip`) — they're gitignored.

The README's stated entry point is `python driver-one-table.py`. The newer driver is `driver-big-correlates.py`, which adds OLS regressions on SEDA covariates. `driver.py` is older/legacy.

There are no tests, no linter, no CI. `quick_test.py` and `test.py` are ad-hoc analysis scripts, not a test suite — `quick_test.py` prints correlations between two `kahuna.*.csv` files; `test.py` is a sanity check that scipy/numpy/statsmodels regression APIs agree.

## Pipeline architecture

Goal: correlate California school test scores (by demographic subgroup) with 2016 precinct-level Clinton/Trump vote share, optionally controlling for SEDA district covariates.

The drivers (`driver.py`, `driver-one-table.py`, `driver-big-correlates.py`) are **shell orchestrators** — they `os.system(...)` out to the worker scripts below rather than importing them. They build a list of `(demographic_prefix, subgroup_id, test_set)` tuples and run the pipeline once per tuple.

Per-tuple pipeline (driven by `os.system` calls):

1. **Split scores by demographic** — `school-data/split_by_demo.py <out.txt> <subgroup_id> [year]` filters the giant `ca{year}_all_csv_v3.txt` (or `sb_ca2017_all_csv_v2.txt` for 2017) by `Subgroup ID` in chunked reads, writing `school-data/<prefix>.<year>.txt`. Subgroup IDs (e.g. 74=afam, 80=white, 78=hispanic, 200=afam econ-disadvantaged, 220=afam econ-ok, 3=male, 4=female, 1=all) come from CDE's STAR/CAASPP file layout.
2. **Join schools to precincts and votes** — `join_precinct_school_method2.py <scores.txt> <year> <test_ids...>` is the heart of the project. It:
   - Reads `school-data/ca2012entities_csv.txt`, `zipcodes/...`, the precinct shapefiles in `election-data/california-2016-election-precinct-maps/shapefiles/*.shp`, and `all_precinct_results.csv`.
   - **Caches** the school↔precinct mapping to `school_to_precinct.csv`. This file is expensive to regenerate (it iterates every shape and does a coarse-grid nearest-zipcode lookup via `geom_lookup`); delete it only when shapefiles or zipcode data change.
   - Tags each precinct as urban/non-urban based on whether its shapefile is in `urban_shapefiles = ['037-los-angeles.shp', '075-san-francisco.shp']`. A school is urban if ≥ half its matched precincts are urban.
   - Filters score rows to specified `Test Id`s (math = `9 10 11 12 13 14 15`, ela = `7`) and grades (hardcoded to 9/10/11), aggregates `Percentage At Or Above Proficient` (2013) or `Percentage Standard Met and Above` (2017) weighted by `Students Tested`, and writes `kahuna.csv`.
   - Score-row inclusion is gated by `params.include_urban()` / `params.include_non_urban()`.
3. **Move output** — drivers `mv kahuna.csv` to `<root_for_outfiles>/<prefix>.<year>.<test_set>.csv`.

`join_precinct_school.py` is **method 1** (zipcode-match only, an earlier/simpler version). `join_precinct_school_method2.py` is **method 2** (nearest-zipcode geometric match) and is what the drivers actually call.

## The `params.py` swap pattern

There are four params files: `params_all.py`, `params_urban.py`, `params_non_urban.py`, `params_only_urban.py`. Each defines `include_urban()` and `include_non_urban()` returning bools. The drivers pick one based on top-of-file booleans:

```python
if urban == False:       root_for_outfiles, param_file = 'non-urban-kahuna-files', 'params_non_urban.py'
elif non_urban == False: root_for_outfiles, param_file = 'urban-kahuna-files',     'params_urban.py'
else:                    root_for_outfiles, param_file = 'kahuna-files',           'params_all.py'
```

…then `cp <param_file> params.py` so the worker scripts pick it up via `import params`. **`params.py` is overwritten on every driver run** — don't hand-edit it; edit the source `params_*.py` instead. Output directory must match the params file (the three `*-kahuna-files/` dirs).

## Output layout

- `kahuna-files/` — both urban and non-urban
- `urban-kahuna-files/` — urban only
- `non-urban-kahuna-files/` — non-urban only

Filename convention: `<prefix>.<year>.<test_set>.csv` where `<test_set>` is the literal Test-Id string (e.g. `"9 10 11 12 13 14 15"`) for old `driver.py`, or `"math"`/`"ela"` for the newer drivers via `ts_name()`. Existing output files are **not regenerated** — drivers skip the pipeline if the target CSV already exists, so to force a rerun delete the file.

After the per-tuple loop, drivers do an all-pairs cross-merge of kahuna CSVs on `School Code`, compute `diff = score_y - score_x`, correlate with `vote_y`, and write `vote_achievement_correlations.csv`. `driver-big-correlates.py` additionally merges in SEDA covariates (`seda/SEDA_cov_geodist_pool_v20.csv`, joined on district name `District_x` ↔ `leaname`) and runs `statsmodels.OLS` regressions of `diff` on covariate sets. `driver-one-table.py` writes `covariates_achievement_correlations.csv` instead.

## Data sources (gitignored, fetch manually)

- `school-data/` — CDE STAR (2013) and CAASPP/Smarter Balanced (2017) score files. `school-data/README` has URLs.
- `election-data/california-2016-election-precinct-maps/` — clone from `github.com/datadesk/california-2016-election-precinct-maps`.
- `seda/SEDA_cov_geodist_pool_v20.csv` — Stanford SEDA district covariates (`make data` fetches it).
- `nces/ccd_lea_052_1516_w_1a_011717.csv` — NCES district directory; used only by `driver-one-table.py` and `get_covariates.py` to bridge SEDA `leaidC` ↔ NCES `ST_LEAID`.
- `zipcodes/US Zip Codes from 2013 Government Data` — ZIP↔lat/lng table.

## Gotchas

- The repo is full of Emacs auto-save and lock-file noise (`#file#`, `.#file`, `file~`). Ignore them; don't commit them.
- `kahuna.csv` at the repo root is a **transient** output of `join_precinct_school_method2.py` — drivers move it after each iteration. Don't treat it as a stable artifact.
- `school_to_precinct.csv` is huge (~11 MB) and regenerating it takes a long time. The cache check is `os.path.isfile(...)`, so any non-empty file at that path will be reused — if you suspect it's stale, delete rather than truncate.
- `driver-big-correlates.py` reassigns `tests` multiple times (lines 16-34); only the last assignment wins. Check which line is uncommented before assuming what will run.
- Hardcoded paths assume the shell is in the repo root (the workers do `pd.read_csv("school-data/...")`). Drivers `cd school-data; ...; cd ..` for `split_by_demo.py` only.
