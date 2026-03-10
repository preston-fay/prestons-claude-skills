# EDA — Full Code Reference

Complete Python implementations for all 6 EDA phases.
Referenced by SKILL.md.

---

## Phase 1: Data Ingestion

### Supported Formats

```python
import pandas as pd

# CSV with options
df = pd.read_csv('file.csv',
                 encoding='utf-8',      # or 'latin-1', 'cp1252'
                 parse_dates=['date'],   # auto-parse dates
                 dtype={'id': str},      # force types
                 na_values=['NA', ''])   # treat as missing

# Excel
df = pd.read_excel('file.xlsx', sheet_name='Sheet1')
all_sheets = pd.read_excel('file.xlsx', sheet_name=None)  # dict of DataFrames

# Parquet (efficient for large data)
df = pd.read_parquet('file.parquet')

# JSON
df = pd.read_json('file.json')
df = pd.json_normalize(json_data)  # for nested JSON

# SQL
from sqlalchemy import create_engine
engine = create_engine('postgresql://user:pass@host/db')
df = pd.read_sql('SELECT * FROM table', engine)

# Large files - chunked reading
chunks = pd.read_csv('large.csv', chunksize=100000)
df = pd.concat(chunks, ignore_index=True)
```

---

## Phase 2: Structural Analysis

### Dataset Overview

```python
def dataset_overview(df):
    """Generate comprehensive dataset overview."""
    print("=" * 60)
    print("DATASET OVERVIEW")
    print("=" * 60)

    print(f"\nShape: {df.shape[0]:,} rows x {df.shape[1]} columns")
    print(f"Memory: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

    print("\n--- Column Types ---")
    print(df.dtypes.value_counts())

    print("\n--- Columns by Type ---")
    for dtype in df.dtypes.unique():
        cols = df.select_dtypes(include=[dtype]).columns.tolist()
        print(f"  {dtype}: {cols[:5]}{'...' if len(cols) > 5 else ''}")

    print("\n--- Missing Values ---")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    missing_df = pd.DataFrame({'count': missing, 'pct': missing_pct})
    missing_df = missing_df[missing_df['count'] > 0].sort_values('count', ascending=False)
    if len(missing_df) > 0:
        print(missing_df)
    else:
        print("  No missing values!")

    print("\n--- Duplicates ---")
    dupes = df.duplicated().sum()
    print(f"  Duplicate rows: {dupes:,} ({dupes/len(df)*100:.2f}%)")

    return missing_df

overview = dataset_overview(df)
```

### Column Profiling

```python
def profile_columns(df):
    """Profile each column with appropriate statistics."""
    profiles = []

    for col in df.columns:
        profile = {
            'column': col,
            'dtype': str(df[col].dtype),
            'non_null': df[col].notna().sum(),
            'null_pct': df[col].isnull().mean() * 100,
            'unique': df[col].nunique(),
            'unique_pct': df[col].nunique() / len(df) * 100
        }

        # Numeric columns
        if pd.api.types.is_numeric_dtype(df[col]):
            profile.update({
                'min': df[col].min(),
                'max': df[col].max(),
                'mean': df[col].mean(),
                'median': df[col].median(),
                'std': df[col].std(),
                'zeros': (df[col] == 0).sum(),
                'negatives': (df[col] < 0).sum()
            })

        # String columns
        elif pd.api.types.is_string_dtype(df[col]) or df[col].dtype == 'object':
            profile.update({
                'min_len': df[col].astype(str).str.len().min(),
                'max_len': df[col].astype(str).str.len().max(),
                'top_value': df[col].mode().iloc[0] if len(df[col].mode()) > 0 else None,
                'top_freq': df[col].value_counts().iloc[0] if len(df[col].value_counts()) > 0 else 0
            })

        # Datetime columns
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            profile.update({
                'min_date': df[col].min(),
                'max_date': df[col].max(),
                'range_days': (df[col].max() - df[col].min()).days
            })

        profiles.append(profile)

    return pd.DataFrame(profiles)

column_profiles = profile_columns(df)
print(column_profiles.to_string())
```

---

## Phase 3: Statistical Analysis

### Numeric Distributions

```python
def analyze_numerics(df):
    """Analyze all numeric columns."""
    numerics = df.select_dtypes(include=['number'])

    print("=" * 60)
    print("NUMERIC ANALYSIS")
    print("=" * 60)

    # Basic stats
    print("\n--- Descriptive Statistics ---")
    print(numerics.describe().T)

    # Skewness and kurtosis
    print("\n--- Distribution Shape ---")
    for col in numerics.columns:
        skew = numerics[col].skew()
        kurt = numerics[col].kurtosis()
        print(f"  {col}: skew={skew:.2f}, kurtosis={kurt:.2f}")
        if abs(skew) > 1:
            print(f"    -> Highly skewed ({'right' if skew > 0 else 'left'})")

    # Outliers (IQR method)
    print("\n--- Outliers (IQR Method) ---")
    for col in numerics.columns:
        Q1 = numerics[col].quantile(0.25)
        Q3 = numerics[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers = ((numerics[col] < Q1 - 1.5*IQR) | (numerics[col] > Q3 + 1.5*IQR)).sum()
        if outliers > 0:
            print(f"  {col}: {outliers} outliers ({outliers/len(df)*100:.2f}%)")

    return numerics.describe()

numeric_stats = analyze_numerics(df)
```

### Categorical Analysis

```python
def analyze_categoricals(df, max_categories=20):
    """Analyze categorical/object columns."""
    categoricals = df.select_dtypes(include=['object', 'category', 'bool'])

    print("=" * 60)
    print("CATEGORICAL ANALYSIS")
    print("=" * 60)

    for col in categoricals.columns:
        print(f"\n--- {col} ---")
        n_unique = df[col].nunique()
        print(f"  Unique values: {n_unique}")

        if n_unique <= max_categories:
            print(f"  Value counts:")
            vc = df[col].value_counts()
            for val, count in vc.items():
                print(f"    {val}: {count} ({count/len(df)*100:.1f}%)")
        else:
            print(f"  Top 10 values:")
            vc = df[col].value_counts().head(10)
            for val, count in vc.items():
                print(f"    {val}: {count} ({count/len(df)*100:.1f}%)")
            print(f"  ... and {n_unique - 10} more")

analyze_categoricals(df)
```

### Correlation Analysis

```python
def analyze_correlations(df, threshold=0.7):
    """Find and report correlations."""
    numerics = df.select_dtypes(include=['number'])

    if len(numerics.columns) < 2:
        print("Not enough numeric columns for correlation analysis")
        return None

    corr = numerics.corr()

    print("=" * 60)
    print("CORRELATION ANALYSIS")
    print("=" * 60)

    # Find high correlations
    print(f"\n--- High Correlations (|r| > {threshold}) ---")
    high_corr = []
    for i in range(len(corr.columns)):
        for j in range(i+1, len(corr.columns)):
            if abs(corr.iloc[i, j]) > threshold:
                high_corr.append({
                    'var1': corr.columns[i],
                    'var2': corr.columns[j],
                    'corr': corr.iloc[i, j]
                })

    if high_corr:
        for item in sorted(high_corr, key=lambda x: abs(x['corr']), reverse=True):
            print(f"  {item['var1']} <-> {item['var2']}: {item['corr']:.3f}")
    else:
        print("  No high correlations found")

    return corr

correlations = analyze_correlations(df)
```

---

## Phase 4: Data Quality Assessment

```python
def assess_data_quality(df):
    """Comprehensive data quality report."""
    print("=" * 60)
    print("DATA QUALITY ASSESSMENT")
    print("=" * 60)

    issues = []

    # 1. Missing values
    missing = df.isnull().sum()
    high_missing = missing[missing / len(df) > 0.1]
    if len(high_missing) > 0:
        issues.append(f"High missing (>10%): {list(high_missing.index)}")

    # 2. Duplicates
    dupes = df.duplicated().sum()
    if dupes > 0:
        issues.append(f"Duplicate rows: {dupes}")

    # 3. Constant columns
    constant = [col for col in df.columns if df[col].nunique() <= 1]
    if constant:
        issues.append(f"Constant columns: {constant}")

    # 4. High cardinality (potential IDs)
    high_card = [col for col in df.columns
                 if df[col].nunique() / len(df) > 0.9
                 and df[col].dtype == 'object']
    if high_card:
        issues.append(f"High cardinality (>90% unique): {high_card}")

    # 5. Mixed types
    for col in df.select_dtypes(include=['object']).columns:
        try:
            numeric_count = pd.to_numeric(df[col], errors='coerce').notna().sum()
            if 0 < numeric_count < len(df[col].dropna()):
                issues.append(f"Mixed types in {col}: {numeric_count} numeric values")
        except:
            pass

    # 6. Negative values in typically positive columns
    for col in df.select_dtypes(include=['number']).columns:
        if any(kw in col.lower() for kw in ['price', 'amount', 'count', 'qty', 'quantity', 'age']):
            neg_count = (df[col] < 0).sum()
            if neg_count > 0:
                issues.append(f"Negative values in {col}: {neg_count}")

    # Report
    if issues:
        print("\nISSUES FOUND:")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
    else:
        print("\nNo major data quality issues detected!")

    # Quality score
    score = 100 - len(issues) * 10
    print(f"\nQuality Score: {max(0, score)}/100")

    return issues

quality_issues = assess_data_quality(df)
```

---

## Phase 5: Visualization

### Apply Kearney Design System

```python
import matplotlib.pyplot as plt

# Kearney colors - USE IN ORDER
KEARNEY_COLORS = [
    '#D2D2D2', '#A5A6A5', '#787878', '#E0D2FA', '#C8A5F0',
    '#AF7DEB', '#4B4B4B', '#1E1E1E', '#9150E1', '#7823DC'
]
KEARNEY_PURPLE = '#7823DC'
KEARNEY_BLACK = '#1E1E1E'

# Apply Kearney style globally
plt.rcParams.update({
    'font.family': 'Arial',
    'font.size': 12,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.spines.left': False,
    'axes.spines.bottom': False,
    'axes.grid': False,  # NO GRIDLINES
    'axes.facecolor': 'white',
    'figure.facecolor': 'white',
    'axes.prop_cycle': plt.cycler(color=KEARNEY_COLORS)
})
```

### Distribution Plots

```python
def plot_distributions(df, cols=None, figsize=(12, 4)):
    """Plot distributions for numeric columns."""
    if cols is None:
        cols = df.select_dtypes(include=['number']).columns[:6]

    n_cols = min(3, len(cols))
    n_rows = (len(cols) + n_cols - 1) // n_cols

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(figsize[0], figsize[1] * n_rows))
    axes = axes.flatten() if hasattr(axes, 'flatten') else [axes]

    for i, col in enumerate(cols):
        ax = axes[i]
        ax.hist(df[col].dropna(), bins=30, color=KEARNEY_COLORS[i % len(KEARNEY_COLORS)],
                edgecolor='white', linewidth=0.5)
        ax.set_title(col, fontsize=14, fontweight='bold')
        ax.set_xlabel('')
        ax.set_ylabel('')

    # Hide unused axes
    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)

    plt.tight_layout()
    plt.savefig('distributions.png', dpi=150, bbox_inches='tight')
    plt.show()

plot_distributions(df)
```

### Correlation Heatmap

```python
def plot_correlation_heatmap(df, figsize=(10, 8)):
    """Create correlation heatmap with Kearney colors."""
    import seaborn as sns

    numerics = df.select_dtypes(include=['number'])
    corr = numerics.corr()

    # Kearney purple gradient
    cmap = sns.diverging_palette(250, 280, s=80, l=55, as_cmap=True)

    fig, ax = plt.subplots(figsize=figsize)

    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, cmap=cmap, center=0,
                square=True, linewidths=0.5,
                annot=True, fmt='.2f', annot_kws={'size': 9},
                cbar_kws={'shrink': 0.8})

    ax.set_title('Correlation Matrix', fontsize=16, fontweight='bold', pad=20)

    plt.tight_layout()
    plt.savefig('correlation_heatmap.png', dpi=150, bbox_inches='tight')
    plt.show()

import numpy as np
plot_correlation_heatmap(df)
```

### Category Bar Charts

```python
def plot_categorical(df, col, top_n=10, figsize=(10, 6)):
    """Horizontal bar chart for categorical data."""
    counts = df[col].value_counts().head(top_n)

    fig, ax = plt.subplots(figsize=figsize)

    bars = ax.barh(range(len(counts)), counts.values, color=KEARNEY_PURPLE)
    ax.set_yticks(range(len(counts)))
    ax.set_yticklabels(counts.index)
    ax.invert_yaxis()

    # Add value labels
    for i, (val, count) in enumerate(zip(counts.index, counts.values)):
        ax.text(count + counts.max() * 0.01, i, f'{count:,}',
                va='center', fontsize=10)

    ax.set_title(f'{col} Distribution', fontsize=16, fontweight='bold')
    ax.set_xlabel('')

    plt.tight_layout()
    plt.savefig(f'{col}_distribution.png', dpi=150, bbox_inches='tight')
    plt.show()

# Example usage for each categorical column
for col in df.select_dtypes(include=['object']).columns[:3]:
    if df[col].nunique() <= 20:
        plot_categorical(df, col)
```

---

## Phase 6: Automated Report

```python
def generate_eda_report(df, output_file='eda_report.md'):
    """Generate comprehensive EDA report as markdown."""

    report = []
    report.append("# Exploratory Data Analysis Report\n")
    report.append(f"**Generated**: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}\n")

    # Overview
    report.append("## Dataset Overview\n")
    report.append(f"- **Rows**: {df.shape[0]:,}")
    report.append(f"- **Columns**: {df.shape[1]}")
    report.append(f"- **Memory**: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB\n")

    # Column types
    report.append("## Column Types\n")
    report.append("| Type | Count |")
    report.append("|------|-------|")
    for dtype, count in df.dtypes.value_counts().items():
        report.append(f"| {dtype} | {count} |")
    report.append("")

    # Missing values
    missing = df.isnull().sum()
    if missing.sum() > 0:
        report.append("## Missing Values\n")
        report.append("| Column | Missing | Percent |")
        report.append("|--------|---------|---------|")
        for col in missing[missing > 0].sort_values(ascending=False).index:
            pct = missing[col] / len(df) * 100
            report.append(f"| {col} | {missing[col]:,} | {pct:.1f}% |")
        report.append("")

    # Numeric summary
    numerics = df.select_dtypes(include=['number'])
    if len(numerics.columns) > 0:
        report.append("## Numeric Variables Summary\n")
        report.append("| Column | Min | Max | Mean | Median | Std |")
        report.append("|--------|-----|-----|------|--------|-----|")
        for col in numerics.columns:
            stats = numerics[col].describe()
            report.append(f"| {col} | {stats['min']:.2f} | {stats['max']:.2f} | {stats['mean']:.2f} | {stats['50%']:.2f} | {stats['std']:.2f} |")
        report.append("")

    # Categorical summary
    categoricals = df.select_dtypes(include=['object', 'category'])
    if len(categoricals.columns) > 0:
        report.append("## Categorical Variables\n")
        for col in categoricals.columns:
            report.append(f"### {col}")
            report.append(f"- Unique values: {df[col].nunique()}")
            if df[col].nunique() <= 10:
                report.append("- Value counts:")
                for val, count in df[col].value_counts().items():
                    report.append(f"  - {val}: {count} ({count/len(df)*100:.1f}%)")
            report.append("")

    # Write report
    with open(output_file, 'w') as f:
        f.write('\n'.join(report))

    print(f"Report saved to {output_file}")
    return '\n'.join(report)

generate_eda_report(df)
```

---

## Automated Full EDA

```python
def run_full_eda(filepath_or_df, output_dir='eda_output'):
    """Run complete EDA pipeline."""
    import os
    os.makedirs(output_dir, exist_ok=True)

    # Load data
    if isinstance(filepath_or_df, str):
        if filepath_or_df.endswith('.csv'):
            df = pd.read_csv(filepath_or_df)
        elif filepath_or_df.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(filepath_or_df)
        elif filepath_or_df.endswith('.parquet'):
            df = pd.read_parquet(filepath_or_df)
        else:
            raise ValueError(f"Unsupported file type: {filepath_or_df}")
    else:
        df = filepath_or_df

    print("Running Full EDA Pipeline...")
    print("=" * 60)

    # 1. Overview
    dataset_overview(df)

    # 2. Profiles
    profiles = profile_columns(df)
    profiles.to_csv(f'{output_dir}/column_profiles.csv', index=False)

    # 3. Numeric analysis
    analyze_numerics(df)

    # 4. Categorical analysis
    analyze_categoricals(df)

    # 5. Correlations
    corr = analyze_correlations(df)
    if corr is not None:
        corr.to_csv(f'{output_dir}/correlations.csv')

    # 6. Quality assessment
    issues = assess_data_quality(df)

    # 7. Visualizations
    plot_distributions(df)
    if corr is not None:
        plot_correlation_heatmap(df)

    # 8. Report
    generate_eda_report(df, f'{output_dir}/eda_report.md')

    print("\n" + "=" * 60)
    print(f"EDA Complete! Outputs saved to {output_dir}/")

    return df

# Usage:
# df = run_full_eda('data.csv')
# df = run_full_eda(existing_dataframe)
```

---

## YData Profiling (Automated Reports)

For comprehensive automated reports, use ydata-profiling:

```python
# pip install ydata-profiling

from ydata_profiling import ProfileReport

# Generate profile
profile = ProfileReport(df,
                        title="Dataset Profile Report",
                        explorative=True,
                        dark_mode=False)

# Save as HTML
profile.to_file("profile_report.html")

# Get as dict for programmatic access
profile_dict = profile.get_description()
```

---

