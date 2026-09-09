# Engineering Spin-outs from Paper Screening — 2026-09-09

> Status: ENGINEERING / RESEARCH TOOLING
>
> Rule: an idea can be weak as paper novelty and still be valuable as a reusable project, benchmark, library, internal research-control system, or future product component.
>
> This file intentionally records project value without reviving ideas as standalone patent claims.

## 1. Multi-resolution event replay and audit toolkit

**Status:** ENGINEERING / directly supports P1

Build one canonical high-frequency event-path object and deterministically generate:

- native/tick views;
- 1s / 5s / 10s / 30s / 1m / 5m close samples;
- OHLC bars;
- metric distortion reports;
- timing-loss reports;
- event replay visualizations.

Useful outside the paper for:

- validating vendor-provided bars;
- diagnosing why a strategy behaves differently on tick vs M1 data;
- execution/replay testing;
- education / quantitative-research QA.

Do not present “multi-resolution resampling” itself as patent novelty.

---

## 2. OHLC information-loss / path-ambiguity analyzer

**Status:** ENGINEERING

Given native ticks and an OHLC representation, quantify what the bar retains and what it destroys:

- extrema retained/lost;
- within-bar high/low ordering ambiguity;
- crossing-order ambiguity;
- stop-loss / take-profit path ambiguity;
- event-timing uncertainty;
- possible execution-sequence ranges consistent with the bar.

Potential applications:

- backtest reliability warnings;
- bar-based execution simulators;
- data-quality dashboards;
- teaching why OHLC does not uniquely determine the underlying path.

Strong practical value; broad concept is not a new patent claim.

---

## 3. Event timestamp provenance and alignment layer

**Status:** ENGINEERING

A reusable event registry that stores:

- official release timestamp;
- source URL/document;
- timezone;
- DST handling;
- scheduled vs actual release time;
- statement / press-conference / minutes event type;
- corrected timestamp history;
- instrument-session mapping.

Use cases:

- FOMC / CPI / NFP / PCE event research;
- gold and FX event studies;
- avoiding silent timezone and boundary errors;
- reproducible event-window extraction.

Overlaps the existing multi-source time-alignment and temporal-causality tooling in the main Idea Bank.

---

## 4. Event-study stability report generator

**Status:** ENGINEERING / RESEARCH QA

Given a research specification, automatically rerun the same event analysis across registered representations and produce:

- metric distortion curves;
- significance-decision flip tables;
- classification flip matrix;
- event-level outlier diagnostics;
- “stable / sensitive / invalid” summary.

This can become a generic pre-publication robustness check for high-frequency studies, even if the specific P1 paper is eventually killed.

---

## 5. Chinese-futures trading-day semantic validator

**Status:** ENGINEERING / supports P2

Build a validator that checks whether data pipelines correctly map:

- natural date;
- exchange trading day;
- night session;
- day session;
- holidays / weekends;
- historical rule versions.

Outputs:

- suspicious session assignments;
- mismatched daily bars;
- returns changed by naive calendar grouping;
- downstream signals affected by the mapping error.

This is a direct project use of the existing historical-session/rule-reconstruction Idea Bank item.

---

## 6. Exchange rule-change event radar

**Status:** ENGINEERING / RESEARCH DISCOVERY

Continuously archive official exchange notices for:

- fee changes;
- close-today fee changes;
- margin changes;
- price-limit changes;
- order / opening / position limits;
- trading-session changes.

For each event, store:

- publication date/time;
- effective date/time;
- affected product/contract;
- unaffected candidate controls;
- rule text provenance;
- possible identification design;
- prior-paper search status.

This can feed both academic quasi-natural experiments and trading/risk research.

---

## 7. Cross-vendor quantitative reproducibility harness

**Status:** ENGINEERING / supports P4

Normalize multiple data sources into one canonical schema, then run identical:

- factor definitions;
- continuous-contract rules;
- return calculations;
- backtests;
- risk metrics.

Produce a structured disagreement report that attributes differences to:

- timestamp semantics;
- missing data;
- adjustments;
- contract mapping;
- price fields;
- vendor corrections;
- implementation settings.

Do not confuse vendor disagreement with alpha.

---

## 8. Point-in-time revision audit toolkit

**Status:** ENGINEERING / supports P5

Extend the existing bitemporal/PIT idea into an audit tool:

- compare current historical values with archived vintages;
- record public / known / tradable time;
- identify factors or reports affected by revision;
- rerun only impacted research outputs where possible;
- generate a look-ahead-risk report.

Useful for fundamentals, macro data, index constituents, and research replication regardless of whether a PIT paper is pursued.

---

## 9. Research negative-control library

**Status:** ENGINEERING / METHODOLOGY

Maintain machine-checkable invariance controls that should hold if a pipeline is correct.

Initial examples:

- fixed-window endpoint return invariance under intermediate resampling;
- deterministic resampling reproducibility;
- timezone round-trip checks;
- trading-day/session mapping consistency;
- no future-known timestamp before feature availability time;
- identical raw path -> identical canonical representation hash.

This is useful across every quantitative project because it catches semantic bugs before they become “research results.”

---

## 10. Publication-grade experiment registry

**Status:** ENGINEERING / RESEARCH GOVERNANCE

A lightweight registry for:

- hypothesis version;
- event/sample manifest;
- exploratory vs confirmatory status;
- exclusions and reasons;
- metric definitions;
- code commit;
- raw-input hashes;
- holdout status;
- rerun history;
- final `ADVANCE / MODIFY / KILL` decision.

The objective is not bureaucracy. It prevents accidental re-use of inspected holdouts, undocumented metric changes, and false claims of untouched validation.

---

# Relationship to the main Idea Bank

These spin-outs extend or instantiate existing items in `research-and-patent-idea-bank.md`, especially:

- multi-source market-data time alignment;
- bitemporal / point-in-time financial data;
- historical trading-session / rule reconstruction;
- backtest temporal-causality audit;
- historical-data revision impact engine.

They are retained because they have project value even when the associated broad concept is already mature in the academic / patent literature.

# Development priority

1. **Multi-resolution event replay + negative controls** — required for P1 pilot.
2. **Event timestamp provenance layer** — required for reliable event studies.
3. **Chinese-futures trading-day semantic validator** — activate when P2 data qualification advances.
4. **Exchange rule-change radar** — low-cost continuous discovery for P3.
5. **Cross-vendor reproducibility harness** — activate when multiple qualified data sources are available.
6. **PIT revision audit** — defer until historical-vintage data access is solved.
