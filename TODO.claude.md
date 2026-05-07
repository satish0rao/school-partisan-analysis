# TODO

Open items from prior sessions. Each entry includes enough context to resume without re-investigating.

## Old `kahuna.<prefix>.<test_set>.csv` files in `kahuna-files/` are tainted

Discovered while regenerating for 2012: `join_precinct_school_method2.py:33` had typo `testsIds = []` (extra "s") that created an unused variable instead of resetting the default `testIds = [7]`. Result: math runs (`testIds.append(int(argv[x]))` for argv `'9 10 11 12 13 14 15'`) ended up with `testIds = [7, 9, 10, 11, 12, 13, 14, 15]`, mixing ela (Test Id 7) into supposedly-math averages.

Fixed in this session (now `testIds = []`). All existing math kahuna files matching `kahuna-files/kahuna.<prefix>.9 10 11 12 13 14 15.csv` (and their urban/non-urban siblings) are contaminated. The `vote_achievement_correlations.csv` and `covariates_achievement_correlations.non-urban.csv` at the repo root were derived from these files, so the +0.352 white-afam math gap correlation reported in chat history is from contaminated data.

Action: regenerate analysis from the clean `<prefix>.<year>.<test>.csv` files now being produced. The old `kahuna.*.csv` files can be deleted once the new ones exist.

## NaN fix #3 — robust district join in `driver-one-table.py`

Two of three fixes are done (diagonal skip + constant-covariate skip, see `driver-one-table.py:76` and `:163-166`). The third — replacing the free-text name merge — is deferred.

Current code at `driver-one-table.py:194`:
```python
combined = combined.merge(nces_seda, left_on='District_x', right_on='leaname')
```

This drops ~4% of off-diagonal rows because California district names don't match cleanly between CDE and SEDA (`"Berkeley Unified"` vs `"Berkeley USD"` etc.).

What I verified before deferring:
- Kahuna files have a `District Code` column from CA CDS, dtype `int64`. Sample values: `61119`, `68338`, `71175` — these are **only 5 digits**, the district portion of the CDS code with no county prefix.
- NCES `ST_LEAID` (filtered to CA via `MSTATE15 == 'CA'`, 1097 rows) is a **7-character zero-padded string** like `'0061119'` containing county+district.
- A direct `District Code → ST_LEAID` join produces zero matches because the kahuna code is missing the 2-digit county prefix.

To make the ID merge work, either:
- (a) Add `County Code` (in `ca2012entities_csv.txt`) to the kahuna file in `join_precinct_school_method2.py:327`, then build the full CDS as `f"{county:02d}{district:05d}"` and join against `ST_LEAID`, or
- (b) Look up the county from `ca2012entities_csv.txt` at merge time in `driver-one-table.py` (no kahuna schema change, but couples the driver more tightly to the entities file).

Option (a) is cleaner and only touches the kahuna writer. Once kahuna has the full 7-digit CDS, the merge becomes:
```python
nces_seda_ca = nces_seda[nces_seda['MSTATE15'] == 'CA'].copy()
combined = combined.merge(nces_seda_ca, left_on='District CDS_x', right_on='ST_LEAID')
```

Note: existing kahuna CSVs would need regeneration to pick up the new column. Cheap — `join_precinct_school_method2.py` reuses `school_to_precinct.csv` (the slow part), so re-running the driver is fast.

## pyshp / dead imports cleanup

`pyshp` (imported as `shapefile`) is in `requirements.txt` but only needed when `school_to_precinct.csv` is missing. The 11 MB cache is committed, so normal runs never touch shapefile-reading code — yet the top-level `import shapefile as shp` still requires pyshp to be installed.

Two changes:
1. Move `import shapefile as shp` inside the cache-miss branch in `join_precinct_school_method2.py` (and `join_precinct_school.py`).
2. Strip the unused `import shapefile as shp` entirely from `driver.py`, `driver-one-table.py`, `driver-big-correlates.py`, `test.py` — none of them call `shp`.

After this, cached runs work without pyshp installed.

## Add ela counterparts to `tests` in `driver-one-table.py`

Lines 13-15 only include math for race groups (`afam`, `white`, and their econ_dis/econ_ok variants). Ela has only `male_ela`/`female_ela`. So race-vs-race comparisons exist only for math.

The missing entries are sitting in `not_used_tests` at lines 17-22:
```python
("afam",74,ela), ("afam_econ_dis",200,ela), ("afam_econ_ok",220,ela),
("white",80,ela), ("white_econ_dis",206,ela), ("white_econ_ok",226,ela)
```
Move these into `tests` to get the ela cross-race correlations.

## Save OLS results in `driver-big-correlates.py`

Lines 244, 253, 263, 275 each call `print(model.summary())` but the regression output isn't saved. To get a tidy "covariate impact on the gap" CSV, extract `model.params`, `model.pvalues`, `model.rsquared`, `model.nobs` from each fit into a long-format DataFrame and write to e.g. `ols_results.csv`.

## Shuffle null test for precinct join

To quantify how much of the observed `corr(diff, vote) ≈ 0.35` is real vs. spurious-from-CA-geography, shuffle the `school → precinct` mapping in `school_to_precinct.csv` and rerun the pipeline. The correlations should collapse to ~0; whatever residual remains is the floor cleared by random matching, and (observed − floor) is the signal attributable to the join.

## Commit hygiene

State at the time this TODO was written: py3 conversion across 8 files, `.gitignore` extended for Emacs/pyc, `CLAUDE.md` updated, `README.claude.md` and `TODO.claude.md` added (untracked), user manually deleted Emacs cruft (`#file#`, `.#file`, `junk`, `mv-ok-to`, etc.) and tracked-but-stale `params.pyc`.

If asked to commit: stage py3 conversions and gitignore as one logical commit; the deletions of editor cruft as a separate "remove tracked editor cruft" commit; docs (CLAUDE.md, README.claude.md, TODO.claude.md) as a third. User has not requested any of these — wait for explicit ask.
