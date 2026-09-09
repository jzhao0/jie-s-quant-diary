# P1 Protocol — Sampling Resolution and Inference Stability in High-Frequency Financial Event Studies

> Created: 2026-09-09
>
> Status: PROTOCOL v0.1 / PILOT AUTHORIZED
>
> Track: Financial econometrics / market microstructure / empirical financial engineering

## 1. Research question

For a precisely timestamped financial event observed in native high-frequency data:

> How sensitive are economically and statistically meaningful event-study conclusions to the researcher's choice of sampling interval and bar representation?

The paper is **not** a generic comparison of tick data versus minute data. It is a controlled measurement study in which all representations are derived from the same underlying event path and are evaluated against explicit invariance and stability criteria.

---

# 2. Core distinction: invariant vs representation-sensitive quantities

## 2.1 Negative-control / invariant quantities

For a fixed event window `[t0, t1]`, if both endpoints are extracted from the same underlying price path according to an identical endpoint rule, then the endpoint log return

`r(t0,t1) = log P(t1) - log P(t0)`

should not materially depend on an intermediate bar size.

Therefore:

- endpoint-return disagreement is a **pipeline diagnostic**;
- it is not automatically evidence of a financial aggregation effect;
- any disagreement must first be explained by timestamp rounding, previous-tick interpolation, next-tick interpolation, quote/trade choice, timezone handling, missing observations, or bar-boundary rules.

This is a required falsification control.

## 2.2 Representation-sensitive quantities

The following may genuinely change with sampling / bar construction:

- maximum absolute excursion from pre-event reference price;
- minimum / maximum excursion;
- time to maximum impact;
- time to first threshold crossing;
- overshoot / reversal classification;
- path length / total variation proxies;
- realized variance and related volatility estimators;
- jump detection and jump timestamp;
- sequence of reference-level crossings;
- significance decisions for high-frequency discontinuity / event tests;
- estimated market-adjustment speed.

OHLC bars deserve separate treatment from close-only samples because OHLC may retain within-bar extrema while discarding event ordering and exact timing.

---

# 3. Research representations

Every event should be transformed from one canonical native path into a fixed representation grid.

## Native benchmark

- tick / quote / transaction-native representation as available;
- canonical UTC timestamps plus original-source timezone metadata;
- no synthetic interpolation unless the metric explicitly requires it.

## Close-only regular grids

Initial pilot:

- 1 second;
- 5 seconds;
- 10 seconds;
- 30 seconds;
- 60 seconds;
- 300 seconds.

If raw density is insufficient for 1-second sampling, retain the grid as `NOT-IDENTIFIABLE` rather than silently filling it.

## OHLC grids

At minimum:

- 10 seconds;
- 30 seconds;
- 60 seconds;
- 300 seconds.

Record whether extrema can be timestamped exactly. Standard OHLC bars generally reveal the high/low values but not their within-bar ordering unless the underlying ticks are retained for benchmarking.

---

# 4. Event universe

## Pilot universe

Use a small paper-specific sample of precisely timestamped U.S. monetary-policy events for which admissible native high-frequency gold data are already available or can be independently reproduced.

The pilot is a **feasibility / effect-size study**, not the publication sample.

Preferred event families:

1. FOMC statement release;
2. FOMC Chair press-conference start / relevant standardized window;
3. optionally selected high-impact macro releases as an external generalization set.

## Publication universe

Expand only after the pilot survives.

Use official / authoritative event timestamps. The San Francisco Fed U.S. Monetary Policy Event-Study Database (USMPD) is a preferred benchmark source for standardized FOMC event definitions and policy-surprise measures:

https://www.frbsf.org/research-and-insights/data-and-indicators/us-monetary-policy-event-study-database/

USMPD currently distinguishes:

- 30-minute statement windows;
- 70-minute press-conference windows;
- combined monetary-event windows;
- 30-minute minutes-release windows.

The paper should not assume those standard windows are optimal for gold; they are an institutional benchmark, not the dependent variable.

---

# 5. Event windows

Pilot windows should be nested and pre-registered before examining aggregate results.

Candidate windows relative to event timestamp `T`:

- `[-5m, +5m]`;
- `[-5m, +15m]`;
- `[-15m, +30m]`;
- event-family-specific standard window for comparison with the literature.

For response-speed metrics, additionally evaluate the first:

- 30 seconds;
- 60 seconds;
- 90 seconds;
- 5 minutes.

Reason: prior gold-futures work reports that much of the macro-announcement response is complete within about 90 seconds.

Reference:
https://www.sciencedirect.com/science/article/pii/S1057521915000289

---

# 6. Primary outcomes

## O1. Peak absolute excursion

Relative to a pre-event reference price `P_ref`:

`MAE_event = max_t |log(P_t / P_ref)|`

For close-only samples, coarse grids mechanically observe a subset / compressed representation of the native path. The study measures the economically relevant loss, not merely whether it is nonzero.

Report:

- absolute error;
- relative error;
- event-level distribution;
- tail quantiles.

## O2. Time to peak

`T_peak = argmax_t |log(P_t / P_ref)| - T_event`

For OHLC bars, distinguish:

- exact native timestamp;
- bar-level interval containing the peak;
- irreducible timing uncertainty caused by representation.

## O3. Overshoot / reversal classification

Create a pre-specified, economically interpretable classification rule.

Example family:

1. initial directional move exceeds threshold `a`;
2. subsequent counter-move exceeds fraction `b` of the initial move within horizon `h`.

Do not tune `a`, `b`, `h` to maximize frequency differences. Use robustness grid / preregistration.

Primary statistic:

`classification_flip_rate(Δ)` = share of events whose classification at sampling interval `Δ` differs from the native benchmark.

## O4. Realized volatility / event variation

Estimate using multiple defensible methods because very high sampling can be contaminated by market microstructure noise.

At minimum:

- naive realized variance at each grid;
- a microstructure-noise-robust benchmark where feasible;
- volatility signature plot around event windows.

Important prior art:

- Aït-Sahalia & Mykland: sampling in the presence of microstructure noise.
  https://www.nber.org/papers/w9611
- Chaboud et al.: critical sampling frequency and announcement-day differences.
  https://www.federalreserve.gov/econres/ifdp/frequency-of-observation-and-the-estimation-of-integrated-volatility-in-deep-and-liquid-financial-markets.htm

The paper must therefore avoid the false assumption that “higher frequency = always more accurate.”

## O5. Jump inference

Use at least two established jump-detection approaches if data permit.

Primary object is not the number of jumps itself, but:

- whether the event is classified as containing a jump;
- jump timing;
- jump sign / size;
- stability of those decisions across sampling intervals.

Recent gold work already performs jump detection at 5-minute frequency and alternative-method robustness, so novelty cannot be “we detect gold jumps.”

Reference:
https://www.sciencedirect.com/science/article/abs/pii/S1057521925004673

## O6. Statistical event-study decision

Where suitable, implement an established high-frequency event-study inference procedure at multiple representations.

Candidate baseline:

- permutation-based discontinuity test in the spirit of Bugni et al.;
- additional nonparametric / fixed-k approach if the data structure supports it.

Reference:
https://onlinelibrary.wiley.com/doi/full/10.3982/QE1775

Primary outcome:

`decision_flip_rate(Δ, α)` = share of event/metric tests whose reject/non-reject decision differs from the native / finest defensible benchmark at significance level `α`.

Do not present a p-value flip by itself as economic importance; pair it with effect-size distortion.

---

# 7. Proposed stability objects

These names are working labels, not patent claims and not assumed to be novel terminology.

## 7.1 Metric distortion curve

For metric `M` and sampling interval `Δ`:

`D_M(Δ) = distance(M_Δ, M_native)`

Use metric-appropriate distances rather than forcing every output into percentage error.

Examples:

- scalar relative/absolute error;
- timing error in seconds;
- classification mismatch indicator;
- test-decision mismatch indicator.

## 7.2 Event-study stability frontier

For a specified metric / conclusion and tolerance `τ`, define the coarsest interval that still preserves the native benchmark within tolerance.

This adapts the logic of a “critical sampling frequency” to event-study conclusions. The paper must credit the existing critical-sampling-frequency literature rather than claiming the broad concept as new.

Possible definition:

`Δ*_e,M(τ) = max {Δ : D_e,M(Δ) <= τ}`

Aggregate across events by median, quantiles, and dependence on event intensity.

## 7.3 Inference flip matrix

Rows = events.

Columns = representations / intervals.

Cells = conclusion category or significance decision.

This makes instability visible without hiding it inside averages.

---

# 8. Hypotheses / propositions for the pilot

## H0-control — endpoint-return invariance

Under identical endpoint rules, fixed-window endpoint returns should be stable across intermediate aggregation choices.

Failure triggers a data-pipeline audit before any economic interpretation.

## H1 — peak-excursion attenuation for close-only sampling

Coarser close-only sampling should weakly lose intra-grid extrema relative to the native path and therefore increase nonnegative peak-loss error.

Economic question: how large is the loss on actual high-impact events?

## H2 — timing uncertainty rises with coarser representation

Time-to-peak and threshold-crossing timing error should increase with interval length, especially during rapid post-announcement adjustment.

## H3 — volatility sensitivity is non-monotone

Very fine sampling may be contaminated by microstructure noise; coarse sampling may omit genuine rapid event variation. Therefore volatility-estimation error need not decline monotonically with finer grids.

## H4 — path classifications can flip at conventional minute frequencies

Overshoot/reversal and jump classifications may differ materially between native/seconds data and 1-minute/5-minute representations.

## H5 — instability is state-dependent

The stability frontier should vary with event intensity, liquidity, and policy-surprise magnitude rather than being a universal constant.

If policy-surprise data are available from USMPD or another authoritative source, test whether larger surprises predict a different stability frontier.

---

# 9. Statistical design

## Unit of analysis

Primary: event.

Avoid treating thousands of ticks inside one event as independent cross-sectional observations.

## Across-event inference

Candidate approaches:

- paired event-level comparisons across representations;
- bootstrap / permutation at the event or event-date level;
- median / quantile distortion with confidence intervals;
- regression of event-level distortion on event intensity / liquidity controls.

If the event sample is small, emphasize effect sizes, exact/randomization inference, and uncertainty rather than asymptotic t-statistics with pseudo-replication.

## Multiple metrics

Pre-specify:

- primary outcomes;
- secondary outcomes;
- family-wise / false-discovery adjustment where formal multiple testing is used.

Do not select only metrics that flip.

---

# 10. Data-construction controls

Each derived representation must be generated from one immutable canonical event-path object.

Required metadata:

- source;
- instrument identifier;
- quote/trade/mid definition;
- timestamp timezone and precision;
- event timestamp source;
- duplicate handling;
- out-of-order handling;
- missing interval policy;
- interpolation policy;
- bar boundary convention;
- left-/right-closed interval semantics;
- reference-price rule;
- code version / commit;
- raw-input hash where permitted.

Never compare separately downloaded M1 data with tick data and call the difference “aggregation bias” unless source/version effects are explicitly part of the design.

The clean baseline is:

`one raw path -> many deterministic representations`.

---

# 11. Research firewall / holdout policy

This paper track must not silently consume any holdout that is locked for another research or trading project.

Rules:

1. create a paper-specific manifest;
2. define pilot dates before aggregate analysis;
3. define any confirmatory holdout separately;
4. do not relabel a previously inspected period as untouched;
5. record every event exclusion with reason;
6. no rerun/reselection after seeing favorable results without marking it exploratory.

---

# 12. Pilot success / kill gates

P1 advances from `PROTOCOL` to `FULL STUDY` only if all of the following are true.

## G1 — data integrity

Endpoint-invariance control passes within a pre-specified numerical/data tolerance.

## G2 — nontrivial economic distortion

At least one primary path-dependent outcome shows distortion large enough to matter economically or methodologically at a frequency researchers plausibly use (especially 1-minute or 5-minute).

## G3 — not only one pathological event

The result is not solely driven by one data-error / flash event. Heterogeneity is allowed, but there must be a reproducible pattern or a defensible state-dependent explanation.

## G4 — novelty survives second search

No directly overlapping paper is found after deeper searches in:

- high-frequency econometrics;
- event-study methodology;
- market microstructure;
- monetary-policy identification;
- gold / commodity microstructure;
- sampling-frequency robustness.

## G5 — paper-scale data feasible

A publication sample with enough events can be obtained without violating data licensing, project holdouts, or time constraints.

### Kill / downgrade conditions

Downgrade P1 to engineering / methodology note if:

- all practical 1-minute / 5-minute conclusions are stable;
- only trivial timing quantization is observed;
- effects disappear after controlling for microstructure noise and endpoint alignment;
- the apparent effect is entirely vendor/source mismatch;
- a directly overlapping paper is found;
- the publication sample cannot be assembled defensibly.

A null pilot is a valid project result and must be archived.

---

# 13. First pilot deliverables

1. immutable `events.csv` / manifest;
2. canonical event-window extractor;
3. deterministic resampler producing all registered grids;
4. endpoint-invariance test;
5. metric library for O1–O5;
6. event-level distortion table;
7. stability-frontier table;
8. inference-flip matrix;
9. plots:
   - representative native vs M1 vs M5 paths;
   - distortion curves;
   - volatility signature plot;
   - timing-error distribution;
   - classification flip heatmap;
10. pilot decision memo: `ADVANCE / MODIFY / KILL`.

---

# 14. Immediate next action

Do not write the paper introduction yet.

First produce the pilot on a paper-specific event set and answer one question:

> Do common 1-minute / 5-minute representations materially change at least one defensible financial event-study conclusion after endpoint alignment and microstructure controls?

If yes, expand literature review and publication sample. If no, kill or reframe before spending time on manuscript polishing.
