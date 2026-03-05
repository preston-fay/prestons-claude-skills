# Data Schemas

TypeScript interfaces for the data structures passed between agents.

---

## VideoSpec

Output of the Interviewer agent. Input to the Scene Composer.

```typescript
interface VideoSpec {
  // Project metadata
  projectName: string;
  description: string;
  createdAt: string; // ISO 8601

  // Canvas & output settings
  canvas: {
    width: number;
    height: number;
    fps: number;
    duration: number;          // seconds
    durationInFrames: number;  // calculated: duration × fps
    outputFormat: 'mp4' | 'webm' | 'gif' | 'png-sequence';
    codec: 'h264' | 'h265' | 'vp8' | 'vp9' | 'prores';
    crf: number;
    pixelFormat: 'yuv420p' | 'yuv444p';
  };

  // Brand & design system
  brand: {
    logo: {
      src: string;           // file path or 'none'
      format: 'svg' | 'png' | 'jpg';
      placement: LogoPlacement;
      size: number;          // px height
      opacity: number;       // 0-1
    } | null;
    colors: {
      primary: string;       // hex
      secondary: string;
      accent: string;
      background: string;
      text: string;
      textSecondary: string;
    };
    fonts: {
      primary: FontDef;
      secondary: FontDef;
      mono: FontDef | null;
    };
    theme: 'light' | 'dark';
  };

  // Scene definitions (high-level, user-facing)
  scenes: SceneSpec[];

  // Motion & animation globals
  motion: {
    intensity: 'subtle' | 'moderate' | 'dramatic' | 'extreme';
    defaultEasing: 'spring' | 'linear' | 'easeInOut';
    springConfig: {
      mass: number;
      stiffness: number;
      damping: number;
    };
    staggerDelay: number;    // frames
    transitionType: TransitionType;
    transitionDuration: number; // seconds
    transitionTiming: 'spring' | 'linear';
  };

  // Audio
  audio: {
    backgroundMusic: AudioDef | null;
    voiceover: AudioDef | null;
    soundEffects: SoundEffectDef[];
    transitionSound: AudioDef | null;
  };

  // Global visual effects
  effects: {
    filmGrain: { intensity: number; animated: boolean } | null;
    vignette: { intensity: number; color: string } | null;
    colorGrade: ColorGrade | null;
    letterbox: { ratio: number; color: string } | null;
    noise: { type: 'perlin' | 'static'; opacity: number } | null;
  };

  // Asset manifest
  assets: AssetManifest;

  // Platform target (informational)
  platform: Platform | null;
}

// Supporting types

type LogoPlacement = 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right' | 'center' | 'none';

type TransitionType = 'fade' | 'slide' | 'wipe' | 'flip' | 'clockWipe' | 'iris' | 'none' | 'mixed';

type ColorGrade = 'warm' | 'cool' | 'vintage' | 'noir' | 'vivid' | 'desaturated';

type Platform = 'youtube' | 'instagram-reels' | 'instagram-story' | 'instagram-post' |
  'tiktok' | 'linkedin' | 'twitter' | 'website' | 'presentation' | 'gif';

interface FontDef {
  name: string;
  source: 'google-fonts' | 'local';
  file?: string;             // path for local fonts
  weight: number;
}

interface AudioDef {
  src: string;
  volume: number;            // 0-1
  fadeIn: number;            // seconds
  fadeOut: number;           // seconds
  trimStart?: number;        // seconds
  trimEnd?: number;          // seconds
}

interface SoundEffectDef {
  src: string;
  sceneId: string;
  frame: number;             // relative to scene start
  volume: number;
}

interface AssetManifest {
  files: AssetFile[];
}

interface AssetFile {
  id: string;
  path: string;              // project-relative path (public/...)
  type: 'image' | 'video' | 'audio' | 'font' | 'svg';
  format: string;            // file extension
  usedInScenes: string[];    // scene IDs that reference this asset
}
```

---

## SceneSpec

Part of VideoSpec — user-level scene definition.

```typescript
interface SceneSpec {
  id: string;
  type: SceneType;
  duration: number;          // seconds (approximate, Scene Composer refines to frames)
  
  // Content
  headline?: string;
  subheadline?: string;
  bodyText?: string;
  bullets?: string[];
  image?: { src: string; fit: 'cover' | 'contain'; position?: string };
  videoClip?: { src: string; startFrom?: number; endAt?: number; volume?: number };
  data?: DataDef;
  quote?: { text: string; attribution: string; avatar?: string };
  cta?: { text: string; url?: string; style: 'button' | 'link' | 'qrcode' };
  
  // Visual
  background?: BackgroundDef;
  layout: LayoutType;
  logoVisible: boolean;
  
  // Per-scene overrides (optional)
  transitionOverride?: TransitionType;
  animationOverride?: string;
}

type SceneType = 'intro' | 'title-card' | 'content' | 'data-viz' | 'quote' | 
  'testimonial' | 'image-showcase' | 'video-clip' | 'split-screen' | 
  'comparison' | 'timeline' | 'cta' | 'outro' | 'problem' | 'solution' | 
  'feature-list' | 'step-sequence' | 'logo-reveal';

type LayoutType = 'full' | 'centered' | 'split-left' | 'split-right' | 
  'split-top' | 'split-bottom' | 'thirds' | 'grid-2x2' | 'overlay' | 'sidebar';

interface DataDef {
  type: 'bar' | 'line' | 'pie' | 'counter' | 'table' | 'progress';
  values: number[];
  labels?: string[];
  prefix?: string;
  suffix?: string;
  targetValue?: number;      // for counters
  decimals?: number;
}

interface BackgroundDef {
  type: 'solid' | 'gradient-linear' | 'gradient-radial' | 'image' | 'video' | 'mesh-gradient';
  value: string | GradientDef | ImageBgDef;
}

interface GradientDef {
  angle?: number;
  colors: { color: string; position: number }[];
}

interface ImageBgDef {
  src: string;
  fit: 'cover' | 'contain';
  opacity: number;
  overlay?: { color: string; opacity: number };
}
```

---

## SceneGraph

Output of the Scene Composer agent. Input to the Code Generator.

```typescript
interface SceneGraph {
  // Global
  totalFrames: number;
  fps: number;
  width: number;
  height: number;
  
  // Scenes in playback order
  scenes: SceneNode[];
  
  // Transitions between scenes
  transitions: TransitionNode[];
  
  // Validation metadata
  validation: {
    effectiveDuration: number;  // Must equal totalFrames
    sceneDurationsSum: number;
    transitionDurationsSum: number;
  };
}

interface SceneNode {
  id: string;
  type: SceneType;
  index: number;
  startFrame: number;          // Absolute frame (for reference only — TransitionSeries handles positioning)
  durationInFrames: number;
  
  layout: LayoutType;
  background: BackgroundDef;
  padding: { top: number; right: number; bottom: number; left: number };
  
  elements: ElementNode[];
}

interface ElementNode {
  id: string;
  type: 'text' | 'image' | 'video' | 'shape' | 'counter' | 'chart' | 'logo' | 'cta' | 'icon';
  
  // Timing (relative to scene start)
  enterFrame: number;
  exitFrame: number;           // scene's durationInFrames if persistent
  
  // Position
  position: {
    x: string;                 // CSS value: '80px', '50%', 'center'
    y: string;
    anchor: 'top-left' | 'center' | 'top-center' | 'bottom-center';
  };
  dimensions: {
    width: string;             // CSS value or 'auto'
    height: string;
  };
  zIndex: number;
  
  // Content (type-specific)
  content: TextContent | ImageContent | VideoContent | ShapeContent |
    CounterContent | ChartContent | LogoContent | CTAContent;
  
  // Animation
  enterAnimation: AnimationDef;
  exitAnimation: AnimationDef | null;
  
  // Base styles
  style: Record<string, string | number>;
}

// Content types
interface TextContent {
  type: 'text';
  text: string;
  role: 'headline' | 'subheadline' | 'body' | 'caption' | 'label';
  fontFamily: string;
  fontSize: number;
  fontWeight: number;
  color: string;
  textAlign?: 'left' | 'center' | 'right';
  maxWidth?: string;
}

interface ImageContent {
  type: 'image';
  src: string;
  alt: string;
  fit: 'cover' | 'contain' | 'fill';
  borderRadius?: number;
  kenBurns?: { startScale: number; endScale: number };
}

interface VideoContent {
  type: 'video';
  src: string;
  volume: number;
  trimBefore?: number;
  trimAfter?: number;
  playbackRate?: number;
}

interface CounterContent {
  type: 'counter';
  from: number;
  to: number;
  duration: number;            // frames
  prefix: string;
  suffix: string;
  decimals: number;
  fontFamily: string;
  fontSize: number;
  color: string;
}

interface ChartContent {
  type: 'chart';
  chartType: 'bar' | 'line' | 'pie' | 'progress';
  data: { label: string; value: number; color?: string }[];
  animationDuration: number;   // frames
}

interface CTAContent {
  type: 'cta';
  text: string;
  url?: string;
  style: 'button' | 'link' | 'qrcode';
  backgroundColor?: string;
  textColor?: string;
  borderRadius?: number;
}

interface LogoContent {
  type: 'logo';
  src: string;
}

interface ShapeContent {
  type: 'shape';
  shape: 'rectangle' | 'circle' | 'line' | 'divider';
  fill?: string;
  stroke?: string;
  strokeWidth?: number;
}

// Animation types
interface AnimationDef {
  type: 'fade' | 'slideUp' | 'slideDown' | 'slideLeft' | 'slideRight' | 
    'scale' | 'blur' | 'typewriter' | 'bounce' | 'elastic' | 'none' |
    'fadeWords' | 'revealLine' | 'scramble' | 'splitChars' | 'countUp' | 'draw';
  duration: number;            // frames
  delay: number;               // frames from scene start (same as enterFrame)
  easing: 'spring' | 'linear' | 'easeIn' | 'easeOut' | 'easeInOut';
  springConfig?: {
    mass: number;
    stiffness: number;
    damping: number;
  };
  distance?: number;           // px for slide animations
}

// Transition types
interface TransitionNode {
  afterSceneIndex: number;     // Transition after this scene
  presentation: 'fade' | 'slide' | 'wipe' | 'flip' | 'clockWipe' | 'iris';
  presentationOptions?: {
    direction?: 'from-left' | 'from-right' | 'from-top' | 'from-bottom';
  };
  timing: 'spring' | 'linear';
  durationInFrames: number;
  timingConfig?: {
    damping?: number;          // for spring
  };
}
```

---

## QCResult

Output of the QC Reviewer agent.

```typescript
interface QCResult {
  passed: boolean;
  timestamp: string;
  
  checks: {
    structural: CheckResult;
    timing: CheckResult;
    assets: CheckResult;
    remotion: CheckResult;
    typescript: CheckResult;
    design: CheckResult;
    codeQuality: CheckResult;
  };
  
  summary: {
    critical: number;
    warnings: number;
    info: number;
    passed: number;
    total: number;
  };
  
  fixInstructions: string[];   // Ordered list of fixes for Code Generator
}

interface CheckResult {
  passed: boolean;
  details: CheckDetail[];
}

interface CheckDetail {
  severity: 'critical' | 'warning' | 'info';
  check: string;
  location?: string;          // file:line
  expected?: string | number;
  actual?: string | number;
  issue?: string;
  fix: string;
}
```
