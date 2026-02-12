# Spit-n-Polish QC Checklist

Quick-reference checklist for reviewers. Every item must be verified on every review.

---

## KDS Brand Compliance

### Colors
- [ ] Primary purple is exactly `#7823DC`
- [ ] Black is `#1E1E1E` (not `#000` or `#111`)
- [ ] Chart colors follow 1-10 sequence
- [ ] No off-brand colors (Bootstrap blue, Tailwind defaults, random hex)
- [ ] Dark theme uses `#9150E1` as primary

### Typography
- [ ] Font stack: `Inter, Arial, sans-serif`
- [ ] Heading sizes match KDS type scale
- [ ] No text below 11px
- [ ] Chart labels 12-14px, legends 12px

### Charts
- [ ] Zero gridlines (search: `grid`, `showGrid`, `axes.grid`)
- [ ] `axisLine={false}`, `tickLine={false}` on all axes
- [ ] Value labels on data points
- [ ] No pie charts >4 segments
- [ ] No 3D effects or drop shadows
- [ ] No dual y-axes
- [ ] Bar chart corners: `radius={[4, 4, 0, 0]}`

### Icons & Logo
- [ ] All icons from `lucide-react`
- [ ] Icons are colored (not unstyled defaults)
- [ ] Logo is an image asset (not styled text)
- [ ] Logo has 16px minimum clear space

---

## Layout & Spacing

### Overflow
- [ ] No horizontal scrollbar at any viewport
- [ ] No text overflowing containers
- [ ] No charts bleeding outside cards
- [ ] Tables handle overflow (responsive or scroll)
- [ ] Tooltips not clipped at edges

### Alignment
- [ ] KPI cards equal height per row
- [ ] Chart titles aligned with chart area
- [ ] Consistent gap between cards (24px / `gap-6`)
- [ ] Grid columns properly aligned

### Spacing
- [ ] Consistent card padding (`p-6`)
- [ ] Proper line-height per KDS spec
- [ ] Adequate whitespace between sections
- [ ] No orphaned headers

### Responsive
- [ ] Usable at 1440px, 768px, 375px
- [ ] Grid collapses: 4-col → 2-col → 1-col
- [ ] No overlapping elements at any width
- [ ] Touch targets ≥ 44x44px on mobile

---

## Data Visualization Quality

### Legends
- [ ] Multi-series charts have legends
- [ ] Legend labels are human-readable (not raw column names)
- [ ] Legend doesn't overlap chart content
- [ ] Legend colors match data series

### Axes
- [ ] X-axis labels don't overlap
- [ ] Y-axis has proper formatting ($, %, K)
- [ ] Axis labels include units
- [ ] Bar chart Y-axis starts at zero

### Content
- [ ] Charts have descriptive titles
- [ ] Key data points are annotated
- [ ] No placeholder data (TODO, lorem ipsum, Sample Data)
- [ ] All charts render without errors
- [ ] Data source cited where applicable

---

## Accessibility (WCAG AA)

- [ ] Text contrast ≥ 4.5:1
- [ ] Focus indicators visible
- [ ] Images have alt text
- [ ] Charts have data table alternatives or aria-labels
- [ ] Heading hierarchy correct (no skips)
- [ ] Meaningful page `<title>`
- [ ] No color-only information
- [ ] Form inputs have labels

---

## Functional

- [ ] No console errors
- [ ] No 404s (images, fonts, scripts)
- [ ] No stuck loading states
- [ ] Tooltips work on hover
- [ ] Links are valid (not `#` or `javascript:void(0)`)
- [ ] No visible dead code or comments

---

## Severity Reference

| Level | Symbol | Meaning | Action |
|-------|--------|---------|--------|
| CRITICAL | `[!!]` | Broken, brand violation, data error | Must fix |
| HIGH | `[!]` | Visual defect, brand inconsistency | Should fix |
| MEDIUM | `[~]` | Minor polish issue | Fix if time allows |
| LOW | `[.]` | Nitpick, enhancement | Nice to have |

## Verdict Criteria

| Verdict | Criteria |
|---------|----------|
| **PASS** | Zero CRITICAL, zero HIGH findings |
| **PASS WITH NOTES** | Zero CRITICAL, 1-3 HIGH findings |
| **FAIL — REWORK NEEDED** | Any CRITICAL findings, or 4+ HIGH findings |
