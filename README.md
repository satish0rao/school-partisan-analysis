# California School Achievement vs Precinct Vote Share

This project analyzes the relationship between California public school test scores (CAASPP/SBAC and earlier STAR) and 2016 precinct-level Clinton/Trump vote share, with focus on Black-white achievement gaps and how they correlate with the political composition of the surrounding precinct.

## ⚠ Caveat

**This is a working repository, not a final report.** The findings below come from an extended analytical session against 2012–2025 California testing data and have been revised multiple times as methodological issues surfaced — caching mistakes caught and corrected, sample-coverage problems identified, framing choices reconsidered, causal-language slippage tightened. They are **observational/associational, not causal**. Read them as "this is what the data looks like, here are the caveats" rather than as a peer-reviewed study.

For transparency, the iteration is preserved in the repo rather than hidden:

- `analysis_findings.md` — structured methodological notes, including earlier framings that were later corrected
- `conversation_transcript.md` — verbatim transcript of the analytical conversation, including pushback, corrections, and dead ends
- Git history — successive tightenings of language and framing are visible commit-by-commit

Generalizations beyond California 2025 should be made carefully. Anyone is welcome to re-run the pipeline against newer data, find further bugs, or push back on framings — the repo is set up for that.

## Findings

### 1. Liberal California precincts have larger Black–white test score gaps in their schools than conservative precincts

The pattern is consistent across years, subjects, and grade bands. Within-econ_ok matched-gap-vote correlations (scale score, n≥11 per group per school):

| Year | G6-8 ELA | G6-8 math | G9-11 ELA | G9-11 math |
|---|---|---|---|---|
| 2018 | +0.41 | +0.41 | +0.18 | +0.17 |
| 2019 | +0.43 | +0.39 | +0.25 | +0.26 |
| 2022 | +0.44 | +0.48 | +0.41 | +0.53 |
| 2023 | +0.45 | +0.59 | +0.43 | +0.38 |
| 2024 | +0.44 | +0.52 | +0.51 | +0.50 |
| 2025 | +0.59 | +0.48 | +0.42 | +0.53 |

**Read:**
- **Middle school (G6-8)**: consistent +0.39 to +0.59 across all six years. 12 of 12 cells at +0.39 or stronger. Not a post-COVID artifact.
- **High school (G9-11)**: +0.40 to +0.53 in all four post-COVID years (2022, 2023, 2024, 2025). The 2018-2019 dip (+0.17 to +0.26) appears to be an SBAC-rollout measurement artifact, not a real pre-COVID baseline (see STAR below).
- **G3-5 econ_ok** mostly suppresses out — Black middle-class elementary populations rarely reach n≥11 at the school level. Race-only Gap A at G3-5 shows +0.17 to +0.28 vote correlations (weaker than MS/HS) but is reliably positive.
- **STAR (2012-2013)**: Gap B HS math was already +0.39 to +0.61 school-weighted (+0.55 to +0.74 student-weighted) at n≥11/group — comparable to the 2022-2025 SBAC era. So the pattern is **durable across testing regimes**, with a measurement-period anomaly in early SBAC (2018-2019). The corr(afam_econ_ok, vote) ranged from −0.20 to −0.51 in STAR — the same "Black scores fall in liberal precincts" signature visible today.

The pattern also holds across methodological choices: school vs student weighting, strict vs matched cutoffs, school vs district aggregation, tested-weighted vs enrolled-weighted within-grade aggregation, and across three score measures (Met & Above, Nearly Met & Above, Mean Scale Score). Scale scores show stronger signal than percent-proficient cuts, and the partisan effect is **not** an artifact of cut-point compression. See `analysis_findings.md` for the methodological iteration.

### 2. The signal is strongest among non-economically-disadvantaged Black vs white at high school math

For 2025 G11 econ_ok math:
- School-weighted matched-gap-vote correlation: **+0.51**
- Student-weighted (harmonic mean): **+0.62**
- District-level (matching SEDA's geographic unit): **+0.66**
- After controlling for white-parent BA+ rate, racial integration, within-district resource sorting, and charter density: β_vote = **+27** (p=0.05) at school level, **+26** (p=0.09) at district level

### 3. Two-sided mechanism

For 2025 G11 econ_ok math, score-by-vote correlations:
- Middle-class white students score **higher** in liberal precincts (corr +0.34 to +0.41)
- Middle-class Black students score **lower** in liberal precincts (corr −0.31 to −0.48)
- Both contribute to the gap-widening
- Hispanic and Asian middle-class show much weaker score-vote correlations (mostly flat or weakly negative)

The Hispanic-white gap-vote correlation (+0.42) is meaningful but smaller than Black-white (+0.62), driven mostly by the white-rises effect since Hispanic doesn't fall. This is important for interpreting the Black-white headline: the white-rises mechanism is doing substantial work in the Black-white gap correlation as well. The Black-falls effect is the distinguishing feature of the Black-white gap relative to Hispanic-white, but a reader should not interpret the +0.62 as if Black-falls explained all of it.

### 4. Trajectory through schooling

afam student score-vote correlations by grade band (2025 math):

| grade | afam (all) | afam_dis | afam_OK |
|---|---|---|---|
| G3-5 | **+0.252** | +0.335 | (small sample) |
| G6-8 | +0.023 | +0.100 | −0.069 |
| G11 | −0.064 | +0.036 | **−0.311** |

At elementary, Black students score *higher* in liberal precincts. By HS, middle-class Black students score lower. The within-Black econ gap **narrows** in liberal areas at both grade levels — but for opposite reasons: at G3-5 because afam_dis rises faster than afam_OK; at HS because afam_OK falls toward afam_dis.

### 5. Course-tracking inflates the level of the gap but doesn't drive the political variation

STAR 2013, econ_ok pair, G9-11:

| course | % afam_econ_ok | % white_econ_ok |
|---|---|---|
| GenMath (low track) | 34% | 22% |
| Geometry | 32% | 31% |
| Algebra II | 24% | 28% |
| Summative (advanced) | 9% | 19% |

afam_econ_ok students are 1.6× more likely in low-track GenMath, half as likely in advanced Summative. **But the within-test gap-vote correlation is +0.30 to +0.47 in EVERY test separately.** Course-tracking inflates the LEVEL of the gap but doesn't drive the political variation.

### 6. Geographic concentration

Within-metro 2025 G11 econ_ok math gap-vote correlation:

| metro | n schools | gap-vote corr |
|---|---|---|
| Bay Area (SF/Oak/Berk) | 11 | **+0.90** |
| LA region | 10 | **+0.86** |
| Sacramento County | 10 | +0.13 |
| San Diego County | 4 | (too few) |
| Rest of California | 61 | +0.30 |

Pattern is concentrated in Bay Area and LA. Sacramento County, with n=10 schools, shows essentially no gap-vote correlation (+0.13) — this is genuine counter-evidence that the pattern is not uniformly statewide. The "Rest of California" +0.30 is also much weaker than the Bay Area / LA headline. Bay Area shows both Black-falls AND white-rises strong; LA shows mostly the white-rises effect (Black scores roughly flat across LA precincts). Interpreting the statewide correlation requires acknowledging that two metros (Bay Area + LA) drive most of the signal.

### 7. Berkeley is an outlier but not unique

Dropping the top-10% of districts by white-BA+ rate (excludes Berkeley, Pasadena, Santa Monica-Malibu):

| sample | β_vote alone | + baplus_wht | + all 4 covs |
|---|---|---|---|
| Full | +60.3 | +34.4 | +30.3 |
| Drop top-10% baplus | +43.9 | +35.2 | +32.8 |
| Drop top-20% baplus | +37.9 | +34.0 | +35.7 |

The univariate effect drops without Berkeley-tier districts. But the controlled coefficient stays at ~+34 — the pattern generalizes to ordinary high-baplus liberal California, not just professor/PhD enclaves.

### 8. Per-pupil spending doesn't predict Black achievement

District-level correlations:

| year | corr(ppexp, **afam** score) | corr(ppexp, **white** score) | corr(ppexp, vote) |
|---|---|---|---|
| 2013 | +0.06 | +0.24 | +0.59 |
| 2018 | −0.18 | −0.01 | +0.50 |
| 2022 | −0.08 | +0.30 | +0.62 |
| 2025 | +0.01 | +0.31 | +0.63 |

Per-pupil spending is strongly correlated with vote share (high-cost-of-living liberal districts spend more) and with white scores (especially 2022/2025). It does **not** correlate with Black scores in any year. Higher district spending tracks higher white-student outcomes but not higher Black-student outcomes.

### 9. Cross-state and external evidence is consistent with the within-CA pattern

- Mississippi, Florida, Texas outperform California on Black-student NAEP despite worse demographics
- Mississippi's Literacy-Based Promotion Act (2013, science-of-reading + accountability) was followed by large Black-student NAEP gains (causal attribution to the Act specifically is contested — other reforms ran in parallel)
- Roland Fryer's Houston RCT (Apollo 20) found that charter-style "no-excuses" methods produced large Black-student gains when injected into traditional schools (this one is RCT-identified)
- KIPP, Wilder's Prep, Rocketship, Success Academy all show high-rigor approaches producing strong Black achievement
- Sean Reardon's SEDA work documents Black-white gaps as largest in heavily-progressive-affluent districts
- Stanford "Acting White" research (Fryer-Torelli) documents within-school peer-comparison effects in integrated upper-middle-class settings

These external lines are *consistent with* the within-California pattern, though the causal evidence varies in quality (Fryer 2014 is an RCT; the Mississippi/Florida cross-state comparisons are quasi-experimental at best, and the Reardon SEDA work is descriptive). The cross-sectional within-California data established here cannot adjudicate between competing causal mechanisms — pedagogical choices, housing-market sorting, differential teacher quality, peer-composition effects, and others all remain on the table.

### 10. Black students at charters score better than at district schools, especially in liberal areas

2025 SBAC math, mean Black student proficiency by school type × precinct vote bucket:

**G3-5 elementary (afam):**

| school type | Trump | Mixed | Liberal | Strong Clinton |
|---|---|---|---|---|
| district | 13.1% (n=2,681) | 18.3% (n=4,512) | 21.0% (n=5,697) | 22.2% (n=5,070) |
| **charter** | 13.5% (n=155) | 34.0% (n=100) | 22.5% (n=961) | **28.0%** (n=2,646) |
| charter advantage | +0.4 | +15.7 (n=100, noisy) | +1.5 | **+5.8** |

**G6-8 middle (afam):** (per-cell n's not recorded for this breakdown; G6-8 Black coverage is ~59% statewide so cells are larger than G3-5 on average)

| school type | Trump | Mixed | Liberal | Strong Clinton |
|---|---|---|---|---|
| district | 14.9% | 18.0% | 14.2% | 16.0% |
| **charter** | 15.7% | 25.8% | **23.7%** | 19.4% |
| charter advantage | +0.8 | +7.8 | **+9.5** | +3.4 |

**G11 high school (afam, sample sizes shrink):**

| school type | Trump | Mixed | Liberal | Strong Clinton |
|---|---|---|---|---|
| district | **17.5%** | 14.9% | 14.5% | 14.5% |
| charter | 8.8% (n=262) | 13.4% | 17.5% | 14.3% |
| charter advantage | −8.7 | −1.5 | +3.0 | −0.2 |

**Pattern:**
- At elementary and middle school, charters show their **biggest advantage in liberal areas** (Strong Clinton bucket at G3-5: +5.8 pts on n=2,646 Black charter students — roughly 34% of all Black G3-5 students in Strong Clinton precincts attend charters, reflecting the concentration of Black-serving networks like KIPP LA, Aspire Bay Area, Rocketship, Wilder's Prep, and Fortune in South LA / Compton / Oakland / SF; Liberal bucket at G6-8: +9.5 pts). The Mixed bucket at G3-5 shows a much larger +15.7 advantage but on only n=100 charter students, too small to lean on.
- In conservative areas (Trump bucket), district-charter difference is small or even reversed
- HS samples are too small for clean comparison; mixed picture

This connects to the broader research on no-excuses charter networks (KIPP Compton, Wilder's Preparatory, Rocketship, Aspire) that explicitly run structured-instruction programs serving Black students in liberal urban California. They tend to outperform the surrounding district schools, with the gap largest in the most-Democratic precincts.

The empirical observation is that **Black-serving charters in liberal urban California outperform the local district schools for Black students at elementary and middle school math**. The mechanism — pedagogical content, scheduling/discipline, family-motivation selection, principal autonomy, teacher hiring practices, school-day length, or some combination — is not identified by this cross-sectional comparison.

**Roland Fryer's work is particularly relevant here.** Fryer (Harvard economist, MacArthur Fellow) has produced the cleanest causal evidence on what makes schools effective for Black students:

- **"Injecting Charter School Best Practices into Traditional Public Schools"** (Fryer 2014, *Quarterly Journal of Economics*) — RCT study of the Apollo 20 program in Houston ISD, injecting no-excuses charter practices (extended day, intensive tutoring, frequent assessments, high behavioral and academic expectations, data-driven instruction) into 20 of Houston's lowest-performing district schools. Result: substantial Black student gains, on the order of 0.15–0.40 SD per year. Showed the effective ingredients of charter-style schooling can be reproduced inside traditional public schools when administrators choose to.
- **"The Production of Human Capital in Developed Countries: Evidence from 196 Randomized Field Experiments"** (Fryer 2017) — meta-analysis: high-dosage tutoring + structured curriculum + expectations have larger Black-student effects than wraparound services or "broader" interventions.
- **Harlem Children's Zone / Promise Academy work** (Dobbie & Fryer 2011, 2013) — the school component (KIPP-style pedagogy) was responsible for nearly all of the gap-closing effect, not the surrounding wraparound services.
- **"Acting White"** (Fryer & Torelli 2010) — documented within-school peer-comparison effects: Black students at racially integrated upper-middle-class schools face peer dynamics that depress achievement, not present at homogeneously-Black schools.

Fryer's program is one of the most rigorous (RCT-based, replicated, peer-reviewed) evidence bases for high-dosage tutoring + structured curriculum + high expectations as effective ingredients for Black-student achievement.

### 11. Substantial Black-student missingness in the data

| filter step | % of CA Black G3-5 retained |
|---|---|
| Estimated CA Black G3-5 (3 grades × ~25K) | 100% |
| Visible in SBAC (any reported value) | 63% |
| After suppression filter (n≥11 reporting threshold) | 34% |
| With vote merged | 24% (28% after charter geocoding addendum) |

37% of Black elementary students are missing from SBAC entirely (private school, opt-out, chronic absence). 46% of those reported have school-level scores suppressed. **Findings generalize to roughly 1/3 of California's Black elementary students.** HS coverage is somewhat better (~65%).

### 12. The matched-pair filter selectively retains schools where both groups co-exist

The headline +0.62 correlation is computed on schools where both econ_ok afam AND econ_ok white students appear in reportable numbers (n≥11 each). That's:

- 97 schools statewide for HS econ_ok math
- 1,972 Black econ_ok students ≈ **46% of California's 4,305 Black econ_ok HS math test-takers** in the 2025 SBAC file. Because Black econ_ok is only ~22% of all Black HS students (the remaining ~71% are econ_dis), the sample covers roughly **10% of all California Black HS students**.

These are unusual schools — diverse suburban, magnet, integrated affluent westside — not representative of where most Black students go. **70% of Black HS students attend majority-Hispanic schools** where the Black-white gap can't be measured because there aren't enough white peers. And among the schools we *can* measure, the OLS regressions with full SEDA controls run on a smaller subset (~69 schools, ~1,371 econ_ok Black students) because some schools are missing district-level covariates.

### 13. Substantive interpretation (caveated)

The cross-sectional pattern is consistent with a *structural-systems* story rather than an individual-bias one:

- After controlling for plausible district-level covariates (white-parent BA+ rate, racial integration, within-district resource sorting, charter density), a residual political-composition effect on the Black-white gap remains at HS math (§2).
- Candidate mechanisms supported by external literature include: housing-market sorting into extreme-cost precincts; within-school tracking and AP/honors gating; within-school differential teacher expectations (documented in Berkeley High case studies, Pollack 2004, Noguera and others); and pedagogical-choice differences across districts.
- Cross-state quasi-experimental evidence (Mississippi LBPA, Florida third-grade retention, charter-network RCTs) is a stronger evidence base than this study for any specific policy mechanism. This study identifies a robust within-California cross-sectional pattern; it cannot adjudicate which mechanism is doing the work.

Readers should be cautious about translating these correlations into policy prescriptions. The findings are consistent with multiple causal stories, including some that don't reduce to "liberal districts are pedagogically failing Black students" — e.g., that extreme housing-price stratification has demographically sorted middle-class Black families into structurally difficult circumstances that even well-resourced districts struggle to overcome.

### 14. Attendance shows the same pattern as scores

Attendance is a behavioral outcome variable, not a confounder — it's downstream of the same school / family / neighborhood / district conditions that affect test scores. So this finding is a *corroborating outcome*, not an explanation that reduces the score finding.

The Black-white absenteeism *gap* (Black chronic-absence rate − white chronic-absence rate) is correlated with precinct vote, and the correlation is stronger at higher-SES schools — the same SES gradient seen in the score-gap pattern:

| sample | n schools | corr(absenteeism gap, vote) |
|---|---|---|
| All schools (n≥11/group) | 3,445 | +0.13 |
| All schools (n≥30/group) | 1,520 | +0.18 |
| econ_ok proxy (sed_share ≤ 0.40, n≥30) | 201 | **+0.39** |
| Very low econ_dis (sed_share ≤ 0.20, n≥11) | 121 | +0.36 |
| High econ_dis (sed_share ≥ 0.70, n≥30) | 826 | +0.10 |

Subgroup absenteeism-vote correlations (2025, school-weighted): afam **+0.143**; white **−0.076**; Hispanic +0.039; Asian +0.006; all_students ≈ 0. Black students are more chronically absent in liberal precincts; white students are less. This directionally matches the §3 score pattern (Black falls, white rises in liberal precincts), now visible in a second behavioral measure that doesn't go through the SBAC suppression filter.

**Two outcome variables moving together is corroborating evidence, not a confound.** Vote correlates with multiple downstream outcomes — test scores AND attendance — in the same direction at the same schools. The fact that both move with vote is consistent with there being a common upstream cause; it doesn't tell us what that cause is, but it does suggest the pattern isn't an artifact of any single measurement system (SBAC suppression, cut-point compression, etc.).

**A caution on the regressions.** It's tempting to add `absent_gap` to the score-gap regression and report that the vote coefficient shrinks (it does: at HS-math econ_ok Gap B, β_vote: 168 → 136 with absent_gap alone; 76 → 63 with absent_gap added to full SEDA controls). But this is **bad-control reasoning** — partialling out a mediator and then reading the residual as the "true" political effect. If vote → environment → both attendance and scores, then conditioning on attendance is conditioning on a downstream outcome and biases the vote coefficient toward zero. The mechanically correct regression numbers are in `results/absent_vs_vote_controlled.csv`; the interpretation "attendance explains some of the score-gap-vote effect" should be made cautiously, with the mediator-control issue acknowledged.

**What this finding does say, cleanly:** Liberal California precincts have larger Black-white *behavioral* gaps (attendance) in addition to larger Black-white *cognitive* gaps (scores), at the same schools, with the same SES gradient. Both gaps strengthen at higher-SES schools, both weaken in conservative precincts, and both are stronger in metros than rural areas. This widens the empirical pattern from "scores" to "scores + attendance" and makes it harder to attribute purely to test-specific artifacts.

## Caveats and limitations

- **Associational, not causal.** Cross-sectional data cannot identify causal mechanisms; the patterns are consistent with multiple causal stories.
- **Coverage bias.** Substantial fractions of Black students are missing from the analyzable data, especially at elementary.
- **Pre-SBAC selection (who appears in the file at all) is distinct from chronic absenteeism (a behavioral outcome of those who appear).** §11 documents the first (37% of Black G3-5 students don't appear in SBAC at all — that's a selection problem affecting which schools enter the analysis). §14 documents the second (Black-white attendance *gap* correlates with vote among schools that do report) — this is a parallel outcome, not a confounder. Neither is a fix to the other.
- **Mediation framing is causally underdetermined.** Treating baplus_wht as a parallel covariate to vote assumes they're independent; if baplus_wht is upstream of vote (more plausible), then "controlling for it" partials out part of the mechanism.
- **Selection effects.** Middle-class Black families in extreme-cost liberal precincts are an unusual demographic (housing-priced-out filter); their kids' outcomes may not generalize to Black middle-class families elsewhere.
- **A long iterative session.** Some early framings in `analysis_findings.md` were corrected later. Treat the finalized findings as best estimates after multiple revisions, not as having undergone formal peer review.

---

## How to run

```bash
make init                    # virtualenv env
make env                     # pip install -r requirements.txt
make data                    # wget SEDA covariate files into seda/
```

Then unzip the SBAC/STAR score files in `school-data/` (e.g. `sb_ca2025_all_csv_v1.zip`).

The repo is now Python 3 (was Python 2 originally). Driver scripts shell out to workers via `python3 ... os.system(...)` calls.

### Driver scripts

- **`driver-one-table.py`** — primary entry point. Runs the per-(prefix, subgroup, test) pipeline, then computes correlation analyses. Set `year = '2025'` (or 2013, 2018, 2022, etc.) at the top.
- **`driver-big-correlates.py`** — adds OLS regressions on SEDA covariates.
- **`driver.py`** — older/legacy driver.

The drivers shell out to:

- **`split_by_demo.py`** (in `school-data/`) — splits a giant SBAC/STAR file into per-subgroup files.
- **`join_precinct_school_method2.py`** — joins schools to precincts (via cached `school_to_precinct.csv`), filters scores to specified Test Ids and grades, aggregates weighted by `Students Tested`, writes `kahuna.csv`.

The `params_*.py` files configure urban/non-urban filtering. Drivers `cp params_X.py params.py` before each run.

### Output directories

- `kahuna-files/` — both urban and non-urban
- `urban-kahuna-files/` — urban only
- `non-urban-kahuna-files/` — non-urban only
- `results/` — correlation tables and OLS results

Filename convention: `<prefix>.<year>.<test_set>.csv`, e.g. `afam_econ_ok.2025.2.csv`.

### Cached artifacts (do not delete unless stale)

- `school_to_precinct.csv` (~11 MB) — base school↔precinct mapping. Expensive to regenerate.
- `school_to_precinct_charter_addendum.csv` — 910 charter schools added via ZIP→KDTree precinct lookup (22,503 mappings).
- `precinct_pts_cache.csv` — first-point representative for each of 25,912 precincts.
- `charter_seda_lookup.csv` — 1,100 charters with proxy SEDA covariates via modal-district-by-ZIP lookup.

These caches are why iterative analyses run quickly. Delete only if shapefiles or CDE data change.

## Data sources (gitignored, fetch manually)

- `school-data/` — CDE STAR (2012/2013) and CAASPP/SBAC (2017–2025) score files. See `school-data/README` for URLs. Files at https://caaspp-elpac.ets.org/caaspp/researchfiles2024 (substitute year).
- `school-data/cde-directory/pubschls.txt` — CDE Public Schools Directory. Download: https://www.cde.ca.gov/schooldirectory/report?rid=dl1&tp=txt
- `election-data/california-2016-election-precinct-maps/` — clone from `github.com/datadesk/california-2016-election-precinct-maps`
- `seda/SEDA_cov_geodist_pool_v20.csv` — Stanford SEDA district covariates. `make data` fetches it.
- `zipcodes/US Zip Codes from 2013 Government Data` — ZIP↔lat/lng table.

## See also

- `analysis_findings.md` — structured account of the analytical investigation with methodological detail
- `california_education_policy.md` — what California legislators and State Board are doing relative to the evidence
- `conversation_transcript.md` — verbatim transcript of the analytical conversation that produced these findings (saved for transparency: shows where the user challenged framings, where corrections happened, what was pushed back on, etc.)
- `CLAUDE.md` — guidance for AI assistants working on this code
- `README.claude.md` — file-by-file reference
- `TODO.claude.md` — open items
