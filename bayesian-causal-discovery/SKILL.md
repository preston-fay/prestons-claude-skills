---
name: bayesian-causal-discovery
description: Run Bayesian causal structure learning on tabular data and deliver a DAG, bootstrap stability analysis, and confidence-tiered edge findings. Use for root-cause analysis, driver mapping, or causal hypothesis generation from CSV, SQLite, or pandas DataFrame inputs.
---

# Bayesian Causal Discovery

## Overview

Discover candidate causal structure with method triangulation (HillClimb + PC + bootstrap) and report only evidence that survives uncertainty checks. Keep claims calibrated: output hypotheses and decision guidance, not causal proof.

## Intake Workflow

Ask one question at a time and adapt to what the user already provided.

1. Confirm the data source.
- Accept CSV path, SQLite path plus table name, or an already-loaded DataFrame.
- If the user gives a file path, inspect shape, columns, and a preview before proceeding.

2. Identify the target variable.
- Ask which variable is the effect/outcome to explain.
- If unclear, propose likely outcome columns and ask for confirmation.

3. Capture exogenous variables.
- Ask which variables are externally determined and must not have incoming arrows.

4. Capture domain constraints.
- Ask for known whitelist/blacklist edges.
- Enforce impossible-edge constraints (for example, future outcomes causing past inputs).

5. Confirm variable scale.
- Under 12 variables: run full analysis directly.
- 12-30 variables: propose grouping and staged drill-down.
- Over 30 variables: require aggregation strategy before deep edge-level claims.

## Execution Workflow

1. Validate data quality.
- Drop constant columns and columns with more than 30% missing values.
- Warn if fewer than 100 rows; heavily caveat conclusions.

2. Configure parameters based on sample size.
- `n_bins=2` if under 200 rows, otherwise default to `3`.
- `hc_restarts=5` if under 200 rows, otherwise default to `3`.
- `n_bootstrap=30` baseline; increase to `50` for large data if runtime allows.

3. Run the engine.
- Prefer the wrapper for reproducibility:
```bash
python3 skills/bayesian-causal-discovery/scripts/run_causal_discovery.py \
  --csv /path/to/data.csv \
  --target target_column \
  --exog weather,month \
  --blacklist month:weather \
  --output ./causal_discovery_output
```
- If needed, call `scripts/engine.py` directly.

4. Interpret with confidence discipline.
- `GREEN`: both methods agree and bootstrap frequency >= 70%.
- `YELLOW`: one method only, or bootstrap between 30% and 70%.
- `RED`: weak support. Mention only when asked or when it changes decisions.

5. Deliver findings in this order.
- Headline (one sentence)
- Causal backbone (top GREEN edges with evidence)
- Emerging signals (YELLOW edges)
- Notable absences (expected edges that did not appear)
- Limitations and caveats
- Next best actions (data collection, experiments, sensitivity checks)

Use `references/report-template.md` for final structure.

## Quality Gates

Verify before final delivery:

- Every GREEN edge has `p < 0.05`.
- Output graph is acyclic.
- Exogenous variables have no incoming edges from endogenous variables.
- Target variable does not have outgoing edges if it represents a future outcome.
- Report distinguishes "consistent with data" from "proven causal effect."

## Edge Case Handling

- Very small data (`< 50` rows): warn strongly and treat results as exploratory only.
- Very high dimensionality (`> 30` variables): force grouped macro-DAG first.
- Disagreement with prior beliefs: explain that disagreement is a discovery signal, then provide plausible mechanisms (mediation, sample limitations, misspecification).

## Follow-Ups to Offer

- Sensitivity analysis: rerun with 2-bin and 4-bin discretization.
- Focused drill-down on one edge or one feature group.
- Stakeholder one-pager summarizing causal implications and decision impact.

## Bundled Resources

- `scripts/engine.py`: core causal discovery engine (HillClimb, PC, bootstrap, plotting).
- `scripts/run_causal_discovery.py`: reproducible command-line wrapper with data-source handling and constraint parsing.
- `references/report-template.md`: standard report skeleton for consistent delivery.

If dependencies are missing (`pandas`, `numpy`, `matplotlib`), state the missing package and stop for user confirmation before attempting installs.
