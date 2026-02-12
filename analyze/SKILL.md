---
name: analyze
description: "Extract insights from data - find key patterns, generate recommendations, and create executive summaries. Use when you need to go beyond EDA to synthesize findings into actionable business insights."
context: fork
agent: general-purpose
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(python *)
  - Bash(pip install *)
  - Write
hooks:
  PostToolUse:
    - matcher: "*"
      command: ["bash", "/Users/pfay01/.claude/hooks/log-tool-use.sh"]
---

# Data Analysis & Insight Extraction

Transform raw data into actionable business insights. This skill focuses on pattern recognition, hypothesis testing, segmentation, and generating strategic recommendations.

## When to Use

- After EDA, when you need to extract **meaning** from patterns
- When stakeholders need **recommendations**, not just statistics
- For creating **executive summaries** with key findings
- When performing **hypothesis testing** or A/B analysis
- For **segmentation** and customer/product analysis

---

## Phase 1: Insight Framework

### The Insight Pyramid

```
         /\
        /  \     RECOMMENDATIONS
       /----\    (What should we do?)
      /      \
     /--------\  INSIGHTS
    /          \ (What does it mean?)
   /------------\
  /              \ FINDINGS
 /----------------\ (What patterns exist?)
/                  \ DATA
```

### Insight Quality Checklist

Every insight should be:
- **Specific**: Quantified with numbers, not vague
- **Actionable**: Leads to a clear next step
- **Relevant**: Matters to the business question
- **Supported**: Backed by evidence in the data
- **Novel**: Not obvious or already known

---

## Phase 2: Pattern Analysis

### Trend Identification

```python
import pandas as pd
import numpy as np

def identify_trends(df, date_col, value_col, window=7):
    """Identify trends in time series data."""
    df = df.sort_values(date_col)

    # Calculate rolling statistics
    df['rolling_mean'] = df[value_col].rolling(window=window).mean()
    df['rolling_std'] = df[value_col].rolling(window=window).std()

    # Calculate trend direction
    df['trend'] = np.where(
        df['rolling_mean'].diff() > 0, 'increasing',
        np.where(df['rolling_mean'].diff() < 0, 'decreasing', 'stable')
    )

    # Detect significant changes
    df['z_score'] = (df[value_col] - df['rolling_mean']) / df['rolling_std']
    df['anomaly'] = abs(df['z_score']) > 2

    # Summary
    recent_trend = df['trend'].iloc[-window:].mode().iloc[0]
    overall_change = (df[value_col].iloc[-1] - df[value_col].iloc[0]) / df[value_col].iloc[0] * 100
    anomaly_count = df['anomaly'].sum()

    print(f"Trend Analysis: {value_col}")
    print(f"  Recent trend: {recent_trend}")
    print(f"  Overall change: {overall_change:+.1f}%")
    print(f"  Anomalies detected: {anomaly_count}")

    return df

# Usage: df = identify_trends(df, 'date', 'revenue')
```

### Segment Comparison

```python
def compare_segments(df, segment_col, metric_cols):
    """Compare performance across segments."""
    results = []

    for metric in metric_cols:
        segment_stats = df.groupby(segment_col)[metric].agg([
            'count', 'mean', 'median', 'std', 'min', 'max'
        ])

        # Calculate relative performance
        overall_mean = df[metric].mean()
        segment_stats['vs_overall'] = ((segment_stats['mean'] - overall_mean) / overall_mean * 100).round(1)
        segment_stats['metric'] = metric

        results.append(segment_stats)

    comparison = pd.concat(results)

    # Find top and bottom performers
    for metric in metric_cols:
        metric_data = comparison[comparison['metric'] == metric]
        top = metric_data['mean'].idxmax()
        bottom = metric_data['mean'].idxmin()
        print(f"\n{metric}:")
        print(f"  Top segment: {top} ({metric_data.loc[top, 'vs_overall']:+.1f}% vs overall)")
        print(f"  Bottom segment: {bottom} ({metric_data.loc[bottom, 'vs_overall']:+.1f}% vs overall)")

    return comparison

# Usage: compare_segments(df, 'region', ['revenue', 'margin', 'customers'])
```

### Pareto Analysis (80/20 Rule)

```python
def pareto_analysis(df, category_col, value_col):
    """Identify the vital few that drive the majority of value."""
    # Aggregate by category
    summary = df.groupby(category_col)[value_col].sum().sort_values(ascending=False)

    # Calculate cumulative percentage
    total = summary.sum()
    summary_df = pd.DataFrame({
        'value': summary,
        'pct': summary / total * 100,
        'cumulative_pct': (summary.cumsum() / total * 100)
    })

    # Find the 80% threshold
    threshold_80 = summary_df[summary_df['cumulative_pct'] <= 80]
    n_vital = len(threshold_80) + 1  # +1 to include the one that crosses 80%
    pct_vital = n_vital / len(summary_df) * 100

    print(f"\nPareto Analysis: {value_col} by {category_col}")
    print(f"  {n_vital} {category_col}s ({pct_vital:.1f}%) drive ~80% of {value_col}")
    print(f"\n  Top 5 {category_col}s:")
    for idx, row in summary_df.head().iterrows():
        print(f"    {idx}: {row['value']:,.0f} ({row['pct']:.1f}%)")

    return summary_df

# Usage: pareto_analysis(df, 'product', 'revenue')
```

---

## Phase 3: Statistical Testing

### Hypothesis Testing

```python
from scipy import stats

def compare_groups(df, group_col, value_col, group_a, group_b, alpha=0.05):
    """Statistical comparison between two groups."""
    a = df[df[group_col] == group_a][value_col].dropna()
    b = df[df[group_col] == group_b][value_col].dropna()

    # Descriptive stats
    print(f"\nComparing {group_a} vs {group_b} on {value_col}")
    print(f"  {group_a}: n={len(a)}, mean={a.mean():.2f}, std={a.std():.2f}")
    print(f"  {group_b}: n={len(b)}, mean={b.mean():.2f}, std={b.std():.2f}")

    # Effect size (Cohen's d)
    pooled_std = np.sqrt(((len(a)-1)*a.std()**2 + (len(b)-1)*b.std()**2) / (len(a)+len(b)-2))
    cohens_d = (a.mean() - b.mean()) / pooled_std
    print(f"  Effect size (Cohen's d): {cohens_d:.3f}", end='')
    if abs(cohens_d) < 0.2:
        print(" (negligible)")
    elif abs(cohens_d) < 0.5:
        print(" (small)")
    elif abs(cohens_d) < 0.8:
        print(" (medium)")
    else:
        print(" (large)")

    # T-test
    t_stat, p_value = stats.ttest_ind(a, b)
    print(f"  T-test: t={t_stat:.3f}, p={p_value:.4f}")

    if p_value < alpha:
        print(f"  SIGNIFICANT at alpha={alpha}")
        diff_pct = (a.mean() - b.mean()) / b.mean() * 100
        print(f"  {group_a} is {diff_pct:+.1f}% vs {group_b}")
    else:
        print(f"  Not significant at alpha={alpha}")

    return {'t_stat': t_stat, 'p_value': p_value, 'cohens_d': cohens_d}

# Usage: compare_groups(df, 'treatment', 'conversion_rate', 'A', 'B')
```

### Correlation Significance

```python
def significant_correlations(df, target_col, alpha=0.05):
    """Find statistically significant correlations with target."""
    numerics = df.select_dtypes(include=['number']).drop(columns=[target_col], errors='ignore')

    results = []
    for col in numerics.columns:
        corr, p_value = stats.pearsonr(df[col].dropna(), df[target_col].dropna())
        results.append({
            'variable': col,
            'correlation': corr,
            'p_value': p_value,
            'significant': p_value < alpha
        })

    results_df = pd.DataFrame(results).sort_values('correlation', key=abs, ascending=False)

    print(f"\nCorrelations with {target_col} (alpha={alpha}):")
    print("-" * 50)
    for _, row in results_df.head(10).iterrows():
        sig = "*" if row['significant'] else ""
        print(f"  {row['variable']}: r={row['correlation']:.3f} (p={row['p_value']:.4f}){sig}")

    return results_df

# Usage: significant_correlations(df, 'revenue')
```

---

## Phase 4: Segmentation

### RFM Analysis (Customer Segmentation)

```python
def rfm_analysis(df, customer_col, date_col, value_col, reference_date=None):
    """RFM (Recency, Frequency, Monetary) customer segmentation."""
    if reference_date is None:
        reference_date = df[date_col].max()

    # Calculate RFM metrics
    rfm = df.groupby(customer_col).agg({
        date_col: lambda x: (reference_date - x.max()).days,  # Recency
        customer_col: 'count',  # Frequency
        value_col: 'sum'  # Monetary
    }).rename(columns={
        date_col: 'recency',
        customer_col: 'frequency',
        value_col: 'monetary'
    })

    # Score each metric (1-5, 5 being best)
    rfm['R_score'] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
    rfm['F_score'] = pd.qcut(rfm['frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
    rfm['M_score'] = pd.qcut(rfm['monetary'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])

    rfm['RFM_score'] = rfm['R_score'].astype(str) + rfm['F_score'].astype(str) + rfm['M_score'].astype(str)

    # Segment labels
    def segment_label(row):
        r, f, m = int(row['R_score']), int(row['F_score']), int(row['M_score'])
        if r >= 4 and f >= 4 and m >= 4:
            return 'Champions'
        elif r >= 4 and f >= 3:
            return 'Loyal Customers'
        elif r >= 3 and f >= 1 and m >= 3:
            return 'Potential Loyalists'
        elif r >= 4 and f <= 2:
            return 'New Customers'
        elif r <= 2 and f >= 3 and m >= 3:
            return 'At Risk'
        elif r <= 2 and f <= 2:
            return 'Lost'
        else:
            return 'Others'

    rfm['segment'] = rfm.apply(segment_label, axis=1)

    # Summary
    print("\nRFM Segmentation Results:")
    print("-" * 40)
    segment_summary = rfm.groupby('segment').agg({
        'recency': 'mean',
        'frequency': 'mean',
        'monetary': ['mean', 'sum', 'count']
    }).round(2)
    print(segment_summary)

    return rfm

# Usage: rfm = rfm_analysis(df, 'customer_id', 'order_date', 'order_value')
```

### K-Means Clustering

```python
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def segment_kmeans(df, features, n_clusters=4):
    """Segment data using K-Means clustering."""
    # Prepare data
    X = df[features].dropna()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Fit K-Means
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df.loc[X.index, 'cluster'] = kmeans.fit_predict(X_scaled)

    # Profile clusters
    print(f"\nK-Means Clustering (k={n_clusters})")
    print("-" * 50)

    cluster_profiles = df.groupby('cluster')[features].mean()
    cluster_sizes = df['cluster'].value_counts().sort_index()

    for cluster in range(n_clusters):
        print(f"\nCluster {cluster} (n={cluster_sizes[cluster]:,}):")
        for feature in features:
            overall_mean = df[feature].mean()
            cluster_mean = cluster_profiles.loc[cluster, feature]
            diff_pct = (cluster_mean - overall_mean) / overall_mean * 100
            direction = "above" if diff_pct > 0 else "below"
            print(f"  {feature}: {cluster_mean:.2f} ({abs(diff_pct):.1f}% {direction} avg)")

    return df, kmeans

# Usage: df, model = segment_kmeans(df, ['revenue', 'frequency', 'tenure'])
```

---

## Phase 5: Generate Recommendations

### Recommendation Framework

```python
def generate_recommendations(findings):
    """Convert findings into actionable recommendations."""
    recommendations = []

    for finding in findings:
        rec = {
            'finding': finding['description'],
            'impact': finding.get('impact', 'Medium'),
            'confidence': finding.get('confidence', 'High'),
            'recommendation': None,
            'next_steps': []
        }

        # Generate recommendation based on finding type
        if finding['type'] == 'trend_decline':
            rec['recommendation'] = f"Investigate root cause of {finding['metric']} decline"
            rec['next_steps'] = [
                "Review recent operational changes",
                "Compare with historical patterns",
                "Identify affected segments"
            ]

        elif finding['type'] == 'segment_underperformance':
            rec['recommendation'] = f"Develop targeted strategy for {finding['segment']}"
            rec['next_steps'] = [
                "Deep-dive analysis on underperforming segment",
                "Benchmark against top performers",
                "Pilot improvement program"
            ]

        elif finding['type'] == 'correlation':
            rec['recommendation'] = f"Leverage {finding['variable']} to improve {finding['target']}"
            rec['next_steps'] = [
                "Validate causal relationship",
                "Design A/B test",
                "Develop action plan if validated"
            ]

        elif finding['type'] == 'pareto':
            rec['recommendation'] = f"Focus resources on top {finding['vital_few_pct']}% of {finding['category']}"
            rec['next_steps'] = [
                "Ensure top performers receive priority attention",
                "Evaluate cost of serving long tail",
                "Consider portfolio optimization"
            ]

        recommendations.append(rec)

    return recommendations

# Example usage
findings = [
    {'type': 'trend_decline', 'description': 'Revenue declined 15% in Q4', 'metric': 'revenue', 'impact': 'High'},
    {'type': 'segment_underperformance', 'description': 'APAC region 30% below target', 'segment': 'APAC'},
    {'type': 'correlation', 'description': 'Strong correlation between NPS and retention', 'variable': 'NPS', 'target': 'retention'},
]

recs = generate_recommendations(findings)
for r in recs:
    print(f"\nFinding: {r['finding']}")
    print(f"Recommendation: {r['recommendation']}")
    print("Next Steps:")
    for step in r['next_steps']:
        print(f"  - {step}")
```

---

## Phase 6: Executive Summary

### Summary Template

```python
def create_executive_summary(analysis_results):
    """Generate executive summary from analysis results."""
    summary = f"""
# Executive Summary

## Key Findings

{chr(10).join([f"- **{f['title']}**: {f['description']}" for f in analysis_results['findings'][:5]])}

## Critical Metrics

| Metric | Current | Change | Status |
|--------|---------|--------|--------|
{chr(10).join([f"| {m['name']} | {m['current']} | {m['change']} | {m['status']} |" for m in analysis_results['metrics']])}

## Top Recommendations

{chr(10).join([f"{i+1}. **{r['title']}**: {r['action']}" for i, r in enumerate(analysis_results['recommendations'][:3])])}

## Risks & Considerations

{chr(10).join([f"- {r}" for r in analysis_results.get('risks', ['No significant risks identified'])])}

## Suggested Next Steps

1. {analysis_results['next_steps'][0] if analysis_results.get('next_steps') else 'Deep-dive into top finding'}
2. {analysis_results['next_steps'][1] if len(analysis_results.get('next_steps', [])) > 1 else 'Validate with stakeholders'}
3. {analysis_results['next_steps'][2] if len(analysis_results.get('next_steps', [])) > 2 else 'Develop action plan'}

---
*Analysis generated on {pd.Timestamp.now().strftime('%Y-%m-%d')}*
"""
    return summary

# Usage: print(create_executive_summary(results))
```

---

## Quick Analysis Templates

### Revenue Analysis

```python
def analyze_revenue(df, date_col, revenue_col, segment_cols=None):
    """Complete revenue analysis."""
    print("=" * 60)
    print("REVENUE ANALYSIS")
    print("=" * 60)

    # Overall metrics
    total = df[revenue_col].sum()
    avg = df[revenue_col].mean()
    median = df[revenue_col].median()
    print(f"\nTotal Revenue: ${total:,.0f}")
    print(f"Average: ${avg:,.0f}")
    print(f"Median: ${median:,.0f}")

    # Time trends
    if date_col:
        df_time = df.groupby(pd.Grouper(key=date_col, freq='M'))[revenue_col].sum()
        mom_growth = df_time.pct_change().iloc[-1] * 100
        yoy_growth = (df_time.iloc[-1] / df_time.iloc[-13] - 1) * 100 if len(df_time) > 12 else None
        print(f"\nMoM Growth: {mom_growth:+.1f}%")
        if yoy_growth:
            print(f"YoY Growth: {yoy_growth:+.1f}%")

    # Segment breakdown
    if segment_cols:
        for seg in segment_cols:
            print(f"\nRevenue by {seg}:")
            seg_rev = df.groupby(seg)[revenue_col].agg(['sum', 'mean', 'count'])
            seg_rev['pct'] = seg_rev['sum'] / total * 100
            print(seg_rev.sort_values('sum', ascending=False).head(10))

    # Pareto
    if segment_cols:
        pareto_analysis(df, segment_cols[0], revenue_col)

# Usage: analyze_revenue(df, 'date', 'revenue', ['product', 'region'])
```

### Churn Analysis

```python
def analyze_churn(df, churn_col, features):
    """Analyze churn patterns and predictors."""
    print("=" * 60)
    print("CHURN ANALYSIS")
    print("=" * 60)

    # Overall churn rate
    churn_rate = df[churn_col].mean() * 100
    print(f"\nOverall Churn Rate: {churn_rate:.1f}%")

    # Churn by segment
    for feature in features:
        if df[feature].dtype in ['object', 'category', 'bool']:
            print(f"\nChurn by {feature}:")
            churn_by_seg = df.groupby(feature)[churn_col].agg(['mean', 'count'])
            churn_by_seg['mean'] = churn_by_seg['mean'] * 100
            churn_by_seg = churn_by_seg.sort_values('mean', ascending=False)
            for idx, row in churn_by_seg.iterrows():
                diff = row['mean'] - churn_rate
                print(f"  {idx}: {row['mean']:.1f}% ({diff:+.1f}% vs avg), n={row['count']:,}")

    # Correlation with numeric features
    print("\nChurn Correlations:")
    for feature in features:
        if pd.api.types.is_numeric_dtype(df[feature]):
            corr = df[feature].corr(df[churn_col])
            print(f"  {feature}: r={corr:.3f}")

# Usage: analyze_churn(df, 'churned', ['tenure', 'plan_type', 'support_tickets'])
```

---

## Tips for Effective Analysis

1. **Start with the business question**: What decision needs to be made?
2. **Use the "So what?" test**: Every finding should answer "so what should we do?"
3. **Quantify everything**: "Revenue is down" vs "Revenue declined 15% ($2.3M)"
4. **Consider alternatives**: What else could explain this pattern?
5. **Validate with stakeholders**: Does this match their intuition? If not, dig deeper.
6. **Prioritize recommendations**: Impact vs. effort matrix
7. **Be honest about uncertainty**: Confidence intervals, caveats, data limitations
