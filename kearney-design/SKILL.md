---
name: kearney-design
description: "Kearney brand design system for creating on-brand deliverables. Use when creating visualizations, dashboards, slides, reports, or any visual output that should follow Kearney brand guidelines. Automatically applies correct colors, typography, chart rules, and component patterns."
user-invocable: false
allowed-tools:
  - Read
---

# Kearney Design System

## Overview

This is the comprehensive design system for creating beautiful, consistent deliverables across all Kearney formats: data visualizations, reports, slides, applications, and dashboards. **All visual output must follow these guidelines.**

## Core Principles

1. **Brand-First Color System**: All colors anchored in official Kearney brand palette
2. **Light & Dark Themes**: Full support for both with optimized legibility
3. **Clean Data Visualization**: No gridlines, minimal decoration, maximum insight clarity
4. **Professional Icons Only**: Use Lucide icons in Kearney colors - never emoticons
5. **Typography**: Primary font is **Inter**, fallback Arial, sans-serif
6. **Accessibility**: WCAG AA compliant (4.5:1 contrast ratio minimum)
7. **Value-First Charts**: Prefer value labels on data points; hide axis values when labels make them clear

---

## Color Palette

### Main Colors

| Color | Hex | RGB | Usage |
|-------|-----|-----|-------|
| Kearney Black | `#1E1E1E` | 30, 30, 30 | Primary text, dark backgrounds |
| Kearney White | `#FFFFFF` | 255, 255, 255 | Light backgrounds, text on dark |
| Kearney Gray | `#A5A5A5` | 165, 165, 165 | Secondary text, subtle elements |
| Kearney Purple | `#7823DC` | 120, 35, 220 | **Primary brand color**, CTAs, emphasis |

### Chart Colors (Use in Order 1-10)

**CRITICAL**: Always use these colors in sequence for multi-series data visualizations.

| Order | Hex | RGB | Description |
|-------|-----|-----|-------------|
| 1 | `#D2D2D2` | 210, 210, 210 | Light gray |
| 2 | `#A5A6A5` | 165, 165, 165 | Medium gray |
| 3 | `#787878` | 120, 120, 120 | Dark gray |
| 4 | `#E0D2FA` | 224, 210, 250 | Light purple |
| 5 | `#C8A5F0` | 200, 165, 240 | Soft purple |
| 6 | `#AF7DEB` | 175, 125, 235 | Medium purple |
| 7 | `#4B4B4B` | 75, 75, 75 | Charcoal |
| 8 | `#1E1E1E` | 30, 30, 30 | Black |
| 9 | `#9150E1` | 145, 80, 225 | Bright purple |
| 10 | `#7823DC` | 120, 35, 220 | Kearney Purple |

**Example**: For 3 data series, use colors 1, 2, 3. For 5 series, use colors 1-5.

### Extended Grays

| Name | Hex | Usage |
|------|-----|-------|
| Gray 100 | `#F5F5F5` | Backgrounds, hover states |
| Gray 200 | `#E6E6E6` | Borders, dividers |
| Gray 300 | `#B9B9B9` | Disabled states |
| Gray 400 | `#8C8C8C` | Placeholder text |
| Gray 500 | `#5F5F5F` | Secondary text |
| Gray 600 | `#323232` | Dark UI elements |

### Extended Purples

| Name | Hex | Usage |
|------|-----|-------|
| Purple 100 | `#D7BEF5` | Light accents |
| Purple 200 | `#B991EB` | Hover states |
| Purple 300 | `#A064E6` | Secondary actions |
| Purple 400 | `#8737E1` | Active states |

---

## Gradients

### Progressive Gradients (for direction/intensity)

```css
/* Purple Intensity */
linear-gradient(135deg, #E0D2FA 0%, #7823DC 100%)

/* Purple Depth */
linear-gradient(135deg, #9150E1 0%, #1E1E1E 100%)

/* Gray to Purple */
linear-gradient(135deg, #A5A5A5 0%, #7823DC 100%)

/* Three-point Purple */
linear-gradient(135deg, #D7BEF5 0%, #9150E1 50%, #7823DC 100%)
```

### Divergent Gradients (for heatmaps/ranges)

```css
/* Purple Divergent */
linear-gradient(90deg, #7823DC 0%, #FFFFFF 50%, #7823DC 100%)

/* Gray to Purple Divergent */
linear-gradient(90deg, #A5A5A5 0%, #E0D2FA 50%, #7823DC 100%)
```

---

## Typography

### Type Scale

| Element | Size | Weight | Line Height | Usage |
|---------|------|--------|-------------|-------|
| H1 | 40px / 2.5rem | Bold (700) | 1.2 | Page titles |
| H2 | 32px / 2rem | Bold (700) | 1.3 | Section headers, slide titles |
| H3 | 24px / 1.5rem | Semibold (600) | 1.4 | Subsections, card titles |
| H4 | 20px / 1.25rem | Semibold (600) | 1.4 | Component titles |
| H5 | 16px / 1rem | Semibold (600) | 1.5 | Small headers, data labels |
| H6 | 14px / 0.875rem | Semibold (600) | 1.5 | Metadata, captions |
| Body Large | 18px / 1.125rem | Normal (400) | 1.6 | Lead text |
| Body | 16px / 1rem | Normal (400) | 1.6 | Default paragraphs |
| Body Small | 14px / 0.875rem | Normal (400) | 1.5 | Secondary info |
| Body XS | 12px / 0.75rem | Normal (400) | 1.4 | Fine print |

### Chart Typography

- **Chart Title**: 18-24px
- **Axis Labels**: 12-14px
- **Data Labels**: 12-14px
- **Legend**: 12px
- **Tooltips**: 12-13px
- **Annotations**: 11-12px

---

## Data Visualization Rules

### FORBIDDEN

| Rule | Reason |
|------|--------|
| ❌ Gridlines | Clutter, distract from data |
| ❌ Pie charts (>4 segments) | Hard to compare |
| ❌ 3D effects | Distort perception |
| ❌ Dual y-axes | Confusing |
| ❌ Rainbow color schemes | Off-brand, accessibility issues |

### RECOMMENDED

| Chart Type | When to Use |
|------------|-------------|
| ✅ Bar Charts | Comparing discrete categories |
| ✅ Line Charts | Continuous trends over time |
| ✅ Area Charts | Emphasizing volume/magnitude |
| ✅ Stacked Bars | Composition across categories |
| ✅ Scatter Plots | Exploring correlations |
| ✅ Heatmaps | Patterns across two dimensions |

### Chart Configuration (Recharts Example)

```tsx
<BarChart data={data}>
  <XAxis
    dataKey="category"
    axisLine={false}
    tickLine={false}
    tick={{ fill: 'currentColor', fontSize: 12 }}
  />
  <YAxis
    axisLine={false}
    tickLine={false}
    tick={{ fill: 'currentColor', fontSize: 12 }}
  />
  <Tooltip
    contentStyle={{
      backgroundColor: 'hsl(var(--card))',
      border: '1px solid hsl(var(--border))',
      borderRadius: '8px'
    }}
  />
  <Bar dataKey="value" fill="#7823DC" radius={[4, 4, 0, 0]} />
</BarChart>
```

### Matplotlib/Seaborn Configuration

```python
import matplotlib.pyplot as plt

# Kearney chart colors
KEARNEY_COLORS = [
    '#D2D2D2', '#A5A6A5', '#787878', '#E0D2FA', '#C8A5F0',
    '#AF7DEB', '#4B4B4B', '#1E1E1E', '#9150E1', '#7823DC'
]

# Apply Kearney style
plt.rcParams.update({
    'font.family': 'Inter, Arial, sans-serif',
    'font.size': 12,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.spines.left': False,
    'axes.spines.bottom': False,
    'axes.grid': False,  # NO GRIDLINES
    'axes.facecolor': 'white',
    'figure.facecolor': 'white',
    'axes.labelcolor': '#1E1E1E',
    'xtick.color': '#787878',
    'ytick.color': '#787878',
})

# Use colors in order
plt.bar(categories, values, color=KEARNEY_COLORS[:len(categories)])
```

### Plotly Configuration

```python
import plotly.graph_objects as go

KEARNEY_COLORS = [
    '#D2D2D2', '#A5A6A5', '#787878', '#E0D2FA', '#C8A5F0',
    '#AF7DEB', '#4B4B4B', '#1E1E1E', '#9150E1', '#7823DC'
]

fig = go.Figure()
fig.update_layout(
    font_family='Inter, Arial, sans-serif',
    paper_bgcolor='white',
    plot_bgcolor='white',
    xaxis=dict(showgrid=False, showline=False, zeroline=False),
    yaxis=dict(showgrid=False, showline=False, zeroline=False),
    colorway=KEARNEY_COLORS
)
```

---

## Theme System

### Light Theme (Default)

Use for: Printed deliverables, slides, reports, formal presentations

```css
--background: #FFFFFF;
--foreground: #1E1E1E;
--primary: #7823DC;
--primary-foreground: #FFFFFF;
--secondary: #F5F5F5;
--muted: #E6E6E6;
--muted-foreground: #787878;
--card: #FFFFFF;
--border: #E6E6E6;
```

### Dark Theme

Use for: Digital dashboards, evening presentations, reduced eye strain

```css
--background: #1E1E1E;
--foreground: #FFFFFF;
--primary: #9150E1;  /* Brighter purple for visibility */
--primary-foreground: #FFFFFF;
--secondary: #323232;
--muted: #4B4B4B;
--muted-foreground: #A5A5A5;
--card: #323232;
--border: #4B4B4B;
```

---

## Component Patterns

### KPI Cards

```tsx
<Card className="p-6">
  <p className="text-sm text-muted-foreground mb-1">Total Revenue</p>
  <h2 className="mb-1">$2.4M</h2>
  <div className="flex items-center gap-1">
    <TrendingUp className="w-4 h-4 text-green-600" />
    <span className="text-sm text-green-600">+12.5%</span>
  </div>
  <Progress value={78} className="mt-4 h-2" />
</Card>
```

### Status Badges

```tsx
<Badge className="bg-green-600">On Track</Badge>
<Badge className="bg-yellow-600">At Risk</Badge>
<Badge className="bg-red-600">Delayed</Badge>
```

### Data Tables

```tsx
<table className="w-full text-sm">
  <thead>
    <tr className="border-b">
      <th className="text-left py-3 px-4">Metric</th>
      <th className="text-right py-3 px-4">Value</th>
    </tr>
  </thead>
  <tbody>
    <tr className="border-b hover:bg-muted/50">
      <td className="py-4 px-4">Revenue</td>
      <td className="text-right py-4 px-4">$2.4M</td>
    </tr>
  </tbody>
</table>
```

---

## Slide Layout Patterns

### Aspect Ratio

Always use **16:9** for slides.

### Margins

- **Outer margins**: 64px on all sides
- **Content area**: Maximum 75% of slide
- **Footer**: 48px height with slide number

### Slide Types

1. **Title Slide**: Large headline (3rem), subtitle, metadata
2. **Key Message**: 2-3 highlighted cards with main points
3. **Data Slide**: Chart with title, description, key insight
4. **Bullet Points**: Maximum 6 bullets, numbered sections
5. **Timeline**: Vertical timeline with phases and milestones
6. **Closing**: Next steps and contact information

---

## Quick Reference: Do's & Don'ts

### Do's ✓

- Use Kearney Purple (#7823DC) for primary actions
- Follow chart color sequence (1-10) consistently
- Start y-axis at zero for bar charts
- Label axes clearly with units
- Use direct labeling when possible
- Sort categories meaningfully
- Include data sources and timestamps
- Test in both light and dark modes
- Ensure generous whitespace

### Don'ts ✗

- Never use gridlines
- Never use dual y-axes
- Don't use pie charts for more than 4 segments
- Don't use 3D effects or shadows
- Don't truncate y-axis to exaggerate differences
- Don't use more than 7-8 series in one chart
- Don't rely solely on color to differentiate
- Don't use rainbow color schemes
- Don't clutter with unnecessary decoration
- Don't use colors outside the official palette

---

## Usage for LLMs

When generating Kearney deliverables:

1. **Always reference this design system** for colors, typography, and patterns
2. **Use exact hex codes** - never approximate or modify colors
3. **Follow chart color order strictly** - colors 1-10 in sequence
4. **No gridlines** - this is a hard rule for all visualizations
5. **Test legibility** - ensure text works on both light and dark backgrounds
6. **Maintain consistency** - use the same patterns throughout a deliverable
7. **Prioritize clarity** - remove any element that doesn't add understanding

---

**Version**: 2.0 | **Status**: Production-ready
