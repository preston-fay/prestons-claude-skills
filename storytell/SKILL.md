---
name: storytell
description: "Data narrative templates and writing techniques. Provides story structures (Problem-Solution, Journey, Comparison), writing techniques (lead with insight, quantify, create contrast), and report templates (exec summary, one-pager, slide outline). Typically invoked by story-architect for simple narrative needs. Use directly when you just need a quick write-up template without full narrative architecture."
allowed-tools:
  - Read
  - Write
  - Glob
---

# Data Storytelling

Transform analytical findings into compelling narratives that drive action. This skill bridges the gap between data analysis and business communication.

## The Data Story Framework

Every data story should answer:
1. **What?** - The key finding or insight
2. **So what?** - Why it matters (impact, implications)
3. **Now what?** - What should be done (recommendations)

```
Data → Finding → Insight → Recommendation → Action
```

---

## Story Structures

### 1. The Problem-Solution Arc

```
SETUP: Here's the situation/problem
↓
TENSION: Here's why it matters (stakes)
↓
INSIGHT: Here's what we discovered
↓
RESOLUTION: Here's what we should do
```

**Example:**
> "Customer churn increased 15% last quarter, costing us $2.3M in lost revenue. Our analysis reveals that 68% of churned customers had unresolved support tickets. By implementing a proactive outreach program for at-risk customers, we can reduce churn by 40% and recover $920K annually."

### 2. The Journey Structure

```
WHERE WE WERE: Historical context
↓
WHAT CHANGED: The catalyst/trend
↓
WHERE WE ARE: Current state
↓
WHERE WE'RE GOING: Future projection
↓
HOW TO GET THERE: Recommendations
```

### 3. The Comparison Frame

```
EXPECTATION: What we expected/benchmarks
↓
REALITY: What actually happened
↓
GAP ANALYSIS: Why the difference
↓
PATH FORWARD: How to close the gap
```

### 4. The "Here's What I Found" Structure

```
QUESTION: What we set out to answer
↓
APPROACH: How we analyzed it (briefly)
↓
KEY FINDING: The headline insight
↓
SUPPORTING EVIDENCE: 2-3 data points
↓
IMPLICATION: What this means
↓
RECOMMENDATION: What to do
```

---

## Writing Techniques

### Lead with the Insight

**Bad:** "We analyzed 50,000 customer records across 12 months..."
**Good:** "High-value customers who engage with our mobile app are 3x more likely to renew."

### Quantify Everything

**Vague:** "Sales improved significantly"
**Specific:** "Sales increased 23% ($4.2M) compared to Q3"

### Use Comparisons

**Without context:** "Our NPS is 42"
**With context:** "Our NPS of 42 trails the industry benchmark of 55 by 13 points"

### Make Numbers Human

**Abstract:** "1.2 million affected customers"
**Relatable:** "1 in 4 customers experienced this issue"

### Create Contrast

**Weak:** "Premium customers are valuable"
**Strong:** "Premium customers generate 8x the revenue of standard customers while representing only 12% of our base"

---

## Narrative Templates

### Executive Summary Template

```markdown
## Executive Summary

**The Headline**
[One sentence capturing the key finding and its implication]

**Key Numbers**
- [Critical metric 1]: [Value] ([Change/Context])
- [Critical metric 2]: [Value] ([Change/Context])
- [Critical metric 3]: [Value] ([Change/Context])

**What This Means**
[2-3 sentences on business implications]

**Recommended Actions**
1. [Priority action with expected impact]
2. [Secondary action with expected impact]
3. [Supporting action with expected impact]

**Bottom Line**
[One sentence: the single most important takeaway]
```

### Insight Slide Template

```markdown
## [Insight as Headline Statement]

**The Finding**
[Clear statement of what the data shows]

**The Evidence**
[Visualization or key data point]

**Why It Matters**
[Business impact in dollars, customers, or risk]

**What To Do**
[Specific, actionable recommendation]
```

### Data Point Narrative

```python
def narrate_metric(name, value, change, benchmark=None, context=None):
    """Generate narrative for a single metric."""
    narrative = f"{name} is {value:,.0f}"

    if change:
        direction = "up" if change > 0 else "down"
        narrative += f", {direction} {abs(change):.1f}% from last period"

    if benchmark:
        comparison = "above" if value > benchmark else "below"
        gap = abs(value - benchmark)
        narrative += f". This is {gap:,.0f} ({comparison}) our target of {benchmark:,.0f}"

    if context:
        narrative += f". {context}"

    return narrative

# Usage
print(narrate_metric(
    name="Monthly Active Users",
    value=125000,
    change=12.5,
    benchmark=150000,
    context="Growth is accelerating for the third consecutive month"
))
# Output: "Monthly Active Users is 125,000, up 12.5% from last period.
#          This is 25,000 (below) our target of 150,000.
#          Growth is accelerating for the third consecutive month."
```

---

## Visualization as Storytelling

### Chart Titles Should Make a Point

**Bad:** "Revenue by Region"
**Good:** "APAC Revenue Growth Outpaces All Other Regions by 2x"

**Bad:** "Customer Satisfaction Over Time"
**Good:** "Satisfaction Scores Recovered to Pre-Incident Levels"

### Annotation Guidelines

```python
import matplotlib.pyplot as plt

def annotated_line_chart(df, x, y, annotations, title):
    """Create line chart with story annotations."""
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(df[x], df[y], color='#7823DC', linewidth=2)

    # Add annotations at key points
    for ann in annotations:
        ax.annotate(
            ann['text'],
            xy=(ann['x'], ann['y']),
            xytext=(ann.get('text_x', ann['x']), ann.get('text_y', ann['y'] * 1.1)),
            fontsize=10,
            ha='center',
            arrowprops=dict(arrowstyle='->', color='#787878')
        )

    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(False)

    return fig

# Usage
annotations = [
    {'x': '2024-03', 'y': 120, 'text': 'Product launch'},
    {'x': '2024-07', 'y': 85, 'text': 'Summer slowdown'},
    {'x': '2024-11', 'y': 145, 'text': 'Record high'}
]
```

### The Rule of Three

Limit each visual to **three** key points:
- One primary insight (the headline)
- One supporting point (evidence)
- One implication or action (so what)

---

## Audience Adaptation

### For Executives

**Focus on:**
- Business impact in dollars
- Strategic implications
- Clear recommendations
- Risk assessment

**Avoid:**
- Methodology details
- Technical jargon
- Too many data points
- Hedging language

**Example:**
> "Revenue is at risk. Without intervention, we project a $5M shortfall by Q4. Our recommendation: accelerate the premium tier launch by 6 weeks."

### For Technical Stakeholders

**Focus on:**
- Methodology transparency
- Statistical confidence
- Data quality notes
- Reproducibility

**Include:**
- Sample sizes
- Confidence intervals
- Assumptions and limitations
- Alternative interpretations

### For Operational Teams

**Focus on:**
- Actionable specifics
- Process implications
- Timeline and resources
- Success metrics

**Make it:**
- Practical
- Sequential (what to do first, second...)
- Measurable

---

## Common Story Patterns

### The "Surprise" Story

When data contradicts expectations:

```
"We assumed X. The data shows Y.
Here's why, and what it means for our strategy."
```

### The "Trend" Story

When identifying a pattern over time:

```
"For the past [period], we've seen [trend].
At this rate, we'll [projection].
To [desired outcome], we need to [action]."
```

### The "Segment" Story

When revealing differences across groups:

```
"Not all [customers/products/regions] are equal.
[Segment A] accounts for [X%] of [outcome] despite being only [Y%] of [total].
By focusing on [segment], we can [impact]."
```

### The "Correlation" Story

When showing relationships:

```
"[Variable A] and [Variable B] are strongly connected.
When A increases, B [also increases/decreases] by [amount].
This suggests [implication], which means we should [action]."
```

### The "Benchmark" Story

When comparing to standards:

```
"Against [benchmark/competitor/best-in-class], we're [ahead/behind] by [gap].
The biggest opportunities are in [area].
Closing this gap would [quantified impact]."
```

---

## Building a Narrative Arc

### Step 1: Identify Your "One Thing"

What is the single most important message? Everything else supports this.

```python
def identify_headline(findings):
    """
    From a list of findings, identify the headline.
    Consider: Impact, novelty, actionability.
    """
    # Score each finding
    scored = []
    for f in findings:
        score = (
            f.get('impact_score', 0) * 3 +  # Impact weighted highest
            f.get('novelty_score', 0) * 2 +  # Novelty second
            f.get('actionability_score', 0) * 1  # Actionability third
        )
        scored.append((f, score))

    # Return top finding
    return max(scored, key=lambda x: x[1])[0]
```

### Step 2: Build Supporting Evidence

Select 2-3 data points that:
1. Directly support the headline
2. Address potential skepticism
3. Add credibility through different angles

### Step 3: Anticipate Questions

What will the audience ask?
- "How confident are we?"
- "What could explain this differently?"
- "What's the cost of action vs. inaction?"
- "What are the risks?"

### Step 4: End with a Clear Call to Action

The ending should make it crystal clear:
- **What** should be done
- **By whom**
- **By when**
- **Expected outcome**

---

## Report Templates

### One-Pager Template

```markdown
# [Compelling Title That States the Main Finding]

## The Situation
[2-3 sentences on context and why this matters now]

## Key Insight
[Visualization or highlighted statistic]

**In plain English:** [One sentence interpretation]

## What This Means for Us
- [Implication 1]
- [Implication 2]
- [Implication 3]

## Recommended Action
[Primary recommendation with expected impact]

**Next Step:** [Specific immediate action with owner and deadline]

---
*Analysis by [Name] | Data as of [Date] | Contact: [Email]*
```

### Presentation Outline

```markdown
## Slide 1: Title
[Provocative title that hints at the conclusion]

## Slide 2: The Question
"We set out to understand [question]"

## Slide 3: The Answer (Headline)
[Key finding as a complete statement]

## Slides 4-6: Supporting Evidence
[One insight per slide with visualization]

## Slide 7: Implications
[What this means for the business - 3 bullet points max]

## Slide 8: Recommendation
[What we should do, with expected impact]

## Slide 9: Next Steps
[Specific actions, owners, timeline]

## Appendix
[Methodology, additional data, Q&A backup]
```

---

## Quality Checklist

Before presenting your data story, verify:

### Clarity
- [ ] Can someone understand the main point in 10 seconds?
- [ ] Are all numbers in context (vs. benchmarks, time periods)?
- [ ] Is jargon eliminated or explained?

### Accuracy
- [ ] Are numbers correct and properly sourced?
- [ ] Are comparisons fair (apples to apples)?
- [ ] Are caveats disclosed?

### Persuasiveness
- [ ] Does the story follow a logical arc?
- [ ] Is evidence sufficient and credible?
- [ ] Are counterarguments addressed?

### Actionability
- [ ] Is the recommendation specific?
- [ ] Is the next step clear?
- [ ] Can the audience act on this?

### Visual Design
- [ ] Do visualizations follow Kearney Design System?
- [ ] Are charts titled with insights, not descriptions?
- [ ] Is there a clear visual hierarchy?

---

## Tips

1. **Start with the end**: Write the recommendation first, then build the story backward
2. **One idea per slide/section**: Don't dilute your message
3. **Use "you" language**: "This affects your customers" not "customers are affected"
4. **Read it aloud**: Does it flow? Does it sound human?
5. **Get a fresh perspective**: Show someone unfamiliar with the analysis
6. **Practice the "grandma test"**: Could you explain this to a smart non-expert?
7. **Kill your darlings**: Remove interesting-but-irrelevant findings
