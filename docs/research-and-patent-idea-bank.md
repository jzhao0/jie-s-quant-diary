# Research & Patent Idea Bank

> Last updated: 2026-09-04
>
> This repository is **public**. Active patent candidates are intentionally recorded only at a high level. Do **not** publish enabling implementation details, formulas, claims, diagrams, benchmarks, or a complete technical disclosure here before filing a patent application.

## Purpose

This document separates two different questions:

1. **Patent track** — Is there still a credible novelty / inventive-step gap after searching finance, economics, mathematics, statistics, computer science, numerical analysis, optimization, databases, papers, and patents?
2. **Engineering track** — Is the idea still worth implementing as infrastructure, a research tool, benchmark, paper prototype, software copyright project, or a module in a larger system?

A patent candidate that is killed by prior art is **not deleted**. It moves to the Engineering Idea Bank if it still has practical value.

## Screening rule

Every patent candidate should survive all five layers before serious implementation effort:

| Layer | Search space | Main question |
|---|---|---|
| L1 | Finance / economics / econometrics | Has the actual domain problem already been solved? |
| L2 | Mathematics / numerical analysis / optimization | Is the supposed core innovation an existing theorem, perturbation result, or optimization technique? |
| L3 | Statistics | Is it already covered by sensitivity, robustness, online inference, resampling, sequential statistics, etc.? |
| L4 | Computer science | Is it an existing database, dynamic algorithm, compiler, streaming, GPU, provenance, state-machine, or incremental-computation pattern? |
| L5 | Patents (CN/US/WO/EP) | Do existing claims already cover the mechanism or an obvious combination of its components? |

### Status labels

- **PATENT-PRIVATE** — active candidate; public details deliberately withheld.
- **PATENT-WATCH** — potentially interesting but prior-art risk remains high.
- **ENGINEERING** — useful to build, but not suitable as the core novelty of our patent.
- **KILLED-AS-PATENT** — core novelty is too directly covered by prior art; retain only for engineering/research use.

---

# A. Active patent research — public-safe index only

## R1-C — Conclusion-stability-aware statistical computation

**Status:** PATENT-PRIVATE

High-level research question: can a statistical/econometric computation system determine that a downstream decision or conclusion is guaranteed not to change after a data revision, and therefore safely avoid unnecessary recomputation?

Public note only. Detailed certificate composition, operator rules, propagation logic, claim structure, and implementation are kept out of this public repository until filing strategy is decided.

Key attack areas still required:

- perturbation theory and robust statistics;
- statistical stability / fragility measures;
- kinetic-data-structure style certificates;
- incremental view maintenance and self-adjusting computation;
- dynamic decision problems;
- patents that condition recomputation on sensitivity or thresholds.

## N1 — Numerical-debt-aware long-running statistical state

**Status:** PATENT-PRIVATE

High-level research question: can long-running streaming statistical / matrix states carry a machine-checkable numerical-error state that determines when a local repair, partial rebuild, or complete rebuild is required?

Do not publish the proposed internal error ledger, propagation equations, repair policy, or subsystem architecture before patent screening is complete.

## B1 — Revision-aware resampling / bootstrap state

**Status:** PATENT-PRIVATE

High-level research question: after historical observations are revised, can resampling-based inference update only the computation genuinely affected by that revision while preserving exact or certified statistical semantics?

Still requires aggressive search against online bootstrap, weighted bootstrap, bagging, sample deletion, distributed resampling, lineage/provenance, and dynamic sufficient statistics.

---

# B. Engineering Idea Bank

These ideas remain worth building even where the patent core is weak or already known.

## 1. Multi-source market-data time alignment and anomaly calibration

**Status:** ENGINEERING

Potential use:

- align exchange/vendor/broker timestamps;
- estimate source offset, drift and jitter;
- handle late / out-of-order messages;
- produce source-confidence diagnostics.

Useful as a market-data ingestion layer, even though time synchronization and multi-source reconstruction are mature patent areas.

## 2. Order-book gap detection and consistent recovery

**Status:** ENGINEERING

Potential modules:

- sequence-gap detection;
- state-invariant checks beyond sequence continuity;
- snapshot / replay / backup-feed recovery;
- recovery latency and state-consistency benchmarks.

Strong infrastructure value; weak as standalone patent novelty because market-data recovery is heavily patented.

## 3. Bitemporal / point-in-time financial data store

**Status:** ENGINEERING

Maintain at least:

- valid/reference time;
- known/public/system time;
- tradable / availability time where relevant;
- revision history and deterministic replay.

Useful for research-data hygiene, avoiding look-ahead bias, macro-data vintages, fundamentals and index constituent history.

## 4. Feature-DAG incremental computation engine

**Status:** ENGINEERING

Potential use:

- dependency graph for factors/features;
- update only affected nodes;
- cached sufficient state;
- selective full recomputation after numerical or semantic invalidation.

Incremental computation is mature CS prior art, but this remains valuable as a reusable quant feature engine.

## 5. Brownian-path geometric envelope / convex-hull query accelerator

**Status:** ENGINEERING / RESEARCH

Idea retained because the engineering result is interesting even though the mathematical foundation (Brownian/random-walk concave majorants and support queries) is old prior art.

Potential applications:

- repeated barrier-event queries across many parameter scenarios;
- Monte Carlo stress grids;
- Greeks / calibration benchmarking;
- computational-geometry demonstration in quantitative finance.

Promising as a paper/prototype or optimization module, not currently preferred as patent core.

## 6. Event-certified mixed-precision Monte Carlo with deterministic RNG replay

**Status:** ENGINEERING / RESEARCH

Potential stack:

- low-precision bulk path execution;
- event-boundary uncertainty detection;
- path-local precision escalation;
- deterministic counter-based RNG replay from checkpoints;
- FP16/FP32/FP64 work queues.

Mixed precision, error filtering, adaptive precision and RNG replay are existing techniques. Still valuable as a GPU risk/pricing engine.

## 7. Historical trading-session / rule reconstruction

**Status:** ENGINEERING / RESEARCH

Potential system:

- infer historical trading sessions from tick/event evidence;
- detect rule-version changes;
- represent exchange/product sessions as versioned automata;
- validate inferred rules by replay;
- audit trading-day/session mapping errors.

Patent risk is high because protocol/state-machine inference and process-mining concept drift are mature cross-domain techniques. Engineering value for Chinese futures data governance remains high.

## 8. Backtest temporal-causality / look-ahead audit

**Status:** ENGINEERING

Potential use:

- carry multiple notions of time through a research pipeline;
- detect availability-time violations;
- point-in-time joins;
- lineage report explaining why a feature or trade was or was not legal at a historical timestamp.

Strong tooling value. Temporal non-interference / point-in-time lineage now has strong recent prior art, so do not treat the broad concept as patent novelty.

## 9. Localized arbitrage repair for option / volatility surfaces

**Status:** ENGINEERING; patent track downgraded

Potential use:

- no-arbitrage constraint graph;
- localize violations;
- sparse/minimal repair;
- warm-start constrained solvers;
- intraday surface QA and rollback.

Important prior art already localizes static option-arbitrage constraints and formulates sparse minimal repair as linear programming. This is still a useful options-data cleaning and surface-engineering module.

## 10. Historical-data revision impact engine

**Status:** ENGINEERING + feeds R1-C research

Potential use:

- ingest macro/fundamental data vintages;
- identify changed observations;
- trace dependent models/reports;
- run exact incremental updates where available;
- produce a revision-impact report.

Even without a patent, this could be useful for econometrics and real-time macro research.

## 11. Long-running numerical self-healing for streaming statistics

**Status:** ENGINEERING + feeds N1 research

Potential targets:

- rolling covariance;
- rolling regression;
- PCA / factor models;
- rank-one matrix updates;
- condition and residual monitoring;
- periodic or adaptive rebase.

Do not claim ordinary condition-number monitoring, Sherman–Morrison/Woodbury updates, or periodic rebuilds as novelty.

## 12. Shared sufficient-statistic state across multiple models

**Status:** ENGINEERING

Potential use:

- share sums, moments, cross-products and matrix state among correlation, regression, covariance, VAR and risk modules;
- common-subexpression elimination across statistical workloads;
- reduce duplicate storage and update work.

Likely weak patent territory because of sufficient statistics, database materialized views and compiler CSE, but useful as a high-performance statistics library.

---

# C. Patent ideas explicitly killed or downgraded

The following should not be revived as standalone patent claims unless a genuinely new mechanism is found.

| Idea | Why it was downgraded |
|---|---|
| Generic high-frequency incremental feature calculation | Sliding-window and incremental computation are mature prior art. |
| Multi-source financial timestamp alignment | Clock drift, reordering and source reconciliation are well-covered. |
| Sequence-gap market-data recovery | Mature market-data recovery / replay patents. |
| Generic financial data versioning / historical replay | Bitemporal/versioned systems and financial historical repair already exist. |
| Path-topology stability certificate alone | Scenario/path reuse and sensitivity methods make the incremental step too close to prior art. |
| Brownian convex-hull path compression as core claim | Underlying concave-majorant / support-function mathematics is old prior art. |
| Generic mixed-precision Monte Carlo | Mature mixed-precision, adaptive precision and error-filtering literature. |
| Progressive random-bit refinement | Random-bit SDE / MLMC literature already exists. |
| Financial contract state machine + GPU compilation | Contract automata and generated GPU pricing code already exist. |
| Historical session change-point detection alone | Change-point detection and process-mining/version discovery are mature. |
| Backtest look-ahead proof in broad form | Temporal non-interference / point-in-time availability work now directly overlaps. |
| Generic local volatility-surface arbitrage repair | Existing work already localizes no-arbitrage constraints and performs sparse minimal repair. |
| Dependency graph + affected-node recomputation | Generic incremental computation / DAG pipeline recomputation is mature CS prior art. |

---

# D. Cross-disciplinary warning list

Before calling any future idea novel, explicitly search these mother technologies:

- dynamic and incremental algorithms;
- kinetic data structures and validity certificates;
- self-adjusting computation;
- incremental view maintenance;
- provenance and data lineage;
- abstract interpretation and verified numerics;
- perturbation theory and condition numbers;
- interval / affine arithmetic;
- robust statistics and sensitivity analysis;
- online / streaming statistics;
- bootstrap, jackknife and resampling systems;
- active-set / parametric optimization;
- process mining and concept drift;
- protocol/state-machine inference;
- GPU mixed precision and reproducibility;
- random-number replay / counter-based RNG;
- computational geometry;
- database synopsis / sufficient-statistic systems.

A finance-specific implementation can still be worth building, but merely changing the application domain is not enough for a strong invention claim.

---

# E. Development policy

1. **Patent-publication firewall:** do not push enabling details of an active patent candidate to this public repository before filing.
2. **Prior art ≠ no development:** prior academic work means we can often reimplement the idea subject to copyright/license constraints; an active patent requires separate freedom-to-operate review before commercialization.
3. **Keep prototypes modular:** engineering ideas should be reusable later as components of a larger system or a genuinely new patentable architecture.
4. **Benchmark everything:** keep baseline, accuracy, numerical-error, latency, memory and reproducibility metrics.
5. **Preserve provenance:** record the paper/patent that caused a patent downgrade so we do not unknowingly revive the same idea later.

---

# F. Immediate research queue

Current order:

1. **R1-C** — attack with kinetic-data-structure certificates, robust-statistics stability, dynamic decision problems, database trigger/recompute patents and perturbation theory.
2. **N1** — attack with verified numerical linear algebra, interval/affine arithmetic, error-aware streaming algorithms and adaptive restart/rebuild literature.
3. **B1** — attack with online/bootstrap update algorithms, bagging, data deletion/unlearning, lineage and distributed resampling.
4. Continue broad white-space scan across mathematics, statistics, numerical computation, optimization, economics/econometrics and computer systems rather than searching only within finance.
