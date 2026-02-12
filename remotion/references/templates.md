# Template Presets

Pre-configured style packages that set dozens of parameters at once.
Users pick a template during the interview; individual parameters can still be overridden.

---

## corporate-minimal

**Best for:** Investor decks, internal comms, quarterly reports, B2B marketing

**Visual character:** Swiss-design inspired. Clean lines, generous whitespace, precise typography.

```typescript
const corporateMinimal = {
  theme: 'light',
  colors: {
    primary: '#1a1a2e',
    secondary: '#16213e',
    accent: '#0f3460',
    background: '#ffffff',
    text: '#1a1a2e',
    textSecondary: '#6b7280',
  },
  fonts: {
    primary: { name: 'DM Sans', weight: 700 },
    secondary: { name: 'DM Sans', weight: 400 },
  },
  motion: {
    intensity: 'subtle',
    springConfig: { mass: 1, stiffness: 80, damping: 26 },
    staggerDelay: 12,
    transitionType: 'fade',
    transitionDuration: 0.7,
  },
  effects: {
    filmGrain: null,
    vignette: null,
    colorGrade: null,
  },
  defaults: {
    enterAnimation: 'fade',
    headlineAnimation: 'slideUp',
    bodyAnimation: 'fade',
    logoPlacement: 'bottom-right',
    logoOpacity: 0.6,
  },
};
```

---

## bold-impact

**Best for:** Product launches, social ads, brand announcements, event promos

**Visual character:** Large typography, high contrast, kinetic energy, attention-grabbing.

```typescript
const boldImpact = {
  theme: 'dark',
  colors: {
    primary: '#ff6b35',
    secondary: '#004e89',
    accent: '#ffd166',
    background: '#0a0a0a',
    text: '#ffffff',
    textSecondary: '#e0e0e0',
  },
  fonts: {
    primary: { name: 'Space Grotesk', weight: 700 },
    secondary: { name: 'Inter', weight: 400 },
  },
  fontSizes: {
    heading: 88,
    subheading: 52,
    body: 36,
  },
  motion: {
    intensity: 'dramatic',
    springConfig: { mass: 1, stiffness: 180, damping: 14 },
    staggerDelay: 5,
    transitionType: 'slide',
    transitionDuration: 0.4,
  },
  effects: {
    filmGrain: null,
    vignette: { intensity: 0.3, color: '#000000' },
    colorGrade: null,
  },
  defaults: {
    enterAnimation: 'slideUp',
    headlineAnimation: 'splitChars',
    bodyAnimation: 'slideUp',
    logoPlacement: 'bottom-left',
    logoOpacity: 0.9,
  },
};
```

---

## cinematic

**Best for:** Brand films, testimonials, product stories, about us videos

**Visual character:** Letterboxed, film grain, slow motion feel, atmospheric lighting.

```typescript
const cinematic = {
  theme: 'dark',
  colors: {
    primary: '#c9a96e',
    secondary: '#2c2c34',
    accent: '#d4a373',
    background: '#1a1a1a',
    text: '#f5f5f5',
    textSecondary: '#a0a0a0',
  },
  fonts: {
    primary: { name: 'Playfair Display', weight: 700 },
    secondary: { name: 'Source Sans 3', weight: 300 },
  },
  motion: {
    intensity: 'subtle',
    springConfig: { mass: 1.5, stiffness: 60, damping: 30 },
    staggerDelay: 15,
    transitionType: 'fade',
    transitionDuration: 1.0,
  },
  effects: {
    filmGrain: { intensity: 0.15, animated: true },
    vignette: { intensity: 0.4, color: '#000000' },
    colorGrade: 'warm',
    letterbox: { ratio: 2.35, color: '#000000' },
  },
  defaults: {
    enterAnimation: 'fade',
    headlineAnimation: 'fade',
    bodyAnimation: 'fade',
    logoPlacement: 'none',
    fps: 24,
  },
};
```

---

## data-driven

**Best for:** Quarterly reports, analytics dashboards, financial summaries, infographics

**Visual character:** Grid-based, monospaced numbers, chart animations, information-dense.

```typescript
const dataDriven = {
  theme: 'dark',
  colors: {
    primary: '#00d4aa',
    secondary: '#7c3aed',
    accent: '#f59e0b',
    background: '#0f172a',
    text: '#f1f5f9',
    textSecondary: '#94a3b8',
  },
  fonts: {
    primary: { name: 'IBM Plex Sans', weight: 600 },
    secondary: { name: 'IBM Plex Sans', weight: 400 },
    mono: { name: 'IBM Plex Mono', weight: 500 },
  },
  motion: {
    intensity: 'moderate',
    springConfig: { mass: 1, stiffness: 100, damping: 22 },
    staggerDelay: 6,
    transitionType: 'wipe',
    transitionDuration: 0.5,
  },
  effects: {
    filmGrain: null,
    vignette: null,
    colorGrade: null,
    noise: { type: 'static', opacity: 0.03 },
  },
  defaults: {
    enterAnimation: 'slideUp',
    headlineAnimation: 'slideUp',
    bodyAnimation: 'fade',
    counterFontSize: 112,
    gridLines: true,
    logoPlacement: 'top-right',
    logoOpacity: 0.5,
  },
};
```

---

## explainer

**Best for:** How-it-works, onboarding, tutorials, product walkthroughs

**Visual character:** Friendly, step-by-step, icon-driven, clear progression.

```typescript
const explainer = {
  theme: 'light',
  colors: {
    primary: '#4361ee',
    secondary: '#3a0ca3',
    accent: '#f72585',
    background: '#f8f9fa',
    text: '#212529',
    textSecondary: '#6c757d',
  },
  fonts: {
    primary: { name: 'Nunito', weight: 700 },
    secondary: { name: 'Nunito', weight: 400 },
  },
  motion: {
    intensity: 'moderate',
    springConfig: { mass: 1, stiffness: 130, damping: 18 },
    staggerDelay: 8,
    transitionType: 'slide',
    transitionDuration: 0.4,
  },
  effects: {
    filmGrain: null,
    vignette: null,
    colorGrade: null,
  },
  defaults: {
    enterAnimation: 'slideUp',
    headlineAnimation: 'slideUp',
    bodyAnimation: 'fadeWords',
    stepNumbers: true,
    progressBar: true,
    logoPlacement: 'top-left',
    logoOpacity: 0.7,
  },
};
```

---

## social-native

**Best for:** TikTok, Instagram Reels, YouTube Shorts — vertical, fast, trendy

**Visual character:** Bold text, fast cuts, high energy, trending motion patterns.

```typescript
const socialNative = {
  theme: 'dark',
  colors: {
    primary: '#ff0050',
    secondary: '#00f2ea',
    accent: '#fffc00',
    background: '#000000',
    text: '#ffffff',
    textSecondary: '#e0e0e0',
  },
  fonts: {
    primary: { name: 'Plus Jakarta Sans', weight: 800 },
    secondary: { name: 'Plus Jakarta Sans', weight: 500 },
  },
  fontSizes: {
    heading: 96,
    subheading: 56,
    body: 40,
  },
  motion: {
    intensity: 'extreme',
    springConfig: { mass: 0.8, stiffness: 250, damping: 10 },
    staggerDelay: 3,
    transitionType: 'mixed',
    transitionDuration: 0.25,
  },
  effects: {
    filmGrain: null,
    vignette: null,
    colorGrade: 'vivid',
  },
  defaults: {
    enterAnimation: 'bounce',
    headlineAnimation: 'splitChars',
    bodyAnimation: 'slideUp',
    logoPlacement: 'none',
    canvas: { width: 1080, height: 1920 },
  },
};
```

---

## event-promo

**Best for:** Conferences, webinars, meetups, launches with date/location info

**Visual character:** Countdown energy, date reveals, venue imagery, urgency.

```typescript
const eventPromo = {
  theme: 'dark',
  colors: {
    primary: '#6366f1',
    secondary: '#8b5cf6',
    accent: '#fbbf24',
    background: '#18181b',
    text: '#ffffff',
    textSecondary: '#d4d4d8',
  },
  fonts: {
    primary: { name: 'Outfit', weight: 700 },
    secondary: { name: 'Outfit', weight: 400 },
  },
  motion: {
    intensity: 'dramatic',
    springConfig: { mass: 1, stiffness: 160, damping: 16 },
    staggerDelay: 6,
    transitionType: 'clockWipe',
    transitionDuration: 0.5,
  },
  effects: {
    filmGrain: null,
    vignette: { intensity: 0.2, color: '#000000' },
    colorGrade: null,
  },
  defaults: {
    enterAnimation: 'slideUp',
    headlineAnimation: 'scale',
    counterEnabled: true,
    dateReveal: true,
    logoPlacement: 'top-left',
    logoOpacity: 0.8,
  },
};
```
