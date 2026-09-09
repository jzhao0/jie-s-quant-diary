# Paper Research Program — 2026-09-09

> Status: ACTIVE RESEARCH PROGRAM
>
> Purpose: convert existing financial-engineering research assets into publishable papers while preserving a hard separation between paper novelty, patent novelty, and engineering value.
>
> This repository is public. Nothing in this document should be interpreted as a patent disclosure. Active patent candidates remain subject to the publication firewall in `research-and-patent-idea-bank.md`.

## 1. Institutional constraint

Current planning assumption from the university recommendation-score document supplied by the student:

- SSCI / SCI / EI full-text indexed paper: rank 1, 2 points per paper, professional relevance required.
- Chinese core journal paper: rank 1, 0.5 points per paper, professional relevance required, capped at 2 points for this item.
- The same paper is not double-counted across the high-score indexed category and Chinese-core category.
- The overall academic/competition category is capped at 10 points.
- Until the college formally clarifies “rank 1”, use the conservative planning assumption: student should be first author / ranked first.

Therefore every paper track is screened on five dimensions simultaneously:

1. financial-engineering relevance;
2. publishable novelty;
3. data feasibility and causal/time correctness;
4. time-to-recognizable publication/indexing;
5. authorship and recognition risk.

---

# 2. Current ranked paper tracks

| Rank | Track | Current status | Main reason |
|---|---|---|---|
| P1 | Sampling / representation sensitivity of high-frequency financial event studies | **START NOW** | Strong reuse of existing event-microstructure work; clear financial-econometrics question; first novelty attack survived after scope correction |
| P2 | Chinese futures trading-day misalignment and backtest bias | **HOLD FOR DATA QUALIFICATION** | Strong question, but historical continuous-contract / roll / session semantics must be research-ready before final empirical work |
| P3 | Futures fee/margin/order-limit changes as quasi-natural experiments | **EVENT RADAR** | Established identification route; value comes from finding a clean, not-yet-exhausted contract-level policy event |
| P4 | Cross-vendor / implementation risk in quantitative finance | **SECOND TIER** | Strong reproducibility relevance but must remain a finance paper rather than software-engineering report |
| P5 | Point-in-time financial-statement revisions and factor look-ahead bias | **DEFER** | Finance relevance is excellent but historical-vintage data cost is high and the broad PIT/bitemporal method itself is no longer novel |

---

# 3. P1 — current lead paper

## Working title

**Sampling Resolution and Inference Stability in High-Frequency Financial Event Studies**

Possible application subtitle:

**Evidence from Gold around U.S. Monetary-Policy Announcements**

## Scope correction after first novelty attack

The paper must **not** claim that temporal aggregation automatically changes a fixed-window cumulative return.

If the event-window endpoints are identical and extracted correctly, the endpoint log return is an invariance / negative-control quantity. A large discrepancy across representations is first evidence of timestamp alignment, interpolation, endpoint, or data-construction differences — not a financial discovery.

The publishable question is narrower and stronger:

> When researchers represent the same underlying high-frequency event path at different sampling intervals or bar representations, when do economically and statistically relevant event-study conclusions remain stable, and when do they flip?

Candidate outcomes:

- peak absolute excursion;
- time-to-peak / price-discovery speed;
- overshoot and reversal classification;
- realized volatility / event volatility;
- jump detection;
- threshold/reference crossing sequence;
- significance decisions from high-frequency event-study tests;
- qualitative event classification.

## First novelty verdict

**SURVIVES — but only in the corrected form above.**

The first literature attack found strong prior art for each neighboring component, but did not find a paper whose central design systematically maps *event-study inference stability* from tick/native data through multiple sampling/bar representations around monetary-policy or macro announcements.

This is not yet proof of novelty. It is a `PROVISIONAL-SURVIVES` state pending a deeper database-level review.

### Prior art that limits what can be claimed

1. **Gold reacts extremely quickly to macro news.** Smales et al. use 10-second and 30-second gold-futures intervals and report that most of the response is complete within roughly 90 seconds. They explicitly motivate high granularity because 5-minute/15-minute work can place most of the reaction inside the first interval.
   - https://www.sciencedirect.com/science/article/pii/S1057521915000289

2. **Sampling frequency is already a mature high-frequency econometrics problem.** Aït-Sahalia & Mykland show that microstructure noise can imply a finite optimal sampling frequency unless noise is modeled explicitly.
   - https://www.nber.org/papers/w9611

3. **Critical sampling frequency differs on announcement days.** Chaboud et al. show that the sampling interval appropriate for integrated-volatility estimation changes with market/liquidity conditions and can differ on U.S. macro-announcement days.
   - https://www.federalreserve.gov/econres/ifdp/frequency-of-observation-and-the-estimation-of-integrated-volatility-in-deep-and-liquid-financial-markets.htm

4. **Sampling interval can affect price-discovery estimates.** The market-microstructure literature explicitly recognizes that aggregation and stale prices alter price-discovery measurement.
   - https://www.sciencedirect.com/science/article/pii/S0927539809000516

5. **Modern high-frequency event-study inference already exists.** Bugni et al. develop permutation-based discontinuity tests and apply them at one-minute frequency around FOMC announcements.
   - https://onlinelibrary.wiley.com/doi/full/10.3982/QE1775

6. **Modern intraday event-study inference is moving quickly.** Recent work develops conformal / fixed-k inference for high-frequency event studies and spot regressions.
   - https://ink.library.smu.edu.sg/etd_coll/769/
   - https://economics.smu.edu.sg/phd-economics/students/job-market-candidates/ren-yuexuan

7. **Identification in high-frequency event-study regressions is itself under active re-examination.** Casini & McCloskey show that a narrow event window alone is not sufficient for causal identification.
   - https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5368752

8. **The current FOMC event-study infrastructure is standardized and active.** The San Francisco Fed USMPD, updated 2026-08-03, provides statement, press-conference, combined-event and minutes windows and can provide timestamps / benchmark monetary-policy surprise measures.
   - https://www.frbsf.org/research-and-insights/data-and-indicators/us-monetary-policy-event-study-database/

9. **Gold jump research is current.** Recent work studies intraday jumps in gold futures / ETFs and uses 5-minute sampling plus alternative jump-detection methods. This blocks any novelty claim based merely on “detecting gold jumps around news.”
   - https://www.sciencedirect.com/science/article/abs/pii/S1057521925004673

### What may remain publishable

The contribution should therefore be framed as a **robustness / measurement paper**:

> Estimate an event-specific inference-stability frontier across sampling intervals and common representations, using a native high-frequency path as the benchmark, while explicitly separating metrics that should be invariant from metrics that are inherently path- and sampling-dependent.

Do **not** claim to invent the concepts of optimal sampling, critical sampling frequency, event studies, realized volatility, or jump detection.

---

# 4. P2 — Chinese futures trading-day misalignment

## Working question

**Which Day Does the Night Session Belong To? Trading-Day Misalignment and Backtest Bias in Chinese Commodity Futures**

Core experiment:

- exchange-aware trading-day assignment;
- naive natural-calendar assignment;
- identical downstream research pipeline;
- compare daily returns, volatility, jumps, momentum/reversal signals, turnover, Sharpe, drawdown, and signal timing.

Potential contribution is not “night trading matters”; that literature already exists. The contribution must be whether **incorrect session/trading-day semantics materially change empirical or backtest conclusions**.

### Gate

Do not run final performance claims until historical contract composition, roll rules, adjustment rules, session versions, and availability semantics pass data qualification.

---

# 5. P3 — exchange-rule quasi-natural experiments

Maintain a rolling event radar for contract-specific or product-specific changes in:

- transaction fees / close-today fees;
- margin requirements;
- price limits;
- opening / order / position limits;
- trading-session rules.

Preferred identification designs:

- difference-in-differences with unaffected maturities/products;
- event study with matched controls;
- synthetic control where treatment is sufficiently isolated.

Candidate outcomes:

- volume and turnover;
- bid-ask spread / liquidity proxies;
- realized volatility;
- intraday speculation intensity;
- price discovery;
- order imbalance where data permit.

This track becomes active only after a clean event survives prior-paper search and data-availability checks.

---

# 6. P4 — data / implementation risk

Working question:

> Under an identical financial hypothesis and strategy specification, do vendor choice, timestamp conventions, continuous-contract construction, and backtest implementation change the economic conclusion?

This can become a financial reproducibility paper if the outputs are financial quantities (alpha, Sharpe, factor significance, drawdown, turnover, price discovery) rather than merely software benchmarks.

Do not present generic “reproducibility tooling” as finance novelty.

---

# 7. P5 — PIT revision bias

The broad bitemporal / point-in-time architecture belongs in the Engineering Idea Bank, not the paper novelty claim.

A still-viable finance question is narrower:

> How much do modern/restated historical fundamentals overstate the apparent profitability or significance of Chinese equity factors relative to information that was actually public/tradable at the time?

Gate: obtain defensible historical-vintage financial statements / publication timestamps before activation.

---

# 8. Directions explicitly rejected for now

Do not spend time on the following generic topics unless a genuinely new mechanism or identification setting appears:

- “Does momentum work in Chinese commodity futures?”
- generic CTA trend-following profitability;
- generic “night-session effect” in Chinese futures;
- generic FOMC effect on gold prices;
- generic macro-news effect on gold volatility;
- generic XGBoost + SHAP financial-distress prediction;
- generic AI/ML stock prediction;
- generic PIT/bitemporal database as a paper novelty;
- generic “high-frequency data are better than low-frequency data.”

These may still be useful as baselines, engineering projects, replication exercises, or teaching material.

---

# 9. Program architecture

The coherent research umbrella is:

## Temporal and Data Integrity in Empirical Financial Engineering

Possible papers:

1. event-study sampling / representation stability;
2. Chinese futures trading-day semantic errors;
3. cross-vendor / backtest implementation risk;
4. point-in-time revision bias;
5. exchange-rule quasi-natural experiments as an independent causal track.

The common principle is:

> A financial conclusion is only as credible as the temporal semantics, data lineage, representation choices, and inference procedure that generated it.

---

# 10. Immediate decision

**P1 = ACTIVE.**

Next artifact: `p1-temporal-aggregation-event-study-protocol.md`.

Kill rule: if deeper literature review finds a directly overlapping study, or if the paper-specific pilot shows that all economically relevant inference decisions remain stable across realistic frequencies, P1 is downgraded rather than forced into a paper.
