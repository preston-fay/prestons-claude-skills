# KDS Spacing Scale Quick Reference

## The 11-Value Scale

All spacing in KDS must come from this scale. No exceptions.

| Value | Token | Base Unit Multiple | Common Usage |
|-------|-------|---------------------|--------------|
| 0px | `--space-0` | 0 | No spacing, flush layouts |
| 4px | `--space-1` | 0.5 (half unit) | Fine control, icon spacing, compact padding |
| 8px | `--space-2` | 1 | Tight spacing, button padding, small gaps |
| 16px | `--space-4` | 2 | Component padding, stack gap, form field spacing |
| 24px | `--space-6` | 3 | Baseline rhythm, section margins, card padding |
| 32px | `--space-8` | 4 | Section gaps, large component padding |
| 40px | `--space-10` | 5 | Large vertical rhythm, between major sections |
| 48px | `--space-12` | 6 | Major section gaps, hero padding |
| 64px | `--space-16` | 8 | Page-level margins (desktop), very large gaps |
| 80px | `--space-20` | 10 | Rare; extra large spacing |
| 96px | `--space-24` | 12 | Rare; maximum spacing value |

## Grid Margins by Breakpoint

| Breakpoint | Margin | Token |
|------------|--------|-------|
| Mobile (≤767px) | 16px | `--space-4` |
| Tablet (768-1199px) | 32px | `--space-8` |
| Desktop (≥1200px) | 64px | `--space-16` |

## Derivation Formula

```
spacing = BASE_UNIT × multiplier
where BASE_UNIT = 8px
      multiplier ∈ {0, 0.5, 1, 2, 3, 4, 5, 6, 8, 10, 12}
```

## Usage in CSS

Always reference via CSS custom properties:

```css
/* Correct */
.component {
  padding: var(--space-6);
  margin-bottom: var(--space-4);
  gap: var(--space-2);
}

/* WRONG - raw pixel values */
.component {
  padding: 24px;
  margin-bottom: 16px;
  gap: 8px;
}
```

## Validation

Any spacing value that does not appear in the scale is invalid and must be rejected or rounded to the nearest valid value.

**Detection:** `value % 4 !== 0` OR `!SPACING_SCALE_SET.has(value)`

**Correction:** Use `nearestSpacingValue(input)` to snap to the closest valid value.

## Source

`~/Projects/kds-design/src/constants.ts` — `SPACING_SCALE`, `SPACING_TOKEN_MAP`
