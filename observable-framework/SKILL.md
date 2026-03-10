---
name: observable-framework
description: "Create Kearney-branded Observable Framework dashboards with 16:9 slide presentations, data visualizations, and executive-ready insights. Use when building interactive dashboards, data-driven presentations, or analytical reports using Observable Framework."
context: fork
agent: general-purpose
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(npm *)
  - Bash(npx *)
  - Bash(node *)
  - Bash(observable *)
hooks:
  PostToolUse:
    - matcher: Write
      command: ["bash", "/Users/pfay01/.claude/hooks/log-tool-use.sh"]
---

# Observable Framework Slide Builder

Create production-grade, Kearney-branded **16:9 slide presentations** that match the official POTX template designs. Output looks exactly like PPTX slides with consistent branding, iconography, and professional layout.

## POTX-Accurate Layout Rules

Based on analysis of official Kearney PowerPoint templates:

### Title Slide Layout
- Title: **LEFT-ALIGNED** at ~3% from left edge
- Title text: 56px, bold, white (dark theme) or purple (light theme)
- Subtitle: Below title, 24px bold
- Meta/date: Below subtitle, 20px regular
- **Logo position**: BOTTOM LEFT (not top right!)

### Content Slide Layout
- Title: **LEFT-ALIGNED** at top (~3% from left)
- Title text: 28px bold
- Subtitle: 16px, gray
- Content area: Full width below title
- **Logo position**: BOTTOM LEFT (absolute positioned)
- **Navigation**: Center bottom arrows

## CRITICAL RULES

### Forbidden Colors - NEVER USE THESE
- ❌ Yellow (#EAB308, #FFC107, any yellow)
- ❌ Orange (#F97316, #FF9800, any orange)
- ❌ Green (#22C55E, #4CAF50, any green) - except subtle status indicators
- ❌ Red (#EF4444, #F44336, any red) - except subtle status indicators
- ❌ Any color not in the Kearney palette below

### Allowed Colors ONLY
```
Kearney Purple:  #7823DC (primary accent)
Kearney Black:   #1E1E1E (text, dark backgrounds)
Kearney Gray:    #A5A5A5 (secondary text — ALL CONTEXTS including dark backgrounds)
Kearney White:   #FFFFFF (backgrounds)

Chart Colors (use in order 1-10):
1. #D2D2D2  2. #A5A6A5  3. #787878  4. #E0D2FA  5. #C8A5F0
6. #AF7DEB  7. #4B4B4B  8. #1E1E1E  9. #9150E1  10. #7823DC

Dark Theme Primary: #9150E1 (brighter purple for visibility)
```

### ⚠️ Text Legibility Rules (STRICTLY ENFORCED)

**`#787878` is a CHART DATA COLOR — it is NOT a text color on dark backgrounds.**

| Background | Secondary text color | Minimum font size |
|------------|---------------------|-------------------|
| Light (#FFF, #F5F5F5) | `#787878` OK | 11px |
| Dark (#1E1E1E, #222, #323232, #2A2A2A) | **`#A5A5A5` REQUIRED** | **12px** |

**NEVER write `color:#787878` in an inline style on a dark card, dark slide, or dark container.** This is the single most common legibility failure in Kearney dashboards.

When writing inline styles on dark backgrounds, always use:
```html
<!-- ✅ CORRECT — dark background -->
<div style="font-size:12px;color:#A5A5A5;line-height:1.6">secondary text</div>

<!-- ❌ WRONG — #787878 is invisible on dark backgrounds -->
<div style="font-size:10px;color:#787878">secondary text</div>
```

When using CSS classes (preferred), `var(--muted-foreground)` is already correct because the theme sets it to `#A5A5A5` in dark mode. The problem only occurs with hardcoded inline hex values.

### Required Elements
- ✅ Kearney logo at BOTTOM LEFT (embedded SVG)
- ✅ 16:9 aspect ratio slides
- ✅ Lucide icons for iconography
- ✅ Fixed 4-column KPI grids (equal sizing)
- ✅ Explicit table column alignment
- ✅ Slide navigation arrows at center bottom
- ✅ NO GRIDLINES on charts

## Kearney Logo SVG (Embed Directly)

### Dark Background (White Logo)
```html
<svg class="kearney-logo" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 334 40">
  <g fill="#FFFFFF">
    <path d="M118.74,0h-9.08L93.41,40H98.7L103,29.28h22.21L129.53,40H135ZM104.9,24.52,112.78,5h2.68l7.84,19.51Z"/>
    <path d="M316.46,23.37V40h-5.21V23.31L293.62,0h6.24l13.95,18.52L327.94,0H334Z"/>
    <path d="M82.43,40H49.61V0H82.43V4.71H54.53V17.63H79.11v4.74H54.53V35.29h27.9Z"/>
    <path d="M283.45,40H250.62V0h32.83V4.71H255.54V17.63h24.58v4.74H255.54V35.29h27.91Z"/>
    <path d="M233.09,40h-4.48L202,9l0,31h-5.05V0h4.48L228,31V0h5.05Z"/>
    <polygon points="36.23 0 29.38 0 11.94 17.5 5.05 17.5 5.05 0 0 0 0 40 5.05 40 5.05 22.5 11.92 22.5 29.38 40 36.23 40 16.61 20 36.23 0"/>
    <path d="M183.2,40,169.86,22.29a15.77,15.77,0,0,0,2.85-.38c4.91-1.55,8.1-5.32,8.1-10.74,0-7.28-5-11.17-14-11.17H147.15V40h5V22.37h11.5L177,40Zm-31-35.29h14.51c5.8,0,8.89,2.21,8.89,6.46s-3,6.46-8.89,6.46H152.18Z"/>
  </g>
</svg>
```

### Light Background (Black Logo)
```html
<svg class="kearney-logo" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 334 40">
  <g fill="#1E1E1E">
    <path d="M118.74,0h-9.08L93.41,40H98.7L103,29.28h22.21L129.53,40H135ZM104.9,24.52,112.78,5h2.68l7.84,19.51Z"/>
    <path d="M316.46,23.37V40h-5.21V23.31L293.62,0h6.24l13.95,18.52L327.94,0H334Z"/>
    <path d="M82.43,40H49.61V0H82.43V4.71H54.53V17.63H79.11v4.74H54.53V35.29h27.9Z"/>
    <path d="M283.45,40H250.62V0h32.83V4.71H255.54V17.63h24.58v4.74H255.54V35.29h27.91Z"/>
    <path d="M233.09,40h-4.48L202,9l0,31h-5.05V0h4.48L228,31V0h5.05Z"/>
    <polygon points="36.23 0 29.38 0 11.94 17.5 5.05 17.5 5.05 0 0 0 0 40 5.05 40 5.05 22.5 11.92 22.5 29.38 40 36.23 40 16.61 20 36.23 0"/>
    <path d="M183.2,40,169.86,22.29a15.77,15.77,0,0,0,2.85-.38c4.91-1.55,8.1-5.32,8.1-10.74,0-7.28-5-11.17-14-11.17H147.15V40h5V22.37h11.5L177,40Zm-31-35.29h14.51c5.8,0,8.89,2.21,8.89,6.46s-3,6.46-8.89,6.46H152.18Z"/>
  </g>
</svg>
```

## Lucide Icons (Required for Iconography)

Always use Lucide icons. Include in head:
```html
<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>
```

Usage:
```html
<i data-lucide="trending-up" style="width:24px;height:24px"></i>
<i data-lucide="alert-circle" style="width:16px;height:16px"></i>
<i data-lucide="database"></i>
<i data-lucide="git-branch"></i>
```

Initialize at end of body: `<script>lucide.createIcons();</script>`


---

## Reference Material

For complete slide templates (dark theme, light theme) and component patterns, see [reference.md](reference.md).

---

## Checklist for Each Slide

- [ ] 16:9 aspect ratio (max-width: 1400px, aspect-ratio: 16/9)
- [ ] Kearney logo at BOTTOM LEFT (embedded SVG)
- [ ] Title LEFT-ALIGNED (not centered)
- [ ] Lucide icons loaded and used
- [ ] KPI cards in fixed 4-column grid (repeat(4, 1fr))
- [ ] All table columns have explicit nth-child alignment
- [ ] ONLY Kearney colors used (no yellow, orange, green, red)
- [ ] Slide navigation arrows at CENTER BOTTOM
- [ ] Print styles for PDF export

## File Naming Convention

```
slides/
├── slide-01-cover.html
├── slide-02-executive-summary.html
├── slide-03-maturity-analysis.html
├── slide-04-technology-stack.html
├── slide-05-genai-opportunities.html
└── slide-06-recommendations.html
```
