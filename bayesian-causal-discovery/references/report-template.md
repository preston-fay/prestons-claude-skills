# Causal Discovery Results Template

Use this structure in the final response.

## Headline

State the main causal storyline in one sentence.

## Causal Backbone (GREEN)

List the most robust edges:
- `source -> target` (bootstrap %, method agreement, p-value)
- Practical interpretation in plain language

## Emerging Signals (YELLOW)

List moderate-confidence edges and what would make them decision-ready.

## Notable Absences

Highlight expected edges that were not found and plausible explanations:
- Mediation through another variable
- Data limitations
- Relationship likely weak or absent

## Limitations

- Observational data caveat (hypothesis generation, not proof)
- Sample-size caveat
- Discretization sensitivity caveat
- Domain-constraint assumptions caveat

## Recommended Next Steps

1. Data improvements that would most reduce uncertainty
2. Validation experiments to test top edges
3. Sensitivity reruns (bin count, bootstrap count, feature subsets)

## Files Produced

- `causal_discovery_results.json`
- `edge_confidence_table.csv`
- `dag_hillclimb.png`
- `dag_pc.png`
- `dag_bootstrap.png`
- `bootstrap_heatmap.png`
- `edge_confidence.png`
