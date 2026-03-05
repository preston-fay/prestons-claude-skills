#!/usr/bin/env python3
"""
Calculate and verify timing for a Remotion video.
Usage: python3 timing.py <video-spec.json>

Reads a VideoSpec JSON and:
1. Calculates total frames from duration × fps
2. Distributes frames across scenes
3. Accounts for transition overlaps
4. Validates that everything adds up
5. Outputs a human-readable timeline

Can also be used standalone:
  python3 timing.py --duration 45 --fps 30 --scenes 6 --transition-duration 0.5
"""

import sys
import json
import argparse
from typing import List, Optional


def frames_from_seconds(seconds: float, fps: int) -> int:
    return round(seconds * fps)


def seconds_from_frames(frames: int, fps: int) -> float:
    return round(frames / fps, 2)


def distribute_frames(
    total_frames: int,
    scene_count: int,
    scene_weights: Optional[List[float]] = None,
    transition_frames: int = 0,
) -> List[int]:
    """
    Distribute total frames across scenes, accounting for transition overlaps.
    
    total_effective = sum(scene_durations) - (scene_count - 1) * transition_frames
    So: sum(scene_durations) = total_effective + (scene_count - 1) * transition_frames
    """
    num_transitions = scene_count - 1
    total_transition_overlap = num_transitions * transition_frames
    available_for_scenes = total_frames + total_transition_overlap

    if scene_weights is None:
        scene_weights = [1.0] * scene_count

    # Normalize weights
    total_weight = sum(scene_weights)
    normalized = [w / total_weight for w in scene_weights]

    # Distribute
    raw_frames = [available_for_scenes * w for w in normalized]
    scene_frames = [round(f) for f in raw_frames]

    # Adjust rounding error on the largest scene
    actual_sum = sum(scene_frames)
    diff = available_for_scenes - actual_sum
    if diff != 0:
        largest_idx = scene_frames.index(max(scene_frames))
        scene_frames[largest_idx] += diff

    return scene_frames


def validate_timing(
    total_frames: int,
    scene_frames: List[int],
    transition_frames: int,
    fps: int,
) -> dict:
    """Validate that timing math is consistent."""
    num_transitions = len(scene_frames) - 1
    total_transition_overlap = num_transitions * transition_frames
    effective_duration = sum(scene_frames) - total_transition_overlap

    return {
        "total_frames_expected": total_frames,
        "total_frames_effective": effective_duration,
        "match": effective_duration == total_frames,
        "scene_frames_sum": sum(scene_frames),
        "transition_overlap_total": total_transition_overlap,
        "num_scenes": len(scene_frames),
        "num_transitions": num_transitions,
        "per_scene": [
            {
                "index": i,
                "frames": f,
                "seconds": seconds_from_frames(f, fps),
            }
            for i, f in enumerate(scene_frames)
        ],
    }


def print_timeline(
    scene_frames: List[int],
    scene_names: List[str],
    transition_frames: int,
    fps: int,
):
    """Print a human-readable timeline."""
    print("\n" + "=" * 60)
    print("VIDEO TIMELINE")
    print("=" * 60)

    current_time = 0.0
    for i, (frames, name) in enumerate(zip(scene_frames, scene_names)):
        duration_s = seconds_from_frames(frames, fps)
        end_time = current_time + duration_s

        # Account for transition overlap on the end
        if i < len(scene_frames) - 1:
            overlap_s = seconds_from_frames(transition_frames, fps)
            effective_end = end_time - overlap_s
        else:
            effective_end = end_time
            overlap_s = 0

        print(f"\n[{current_time:.1f}s — {effective_end:.1f}s] Scene {i + 1}: {name}")
        print(f"  Duration: {frames} frames ({duration_s}s)")

        if i < len(scene_frames) - 1:
            trans_s = seconds_from_frames(transition_frames, fps)
            print(f"  ──── transition ({transition_frames}f / {trans_s}s) ────")
            current_time = effective_end
        else:
            current_time = end_time

    total_s = seconds_from_frames(
        sum(scene_frames) - (len(scene_frames) - 1) * transition_frames, fps
    )
    print(f"\n{'─' * 60}")
    print(f"Total: {total_s}s ({frames_from_seconds(total_s, fps)} frames @ {fps}fps)")
    print("─" * 60 + "\n")


def from_spec(spec_path: str):
    """Calculate timing from a VideoSpec JSON file."""
    with open(spec_path) as f:
        spec = json.load(f)

    canvas = spec["canvas"]
    fps = canvas["fps"]
    total_frames = canvas["durationInFrames"]

    scenes = spec["scenes"]
    scene_count = len(scenes)

    motion = spec["motion"]
    transition_duration_s = motion["transitionDuration"]
    transition_frames = frames_from_seconds(transition_duration_s, fps)

    # Extract scene durations if specified, otherwise distribute evenly
    scene_weights = []
    scene_names = []
    for scene in scenes:
        scene_names.append(f"{scene.get('type', 'scene')} — {scene.get('headline', '')[:30]}")
        duration = scene.get("duration", None)
        if duration:
            scene_weights.append(duration)
        else:
            scene_weights.append(1.0)

    scene_frames = distribute_frames(total_frames, scene_count, scene_weights, transition_frames)

    validation = validate_timing(total_frames, scene_frames, transition_frames, fps)
    print_timeline(scene_frames, scene_names, transition_frames, fps)

    print("\nValidation:")
    print(json.dumps(validation, indent=2))

    if not validation["match"]:
        print(f"\n*** TIMING MISMATCH: expected {total_frames}, got {validation['total_frames_effective']} ***")
        return 1

    # Output the scene frames for use by the code generator
    output = {
        "fps": fps,
        "totalFrames": total_frames,
        "transitionFrames": transition_frames,
        "scenes": [
            {
                "id": scenes[i].get("id", f"scene-{i+1}"),
                "durationInFrames": scene_frames[i],
            }
            for i in range(scene_count)
        ],
    }

    output_path = spec_path.replace(".json", "-timing.json")
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nTiming output saved to: {output_path}")

    return 0


def from_args():
    """Calculate timing from command-line arguments."""
    parser = argparse.ArgumentParser(description="Calculate Remotion video timing")
    parser.add_argument("spec", nargs="?", help="Path to video-spec.json")
    parser.add_argument("--duration", type=float, help="Video duration in seconds")
    parser.add_argument("--fps", type=int, default=30, help="Frames per second")
    parser.add_argument("--scenes", type=int, help="Number of scenes")
    parser.add_argument("--transition-duration", type=float, default=0.5, help="Transition duration in seconds")
    parser.add_argument("--weights", type=str, help="Comma-separated scene weights (e.g., 1,2,3,1)")

    args = parser.parse_args()

    if args.spec:
        return from_spec(args.spec)

    if not args.duration or not args.scenes:
        parser.error("Either provide a spec file or --duration and --scenes")

    fps = args.fps
    total_frames = frames_from_seconds(args.duration, fps)
    transition_frames = frames_from_seconds(args.transition_duration, fps)

    weights = None
    if args.weights:
        weights = [float(w) for w in args.weights.split(",")]
        if len(weights) != args.scenes:
            parser.error(f"Weights count ({len(weights)}) must match scene count ({args.scenes})")

    scene_frames = distribute_frames(total_frames, args.scenes, weights, transition_frames)
    scene_names = [f"Scene {i + 1}" for i in range(args.scenes)]

    validation = validate_timing(total_frames, scene_frames, transition_frames, fps)
    print_timeline(scene_frames, scene_names, transition_frames, fps)

    print("\nValidation:")
    print(json.dumps(validation, indent=2))

    return 0 if validation["match"] else 1


if __name__ == "__main__":
    sys.exit(from_args())
