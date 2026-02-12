# Remotion API Reference

Authoritative reference for generating correct Remotion code.
Derived from Remotion's official documentation and LLM system prompt.

**Always follow these patterns exactly. Deviations break renders.**

---

## Project Structure

```
project/
├── src/
│   ├── index.ts          # Entry: registerRoot(Root)
│   ├── Root.tsx           # Composition definitions
│   └── *.tsx              # Components
├── public/                # Static assets (images, fonts, audio, video)
├── package.json
├── tsconfig.json
└── remotion.config.ts
```

Scaffold with: `npx create-video@latest --blank`

---

## Core Imports

```typescript
// From 'remotion' (core)
import {
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
  random,
  staticFile,
  Sequence,
  Series,
  AbsoluteFill,
  Composition,
  Img,
  registerRoot,
  Easing,
} from 'remotion';

// From '@remotion/media' (video and audio — NOT from 'remotion')
import {Video} from '@remotion/media';
import {Audio} from '@remotion/media';

// From '@remotion/transitions'
import {TransitionSeries, linearTiming, springTiming} from '@remotion/transitions';

// Transition presentations (each from its own path)
import {fade} from '@remotion/transitions/fade';
import {slide} from '@remotion/transitions/slide';
import {wipe} from '@remotion/transitions/wipe';
import {flip} from '@remotion/transitions/flip';
import {clockWipe} from '@remotion/transitions/clock-wipe';
import {iris} from '@remotion/transitions/iris';

// Google Fonts
import {loadFont} from '@remotion/google-fonts/FontName';

// GIFs
import {Gif} from '@remotion/gif';
```

---

## Composition Definition

```typescript
<Composition
  id="MyVideo"
  component={MyComponent}
  durationInFrames={900}     // 30 seconds at 30fps
  width={1920}
  height={1080}
  fps={30}
  defaultProps={{}}          // Must match component's prop types
/>
```

**Rules:**
- Default fps=30, width=1920, height=1080
- `durationInFrames` must be exact integer
- `defaultProps` shape must match the component's props interface

---

## useCurrentFrame()

Returns the current frame number, starting at 0.

```typescript
const frame = useCurrentFrame();
```

**Inside a `<Sequence>`:** Returns frame relative to that Sequence's start (not absolute).

```typescript
// At absolute frame 100, inside <Sequence from={80}>:
// useCurrentFrame() returns 20
```

---

## useVideoConfig()

```typescript
const {fps, durationInFrames, width, height} = useVideoConfig();
```

Always use this instead of hardcoding values.

---

## interpolate()

```typescript
const opacity = interpolate(
  frame,          // input value
  [0, 30],        // input range
  [0, 1],         // output range
  {
    extrapolateLeft: 'clamp',   // ALWAYS include
    extrapolateRight: 'clamp',  // ALWAYS include
  }
);
```

**MANDATORY:** Always include `extrapolateLeft: 'clamp'` and `extrapolateRight: 'clamp'`.
Without clamping, values can go negative or above 1, causing visual bugs.

**Multiple ranges:**
```typescript
const scale = interpolate(frame, [0, 15, 30], [0.8, 1.05, 1.0], {
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
});
```

---

## spring()

Physics-based animation. Always pass `fps` from `useVideoConfig()`.

```typescript
const {fps} = useVideoConfig();
const frame = useCurrentFrame();

const value = spring({
  fps,
  frame: frame - delay,    // Subtract delay for stagger
  config: {
    damping: 200,           // Higher = less bounce (200 = overdamped/smooth)
    mass: 1,                // Higher = heavier/slower
    stiffness: 100,         // Higher = snappier
  },
});
// Returns 0 → 1 (approximately)
```

**Recommended damping values:**
- 200+ : No bounce, smooth arrival (corporate, subtle)
- 100-200: Slight overshoot (moderate, professional)
- 20-100: Visible bounce (dramatic, playful)
- 10-20: Very bouncy (extreme, attention-grabbing)

**Delay with spring:** Subtract delay frames from `frame`:
```typescript
const progress = spring({fps, frame: frame - 15, config: {damping: 200}});
```
When `frame - delay` is negative, spring returns 0 (not started yet).

---

## Sequence

Time-shift children. `useCurrentFrame()` inside returns frame relative to Sequence start.

```typescript
<Sequence from={30} durationInFrames={60}>
  <MyComponent />  {/* useCurrentFrame() starts at 0 inside here */}
</Sequence>
```

- `from`: Frame number where children appear
- `durationInFrames`: How long children are visible
- `from` can be negative (starts immediately but skips first frames)

---

## Series

Display children sequentially, one after another:

```typescript
<Series>
  <Series.Sequence durationInFrames={60}>
    <SceneA />
  </Series.Sequence>
  <Series.Sequence durationInFrames={90}>
    <SceneB />  {/* Starts at frame 60 */}
  </Series.Sequence>
  <Series.Sequence durationInFrames={60} offset={-10}>
    <SceneC />  {/* Starts at frame 140 (60+90-10) */}
  </Series.Sequence>
</Series>
```

`offset`: Shifts start by N frames (negative = overlap, positive = gap).

---

## TransitionSeries

Scenes with transitions between them. **This is the primary tool for multi-scene videos.**

```typescript
<TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={120}>
    <SceneA />
  </TransitionSeries.Sequence>

  <TransitionSeries.Transition
    presentation={fade()}
    timing={springTiming({config: {damping: 200}})}
  />

  <TransitionSeries.Sequence durationInFrames={150}>
    <SceneB />
  </TransitionSeries.Sequence>

  <TransitionSeries.Transition
    presentation={slide({direction: 'from-right'})}
    timing={linearTiming({durationInFrames: 20})}
  />

  <TransitionSeries.Sequence durationInFrames={90}>
    <SceneC />
  </TransitionSeries.Sequence>
</TransitionSeries>
```

**CRITICAL ORDERING:** Must alternate Sequence → Transition → Sequence → Transition → Sequence.
Never two Transitions or two Sequences in a row.

**Duration math:** Total effective duration = Σ(sceneDurations) - Σ(transitionDurations).
With scenes of 120, 150, 90 frames and transitions of 15, 20 frames:
Effective = (120 + 150 + 90) - (15 + 20) = 325 frames.

**Available presentations:**
| Presentation | Import | Options |
|-------------|--------|---------|
| `fade()` | `@remotion/transitions/fade` | `{exitFade?: boolean}` |
| `slide()` | `@remotion/transitions/slide` | `{direction: 'from-left'|'from-right'|'from-top'|'from-bottom'}` |
| `wipe()` | `@remotion/transitions/wipe` | `{direction: 'from-left'|...8 directions}` |
| `flip()` | `@remotion/transitions/flip` | `{direction: 'from-left'|'from-right'|'from-top'|'from-bottom'}` |
| `clockWipe()` | `@remotion/transitions/clock-wipe` | `{width, height}` |
| `iris()` | `@remotion/transitions/iris` | |
| `none()` | `@remotion/transitions/none` | Audio-only transitions |

**Timing options:**
```typescript
springTiming({config: {damping: 200}})              // Spring-based
springTiming({config: {damping: 200}, durationInFrames: 25})  // Spring with max duration
linearTiming({durationInFrames: 20})                // Linear
linearTiming({durationInFrames: 20, easing: Easing.ease})  // Linear with easing
```

**Get transition duration:**
```typescript
const timing = linearTiming({durationInFrames: 20});
const frames = timing.getDurationInFrames({fps: 30}); // 20
```

---

## AbsoluteFill

Full-screen absolutely positioned container. Use for layering.

```typescript
<AbsoluteFill style={{backgroundColor: 'blue'}}>
  <AbsoluteFill>{/* Back layer */}</AbsoluteFill>
  <AbsoluteFill>{/* Front layer */}</AbsoluteFill>
</AbsoluteFill>
```

---

## Media Components

### Images
```typescript
import {Img} from 'remotion';
<Img src={staticFile('logo.png')} style={{width: 200}} />
```
Use `<Img>` not `<img>`. It waits for the image to load before rendering the frame.

### Video
```typescript
import {Video} from '@remotion/media';
<Video
  src={staticFile('clip.mp4')}
  style={{width: '100%'}}
  volume={0.5}
  trimBefore={30}      // Skip first 30 frames
  trimAfter={120}      // End after frame 120
/>
```

### Audio
```typescript
import {Audio} from '@remotion/media';
<Audio
  src={staticFile('music.mp3')}
  volume={0.3}
  trimBefore={0}
  trimAfter={900}
/>
```

### Static files
```typescript
import {staticFile} from 'remotion';
const logoUrl = staticFile('logo.svg');  // → public/logo.svg
```

---

## Randomness

**NEVER use `Math.random()`** — it breaks deterministic rendering.

```typescript
import {random} from 'remotion';
const value = random('my-unique-seed');  // Returns 0-1, same every render
const value2 = random(`particle-${index}`);  // Unique per element
```

---

## Rendering

```bash
# Preview in Studio
npx remotion studio

# Render to MP4
npx remotion render MyVideo

# Render with options
npx remotion render MyVideo --codec h264 --crf 18

# Render a still frame
npx remotion still MyVideo --frame 0
```

---

## Google Fonts

```typescript
import {loadFont} from '@remotion/google-fonts/Montserrat';
const {fontFamily} = loadFont();

// Use in styles
<div style={{fontFamily}}>Hello</div>
```

Install: `npx remotion add @remotion/google-fonts`

**Font name mapping:** Use PascalCase with no spaces:
- "Open Sans" → `@remotion/google-fonts/OpenSans`
- "DM Sans" → `@remotion/google-fonts/DMSans`
- "IBM Plex Mono" → `@remotion/google-fonts/IBMPlexMono`
- "Plus Jakarta Sans" → `@remotion/google-fonts/PlusJakartaSans`

---

## Common Patterns

### Fade in an element
```typescript
const opacity = interpolate(frame, [0, 20], [0, 1], {
  extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
});
<div style={{opacity}}>Content</div>
```

### Slide up with spring
```typescript
const progress = spring({fps, frame, config: {damping: 200}});
const translateY = interpolate(progress, [0, 1], [40, 0]);
<div style={{opacity: progress, transform: `translateY(${translateY}px)`}}>Content</div>
```

### Staggered elements
```typescript
{items.map((item, i) => {
  const delay = i * 8; // 8 frames apart
  const progress = spring({fps, frame: frame - delay, config: {damping: 200}});
  return <div key={i} style={{opacity: progress}}>{item}</div>;
})}
```

### Animated counter
```typescript
const count = interpolate(frame, [0, 60], [0, 4200], {
  extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
});
<div>${Math.round(count).toLocaleString()}</div>
```
