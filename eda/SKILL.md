---
name: eda
description: "Exploratory Data Analysis - Profile datasets, discover patterns, generate statistical summaries, and create visualizations. Use when analyzing CSV, Excel, Parquet, or database data to understand structure, quality, distributions, correlations, and anomalies."
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

# Exploratory Data Analysis (EDA)

Comprehensive data exploration workflow for any dataset. Generates statistical profiles, identifies patterns, assesses data quality, and produces publication-ready visualizations.

## Quick Start

```python
import pandas as pd

# Load data
df = pd.read_csv('data.csv')  # or read_excel, read_parquet, etc.

# Quick profile
print(f"Shape: {df.shape}")
print(f"Columns: {list(df.columns)}")
print(f"Types:\n{df.dtypes}")
print(f"Missing:\n{df.isnull().sum()}")
df.describe(include='all')
```

---

---

## Phases (detailed code in [reference.md](reference.md))

| Phase | What happens |
|-------|-------------|
| 1. Data Ingestion | Load CSV, Excel, Parquet, JSON, SQL; handle encoding, types, chunking |
| 2. Structural Analysis | Shape, memory, dtypes, missing values, duplicates, column profiles |
| 3. Statistical Analysis | Numeric distributions, skew, outliers; categorical counts; correlations |
| 4. Data Quality | Missing >10%, duplicates, constants, high cardinality, mixed types, negatives |
| 5. Visualization | Distributions, correlation heatmap, bar charts — Kearney palette enforced |
| 6. Automated Report | Markdown report with tables; `run_full_eda()` pipeline; ydata-profiling option |

---

## Tips

1. **Start broad, then focus**: Run overview first, then dive into interesting columns
2. **Check for data leakage**: Look for columns that shouldn't be in training data
3. **Document findings**: Use the markdown report as a starting point
4. **Iterate**: EDA is not linear - revisit earlier steps as you learn more
5. **Apply Kearney Design System**: All visualizations must follow brand guidelines
