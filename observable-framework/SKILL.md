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
Kearney Gray:    #A5A5A5 (secondary text)
Kearney White:   #FFFFFF (backgrounds)

Chart Colors (use in order 1-10):
1. #D2D2D2  2. #A5A6A5  3. #787878  4. #E0D2FA  5. #C8A5F0
6. #AF7DEB  7. #4B4B4B  8. #1E1E1E  9. #9150E1  10. #7823DC

Dark Theme Primary: #9150E1 (brighter purple for visibility)
```

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

## DARK THEME TEMPLATES (Based on POTX Analysis)

### Title Slide - Dark Theme (POTX-Accurate)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Slide 1 - Cover | Project Name</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --kearney-purple: #7823DC;
      --kearney-purple-bright: #9150E1;
      --kearney-black: #1E1E1E;
      --kearney-gray: #A5A5A5;
      --kearney-white: #FFFFFF;
      --chart-1: #D2D2D2; --chart-2: #A5A6A5; --chart-3: #787878;
      --chart-4: #E0D2FA; --chart-5: #C8A5F0; --chart-6: #AF7DEB;
      --chart-7: #4B4B4B; --chart-8: #1E1E1E; --chart-9: #9150E1;
      --chart-10: #7823DC;
      --background: #1E1E1E;
      --foreground: #FFFFFF;
      --primary: #9150E1;
      --card: #323232;
      --border: #4B4B4B;
      --muted-foreground: #A5A5A5;
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: 'Inter', Arial, sans-serif;
      background: #0A0A0A;
      color: var(--foreground);
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      padding: 20px;
    }
    .slide {
      width: 100%;
      max-width: 1400px;
      aspect-ratio: 16 / 9;
      background: var(--background);
      box-shadow: 0 4px 40px rgba(0,0,0,0.5);
      padding: 48px 48px 40px 48px;
      display: flex;
      flex-direction: column;
      position: relative;
    }
    /* Title - LEFT ALIGNED per POTX */
    .cover-content {
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      padding-top: 5%;
    }
    .cover-title {
      font-size: 56px;
      font-weight: 700;
      color: var(--foreground);
      line-height: 1.1;
      letter-spacing: -0.02em;
      max-width: 50%;
    }
    .cover-subtitle {
      font-size: 24px;
      color: var(--foreground);
      margin-top: 32px;
      font-weight: 700;
      max-width: 50%;
    }
    .cover-meta {
      font-size: 20px;
      color: var(--foreground);
      margin-top: 8px;
      font-weight: 400;
      max-width: 50%;
    }
    /* Logo - BOTTOM LEFT per POTX */
    .kearney-logo {
      position: absolute;
      bottom: 40px;
      left: 48px;
      width: 140px;
      height: auto;
    }
    /* Slide Navigation - CENTER BOTTOM */
    .slide-nav {
      position: absolute;
      bottom: 16px;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      gap: 24px;
      align-items: center;
    }
    .nav-arrow {
      width: 32px;
      height: 32px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--muted-foreground);
      cursor: pointer;
      transition: color 0.2s;
      text-decoration: none;
    }
    .nav-arrow:hover { color: var(--foreground); }
    .nav-arrow.disabled { opacity: 0.3; cursor: default; }
    .slide-number {
      font-size: 12px;
      color: var(--muted-foreground);
      font-weight: 500;
    }
    @media print {
      body { background: var(--background); }
      .slide { box-shadow: none; min-height: 100vh; }
    }
    @page { size: A4 landscape; margin: 0; }
  </style>
</head>
<body>
  <div class="slide">
    <div class="cover-content">
      <h1 class="cover-title">Project Title Here</h1>
      <p class="cover-subtitle">Subtitle or Description</p>
      <p class="cover-meta">Category | Month Year</p>
    </div>
    <!-- KEARNEY LOGO - BOTTOM LEFT -->
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
    <!-- Slide Navigation -->
    <div class="slide-nav">
      <span class="nav-arrow disabled">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="15 18 9 12 15 6"></polyline>
        </svg>
      </span>
      <span class="slide-number">1</span>
      <a href="slide-02-xxx.html" class="nav-arrow">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="9 18 15 12 9 6"></polyline>
        </svg>
      </a>
    </div>
  </div>
</body>
</html>
```

### Content Slide - Dark Theme (POTX-Accurate)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Slide 2 - Content | Project Name</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>
  <style>
    :root {
      --kearney-purple: #7823DC;
      --kearney-purple-bright: #9150E1;
      --kearney-black: #1E1E1E;
      --kearney-gray: #A5A5A5;
      --kearney-white: #FFFFFF;
      --chart-1: #D2D2D2; --chart-2: #A5A6A5; --chart-3: #787878;
      --chart-4: #E0D2FA; --chart-5: #C8A5F0; --chart-6: #AF7DEB;
      --chart-7: #4B4B4B; --chart-8: #1E1E1E; --chart-9: #9150E1;
      --chart-10: #7823DC;
      --background: #1E1E1E;
      --foreground: #FFFFFF;
      --primary: #9150E1;
      --card: #323232;
      --border: #4B4B4B;
      --muted: #323232;
      --muted-foreground: #A5A5A5;
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: 'Inter', Arial, sans-serif;
      background: #0A0A0A;
      color: var(--foreground);
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      padding: 20px;
    }
    .slide {
      width: 100%;
      max-width: 1400px;
      aspect-ratio: 16 / 9;
      background: var(--background);
      box-shadow: 0 4px 40px rgba(0,0,0,0.5);
      padding: 48px 48px 56px 48px;
      display: flex;
      flex-direction: column;
      position: relative;
    }
    /* Title - LEFT ALIGNED per POTX */
    .slide-title {
      font-size: 28px;
      font-weight: 700;
      color: var(--foreground);
      letter-spacing: -0.02em;
      margin-bottom: 6px;
    }
    .slide-subtitle {
      font-size: 16px;
      font-weight: 400;
      color: var(--muted-foreground);
      margin-bottom: 24px;
    }
    .slide-content { flex: 1; overflow: hidden; }
    /* Summary Box */
    .summary-box {
      background: linear-gradient(135deg, var(--card) 0%, var(--background) 100%);
      border: 1px solid var(--border);
      border-left: 4px solid var(--primary);
      border-radius: 4px;
      padding: 14px 18px;
      margin-bottom: 18px;
      font-size: 13px;
      line-height: 1.6;
      color: var(--foreground);
    }
    /* KPI Cards - FIXED 4 COLUMN */
    .kpi-row {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      margin-bottom: 18px;
    }
    .kpi-card {
      background: var(--card);
      border: 1px solid var(--border);
      border-top: 4px solid var(--primary);
      border-radius: 4px;
      padding: 14px;
      text-align: center;
    }
    .kpi-card.secondary { border-top-color: var(--chart-6); }
    .kpi-card.tertiary { border-top-color: var(--chart-5); }
    .kpi-card.quaternary { border-top-color: var(--chart-2); }
    .kpi-icon {
      color: var(--primary);
      margin-bottom: 8px;
      display: flex;
      justify-content: center;
    }
    .kpi-value {
      font-size: 28px;
      font-weight: 700;
      color: var(--primary);
      line-height: 1.1;
    }
    .kpi-value.white { color: var(--foreground); }
    .kpi-value.gray { color: var(--muted-foreground); }
    .kpi-label {
      font-size: 10px;
      font-weight: 600;
      color: var(--muted-foreground);
      margin-top: 6px;
      text-transform: uppercase;
      letter-spacing: 0.03em;
    }
    /* Two Column Layout */
    .two-col {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
    }
    .section-title {
      font-size: 14px;
      font-weight: 600;
      color: var(--foreground);
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .section-title i { color: var(--primary); }
    ul.styled-list {
      list-style: none;
      padding: 0;
    }
    ul.styled-list li {
      padding: 7px 0;
      padding-left: 18px;
      position: relative;
      font-size: 12px;
      color: var(--muted-foreground);
      border-bottom: 1px solid var(--border);
      line-height: 1.5;
    }
    ul.styled-list li:last-child { border-bottom: none; }
    ul.styled-list li::before {
      content: "";
      position: absolute;
      left: 0;
      top: 12px;
      width: 6px;
      height: 6px;
      background: var(--primary);
      border-radius: 2px;
    }
    ul.styled-list li strong { color: var(--foreground); }
    /* Data Tables */
    .data-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
      margin-bottom: 20px;
    }
    .data-table th {
      background: var(--border);
      color: var(--foreground);
      padding: 12px 14px;
      font-weight: 600;
      font-size: 10px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    /* EXPLICIT COLUMN ALIGNMENT - Use nth-child for each column */
    .data-table th:nth-child(1) { text-align: left; }
    .data-table td:nth-child(1) { text-align: left; font-weight: 500; }
    /* Add more nth-child rules as needed for your table */
    .data-table td {
      padding: 12px 14px;
      border-bottom: 1px solid var(--border);
      vertical-align: middle;
      color: var(--foreground);
    }
    .data-table tr:last-child td { border-bottom: none; }
    .data-table tr:hover { background: var(--muted); }
    /* Badges - ONLY KEARNEY COLORS */
    .badge {
      display: inline-block;
      padding: 4px 10px;
      border-radius: 4px;
      font-size: 11px;
      font-weight: 600;
    }
    .badge.excellent { background: var(--primary); color: white; }
    .badge.good { background: var(--chart-6); color: white; }
    .badge.fair { background: var(--chart-5); color: var(--kearney-black); }
    .badge.poor { background: var(--chart-2); color: white; }
    .badge.critical { background: var(--chart-3); color: white; }
    /* Score indicators */
    .score-high { color: var(--primary); font-weight: 600; }
    .score-medium { color: var(--chart-5); font-weight: 600; }
    .score-low { color: var(--chart-2); font-weight: 600; }
    /* Insights Panel */
    .insights-panel {
      background: var(--card);
      border: 1px solid var(--border);
      border-left: 4px solid var(--primary);
      border-radius: 4px;
      padding: 14px 18px;
    }
    .insights-title {
      font-size: 13px;
      font-weight: 600;
      color: var(--foreground);
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .insights-title i { color: var(--primary); }
    .insights-text {
      font-size: 12px;
      color: var(--muted-foreground);
      line-height: 1.6;
    }
    .insights-text strong { color: var(--foreground); }
    /* Logo - BOTTOM LEFT per POTX */
    .kearney-logo {
      position: absolute;
      bottom: 36px;
      left: 48px;
      width: 120px;
      height: auto;
    }
    /* Slide Navigation - CENTER BOTTOM */
    .slide-nav {
      position: absolute;
      bottom: 16px;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      gap: 24px;
      align-items: center;
    }
    .nav-arrow {
      width: 32px;
      height: 32px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--muted-foreground);
      cursor: pointer;
      transition: color 0.2s;
      text-decoration: none;
    }
    .nav-arrow:hover { color: var(--foreground); }
    .nav-arrow.disabled { opacity: 0.3; cursor: default; }
    .slide-number {
      font-size: 12px;
      color: var(--muted-foreground);
      font-weight: 500;
    }
    @media print {
      body { background: var(--background); }
      .slide { box-shadow: none; min-height: 100vh; }
    }
    @page { size: A4 landscape; margin: 0; }
  </style>
</head>
<body>
  <div class="slide">
    <h1 class="slide-title">Slide Title Here</h1>
    <p class="slide-subtitle">Subtitle or context</p>

    <div class="slide-content">
      <!-- Content goes here -->
    </div>

    <!-- KEARNEY LOGO - BOTTOM LEFT -->
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

    <!-- Slide Navigation -->
    <div class="slide-nav">
      <a href="slide-01-cover.html" class="nav-arrow">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="15 18 9 12 15 6"></polyline>
        </svg>
      </a>
      <span class="slide-number">2</span>
      <a href="slide-03-xxx.html" class="nav-arrow">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="9 18 15 12 9 6"></polyline>
        </svg>
      </a>
    </div>
  </div>
  <script>lucide.createIcons();</script>
</body>
</html>
```

---

## LIGHT THEME TEMPLATES

### Title Slide - Light Theme

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Slide 1 - Cover | Project Name</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --kearney-purple: #7823DC;
      --kearney-black: #1E1E1E;
      --kearney-gray: #A5A5A5;
      --kearney-white: #FFFFFF;
      --gray-100: #F5F5F5;
      --gray-200: #E6E6E6;
      --card: #F5F5F5;
      --border: #E6E6E6;
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: 'Inter', Arial, sans-serif;
      background: var(--gray-100);
      color: var(--kearney-black);
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      padding: 20px;
    }
    .slide {
      width: 100%;
      max-width: 1400px;
      aspect-ratio: 16 / 9;
      background: var(--kearney-white);
      box-shadow: 0 4px 20px rgba(0,0,0,0.08);
      padding: 48px 48px 40px 48px;
      display: flex;
      flex-direction: column;
      position: relative;
    }
    .cover-content {
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      padding-top: 5%;
    }
    .cover-title {
      font-size: 56px;
      font-weight: 700;
      color: var(--kearney-purple);
      line-height: 1.1;
      letter-spacing: -0.02em;
      max-width: 50%;
    }
    .cover-subtitle {
      font-size: 24px;
      color: var(--kearney-black);
      margin-top: 32px;
      font-weight: 700;
      max-width: 50%;
    }
    .cover-meta {
      font-size: 20px;
      color: var(--kearney-black);
      margin-top: 8px;
      font-weight: 400;
      max-width: 50%;
    }
    .kearney-logo {
      position: absolute;
      bottom: 40px;
      left: 48px;
      width: 140px;
      height: auto;
    }
    .slide-nav {
      position: absolute;
      bottom: 16px;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      gap: 24px;
      align-items: center;
    }
    .nav-arrow {
      width: 32px;
      height: 32px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--kearney-gray);
      cursor: pointer;
      transition: color 0.2s;
      text-decoration: none;
    }
    .nav-arrow:hover { color: var(--kearney-black); }
    .nav-arrow.disabled { opacity: 0.3; cursor: default; }
    .slide-number {
      font-size: 12px;
      color: var(--kearney-gray);
      font-weight: 500;
    }
    @media print {
      body { background: white; }
      .slide { box-shadow: none; min-height: 100vh; }
    }
    @page { size: A4 landscape; margin: 0; }
  </style>
</head>
<body>
  <div class="slide">
    <div class="cover-content">
      <h1 class="cover-title">Project Title Here</h1>
      <p class="cover-subtitle">Subtitle or Description</p>
      <p class="cover-meta">Category | Month Year</p>
    </div>
    <!-- KEARNEY LOGO - BOTTOM LEFT (BLACK for light bg) -->
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
    <div class="slide-nav">
      <span class="nav-arrow disabled">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="15 18 9 12 15 6"></polyline>
        </svg>
      </span>
      <span class="slide-number">1</span>
      <a href="slide-02-xxx.html" class="nav-arrow">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="9 18 15 12 9 6"></polyline>
        </svg>
      </a>
    </div>
  </div>
</body>
</html>
```

---

## Component Patterns

### KPI Row with Icons (Fixed 4 Columns)

```html
<div class="kpi-row">
  <div class="kpi-card">
    <div class="kpi-icon"><i data-lucide="database" style="width:24px;height:24px"></i></div>
    <div class="kpi-value">179+</div>
    <div class="kpi-label">Public Repositories</div>
  </div>
  <div class="kpi-card secondary">
    <div class="kpi-icon"><i data-lucide="git-commit" style="width:24px;height:24px"></i></div>
    <div class="kpi-value white">1,639</div>
    <div class="kpi-label">Total Commits</div>
  </div>
  <div class="kpi-card tertiary">
    <div class="kpi-icon"><i data-lucide="building-2" style="width:24px;height:24px"></i></div>
    <div class="kpi-value gray">8</div>
    <div class="kpi-label">GitHub Orgs</div>
  </div>
  <div class="kpi-card quaternary">
    <div class="kpi-icon"><i data-lucide="code-2" style="width:24px;height:24px"></i></div>
    <div class="kpi-value gray">12+</div>
    <div class="kpi-label">Languages</div>
  </div>
</div>
```

### Table with Explicit Column Alignment

```html
<style>
  /* Define alignment for EACH column */
  .data-table th:nth-child(1) { text-align: left; width: 200px; }
  .data-table th:nth-child(2) { text-align: center; width: 100px; }
  .data-table th:nth-child(3) { text-align: center; width: 80px; }
  .data-table th:nth-child(4) { text-align: center; width: 80px; }
  .data-table th:nth-child(5) { text-align: left; }

  .data-table td:nth-child(1) { text-align: left; font-weight: 500; }
  .data-table td:nth-child(2) { text-align: center; }
  .data-table td:nth-child(3) { text-align: center; }
  .data-table td:nth-child(4) { text-align: center; }
  .data-table td:nth-child(5) { text-align: left; color: var(--muted-foreground); }
</style>

<table class="data-table">
  <thead>
    <tr>
      <th>Category</th>
      <th>Score</th>
      <th>CI/CD</th>
      <th>Tests</th>
      <th>Key Finding</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Design Systems</td>
      <td><span class="badge excellent">85/100</span></td>
      <td class="score-high">10/10</td>
      <td class="score-high">9/10</td>
      <td>Automated releases, comprehensive testing</td>
    </tr>
  </tbody>
</table>
```

### Navigation Arrows Pattern

```html
<!-- Slide Navigation - CENTER BOTTOM -->
<div class="slide-nav">
  <a href="slide-01-cover.html" class="nav-arrow">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <polyline points="15 18 9 12 15 6"></polyline>
    </svg>
  </a>
  <span class="slide-number">2</span>
  <a href="slide-03-xxx.html" class="nav-arrow">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <polyline points="9 18 15 12 9 6"></polyline>
    </svg>
  </a>
</div>

<!-- First slide: use disabled class on back arrow -->
<span class="nav-arrow disabled">...</span>

<!-- Last slide: use disabled class on forward arrow -->
<span class="nav-arrow disabled">...</span>
```

---

## CRITICAL: Observable Plot SVG Sizing in Flex Containers

When an Observable Plot chart is placed inside a flex container (like a slide layout), the SVG's intrinsic height often exceeds the container's available height. Because SVGs default to `preserveAspectRatio="xMidYMid meet"`, the entire SVG scales down proportionally to fit the height — **shrinking the width too**, even though there's plenty of horizontal space.

### Symptoms
- Chart appears to waste horizontal space on both left and right
- Changing `marginLeft`/`marginRight` in Plot config has no visible effect
- DOM inspection shows the SVG `width` attribute matches the container, but rendered width is smaller
- The width/height scaling ratio is < 1 (e.g., 0.69)

### Root Cause
The SVG viewBox (e.g., `0 0 1152 300`) has a taller aspect ratio than the flex container provides. With `preserveAspectRatio="xMidYMid meet"` (the default), the browser uniformly scales to fit the smaller dimension (height), shrinking width proportionally.

### Fix Pattern
```js
const chartSvg = Plot.plot({
  width: 1152,
  height: 220,        // Match available container height, not desired chart height
  marginLeft: 42,
  marginRight: 5,
  marginBottom: 30,
  // ... rest of config
});
chartSvg.setAttribute("preserveAspectRatio", "none");
chartSvg.style.width = "100%";
const chart = chartSvg;
```

### Key Points
1. **Set SVG height to match container height** — not your ideal chart height. If the container is ~220px tall, use `height: 220`.
2. **Set `preserveAspectRatio="none"`** — allows width and height to stretch independently.
3. **Set `style.width = "100%"`** — ensures the SVG fills the full container width.
4. **Separate title/legend from chart container** — put them outside the chart div with their own padding so the chart SVG can go edge-to-edge.

### Container Pattern
```html
<div style="padding-left:16px;">Chart Title</div>
<div class="chart-container" style="padding:4px 16px;overflow:hidden;">
  ${chart}
</div>
<div style="padding-left:16px;">${legend}</div>
```

### Also Remember: Observable Plot `r` Scale
When using `r` as a channel (function) in `Plot.dot()`, values go through a **sqrt scale** with a tiny default output range. The raw values don't translate directly to pixels.

**Fix:** Add `r: {range: [minPx, maxPx]}` at the plot level:
```js
Plot.plot({
  r: {range: [4, 12]},  // Output range in actual pixels
  marks: [
    Plot.dot(data, {
      r: d => Math.max(18, d.magnitude * 300),  // Input values — scaled through r
    })
  ]
});
```

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
