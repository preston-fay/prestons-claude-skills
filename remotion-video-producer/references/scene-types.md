# Scene Type Library

Every available scene type, what it looks like, when to use it, and which elements it contains.
The Scene Composer uses this to translate user content into concrete layouts.

---

## Intro / Logo Reveal

**Purpose:** Open the video with brand identity. Set the tone.

**Typical duration:** 3-5 seconds (90-150 frames at 30fps)

**Layouts:**
- `centered` — Logo center screen, tagline below
- `full` — Full-screen branded background with logo reveal

**Default elements:**
| Element | Position | Enter | Animation |
|---------|----------|-------|-----------|
| Background | Fill | Frame 0 | Instant or gradient fade |
| Logo | Center, 60% height | Frame 5-10 | Scale in (0.8→1.0) with spring |
| Tagline | Center, below logo | Frame 20-30 | Fade + slideUp |

**Pro tip:** Keep it short. The intro earns attention; it doesn't hold it.

---

## Title Card

**Purpose:** Bold text-dominant scene for section headers or key statements.

**Typical duration:** 3-6 seconds

**Layouts:**
- `centered` — Text centered with generous padding
- `overlay` — Text over subtle background image

**Default elements:**
| Element | Position | Enter | Animation |
|---------|----------|-------|-----------|
| Background | Fill | Frame 0 | Solid or gradient |
| Headline | Center | Frame 5 | slideUp or revealMask |
| Divider line | Center, below headline | Frame 15 | Draw left→right |
| Subtitle | Center, below divider | Frame 25 | Fade |

---

## Content

**Purpose:** General-purpose scene for presenting information. The workhorse.

**Typical duration:** 5-10 seconds

**Layouts:**
- `split-left` — Text left, image/visual right
- `split-right` — Image/visual left, text right
- `centered` — Text block centered

**Default elements:**
| Element | Position | Enter | Animation |
|---------|----------|-------|-----------|
| Background | Fill | Frame 0 | Solid or gradient |
| Headline | Left/right half, top | Frame 5 | slideUp |
| Body text | Below headline | Frame 15 | fade or fadeWords |
| Image | Opposite half | Frame 5-10 | scale or slideIn |
| Logo watermark | Bottom-right corner | Frame 0 | Persistent, low opacity |

---

## Problem Statement

**Purpose:** Set up the pain point. Create tension. Make the audience feel the problem.

**Typical duration:** 5-8 seconds

**Layouts:**
- `centered` — Bold question/statement centered
- `split-left` — Problem text left, frustrated icon/image right

**Default elements:**
| Element | Position | Enter | Animation |
|---------|----------|-------|-----------|
| Dark/red-tinted background | Fill | Frame 0 | Gradient or solid |
| Headline (question format) | Center | Frame 5 | typewriter or slideUp |
| Supporting icons/stats | Below or beside | Frame 20 | Staggered fade |

**Pro tip:** Frame as a question the audience asks themselves. "Still managing data across 5 tools?" > "Data management is difficult."

---

## Solution

**Purpose:** Answer the problem. Show the product/answer. Relief moment.

**Typical duration:** 6-10 seconds

**Layouts:**
- `split-right` — Product screenshot right, benefits left
- `centered` — Hero visual centered with overlay text

**Default elements:**
| Element | Position | Enter | Animation |
|---------|----------|-------|-----------|
| Bright/brand-colored background | Fill | Frame 0 | Transition from problem's dark bg |
| Headline | Top or left | Frame 5 | slideUp |
| Product screenshot/visual | Center or right | Frame 10 | scale with shadow |
| Key benefit bullets (2-3) | Left or below | Frame 20 | Staggered slideUp |

---

## Data Visualization

**Purpose:** Present numbers, statistics, or data with animated charts.

**Typical duration:** 5-8 seconds

**Layouts:**
- `centered` — Single large chart/counter centered
- `split-left` — Chart left, context text right
- `grid-2x2` — Multiple small charts

**Chart types available:**
| Chart | Best for | Animation |
|-------|----------|-----------|
| Counter | Single impressive number ("4.2M users") | Count up from 0 |
| Bar chart | Comparison across categories | Bars grow from bottom |
| Line chart | Trends over time | Draw left to right |
| Pie chart | Part-of-whole | Segments expand from center |
| Progress bar | Percentage/completion | Fill left to right |

**Default elements:**
| Element | Position | Enter | Animation |
|---------|----------|-------|-----------|
| Background | Fill | Frame 0 | Solid |
| Context label | Top | Frame 5 | fade |
| Chart/counter | Center | Frame 10 | Type-specific animation |
| Source/footnote | Bottom | Frame 30 | fade (low opacity) |

---

## Quote / Testimonial

**Purpose:** Social proof or impactful statement from a person.

**Typical duration:** 4-7 seconds

**Layouts:**
- `centered` — Quote text large and centered
- `split-left` — Avatar/photo left, quote right

**Default elements:**
| Element | Position | Enter | Animation |
|---------|----------|-------|-----------|
| Background | Fill | Frame 0 | Subtle, muted |
| Opening quotation mark | Top-left of quote | Frame 5 | Scale or fade |
| Quote text | Center | Frame 10 | fadeWords (word by word) |
| Attribution | Below quote | Frame 30 | fade |
| Avatar (optional) | Left of quote or beside attribution | Frame 5 | scale in circular mask |

---

## Image Showcase

**Purpose:** Display a product screenshot, photo, or visual prominently.

**Typical duration:** 4-7 seconds

**Layouts:**
- `full` — Full-bleed image
- `centered` — Image with padding, optional device frame
- `overlay` — Image with text overlay and gradient scrim

**Default elements:**
| Element | Position | Enter | Animation |
|---------|----------|-------|-----------|
| Image | Fill or centered | Frame 0-5 | Ken Burns zoom, scale, or fade |
| Caption/label (optional) | Bottom | Frame 15 | slideUp |
| Gradient scrim (if overlay) | Bottom 30% | Frame 0 | Fade in |

---

## Feature List

**Purpose:** Present 3-5 features or benefits in sequence.

**Typical duration:** 6-12 seconds

**Layouts:**
- `centered` — Stacked list with icons
- `thirds` — Three features side by side
- `split-left` — List left, hero image right

**Default elements:**
| Element | Position | Enter | Animation |
|---------|----------|-------|-----------|
| Background | Fill | Frame 0 | Solid |
| Section headline | Top | Frame 5 | slideUp |
| Feature items (staggered) | Centered or left | Frame 15+ | Staggered slideUp with icons |

**Stagger pattern:** Each feature enters `staggerDelay × index` frames after the previous.

---

## Step Sequence

**Purpose:** Walk through a process: "Step 1, Step 2, Step 3."

**Typical duration:** 8-15 seconds

**Layouts:**
- `centered` — Steps appear one at a time
- `split-left` — Step text left, illustration right

**Default elements:**
| Element | Position | Enter | Animation |
|---------|----------|-------|-----------|
| Step number | Large, accent-colored | Per step timing | Scale + fade |
| Step title | Below/beside number | Staggered | slideUp |
| Step description | Below title | Staggered | fade |
| Progress indicator | Bottom | Frame 0 | Progressive fill |

---

## Comparison

**Purpose:** Side-by-side comparison (before/after, us vs them, plan A vs B).

**Typical duration:** 5-8 seconds

**Layouts:**
- `split-left` / `split-right` — 50/50 split with divider
- `thirds` — Three options

**Default elements:**
| Element | Position | Enter | Animation |
|---------|----------|-------|-----------|
| Left column header | Top-left half | Frame 5 | slideDown |
| Right column header | Top-right half | Frame 5 | slideDown |
| Divider line | Center vertical | Frame 10 | Draw top to bottom |
| Comparison items | Each half | Frame 15+ | Staggered fade |

---

## CTA (Call to Action)

**Purpose:** Final push. Tell the viewer what to do next.

**Typical duration:** 3-5 seconds

**Layouts:**
- `centered` — CTA centered with emphasis
- `overlay` — CTA over blurred background from previous scene

**Default elements:**
| Element | Position | Enter | Animation |
|---------|----------|-------|-----------|
| Background | Fill | Frame 0 | Brand primary color or gradient |
| CTA headline | Center | Frame 5 | slideUp + scale emphasis |
| URL / button | Below headline | Frame 15 | Fade + pulse |
| Logo | Below URL | Frame 20 | Fade |

---

## Outro

**Purpose:** Close the video with brand reinforcement.

**Typical duration:** 2-4 seconds

**Layouts:**
- `centered` — Logo centered, "Thank you" or tagline

**Default elements:**
| Element | Position | Enter | Animation |
|---------|----------|-------|-----------|
| Background | Fill | Frame 0 | Solid brand color |
| Logo | Center | Frame 5 | Scale in |
| Tagline | Below logo | Frame 15 | Fade |
| Social handles (optional) | Bottom | Frame 20 | Fade |
