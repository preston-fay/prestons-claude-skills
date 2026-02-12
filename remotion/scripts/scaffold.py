#!/usr/bin/env python3
"""
Scaffold a Remotion project directory from a VideoSpec.
Usage: python3 scaffold.py <output-dir> [--from-spec video-spec.json]

Creates the full directory structure with boilerplate files.
The Code Generator agent then fills in the scene components.
"""

import sys
import os
import json
import argparse
from pathlib import Path


def scaffold_project(
    output_dir: str,
    project_name: str = "my-video",
    width: int = 1920,
    height: int = 1080,
    fps: int = 30,
    duration_frames: int = 900,
    scenes: list = None,
    remotion_version: str = "4.0.0",
):
    """Create the project directory structure with boilerplate files."""

    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)

    # Directories
    (root / "src" / "scenes").mkdir(parents=True, exist_ok=True)
    (root / "src" / "components").mkdir(parents=True, exist_ok=True)
    (root / "src" / "lib").mkdir(parents=True, exist_ok=True)
    (root / "public" / "fonts").mkdir(parents=True, exist_ok=True)
    (root / "public" / "images").mkdir(parents=True, exist_ok=True)
    (root / "public" / "audio").mkdir(parents=True, exist_ok=True)

    # package.json
    pkg = {
        "name": project_name,
        "version": "1.0.0",
        "private": True,
        "scripts": {
            "start": "npx remotion studio",
            "build": "npx remotion render MyVideo",
            "preview": "npx remotion preview",
        },
        "dependencies": {
            "remotion": remotion_version,
            "@remotion/cli": remotion_version,
            "@remotion/media": remotion_version,
            "@remotion/transitions": remotion_version,
            "@remotion/google-fonts": remotion_version,
            "react": "^18.0.0",
            "react-dom": "^18.0.0",
        },
        "devDependencies": {
            "typescript": "^5.0.0",
            "@types/react": "^18.0.0",
        },
    }
    (root / "package.json").write_text(json.dumps(pkg, indent=2))

    # tsconfig.json
    tsconfig = {
        "compilerOptions": {
            "target": "ES2018",
            "module": "commonjs",
            "jsx": "react-jsx",
            "strict": True,
            "esModuleInterop": True,
            "skipLibCheck": True,
            "forceConsistentCasingInFileNames": True,
            "outDir": "./dist",
            "rootDir": "./src",
        },
        "include": ["src"],
    }
    (root / "tsconfig.json").write_text(json.dumps(tsconfig, indent=2))

    # remotion.config.ts
    (root / "remotion.config.ts").write_text(
        """import {Config} from '@remotion/cli/config';

Config.setVideoImageFormat('jpeg');
Config.setOverwriteOutput(true);
"""
    )

    # src/index.ts
    (root / "src" / "index.ts").write_text(
        """import {registerRoot} from 'remotion';
import {Root} from './Root';

registerRoot(Root);
"""
    )

    # src/types.ts (placeholder)
    (root / "src" / "types.ts").write_text(
        """// Video prop types — filled by Code Generator
export interface VideoProps {
  // Add parameterized props here
}
"""
    )

    # src/Root.tsx (placeholder with correct structure)
    (root / "src" / "Root.tsx").write_text(
        f"""import React from 'react';
import {{Composition}} from 'remotion';
import {{Video}} from './Video';

export const Root: React.FC = () => {{
  return (
    <Composition
      id="MyVideo"
      component={{Video}}
      durationInFrames={{{duration_frames}}}
      width={{{width}}}
      height={{{height}}}
      fps={{{fps}}}
      defaultProps={{{{}}}}
    />
  );
}};
"""
    )

    # src/Video.tsx (placeholder)
    (root / "src" / "Video.tsx").write_text(
        """import React from 'react';
import {AbsoluteFill} from 'remotion';

// TODO: Code Generator fills this with TransitionSeries and scene components

export const Video: React.FC = () => {
  return (
    <AbsoluteFill style={{backgroundColor: '#0f0f0f'}}>
      {/* Scenes go here */}
    </AbsoluteFill>
  );
};
"""
    )

    # src/theme.ts (placeholder)
    (root / "src" / "theme.ts").write_text(
        """// Design tokens — filled by Code Generator from VideoSpec

export const colors = {
  primary: '#1a1a2e',
  secondary: '#16213e',
  accent: '#e94560',
  background: '#0f0f0f',
  text: '#ffffff',
  textSecondary: '#cccccc',
} as const;

export const fonts = {
  primary: 'sans-serif',
  secondary: 'sans-serif',
} as const;

export const fontSizes = {
  heading: 72,
  subheading: 48,
  body: 36,
  caption: 24,
  counter: 96,
} as const;

export const spacing = {
  page: 80,
  section: 40,
  element: 20,
} as const;

export const motion = {
  springConfig: {mass: 1, stiffness: 120, damping: 20},
  staggerDelay: 8,
  transitionDuration: 15,
} as const;
"""
    )

    # src/lib/animations.ts
    (root / "src" / "lib" / "animations.ts").write_text(
        """import {interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';

export const useFadeIn = (delay: number = 0, duration: number = 20) => {
  const frame = useCurrentFrame();
  return interpolate(frame - delay, [0, duration], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
};

export const useSlideUp = (delay: number = 0, distance: number = 40) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const progress = spring({
    fps,
    frame: frame - delay,
    config: {damping: 200},
  });
  return {
    opacity: progress,
    transform: `translateY(${interpolate(progress, [0, 1], [distance, 0])}px)`,
  };
};

export const useScaleIn = (delay: number = 0, from: number = 0.8) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const progress = spring({
    fps,
    frame: frame - delay,
    config: {damping: 200},
  });
  return {
    opacity: progress,
    transform: `scale(${interpolate(progress, [0, 1], [from, 1])})`,
  };
};

export const useSlideLeft = (delay: number = 0, distance: number = 60) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const progress = spring({
    fps,
    frame: frame - delay,
    config: {damping: 200},
  });
  return {
    opacity: progress,
    transform: `translateX(${interpolate(progress, [0, 1], [distance, 0])}px)`,
  };
};

export const useSlideRight = (delay: number = 0, distance: number = 60) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const progress = spring({
    fps,
    frame: frame - delay,
    config: {damping: 200},
  });
  return {
    opacity: progress,
    transform: `translateX(${interpolate(progress, [0, 1], [-distance, 0])}px)`,
  };
};

export const useCounter = (
  target: number,
  delay: number = 0,
  duration: number = 45,
  prefix: string = '',
  suffix: string = '',
) => {
  const frame = useCurrentFrame();
  const value = interpolate(frame - delay, [0, duration], [0, target], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  return `${prefix}${Math.round(value).toLocaleString()}${suffix}`;
};

export const useTypewriter = (
  text: string,
  delay: number = 0,
  charsPerFrame: number = 0.5,
) => {
  const frame = useCurrentFrame();
  const charsToShow = Math.floor((frame - delay) * charsPerFrame);
  return text.slice(0, Math.max(0, charsToShow));
};

export const useProgress = (
  delay: number = 0,
  duration: number = 30,
) => {
  const frame = useCurrentFrame();
  return interpolate(frame - delay, [0, duration], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
};
"""
    )

    # Create placeholder scene files if scene list provided
    if scenes:
        for scene in scenes:
            scene_id = scene.get("id", "scene")
            # Convert scene ID to PascalCase component name
            parts = scene_id.replace("-", " ").replace("_", " ").split()
            component_name = "".join(p.capitalize() for p in parts)
            filename = f"{component_name}.tsx"

            (root / "src" / "scenes" / filename).write_text(
                f"""import React from 'react';
import {{AbsoluteFill, useCurrentFrame, useVideoConfig}} from 'remotion';
import {{colors, fonts, fontSizes, spacing}} from '../theme';

export const {component_name}: React.FC = () => {{
  const frame = useCurrentFrame();
  const {{fps}} = useVideoConfig();

  return (
    <AbsoluteFill style={{{{
      backgroundColor: colors.background,
      padding: spacing.page,
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
    }}}}>
      {{/* TODO: Code Generator fills scene content */}}
    </AbsoluteFill>
  );
}};
"""
            )

    # README.md
    (root / "README.md").write_text(
        f"""# {project_name}

Generated by Remotion Video Producer skill.

## Quick Start

```bash
npm install
npm start        # Opens Remotion Studio for live preview
```

## Render to MP4

```bash
npm run build    # Output: out/MyVideo.mp4
```

## Customization

- **Design tokens**: `src/theme.ts` — colors, fonts, spacing
- **Scene content**: `src/scenes/` — one file per scene
- **Animations**: `src/lib/animations.ts` — reusable animation hooks
- **Assets**: `public/` — images, fonts, audio, video

## Specification

The `video-spec.json` file contains the full specification used to generate
this project. Modify it and re-run the skill to regenerate.

## Technical Details

- Resolution: {width}×{height}
- FPS: {fps}
- Duration: {duration_frames} frames ({duration_frames / fps:.1f}s)
- Framework: Remotion + React + TypeScript
"""
    )

    print(f"Project scaffolded at: {root}")
    print(f"  {len(list(root.rglob('*.ts*')))} TypeScript files")
    print(f"  {len(list(root.rglob('*.json')))} JSON files")
    return str(root)


def main():
    parser = argparse.ArgumentParser(description="Scaffold a Remotion project")
    parser.add_argument("output_dir", help="Output directory for the project")
    parser.add_argument("--from-spec", help="Path to video-spec.json to read settings from")
    parser.add_argument("--name", default="my-video", help="Project name")
    parser.add_argument("--width", type=int, default=1920)
    parser.add_argument("--height", type=int, default=1080)
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--duration", type=float, default=30, help="Duration in seconds")

    args = parser.parse_args()

    if args.from_spec:
        with open(args.from_spec) as f:
            spec = json.load(f)
        canvas = spec.get("canvas", {})
        scaffold_project(
            output_dir=args.output_dir,
            project_name=spec.get("projectName", args.name),
            width=canvas.get("width", 1920),
            height=canvas.get("height", 1080),
            fps=canvas.get("fps", 30),
            duration_frames=canvas.get("durationInFrames", 900),
            scenes=spec.get("scenes", []),
        )
    else:
        scaffold_project(
            output_dir=args.output_dir,
            project_name=args.name,
            width=args.width,
            height=args.height,
            fps=args.fps,
            duration_frames=round(args.duration * args.fps),
        )


if __name__ == "__main__":
    main()
