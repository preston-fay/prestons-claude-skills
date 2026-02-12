---
name: duckdb-agent
description: Use this skill when you need to reason over real data—CSVs, Parquet files, JSON—with verified answers instead of guessing. Implements the "model plans, DuckDB proves" pattern for agents that query, verify, then explain. Use this for any analytical question over local or remote data files.
---

# DuckDB Agent: Local Reasoning Over Real Data

## Core Philosophy

Agents should **look before they talk**. Don't guess at data answers—query, verify, then explain.

**The Pattern:**
- LLM as **planner** (translates questions to SQL)
- DuckDB as **tool** (executes queries with guardrails)
- LLM as **narrator** (explains results, flags uncertainty)

```
[User Question]
      |
      v
[Agent Planner]
  - clarifies intent
  - chooses tables/files
  - drafts SQL
      |
      v
[DuckDB Tool]
  - executes SQL (read-only)
  - returns rows + schema + stats
      |
      v
[Agent Writer]
  - explains results
  - flags uncertainty
  - suggests next query if needed
```

## Quick Start

```python
import duckdb

# Query any file directly
result = duckdb.sql("""
    SELECT customer_id, COUNT(*) AS orders
    FROM read_parquet('data/orders.parquet')
    GROUP BY customer_id
    ORDER BY orders DESC
    LIMIT 20
""").fetchall()
```

## Guardrails (Non-Negotiable)

When executing SQL for agent reasoning, **always enforce**:

1. **Read-only mode** — no writes unless explicitly needed
2. **Row limits** — max 200 rows returned (prevents context blowout)
3. **Query timeout** — 2-5 seconds max
4. **Single statements only** — reject queries with multiple semicolons
5. **Deny-list** — block INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, COPY

Use the tool wrapper in `scripts/duckdb_tool.py` which enforces all of these.

## The Tool Wrapper

```python
from scripts.duckdb_tool import duckdb_query, list_tables, describe_table, sample_rows

# Execute a guarded query
result = duckdb_query("""
    SELECT region, AVG(sale_amount) as avg_sale
    FROM read_csv('sales.csv')
    GROUP BY region
""")

# Returns: {columns, row_count_returned, rows, sql_executed}
```

## Schema Discovery (Reduces Hallucinated Column Names)

Before writing queries, **always discover the schema first**:

```python
# What files/tables are available?
list_tables()

# What columns does this table have?
describe_table('sales.csv')

# What does the data look like?
sample_rows('sales.csv', n=5)
```

This dramatically reduces made-up column names.

## Workflow for Answering Data Questions

### Step 1: Understand the data shape
```python
# Discover what's available
describe_table('events.parquet')
sample_rows('events.parquet', n=3)
```

### Step 2: Draft and execute SQL
```python
result = duckdb_query("""
    SELECT event_type, COUNT(*) as cnt
    FROM read_parquet('events.parquet')
    WHERE event_date >= '2025-01-01'
    GROUP BY event_type
    ORDER BY cnt DESC
""")
```

### Step 3: Narrate with uncertainty
When presenting results, always note:
- How many rows were scanned vs. returned
- Any null rates in key columns
- Whether results were truncated at the limit
- Assumptions made in the query

## Confidence Notes

Agents should admit uncertainty. Generate confidence notes based on:

```python
from scripts.duckdb_tool import compute_confidence

confidence = compute_confidence(result)
# Returns notes like:
# - "Results truncated at 200 rows; full dataset may differ."
# - "Column 'revenue' has 12% null values."
```

## Supported File Formats

DuckDB can query directly without import:

| Format | Function | Example |
|--------|----------|---------|
| Parquet | `read_parquet()` | `read_parquet('data/*.parquet')` |
| CSV | `read_csv()` | `read_csv('sales.csv')` |
| JSON | `read_json()` | `read_json('events.json')` |
| Excel | `read_xlsx()` | Requires spatial extension |

Glob patterns work: `read_parquet('data/2024/*.parquet')`

## Remote Data

DuckDB can query remote files without downloading:

```python
# S3
duckdb.sql("SELECT * FROM read_parquet('s3://bucket/path/file.parquet')")

# HTTP
duckdb.sql("SELECT * FROM read_csv('https://example.com/data.csv')")
```

For S3, set credentials:
```python
duckdb.sql("SET s3_access_key_id='...'")
duckdb.sql("SET s3_secret_access_key='...'")
```

## Dataset Contracts

Wrap raw files behind stable view names so file locations can change without breaking queries:

```python
con = duckdb.connect()
con.execute("""
    CREATE VIEW customers AS SELECT * FROM read_parquet('data/v2/customers.parquet');
    CREATE VIEW orders AS SELECT * FROM read_parquet('data/v2/orders.parquet');
    CREATE VIEW events AS SELECT * FROM read_parquet('data/v2/events.parquet');
""")
```

Now queries use stable names: `SELECT * FROM customers`

## Caching for Repeated Queries

If the agent runs similar queries repeatedly, materialize intermediate results:

```python
# Create a persistent local database
con = duckdb.connect('analytics_cache.duckdb')

# Materialize expensive aggregations
con.execute("""
    CREATE TABLE IF NOT EXISTS daily_metrics AS
    SELECT date_trunc('day', event_time) as day, COUNT(*) as events
    FROM read_parquet('events/*.parquet')
    GROUP BY 1
""")
```

## Common Patterns

### Churn Analysis
```sql
SELECT 
    segment,
    COUNT(*) FILTER (WHERE churned = true) as churned,
    COUNT(*) as total,
    ROUND(100.0 * COUNT(*) FILTER (WHERE churned = true) / COUNT(*), 2) as churn_rate
FROM customers
GROUP BY segment
ORDER BY churn_rate DESC
```

### Time-Series Aggregation
```sql
SELECT 
    date_trunc('week', event_time) as week,
    COUNT(*) as events,
    COUNT(DISTINCT user_id) as unique_users
FROM events
WHERE event_time >= CURRENT_DATE - INTERVAL '90 days'
GROUP BY 1
ORDER BY 1
```

### Join Pattern
```sql
SELECT 
    c.segment,
    AVG(o.order_value) as avg_order_value
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.segment
```

## What Makes This Different from Guessing

| Guessing | DuckDB Agent |
|----------|--------------|
| "Churn is probably around 5%" | "Churn is 5.3% based on 12,847 customers in the dataset" |
| "The top segment is likely Enterprise" | "Enterprise has 34% higher AOV (query attached)" |
| Makes up column names | Discovers schema first |
| Can't show its work | SQL is logged and auditable |

## Troubleshooting

**"Column not found"** — Run `describe_table()` first to see actual column names.

**Query too slow** — Add `LIMIT`, use Parquet instead of CSV, or filter early with WHERE.

**Out of memory** — Use `read_parquet()` with glob patterns and aggregations instead of loading all data.

**Results don't look right** — Use `sample_rows()` to inspect raw data before aggregating.

## Next Steps

- See `scripts/duckdb_tool.py` for the guardrailed tool implementation
- See `REFERENCE.md` for advanced DuckDB SQL patterns
