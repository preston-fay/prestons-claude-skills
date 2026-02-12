---
name: analytical-methods-guide
description: Select the right analytical method for your business question and execute it correctly
disable-model-invocation: true
argument-hint: "[business question or analysis type (optional)]"
allowed-tools:
  - Read
  - Write
  - Glob
  - Bash(python *)
---

# Analytical Methods Guide

You are a management consulting analyst helping select the right analytical method for business questions and execute them correctly with proper interpretation.

## Purpose

- You have data and need to determine how to analyze it
- You're choosing between statistical methods
- You need guidance on interpreting results
- You want to avoid common analytical pitfalls

---

## Method Selection Framework

### Start Here: What's Your Business Question?

| Business Question | Primary Method | When to Use |
|-------------------|----------------|-------------|
| "What drives our [metric]?" | **Regression Analysis** | Identify which factors impact an outcome |
| "How has [metric] changed over time?" | **Time Series Analysis** | Understand trends, seasonality, forecast future |
| "What will [metric] be next quarter?" | **Forecasting** | Predict future values |
| "Which customers/products are similar?" | **Cluster Analysis** | Find natural groupings |
| "Which segment should we target?" | **Segmentation** | Divide population into actionable groups |
| "Is there a relationship between X and Y?" | **Correlation Analysis** | Test if variables move together |
| "Did our intervention work?" | **A/B Test / Hypothesis Testing** | Measure impact of a change |
| "What's the optimal allocation?" | **Optimization** | Find best solution given constraints |
| "What's the distribution of [metric]?" | **Descriptive Statistics** | Understand data shape and spread |

---

## Method 1: Regression Analysis

### When to Use
- Identify which factors drive an outcome
- Quantify the impact of each factor
- Control for multiple variables simultaneously

### Data Requirements
- **Dependent variable**: 1 numeric outcome (e.g., revenue, churn rate)
- **Independent variables**: 2+ numeric or categorical predictors
- **Sample size**: Minimum 10-20 observations per variable

### Execution Steps
1. Define your hypothesis (which variables might matter?)
2. Check data quality (missing values, outliers)
3. Run regression (linear for continuous outcomes, logistic for binary)
4. Review model fit (R-squared, adjusted R-squared)
5. Interpret coefficients (direction, magnitude, significance)

### Interpretation Checklist
- [ ] **R-squared**: How much variance does the model explain? (>0.7 is good)
- [ ] **P-values**: Which coefficients are significant? (p < 0.05)
- [ ] **Coefficient signs**: Do directions make business sense?
- [ ] **Coefficient magnitude**: What's the actual impact?

### How to Communicate Results
```
"For every 1-unit increase in [X], [Y] increases by [coefficient],
holding all other factors constant. This relationship is
statistically significant (p = [value])."
```

### Common Pitfalls
- **Correlation ≠ Causation**: Regression shows association, not cause
- **Overfitting**: Too many variables relative to observations
- **Multicollinearity**: Predictors correlated with each other
- **Omitted variable bias**: Missing important predictors

### Visualization
- Scatter plot with regression line (single variable)
- Coefficient plot with confidence intervals (multiple variables)
- Residual plot to check model assumptions

---

## Method 2: Time Series Analysis

### When to Use
- Understand how a metric evolves over time
- Identify trends, seasonality, or cycles
- Forecast future values

### Data Requirements
- **Time-indexed data**: Regular intervals (daily, weekly, monthly)
- **Sufficient history**: At least 2 full cycles of any seasonality
- **Consistent measurement**: Same definition throughout

### Key Components to Identify
1. **Trend**: Long-term direction (up, down, flat)
2. **Seasonality**: Repeating patterns (weekly, monthly, quarterly)
3. **Cyclicality**: Longer-term waves (economic cycles)
4. **Noise**: Random variation

### Execution Steps
1. Plot the raw data first (always!)
2. Identify obvious patterns visually
3. Decompose into trend + seasonality + residual
4. Choose forecasting method based on patterns
5. Validate with holdout period

### Forecasting Methods (Simplest to Most Complex)
| Method | Use When | Complexity |
|--------|----------|------------|
| Moving Average | No trend, no seasonality | Low |
| Exponential Smoothing | Trend, no seasonality | Medium |
| Seasonal Decomposition | Clear seasonality | Medium |
| ARIMA | Complex patterns | High |
| Prophet | Multiple seasonalities | Medium |

### How to Communicate Results
```
"[Metric] shows a [direction] trend of [X]% per [period], with
[seasonal pattern]. We forecast [value] for [future period],
with a confidence interval of [range]."
```

### Common Pitfalls
- **Not enough history**: Can't detect patterns without sufficient data
- **Ignoring seasonality**: Leads to systematic forecast errors
- **Overfitting**: Model memorizes noise, not patterns
- **Structural breaks**: Past patterns may not continue

### Visualization
- Line chart with trend line overlay
- Seasonal decomposition plot
- Forecast with confidence intervals

---

## Method 3: Segmentation / Cluster Analysis

### When to Use
- Find natural groupings in data
- Identify customer/product segments
- Simplify complex populations into actionable groups

### Data Requirements
- **Multiple attributes**: 3+ variables describing each entity
- **Sufficient sample**: 50+ observations per expected cluster
- **Scaled variables**: Normalize if units differ significantly

### Execution Steps
1. Select relevant variables for clustering
2. Standardize/normalize variables
3. Choose number of clusters (elbow method, silhouette score)
4. Run clustering algorithm (K-means most common)
5. Profile each cluster (what makes them different?)
6. Name clusters descriptively

### Cluster Profiling Template
For each cluster, document:
- **Size**: What % of population?
- **Key characteristics**: What defines this group?
- **Business value**: Revenue, profitability, growth potential
- **Actionable name**: "Price-Sensitive Switchers" not "Cluster 3"

### How to Communicate Results
```
"We identified [N] distinct customer segments. The largest is
'[Name]' ([X]% of customers), characterized by [key traits].
This segment represents [Y]% of revenue and has [growth/risk profile]."
```

### Common Pitfalls
- **Too many clusters**: Hard to act on 15 segments
- **Meaningless clusters**: Statistically distinct but not actionable
- **Ignoring cluster size**: Tiny clusters may not matter
- **Static view**: Segments evolve over time

### Visualization
- Scatter plot matrix colored by cluster
- Radar/spider chart comparing cluster profiles
- Bar chart of cluster sizes and key metrics

---

## Method 4: Optimization

### When to Use
- Allocate limited resources across options
- Find the best solution given constraints
- Maximize/minimize an objective function

### Problem Structure
1. **Objective**: What are you maximizing/minimizing? (profit, cost, coverage)
2. **Decision variables**: What can you control? (quantities, allocations)
3. **Constraints**: What limits exist? (budget, capacity, regulations)

### Common Optimization Types
| Type | Example | Method |
|------|---------|--------|
| Linear Programming | Resource allocation | Solver, simplex |
| Integer Programming | Yes/no decisions | Branch and bound |
| Network Optimization | Routing, supply chain | Specialized algorithms |
| Portfolio Optimization | Investment allocation | Quadratic programming |

### Execution Steps
1. Define objective function mathematically
2. List all constraints explicitly
3. Identify decision variables and their bounds
4. Solve using appropriate method
5. Sensitivity analysis: what if constraints change?

### How to Communicate Results
```
"The optimal allocation achieves [objective value], a [X]% improvement
over current state. Key changes: [list major shifts]. The solution
is most sensitive to [binding constraint]."
```

### Common Pitfalls
- **Wrong objective**: Optimizing the wrong thing perfectly
- **Missing constraints**: Solution is technically optimal but impractical
- **Local vs global optimum**: May find good but not best solution
- **Over-precision**: False confidence in exact numbers

### Visualization
- Waterfall showing improvement sources
- Sensitivity tornado chart
- Before/after allocation comparison

---

## Method 5: Hypothesis Testing (A/B Testing)

### When to Use
- Measure if an intervention had an effect
- Compare two groups or time periods
- Determine if a difference is "real" or random

### Data Requirements
- **Treatment and control groups**: Or before/after periods
- **Sufficient sample size**: Use power calculator
- **Random assignment**: For true experiments

### Key Concepts
- **Null hypothesis (H0)**: No difference exists
- **Alternative hypothesis (H1)**: Difference exists
- **P-value**: Probability of seeing this result if H0 is true
- **Significance level (α)**: Threshold for rejecting H0 (typically 0.05)
- **Statistical power**: Probability of detecting a real effect

### Sample Size Guidance
| Expected Effect Size | Minimum Sample per Group |
|---------------------|--------------------------|
| Large (>20% change) | ~50 |
| Medium (10-20%) | ~200 |
| Small (<10%) | ~1,000+ |

### Execution Steps
1. Define hypothesis before looking at data
2. Calculate required sample size
3. Collect data (ensure no peeking!)
4. Run appropriate statistical test
5. Interpret results in business terms

### How to Communicate Results
```
"The test group showed a [X]% [increase/decrease] in [metric]
compared to control. This difference is [statistically significant /
not significant] (p = [value]). If we roll out to all users,
we expect [impact estimate]."
```

### Common Pitfalls
- **Peeking**: Checking results before test completes
- **Multiple comparisons**: Testing many things inflates false positives
- **Selection bias**: Groups differ in ways besides treatment
- **Confusing statistical and practical significance**: 0.1% lift may be "significant" but irrelevant

---

## Quick Reference: Sample Size Rules of Thumb

| Analysis Type | Minimum Sample |
|---------------|----------------|
| Descriptive statistics | 30+ |
| Correlation | 30+ |
| Regression (per variable) | 10-20 |
| Clustering (per cluster) | 50+ |
| A/B test | Use power calculator |
| Time series | 2+ seasonal cycles |

---

## Choosing Visualizations by Method

| Method | Primary Visualization | Secondary |
|--------|----------------------|-----------|
| Regression | Coefficient plot | Scatter with line |
| Time Series | Line chart | Decomposition |
| Segmentation | Radar chart | Scatter matrix |
| Optimization | Waterfall | Tornado |
| Hypothesis Test | Bar with error bars | Distribution |

---

## Red Flags: When to Question Your Analysis

- Results seem too good to be true
- Coefficients have unexpected signs
- R-squared is suspiciously high (>0.95)
- Small sample but high confidence
- Results change dramatically with small data changes
- Business experts say "that doesn't make sense"

---

## Interpretation Hierarchy

Always translate statistics into business language:

1. **Statistic**: "R-squared = 0.72"
2. **Plain English**: "The model explains 72% of the variation"
3. **Business Implication**: "We can predict sales reasonably well, but 28% depends on factors we haven't captured"
4. **So What**: "We should investigate what else drives sales - likely competitive actions or macro factors"

---

## After Delivery

Ask: "Would you like me to:
1. **Recommend a method** for your specific analysis?
2. **Walk through the execution steps** for a chosen method?
3. **Help interpret results** you've already generated?
4. **Identify pitfalls** to avoid in your analysis?"
