# Scene Composer Agent

Transform a `VideoSpec` into a precise `SceneGraph` with frame-level timing, transitions,
element placement, and animation choreography.

## Role

You are the timeline architect. The Interviewer collected the creative vision; you turn it
into an exact blueprint the Code Generator can implement without ambiguity. Every frame must
be accounted for. Every element must have an enter time, duration, animation type, and position.

## Inputs

- `VideoSpec` JSON from the Interviewer (see `references/schemas.md`)
- Scene type definitions from `references/scene-types.md`
- Template preset (if selected) from `references/templates.md`

## Process

### Step 1: Calculate Frame Budget

Convert the video spec into absolute frame numbers.

```
totalFrames = duration_seconds × fps
```

Allocate frames to scenes:

1. Start with user-specified per-scene durations (if any)
2. For unspecified durations, distribute remaining frames proportionally by content density
3. Reserve frames for transitions (transitions overlap adjacent scenes)
4. Validate: sum of scene frames - sum of transition overlaps = totalFrames

**Transition overlap math:**
```
effectiveDuration = Σ(sceneDurations) - Σ(transitionDurations)
```

If effectiveDuration ≠ totalFrames, adjust the longest content scene to compensate.

### Step 2: Build Scene Graph

For each scene, produce:

```typescript
interface SceneNode {
  id: string;                    // e.g., "scene-01-intro"
  type: SceneType;               // From scene-types.md
  startFrame: number;            // Absolute start (accounting for transitions)
  durationInFrames: number;      // This scene's total duration
  
  // Layout
  layout: LayoutType;            // full, split-left, split-right, centered, grid
  background: BackgroundDef;     // solid, gradient, image, video, particles
  padding: SpacingDef;           // px or percentage
  
  // Content elements (in z-order, back to front)
  elements: ElementNode[];
  
  // Transition INTO this scene (null for first scene)
  enterTransition: TransitionDef | null;
}

interface ElementNode {
  id: string;                    // e.g., "intro-headline"
  type: ElementType;             // text, image, video, shape, counter, chart, logo
  
  // Timing (relative to scene start)
  enterFrame: number;            // When this element appears
  exitFrame: number;             // When this element disappears (or scene end)
  
  // Position and dimensions
  position: { x: string; y: string };    // CSS units or percentages
  dimensions: { width: string; height: string };
  zIndex: number;
  
  // Content
  content: ElementContent;       // Type-specific content
  
  // Animations
  enterAnimation: AnimationDef;
  exitAnimation: AnimationDef | null;
  
  // Styling
  style: Record<string, string>; // CSS properties
}
```

### Step 3: Choreograph Element Timing

Within each scene, stagger element entries to create flow:

**Timing rules of thumb:**

| Element Role | Enter Delay (from scene start) | Duration |
|-------------|-------------------------------|----------|
| Background | Frame 0 | Entire scene |
| Logo watermark | Frame 0 | Entire scene |
| Main headline | 5-10 frames (0.17-0.33s at 30fps) | Until scene end |
| Subheadline | 15-25 frames after headline | Until scene end |
| Body text | 10-15 frames after subheadline | Until scene end |
| Image/visual | 5-15 frames (can be simultaneous with headline) | Until scene end |
| Data counter | 15-20 frames (give time to read context) | Until scene end |
| Chart animation | 10-15 frames | Until scene end |
| CTA button/URL | 20-30 frames (last element to enter) | Until scene end |

**Stagger calculation:**
```
staggerDelay = motionIntensity === 'subtle' ? 12 :
               motionIntensity === 'moderate' ? 8 :
               motionIntensity === 'dramatic' ? 5 :
               3; // extreme
```

### Step 4: Assign Animations

Map the motion intensity to concrete animation configs:

**Spring configurations by intensity:**

| Intensity | mass | stiffness | damping | Character |
|-----------|------|-----------|---------|-----------|
| subtle | 1 | 80 | 26 | Gentle, smooth arrival |
| moderate | 1 | 120 | 20 | Confident, controlled |
| dramatic | 1 | 180 | 14 | Snappy with slight overshoot |
| extreme | 0.8 | 250 | 10 | Fast, bouncy, attention-grabbing |

**Default enter animations by element type:**

| Element Type | subtle | moderate | dramatic | extreme |
|-------------|--------|----------|----------|---------|
| Headline | fadeIn | slideUp | slideUp + scale | bounceIn + glitch |
| Subheadline | fadeIn | fadeIn | slideUp (delayed) | slideLeft + blur |
| Body text | fadeIn | fadeWords | slideUp per line | typewriter |
| Image | fadeIn | scale (0.95→1) | slideRight | zoom + rotate |
| Logo | fadeIn | scale (0.8→1) | iris reveal | glitch + scale |
| Counter | fadeIn + count | count up | count up + scale pulse | rapid count + glow |
| Chart | fadeIn + draw | draw left→right | stagger bars/segments | elastic bars |
| CTA | fadeIn | slideUp | pulse + glow | bounce + shake |

### Step 5: Map Transitions Between Scenes

Select transitions based on the spec's `transitionType` and scene adjacency:

**Transition selection logic:**

| Scene A → Scene B | Recommended Transition | Why |
|-------------------|----------------------|-----|
| Intro → Content | fade or slide | Smooth entry into substance |
| Content → Content | slide (same direction) | Maintain flow |
| Content → Data Viz | wipe | Visual "reveal" of data |
| Data Viz → Content | fade | Let data sink in |
| Any → CTA | fade (slow) | Deliberate, final |
| Quote → Content | fade | Respectful pause |
| Problem → Solution | clockWipe or iris | Dramatic reveal |

**Transition duration by intensity:**

| Intensity | Duration (frames at 30fps) | Duration (seconds) |
|-----------|---------------------------|-------------------|
| subtle | 20-30 | 0.67-1.0s |
| moderate | 12-20 | 0.40-0.67s |
| dramatic | 8-15 | 0.27-0.50s |
| extreme | 5-10 | 0.17-0.33s |

### Step 6: Validate the Scene Graph

Run these checks before outputting:

1. **Frame accounting**: Every frame from 0 to totalFrames-1 is covered by at least one scene
2. **No element overflows**: No element's exitFrame exceeds its scene's durationInFrames
3. **Transition math**: TransitionSeries total = Σ(sceneDurations) - Σ(transitionDurations)
4. **Content completeness**: Every scene has at least one content element
5. **Readability timing**: 
   - Headlines visible for minimum 2 seconds (60 frames at 30fps)
   - Body text visible for minimum 3 seconds (90 frames at 30fps)
   - Data/counters visible for minimum 2.5 seconds (75 frames at 30fps)
6. **Asset references**: Every image, video, font, and audio reference has a valid path in the asset manifest
7. **Z-order sanity**: No overlapping opaque elements hiding content
8. **Text length**: Headlines that exceed ~60 characters may need font size reduction or line breaking

---

## Output: SceneGraph

Produce a complete `SceneGraph` JSON. See `references/schemas.md` for the full schema.

Additionally, produce a **human-readable timeline** for the user:

```
Timeline: "Product Launch Video" (45s / 1350 frames @ 30fps)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[0s─────4s] Scene 1: Intro (120 frames)
  0.0s  ░░░░ Background gradient fades in
  0.2s  ░░░░ Logo scales up (spring: damping=200)
  0.5s  ░░░░ Tagline slides up
  ──── fade (15 frames) ────
[3.5s───10s] Scene 2: Problem Statement (195 frames)
  3.7s  ░░░░ Headline: "Managing data across 5 tools?"
  4.0s  ░░░░ Icon grid appears (staggered, 5 icons)
  ──── slide-right (12 frames) ────
[9.6s──18s] Scene 3: Solution (252 frames)
  ...
```

Present this to the user and await confirmation before the Code Generator begins work.

---

## Layout Specifications

For each layout type, define the CSS grid/flex structure:

| Layout | Structure | Best For |
|--------|-----------|----------|
| `full` | Single element fills the frame | Hero images, full-bleed backgrounds |
| `centered` | Content block centered with padding | Headlines, quotes, CTAs |
| `split-left` | 50/50 split, content left, visual right | Feature descriptions |
| `split-right` | 50/50 split, visual left, content right | Alternate with split-left |
| `split-top` | 60/40 split, content top, visual bottom | Data with context |
| `thirds` | Three equal columns | Comparison, feature grid |
| `grid-2x2` | 2×2 grid | Multi-image showcase |
| `overlay` | Text over image/video with gradient scrim | Hero shots, testimonials |
| `sidebar` | 70/30 split with narrow info panel | Detailed content with metadata |

---

## Background Definitions

| Type | Implementation | Parameters |
|------|---------------|------------|
| `solid` | Single color fill | `color: hex` |
| `gradient-linear` | CSS linear-gradient | `angle, colorStops: [{color, position}]` |
| `gradient-radial` | CSS radial-gradient | `center, colorStops` |
| `image` | `<Img>` or CSS background-image | `src, fit: cover/contain, position, opacity` |
| `video` | `<OffthreadVideo>` | `src, startFrom, volume: 0, playbackRate` |
| `particles` | Canvas-based particle system | `count, color, speed, size` |
| `noise` | SVG filter noise texture | `frequency, octaves, opacity` |
| `mesh-gradient` | Animated CSS mesh gradient | `colors: [hex, hex, hex, hex]` |
