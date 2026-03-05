# KDS Type Scale Quick Reference

## Major Third Scale (1.25 ratio)

All font sizes must come from this 9-level scale. No exceptions.

| Level | Font Size | Line Height | Token | Weight Range | Common Usage |
|-------|-----------|-------------|-------|--------------|--------------|
| 0 | 8px | 12px | `--type-display-sm` | 400-500 | Rare; micro labels (not for body text) |
| 1 | 10px | 12px | `--type-caption` | 400-500 | Captions, footnotes, fine print |
| 2 | 13px | 16px | `--type-small` | 400-600 | Small text, secondary content, labels |
| 3 | 16px | 24px | `--type-body` | 400-600 | **Body text (base)**, paragraphs, default |
| 4 | 20px | 32px | `--type-lead` | 400-600 | Lead paragraphs, emphasized body |
| 5 | 25px | 32px | `--type-h3` | 500-700 | H3 headings, section titles |
| 6 | 31px | 40px | `--type-h2` | 600-700 | H2 headings, page subsections |
| 7 | 39px | 48px | `--type-h1` | 600-700 | H1 headings, page titles |
| 8 | 49px | 64px | `--type-display` | 700 | Display headings, hero text, KPIs |

## Derivation Formula

```
fontSize(level) = 16 × 1.25^(level - 3)

lineHeight(level) = fontSize(level) × lineHeightMultiplier
  where lineHeightMultiplier = level ≥ 3 ? 1.5 : 1.25
  
lineHeight rounded to nearest 4px
```

## Font Weights

Valid weights: **400, 500, 600, 700**

Mapping:
- 400 = Regular (body text, captions)
- 500 = Medium (emphasis, subheadings)
- 600 = Semi-bold (headings, important content)
- 700 = Bold (major headings, KPIs, high emphasis)

## Hierarchy Rules

1. **Parent must be strictly larger than child** (no inversions)
   - Invalid: H3 (25px) followed by child at 25px or larger
   - Valid: H3 (25px) followed by body (16px)

2. **Hierarchy expressed through scale and weight only**
   - Never use color alone to indicate hierarchy
   - Combine size + weight for maximum clarity

3. **Monotonic descending order**
   - Primary content → largest size/weight
   - Secondary content → medium size/weight
   - Tertiary content → smallest size/weight

## Usage in CSS

Always reference via CSS custom properties:

```css
/* Correct */
h1 {
  font-size: var(--type-h1);
  line-height: 48px;
  font-weight: 700;
}

.body {
  font-size: var(--type-body);
  line-height: 24px;
  font-weight: 400;
}

/* WRONG - raw pixel values */
h1 {
  font-size: 39px;
  line-height: 1.2;
}
```

## Line Height Details

| Level | Font Size | Raw LH Calculation | Rounded Line Height |
|-------|-----------|-------------------|---------------------|
| 0 | 8px | 8 × 1.25 = 10px | 12px (↑ to 4px multiple) |
| 1 | 10px | 10 × 1.25 = 12.5px | 12px (↓ to 4px multiple) |
| 2 | 13px | 13 × 1.25 = 16.25px | 16px (↓ to 4px multiple) |
| 3 | 16px | 16 × 1.5 = 24px | 24px (exact) |
| 4 | 20px | 20 × 1.5 = 30px | 32px (↑ to 4px multiple) |
| 5 | 25px | 25 × 1.5 = 37.5px | 40px (↑ to 4px multiple) |
| 6 | 31px | 31 × 1.5 = 46.5px | 48px (↑ to 4px multiple) |
| 7 | 39px | 39 × 1.5 = 58.5px | 60px (↑ to 4px multiple) |
| 8 | 49px | 49 × 1.5 = 73.5px | 76px (↑ to 4px multiple) |

**Note:** Line heights ≥ level 3 use 1.5× multiplier for readability. Levels 0-2 use 1.25× for tighter spacing.

## Font Family

**Primary:** Inter (KDS standard)
**Fallback:** `Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`

## Validation

Any font size not on the scale is invalid and must be rejected.

**Detection:** `!VALID_FONT_SIZES.has(fontSize)`

**Correction:** Use `deriveFontSize(level)` to compute the correct size for a given level.

## Contrast Requirements

- Body text (level 0-3): contrast ratio ≥ 4.5:1
- Large text (level 4-8): contrast ratio ≥ 3.0:1
- Bold text ≥14pt: also qualifies as "large text" (≥ 3.0:1)

## Source

`~/Projects/kds-design/src/constants.ts` — `TYPE_SCALE_ENTRIES`, `TYPE_TOKEN_MAP`, `TYPE_SCALE_SIZES`, `TYPE_SCALE_LINE_HEIGHTS`
