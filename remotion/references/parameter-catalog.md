# Parameter Catalog

Complete reference of every parameter the Remotion Video Producer can accept.
The Interviewer agent uses this to know what's possible; it does NOT ask the user
about every parameter — it uses progressive disclosure (Tiers 1-4).

## Table of Contents

1. [Canvas & Output](#canvas--output)
2. [Brand & Design System](#brand--design-system)
3. [Typography](#typography)
4. [Scene Architecture](#scene-architecture)
5. [Per-Scene Content Model](#per-scene-content-model)
6. [Motion & Animation](#motion--animation)
7. [Camera & Spatial Effects](#camera--spatial-effects)
8. [Visual Effects & Post-Processing](#visual-effects--post-processing)
9. [Typography Animation](#typography-animation)
10. [Audio](#audio)
11. [Rendering & Output](#rendering--output)

---

## Canvas & Output

| Parameter | Type | Options / Range | Default | Tier | Notes |
|-----------|------|----------------|---------|------|-------|
| `resolution` | preset or custom | 1080p (1920×1080), 4K (3840×2160), 720p, Square (1080×1080), Portrait (1080×1920), Custom | 1080p | 1 | Auto-set from platform |
| `width` | number | 320-7680 | 1920 | 3 | Override for custom |
| `height` | number | 320-4320 | 1080 | 3 | Override for custom |
| `fps` | number | 24, 25, 30, 60 | 30 | 3 | 24=cinematic, 60=smooth motion |
| `duration` | number (seconds) | 1-600 | 30 | 1 | Converted to durationInFrames internally |
| `outputFormat` | string | mp4, webm, gif, png-sequence | mp4 | 3 | GIF for short loops only |
| `codec` | string | h264, h265, vp8, vp9, prores | h264 | 4 | h265=smaller, prores=lossless |
| `crf` | number | 0-51 | 18 | 3 | Lower=higher quality, 0=lossless |
| `pixelFormat` | string | yuv420p, yuv444p | yuv420p | 4 | 444 for max color fidelity |
| `audioBitrate` | string | 128k, 192k, 256k, 320k | 192k | 4 | Only if audio included |

---

## Brand & Design System

| Parameter | Type | Format | Default | Tier | Notes |
|-----------|------|--------|---------|------|-------|
| `logo` | file | SVG (best), PNG (≥500px, transparency), JPG | none | 1 | SVG scales without quality loss |
| `logoPlacement` | enum | top-left, top-right, bottom-left, bottom-right, center, none | bottom-right | 2 | Per-scene override possible |
| `logoSize` | number | 40-200 (px height) | 60 | 3 | Auto-scales width proportionally |
| `logoOpacity` | number | 0-1 | 0.8 | 3 | For watermark usage |
| `primaryColor` | hex/rgb | #RRGGBB or rgb(r,g,b) | #1a1a2e | 1 | Main brand color |
| `secondaryColor` | hex/rgb | #RRGGBB | #16213e | 1 | Supporting color |
| `accentColor` | hex/rgb | #RRGGBB | #e94560 | 2 | CTAs, highlights |
| `backgroundColor` | hex/rgb/gradient | hex or gradient definition | #0f0f0f | 2 | Default scene background |
| `textColor` | hex/rgb | #RRGGBB | #ffffff | 2 | Default text color |
| `textColorSecondary` | hex/rgb | #RRGGBB | #cccccc | 3 | Subtitle/caption color |
| `theme` | enum | light, dark, custom | dark | 2 | Sets default bg/text |

---

## Typography

| Parameter | Type | Options | Default | Tier | Notes |
|-----------|------|---------|---------|------|-------|
| `fontPrimary` | string | Google Fonts name or file path | Montserrat | 2 | Headlines |
| `fontSecondary` | string | Google Fonts name or file path | Open Sans | 2 | Body text |
| `fontMono` | string | Google Fonts name or file path | JetBrains Mono | 3 | Code/data |
| `fontHeadingSize` | number | 36-120 (px at 1080p) | 72 | 3 | Auto-scaled for resolution |
| `fontSubheadingSize` | number | 28-80 | 48 | 3 | |
| `fontBodySize` | number | 24-60 | 36 | 3 | |
| `fontCaptionSize` | number | 18-36 | 24 | 3 | |
| `fontCounterSize` | number | 48-144 | 96 | 3 | For number counters |
| `fontHeadingWeight` | number | 100-900 | 700 | 3 | |
| `fontBodyWeight` | number | 100-900 | 400 | 3 | |
| `lineHeight` | number | 1.0-2.0 | 1.4 | 4 | |
| `letterSpacing` | number (em) | -0.05 to 0.2 | 0 | 4 | Negative for tight headlines |

---

## Scene Architecture

| Parameter | Type | Options | Default | Tier | Notes |
|-----------|------|---------|---------|------|-------|
| `sceneCount` | number | 1-20 | auto | 1 | Calculated from content |
| `sceneDurations` | number[] | Per-scene seconds | auto | 2 | Or auto from total/count |
| `sceneTypes` | enum[] | See scene-types.md | auto | 2 | Inferred from content |
| `sceneOrder` | number[] | Explicit ordering | sequential | 3 | |
| `transitionType` | enum | fade, slide, wipe, flip, clockWipe, iris, none, mixed | fade | 2 | Global default |
| `transitionDuration` | number | 0.2-2.0 (seconds) | 0.5 | 3 | |
| `transitionTiming` | enum | spring, linear | spring | 3 | |
| `transitionSpringConfig` | object | {damping: number} | {damping: 200} | 4 | For spring timing |

---

## Per-Scene Content Model

Each scene can contain:

| Field | Type | Description | Tier |
|-------|------|-------------|------|
| `headline` | string | Main heading text (≤ 80 chars recommended) | 1 |
| `subheadline` | string | Secondary text | 2 |
| `bodyText` | string | Paragraph content | 2 |
| `bullets` | string[] | Bullet point items | 2 |
| `image` | object | `{src, fit: cover|contain, position, opacity}` | 1 |
| `videoClip` | object | `{src, startFrom, endAt, volume, playbackRate}` | 2 |
| `data` | object | `{type: bar|line|pie|counter|table, values, labels}` | 2 |
| `quote` | object | `{text, attribution, avatar}` | 2 |
| `cta` | object | `{text, url, style: button|link|qrcode}` | 1 |
| `background` | object | `{type: solid|gradient|image|video, value}` | 2 |
| `overlay` | object | `{type: color|gradient|noise, opacity}` | 3 |
| `layout` | enum | full, centered, split-left, split-right, thirds, grid, overlay | 2 |
| `logoVisible` | boolean | Show/hide logo watermark this scene | 3 |

---

## Motion & Animation

| Parameter | Type | Options | Default | Tier | Notes |
|-----------|------|---------|---------|------|-------|
| `motionIntensity` | enum | subtle, moderate, dramatic, extreme | moderate | 2 | Sets global feel |
| `enterAnimation` | enum | fade, slideUp, slideDown, slideLeft, slideRight, scale, blur, typewriter, bounce, elastic, none | slideUp | 3 | Global default for elements |
| `exitAnimation` | enum | same as enter | fade | 3 | |
| `easing` | enum or custom | spring, linear, easeIn, easeOut, easeInOut | spring | 3 | |
| `springMass` | number | 0.1-5 | 1 | 4 | |
| `springStiffness` | number | 10-500 | 120 | 4 | |
| `springDamping` | number | 1-100 | 20 | 4 | |
| `staggerDelay` | number (frames) | 0-30 | 8 | 3 | Between sequential elements |
| `looping` | boolean | true/false | false | 3 | For GIF-style loops |

---

## Camera & Spatial Effects

| Parameter | Type | Options | Default | Tier | Notes |
|-----------|------|---------|---------|------|-------|
| `kenBurns` | object | `{startScale, endScale, startPos, endPos}` | none | 3 | Slow zoom on still images |
| `kenBurnsIntensity` | enum | subtle (1.0→1.05), moderate (1.0→1.1), dramatic (1.0→1.2) | none | 2 | Simplified Ken Burns |
| `parallaxEnabled` | boolean | true/false | false | 3 | Multi-layer depth effect |
| `parallaxLayers` | number | 2-5 | 3 | 4 | Number of depth layers |
| `cameraZoom` | object | `{from: 1.0, to: 1.1, startFrame, endFrame}` | none | 4 | Programmatic zoom |
| `cameraPan` | object | `{fromX, toX, fromY, toY}` | none | 4 | |
| `perspective` | enum | flat, shallow (200px), deep (800px) | flat | 4 | 3D transform depth |

---

## Visual Effects & Post-Processing

| Parameter | Type | Options | Default | Tier | Notes |
|-----------|------|---------|---------|------|-------|
| `filmGrain` | object | `{intensity: 0-1, animated: bool}` | none | 3 | Cinematic texture |
| `vignette` | object | `{intensity: 0-1, color: hex}` | none | 3 | Edge darkening |
| `colorGrade` | enum | none, warm, cool, vintage, noir, vivid, desaturated | none | 3 | Overall color treatment |
| `blur` | object | `{type: gaussian|motion, amount: 0-20, animated: bool}` | none | 4 | Typically for backgrounds |
| `glitch` | object | `{frequency: 0-1, intensity: 0-1}` | none | 4 | Digital distortion |
| `noise` | object | `{type: perlin|static, opacity: 0-0.5}` | none | 4 | Texture overlay |
| `letterbox` | object | `{ratio: 2.35|2.39|1.85, color: hex}` | none | 3 | Cinematic bars |
| `dropShadow` | object | `{color, blur, offsetX, offsetY}` | none | 3 | Element shadows |
| `borderRadius` | number | 0-40 (px) | 0 | 3 | Rounded corners on elements |
| `glassMorphism` | boolean | Background blur + transparency | false | 4 | Modern UI effect |

---

## Typography Animation

| Parameter | Type | Options | Default | Tier | Notes |
|-----------|------|---------|---------|------|-------|
| `headlineAnimation` | enum | fade, slideUp, revealMask, typewriter, scramble, splitChars, bounceIn, none | slideUp | 3 | |
| `bodyAnimation` | enum | fade, slideUp, fadeWords, revealLine, typewriter, none | fade | 3 | |
| `counterFormat` | object | `{from, to, duration, prefix, suffix, decimals}` | auto | 2 | e.g., "$0 → $4.2M" |
| `highlightStyle` | enum | underline-draw, background-wipe, color-shift, glow, none | none | 3 | For emphasized words |
| `typewriterSpeed` | number | 0.2-2.0 chars/frame | 0.5 | 4 | |

---

## Audio

| Parameter | Type | Options | Default | Tier | Notes |
|-----------|------|---------|---------|------|-------|
| `backgroundMusic` | file/url | MP3, WAV, AAC | none | 2 | |
| `musicVolume` | number | 0-1 | 0.3 | 3 | Background volume |
| `musicFadeIn` | number (seconds) | 0-3 | 1 | 3 | |
| `musicFadeOut` | number (seconds) | 0-3 | 2 | 3 | |
| `soundEffects` | object[] | Per-scene SFX: `{src, frame, volume}` | none | 3 | |
| `transitionSound` | file/url | Sound for transitions | none | 3 | Via TransitionSeries.Overlay |
| `voiceover` | file/url | Narration track | none | 2 | Must match video duration |
| `voiceoverVolume` | number | 0-1 | 1.0 | 3 | |

---

## Rendering & Output

| Parameter | Type | Options | Default | Tier | Notes |
|-----------|------|---------|---------|------|-------|
| `outputCodec` | enum | h264, h265, vp8, vp9, prores | h264 | 3 | |
| `outputFormat` | enum | mp4, webm, gif | mp4 | 3 | |
| `imageFormat` | enum | jpeg, png | jpeg | 4 | Frame format during render |
| `quality` | number | 0-100 | 80 | 4 | JPEG quality for frames |
| `scale` | number | 0.5-4 | 1 | 4 | Render at different scale |
| `concurrency` | number | 1-16 | auto | 4 | Parallel frame rendering |
| `lambdaRender` | boolean | true/false | false | 4 | Render on AWS Lambda |
| `stillMode` | boolean | true/false | false | 4 | Render single frame as image |
| `stillFrame` | number | 0-totalFrames | 0 | 4 | Which frame for still |
