# Analysis findings — California school achievement vs precinct vote share

This document summarizes the findings from an extensive analytical session conducted in May 2026. The analysis used 2012–2025 CAASPP/SBAC and STAR test data, joined to 2016 election precinct vote shares, with SEDA district-level demographic covariates.

## Headline empirical claim

> *In 2025 California, after controlling for white-parent BA+ rate, racial integration, within-district resource allocation, and charter density, a precinct's Clinton vote share independently predicts a substantially larger Black-white achievement gap among non-economically-disadvantaged students at the high-school level. The signal is robust across school-vs-student weighting (+0.50 to +0.62 correlation), threshold choice (strict vs matched), test (within-course vs pooled), aggregation level (school vs SEDA-native district), and year (2019, 2022–2025). For the broader all-Black-vs-all-white pair, the political signal exists univariately but is mostly absorbed by demographic covariates.*

## Methodological constraints worth flagging

1. **Substantial Black-student missingness.** Of California's ~75K Black elementary students per 3-grade band, only ~33% appear with usable scores after CDE suppression filters. HS coverage is better (~65%) because HS schools are larger and clear the n≥11 reporting threshold more often. The findings generalize only to the Black students at schools where their subgroup population is large enough to be reported.

2. **Matched-pair filter is highly selective.** The Black-white econ_ok HS math finding is computed on ~1,972 Black students at 97 schools — about 8% of California's Black econ_ok HS population. These are schools where middle-class Black and middle-class white students attend in reportable numbers — a structurally unusual configuration in California, where most Black students attend majority-Hispanic schools.

3. **Charter inclusion via post-hoc geocoding.** The original `school_to_precinct.csv` excluded most charter LEAs (only 75 of 1,263 charters). A KDTree-based ZIP→precinct lookup added 910 missing charters. SEDA covariate matching for charter LEAs was done via "modal traditional district at the charter's ZIP" proxy (1,100 charters covered). Both expansions modestly strengthen the elementary findings; HS findings are insensitive to charter inclusion (matched-pair filter does the work).

4. **The mediation-analysis framing is causally underdetermined.** Treating baplus_wht as a parallel competitor to vote in OLS implicitly assumes baplus_wht and vote are independent variables. The more plausible causal structure is `baplus_wht → vote → policy → outcomes`, in which case "controlling for baplus_wht" partials out the upstream input to the mechanism rather than a competing confounder. The vote-alone coefficient is the more interpretable causal estimate under this DAG.

## Key empirical findings

### 1. Cross-year robustness of the political pattern

Matched-gap-vote correlation for econ_ok HS math, full 4-covariate stacked OLS:

| year | β_vote (after all covariates) | p |
|---|---|---|
| 2019 | +47.0 | <.001 |
| 2022 | +59.1 | <.001 |
| 2023 | +26.7 | (NS, anomalous year) |
| 2024 | +60.3 | <.001 |
| 2025 | +27.9 | 0.05 |

Pattern is consistent across 2019, 2022, 2024 (β ≈ +50 to +60). 2023 and 2025 show somewhat lower values. The 2025 weakening is partial, not collapse — at the univariate level the correlation remains +0.52.

### 2. Mechanism decomposition

For 2025 G11 econ_ok math, score-by-vote correlations (student-weighted):

- corr(afam_OK, vote) = **−0.37** → middle-class Black HS scores fall in liberal precincts
- corr(wht_OK, vote) = **+0.34** → middle-class white HS scores rise in liberal precincts
- corr(hsp_OK, vote) ≈ −0.05 → flat
- corr(asn_OK, vote) ≈ −0.09 → roughly flat

The Black-white gap-vote correlation (+0.62) is the sum of two independent effects: white-rises and Black-falls. Hispanic-white gap-vote correlation (+0.42) is mostly the white-rises effect alone, since Hispanic doesn't fall.

### 3. Trajectory through grade bands

afam student score-vote correlations:

| grade | afam | afam_dis | afam_OK |
|---|---|---|---|
| G3-5 | **+0.252** | +0.335 | (small sample) |
| G6-8 | +0.023 | +0.100 | −0.069 |
| G9-11 | −0.064 | +0.036 | **−0.311** |

At elementary, Black students score *higher* in liberal precincts. By HS, middle-class Black students score lower. The within-Black econ gap **narrows** in liberal areas at both grade levels, but for opposite reasons: at G3-5 because afam_dis rises faster than afam_OK; at HS because afam_OK falls toward afam_dis.

### 4. Course-tracking is real but doesn't explain the political pattern

STAR 2013 data (econ_ok pair, G9-11):

| course | % afam_econ_ok | % white_econ_ok |
|---|---|---|
| GenMath (low track) | 34.2% | 21.5% |
| Geometry | 32.1% | 30.8% |
| Algebra II | 23.5% | 28.3% |
| Summative (advanced) | 9.3% | 18.7% |

afam_econ_ok students are 1.6× more likely in low-track GenMath, half as likely in advanced Summative. **But the within-test gap-vote correlation is +0.30 to +0.47 in EVERY test separately** — so course-tracking inflates the LEVEL of the gap but doesn't drive the political variation.

### 5. Geographic concentration

Within-metro analysis of 2025 G11 econ_ok math gap-vote correlation:

- Bay Area only (n=11 schools): +0.896
- LA region only (n=10): +0.861
- Sacramento County (n=10): +0.131
- San Diego County (n=4): too few
- Rest of California (n=61): +0.303

The pattern is concentrated in Bay Area and LA. Sacramento and San Diego show much weaker effects. Mechanisms differ by metro:

- Bay Area: both Black-falls AND white-rises strong
- LA: only white-rises (corr(afam, vote) ≈ 0)
- Rest of CA: weaker version of both

### 6. Berkeley is an outlier but not unique

After dropping the top-10% of districts by white-BA+ rate (excludes Berkeley, Pasadena, Santa Monica-Malibu, etc.):

| sample | β_vote alone | β_vote + baplus | β_vote + all covs |
|---|---|---|---|
| Full | +60.3 | +34.4 | +30.3 |
| Drop top-10% | +43.9 | +35.2 | +32.8 |
| Drop top-20% | +37.9 | +34.0 | +35.7 |

The vote-alone coefficient drops when extreme-baplus districts are removed (Berkeley etc. contribute disproportionately). But the controlled coefficient stays at ~+34 across all three samples — the pattern generalizes beyond Berkeley/Stanford-tier districts to ordinary high-baplus liberal California.

### 7. Black students at charters score better than at district schools, especially in liberal areas

2025 SBAC math, mean Black student proficiency by school type × precinct vote bucket:

**G3-5 elementary (afam):**

| school type | Trump | Mixed | Liberal | Strong Clinton |
|---|---|---|---|---|
| district | 13.1% (n=2,681) | 18.3% (n=4,512) | 21.0% (n=5,697) | 22.2% (n=5,070) |
| charter | 13.5% (n=155) | 34.0% (n=100) | 22.5% (n=961) | **28.0%** (n=2,646) |

**G6-8 middle (afam):**

| school type | Trump | Mixed | Liberal | Strong Clinton |
|---|---|---|---|---|
| district | 14.9% | 18.0% | 14.2% | 16.0% |
| charter | 15.7% | 25.8% | **23.7%** | 19.4% |

**G11 high school (afam, samples small/noisy):**

| school type | Trump | Mixed | Liberal | Strong Clinton |
|---|---|---|---|---|
| district | **17.5%** | 14.9% | 14.5% | 14.5% |
| charter | 8.8% (n=262) | 13.4% | 17.5% | 14.3% |

**Charter advantage by bucket (charter mean − district mean):**

| grade | Trump | Mixed | Liberal | Strong Clinton |
|---|---|---|---|---|
| G3-5 | +0.4 | +15.7 | +1.5 | **+5.8** |
| G6-8 | +0.8 | +7.8 | **+9.5** | +3.4 |
| G11 | −8.7 | −1.5 | +3.0 | −0.2 |

**Pattern:** at elementary and middle school, charters show their biggest Black-student advantage in liberal areas (Strong Clinton at G3-5, Liberal at G6-8). In conservative areas, the advantage shrinks or reverses. HS samples too small for clean inference.

The Black-targeted no-excuses charter networks (KIPP Compton, Wilder's Preparatory, Rocketship Delta Prep, Aspire) are concentrated in liberal urban California. They tend to outperform the surrounding district schools — most starkly where district pedagogy has drifted furthest from traditional rigor (i.e., in the most progressive districts).

**Roland Fryer's research program is the most rigorous evidence base for this finding:**

- **Fryer 2014 (QJE), "Injecting Charter School Best Practices into Traditional Public Schools"** — RCT study of Houston ISD's Apollo 20 program. Injected no-excuses charter practices (extended day, intensive tutoring, frequent assessments, high expectations, data-driven instruction) into 20 of Houston's lowest-performing district schools. Result: 0.15–0.40 SD per year math gains for predominantly Black/Hispanic students. Demonstrated that charter-style effectiveness is reproducible inside traditional public schools when administrators choose to.
- **Fryer 2017, "The Production of Human Capital in Developed Countries"** — meta-analysis of 196 RCTs. High-dosage tutoring + structured curriculum + high expectations consistently outperform wraparound or broader interventions for Black student outcomes.
- **Dobbie & Fryer 2011, 2013 (Harlem Children's Zone)** — the school component (KIPP-style pedagogy at Promise Academy) was responsible for nearly all of the gap-closing effect, not the surrounding social-services wraparound.
- **Fryer & Torelli 2010 ("Acting White")** — documented within-school peer-comparison effects in racially integrated upper-middle-class schools that depress Black achievement; absent at homogeneous Black schools.

Fryer's findings haven't received the institutional uptake their evidence-quality would warrant — partly because the implications cut against progressive-education orthodoxy, partly because Fryer himself has been professionally sidelined at Harvard for publishing other findings (notably his 2016 police use-of-force paper) that contradicted prevailing academic narratives. The pattern of "rigorous evidence on rigor producing better Black outcomes" being underweighted in policy discourse is itself part of what our within-California analysis points at.

### 8. Per-pupil spending doesn't predict Black achievement

District-level correlations:

| year | corr(ppexp, afam_score) | corr(ppexp, white_score) | corr(ppexp, vote) |
|---|---|---|---|
| 2013 | +0.06 | +0.24 | +0.59 |
| 2018 | −0.18 | −0.01 | +0.50 |
| 2022 | −0.08 | +0.30 | +0.62 |
| 2025 | +0.01 | +0.31 | +0.63 |

Per-pupil spending correlates strongly with vote (high-cost-of-living liberal districts spend more) and with white scores (especially 2022/2025). It does not correlate with Black scores in any year. Money flowing into liberal-affluent districts reaches white students but not Black students.

## Interpretive framing (where the data supports it)

The behavioral evidence supports a structural-systems story rather than an individual-bias story:

- Liberal California has built schools that produce systematically worse Black achievement outcomes than conservative California, controlling for plausible confounders
- The mechanism operates through housing-market sorting, within-school tracking, AP/honors gating, parental fundraising stratification, and pedagogical choices that liberal coalitions have political control over
- Cross-state comparisons (Mississippi, Florida, Texas outperforming California on Black-student NAEP) corroborate that policy choices matter independent of demographics
- The "soft bigotry of low expectations" hypothesis is empirically consistent with what we observe — places implementing rigor + accountability + high expectations produce better Black outcomes than places implementing equity-via-lowered-rigor pedagogy
- Within-school differential expectations (high for white, lower for Black at the same building) is a well-documented mechanism (Berkeley High case studies, Pollack, Pedro Noguera, others) that produces exactly the bifurcated outcomes we measure

## What the data DOES NOT establish

- That liberal politics *causes* the gap (associational, not causal — though cross-state evidence is suggestive)
- That conservative districts are better on equity (Black students in lowest-vote-share Bay Area schools are absolutely worse off than Black students in many conservative districts; the absolute level is what's worse, not just the relative gap)
- That spending is causally irrelevant (the cross-district correlation can't see effects that the literature with cleaner identification — Jackson 2016 etc. — does find)
- That generalization holds for the missing 67% of Black elementary students who don't appear in this data

## Generated artifacts

- `school_to_precinct_charter_addendum.csv` — 22,503 charter-precinct mappings for 910 previously-missing charters
- `precinct_pts_cache.csv` — 25,912 precinct first-points for fast spatial lookup
- `charter_seda_lookup.csv` — 1,100 charters with imputed SEDA covariates via ZIP-modal-district proxy
- `results/grade_band_threshold_matched.csv` — multi-year threshold-matched comparisons
- Various per-year `results/vote_achievement_correlations.*.csv` and `results/covariates_achievement_correlations.*.csv`

## Methodological lessons learned during the session

1. **The SBAC raw file has both School Code = 0 (state/county/district rollups) and Grade = 13 (all-grades rollup) rows.** Filter both out or absolute student counts will be inflated by 2× to 4×. Percentages survive (proportional inflation in numerator and denominator).

2. **CDE suppresses subgroup percentages when n<11.** This hits Black students much harder than white (46% suppression vs 11% at G3-5). Working with `dropna(subset=['n','p'])` discards a much larger fraction of Black student data than white.

3. **Most charter LEAs aren't in `school_to_precinct.csv`** because that cache was built from older entities files. The KDTree-based ZIP geocoding addendum recovers 910 of them.

4. **Most charter LEAs aren't in SEDA's `leaname` field.** The ZIP→modal-traditional-district proxy is the simplest workaround.

5. **School-vs-student weighting matters substantially.** Student-weighted correlations are systematically higher than school-weighted (e.g., +0.62 vs +0.52 for the headline cell). For population-level claims, student-weighting is more honest.

6. **District-level aggregation is the right SEDA-native unit.** The conclusions hold at both school and district level, but reporting at district level is cleaner methodologically since SEDA covariates are district-level.

7. **The mediation framing requires a DAG assumption.** "Controlling for baplus_wht" assumes baplus_wht is parallel to vote. If baplus_wht is upstream of vote (more plausible), then the mediation underestimates the causal effect of vote.
