# Patent screening log — 2026-09-04

> Public-safe research log. This repository is public, so active patent candidates are recorded only at a non-enabling level. Detailed derivations, implementation recipes, claim language, diagrams, and benchmark designs stay private until filing strategy is decided.

## Screening update

The search scope is no longer limited to finance. Every candidate is attacked using finance/economics/econometrics, mathematics, statistics, numerical analysis/optimization, computer science/data structures/databases, and CN/US/WO/EP patent prior art.

### R1-C — conclusion-stability-aware statistical computation

**Status: PATENT-WATCH; engineering value remains high.**

Broad claim concept was weakened by cross-domain prior art:

- kinetic data structures already use validity certificates and update a maintained result when certificates fail;
- retroactive and non-oblivious retroactive data structures already study edits to past operations and reporting which later query first changes;
- generic incremental statistics systems already decide between incremental maintenance and full recomputation.

A narrower statistics-specific mechanism may still be researchable, but the generic pattern “historical revision -> certificate says conclusion unchanged -> skip recomputation” must not be claimed as the invention by itself.

### N1 — numerical-debt-aware long-running statistical state

**Status: PATENT-WATCH / ENGINEERING.**

Broad error-threshold / refresh scheduling is crowded. Incremental matrix-factorization work already tracks approximation/stability metrics and compares periodic, error-threshold, angle-threshold and adaptive refresh policies. Ordinary condition-number monitoring, error-threshold refresh and periodic rebuild are therefore implementation components, not patent novelty.

### B1 — revision-aware resampling / bootstrap state

**Status: PATENT-WATCH.**

Online bootstrap for dependent time series already exists, while retroactive data structures provide a broad framework for edits to the past. The specific problem of efficiently updating inference after historical observation revisions still merits research, but a viable patent would need a non-obvious exact/certified mechanism beyond simply combining online bootstrap with provenance.

### V1 — localized option-surface arbitrage repair

**Status: ENGINEERING; patent core strongly downgraded.**

Prior work already localizes static option-arbitrage constraints and formulates sparse/minimal arbitrage repair. Keep this as an options-data quality and surface-engineering project, not as the current patent core.

---

## New candidate: HAC-R

### Retroactive robust-inference maintenance for revised time-series data

**Status: PATENT-WATCH — initial direct-match search survived; obviousness attack still in progress.**

High-level question:

> Can a time-series/econometric inference engine update HAC/Newey-West-type robust inference after arbitrary corrections to historical observations without rescanning the full sample, while preserving exact or explicitly certified semantics?

Why this is interesting:

- real economic and financial datasets are revised after first publication;
- HAC inference depends on lagged score/residual interactions, so correcting one past observation can have both local lag effects and a global effect through re-estimated model parameters;
- existing fast HAC work is primarily batch computation; online autocovariance focuses on append/stream settings; incremental HC/White-style sandwich updates do not directly solve the lagged HAC problem.

Current warning:

The candidate is **not yet a patent result**. If prior art is found for exact lag-indexed sufficient-state maintenance, retroactive sandwich/HAC inference, or an obvious algebraic reduction of the same mechanism, it will be downgraded to Engineering Track.

Public implementation details are intentionally withheld.

---

## Engineering policy reaffirmed

Patent rejection does not delete an idea. A killed/downgraded idea remains usable for:

- research prototypes and notebooks;
- quant/econometric infrastructure;
- benchmarks and papers;
- software-copyright projects;
- components of a future larger system.

Before commercializing an implementation derived from an active third-party patent, perform a separate freedom-to-operate review. Academic papers and open-source implementations also require their respective copyright/license terms to be respected.

## Next attack queue

1. HAC-R: search exact retroactive HAC / long-run covariance / dynamic GMM inference, including patents.
2. HAC-R: test whether a useful exact update can avoid dependence on full sample length without impractical state growth.
3. B1: search historical-revision bootstrap, dynamic resampling lineage, deletion/unlearning and exact weighted-replicate updates.
4. Continue broad white-space scanning beyond finance, especially numerical statistics, dynamic algorithms, verified computation and mutable-data inference.
