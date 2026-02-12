---
name: remotion-video-producer
description: >
  End-to-end video production skill that interviews users, collects brand assets, composes scenes,
  and generates complete Remotion projects — no video editing experience required. Use this skill
  whenever the user wants to create a video, motion graphics, animated explainer, product demo,
  social media clip, presentation video, promotional video, or any programmatic video content.
  Also trigger when users mention Remotion, video from code, animated content, video templates,
  or video generation. This skill handles the ENTIRE pipeline: creative interview → scene composition
  → Remotion code generation → quality review. Even if the user only says "make me a video" or
  "I need a promo clip," this skill guides them through every decision they need to make.
---

# Remotion Video Producer

A multi-agent skill that turns a plain-English video idea into a production-ready Remotion project.
The user does NOT need video editing experience, Remotion knowledge, or React expertise. This skill
conducts a structured creative interview, composes scenes with frame-level timing, generates
TypeScript/React code, and validates everything before delivery.

## Quick Start

When this skill triggers, follow this sequence:

1. **Read the interview agent** → `agents/interviewer.md`
2. Conduct the interview (Phases 1-4, progressive disclosure)
3. **Read the scene composer agent** → `agents/scene-composer.md`
4. Compose the scene graph from the collected spec
5. **Read the code generator agent** → `agents/code-generator.md`
6. Generate the full Remotion project
7. **Read the QC reviewer agent** → `agents/qc-reviewer.md`
8. Validate everything; loop back to step 5 if issues found

If subagents are available, Phase 5+6 and Phase 7 can run in parallel where independent.

---

## Architecture

```
User → Interviewer → Scene Composer → Code Generator → QC Reviewer → Delivered Project
                                            ↑                |
                                            └── fix loop ────┘
```

### Agent Roles

| Agent | File | Responsibility |
|-------|------|----------------|
| **Interviewer** | `agents/interviewer.md` | Structured creative interview across 4 phases. Collects the full `VideoSpec`. |
| **Scene Composer** | `agents/scene-composer.md` | Translates `VideoSpec` into a `SceneGraph` with frame-level timing, transitions, and layout. |
| **Code Generator** | `agents/code-generator.md` | Generates a complete, runnable Remotion project from the `SceneGraph`. |
| **QC Reviewer** | `agents/qc-reviewer.md` | Validates TypeScript compilation, timing math, asset references, design consistency. |

### State Object

The pipeline passes a single state object between agents:

```typescript
interface PipelineState {
  spec: VideoSpec;           // From Interviewer
  sceneGraph: SceneGraph;    // From Scene Composer
  projectFiles: FileMap;     // From Code Generator
  qcResult: QCResult;        // From QC Reviewer
  iteration: number;         // Fix loop counter (max 3)
}
```

Schemas for `VideoSpec`, `SceneGraph`, and `QCResult` are in `references/schemas.md`.

---

## Interview Strategy: Progressive Disclosure

The Interviewer does NOT dump 80+ parameters on the user. It uses tiered questioning:

| Tier | When Asked | Examples |
|------|-----------|----------|
| **Tier 1 — Always** | Every video | Purpose, platform, duration, brand colors, logo, content outline |
| **Tier 2 — Contextual** | When relevant based on Tier 1 answers | Typography, motion intensity, audio, specific scene types |
| **Tier 3 — Smart Defaults** | Confirm only | FPS, codec, easing curves, spring configs, CRF quality |
| **Tier 4 — Expert Override** | Only if user signals expertise | Raw Remotion config, custom easing functions, pixel format, Lambda rendering |

The interviewer infers as much as possible. If the user says "LinkedIn ad," it automatically sets
1920×1080, 30fps, 30-60 second duration, corporate-minimal template. The user confirms or overrides.

---

## Key References

Read these as needed during each phase:

| Reference | Path | When to Read |
|-----------|------|-------------|
| **Full Parameter Catalog** | `references/parameter-catalog.md` | During interview — know every possible parameter |
| **Remotion API Reference** | `references/remotion-api.md` | During code generation — correct Remotion patterns |
| **Scene Type Library** | `references/scene-types.md` | During scene composition — available layouts and scene patterns |
| **Template Presets** | `references/templates.md` | During interview — when user picks a style |
| **Data Schemas** | `references/schemas.md` | When constructing or validating `VideoSpec` / `SceneGraph` |

---

## Orchestrator Responsibilities

1. **Guide the user conversationally.** Never present a wall of questions. Group logically, suggest
   smart defaults, and confirm. The user should feel like they're talking to a creative director,
   not filling out a form.

2. **Validate assets early.** When the user provides a logo, check format and dimensions immediately.
   When they mention a font, verify it exists on Google Fonts or ask for the file. Don't wait until
   code generation to discover problems.

3. **Show progress.** After each phase, give the user a summary of what was collected/decided and
   what comes next. For the scene graph, present a visual timeline before generating code.

4. **Handle the QC loop.** If the QC reviewer finds issues, fix them automatically (up to 3
   iterations). Only escalate to the user if the fix requires a creative decision.

5. **Deliver cleanly.** The final output is a complete Remotion project directory the user can
   `npm install && npm start` to preview. Include a README with render instructions.

---

## Platform-Aware Defaults

When the user specifies a platform, auto-set these defaults (user can override):

| Platform | Resolution | Aspect | Duration | FPS | Template Suggestion |
|----------|-----------|--------|----------|-----|-------------------|
| YouTube | 1920×1080 | 16:9 | 60-120s | 30 | cinematic, explainer |
| Instagram Reels | 1080×1920 | 9:16 | 15-60s | 30 | social-native, bold-impact |
| TikTok | 1080×1920 | 9:16 | 15-60s | 30 | social-native |
| LinkedIn | 1920×1080 | 16:9 | 30-90s | 30 | corporate-minimal, data-driven |
| Twitter/X | 1920×1080 | 16:9 | 15-60s | 30 | bold-impact |
| Instagram Story | 1080×1920 | 9:16 | 5-15s | 30 | social-native |
| Instagram Post | 1080×1080 | 1:1 | 3-60s | 30 | bold-impact |
| Presentation | 1920×1080 | 16:9 | varies | 30 | corporate-minimal |
| GIF/Loop | 800×600 | 4:3 | 2-5s | 15 | bold-impact |

---

## Error Handling

| Error | Resolution |
|-------|-----------|
| User provides JPG logo (no transparency) | Ask for SVG or PNG with transparency; explain why |
| Font not found on Google Fonts | Suggest 3 similar alternatives from the same category |
| Duration too short for scene count | Suggest reducing scenes or increasing duration; show math |
| Asset URL unreachable | Flag immediately, ask for alternative or local file |
| QC fails after 3 iterations | Present the issues to the user with specific fix suggestions |
| User wants features Remotion doesn't support | Explain limitation, suggest workaround or alternative approach |

---

## Output Structure

The final delivered project looks like this:

```
my-video/
├── README.md                    # How to preview and render
├── package.json                 # Dependencies with exact versions
├── tsconfig.json                # TypeScript config
├── remotion.config.ts           # Remotion render settings
├── src/
│   ├── index.ts                 # Entry point (registerRoot)
│   ├── Root.tsx                 # Composition definitions
│   ├── Video.tsx                # Main video component
│   ├── types.ts                 # TypeScript interfaces for props
│   ├── theme.ts                 # Colors, fonts, spacing constants
│   ├── scenes/
│   │   ├── Intro.tsx
│   │   ├── ContentScene.tsx
│   │   ├── DataViz.tsx
│   │   ├── CTA.tsx
│   │   └── Outro.tsx
│   ├── components/
│   │   ├── AnimatedText.tsx
│   │   ├── Logo.tsx
│   │   ├── Background.tsx
│   │   └── ProgressBar.tsx
│   └── lib/
│       ├── animations.ts        # Reusable animation helpers
│       └── timing.ts            # Frame calculation utilities
├── public/
│   ├── logo.svg
│   ├── fonts/
│   └── images/
└── video-spec.json              # The full VideoSpec for reproducibility
```

---

## Licensing Note

Remotion requires a company license for organizations with more than 3 employees.
See https://www.remotion.dev/license for details. This skill generates code — the user
is responsible for Remotion licensing compliance.
