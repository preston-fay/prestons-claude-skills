# KDS Color Violation Quick Reference

Common off-brand colors found in reviews, and what they should be replaced with.

## Wrong Purples

| Found | Source | Replace With |
|-------|--------|-------------|
| `#6f42c1` | Bootstrap purple | `#7823DC` |
| `#8B5CF6` | Tailwind violet-500 | `#7823DC` |
| `#7C3AED` | Tailwind violet-600 | `#7823DC` |
| `#6D28D9` | Tailwind violet-700 | `#7823DC` |
| `#A855F7` | Tailwind purple-500 | `#9150E1` or `#AF7DEB` |
| `#9333EA` | Tailwind purple-600 | `#9150E1` |
| `#6366F1` | Tailwind indigo-500 | `#7823DC` |
| `purple` | CSS named color | `#7823DC` |
| `rgb(128, 0, 128)` | CSS named purple | `#7823DC` |

## Wrong Blacks

| Found | Source | Replace With |
|-------|--------|-------------|
| `#000000` | Pure black | `#1E1E1E` |
| `#000` | Shorthand black | `#1E1E1E` |
| `#111111` | Near black | `#1E1E1E` |
| `#111827` | Tailwind gray-900 | `#1E1E1E` |
| `#0F172A` | Tailwind slate-900 | `#1E1E1E` |
| `black` | CSS named color | `#1E1E1E` |

## Wrong Grays

| Found | Source | Replace With |
|-------|--------|-------------|
| `#6B7280` | Tailwind gray-500 | `#787878` |
| `#9CA3AF` | Tailwind gray-400 | `#A5A5A5` |
| `#D1D5DB` | Tailwind gray-300 | `#D2D2D2` |
| `#E5E7EB` | Tailwind gray-200 | `#E6E6E6` |
| `#F3F4F6` | Tailwind gray-100 | `#F5F5F5` |
| `#F9FAFB` | Tailwind gray-50 | `#FFFFFF` |
| `#374151` | Tailwind gray-700 | `#4B4B4B` |
| `gray` | CSS named color | `#A5A5A5` |

## Wrong Blues (should not appear at all)

| Found | Source | Action |
|-------|--------|--------|
| `#3B82F6` | Tailwind blue-500 | Remove — use KDS chart sequence |
| `#2563EB` | Tailwind blue-600 | Remove — use KDS chart sequence |
| `#0D6EFD` | Bootstrap primary | Remove — use `#7823DC` |
| `#007BFF` | Bootstrap 4 primary | Remove — use `#7823DC` |
| `steelblue` | D3 default | Remove — use KDS chart sequence |

## Correct KDS Palette (for reference)

### Brand Core
| Name | Hex |
|------|-----|
| Kearney Purple | `#7823DC` |
| Kearney Black | `#1E1E1E` |
| Kearney White | `#FFFFFF` |
| Kearney Gray | `#A5A5A5` |

### Chart Sequence (1-10)
| # | Hex | Description |
|---|-----|-------------|
| 1 | `#D2D2D2` | Light gray |
| 2 | `#A5A6A5` | Medium gray |
| 3 | `#787878` | Dark gray |
| 4 | `#E0D2FA` | Light purple |
| 5 | `#C8A5F0` | Soft purple |
| 6 | `#AF7DEB` | Medium purple |
| 7 | `#4B4B4B` | Charcoal |
| 8 | `#1E1E1E` | Black |
| 9 | `#9150E1` | Bright purple |
| 10 | `#7823DC` | Kearney Purple |

### Extended Grays
| Name | Hex |
|------|-----|
| Gray 100 | `#F5F5F5` |
| Gray 200 | `#E6E6E6` |
| Gray 300 | `#B9B9B9` |
| Gray 400 | `#8C8C8C` |
| Gray 500 | `#5F5F5F` |
| Gray 600 | `#323232` |

### Extended Purples
| Name | Hex |
|------|-----|
| Purple 100 | `#D7BEF5` |
| Purple 200 | `#B991EB` |
| Purple 300 | `#A064E6` |
| Purple 400 | `#8737E1` |

### Sequential Map Scale
`#F5F5F5` → `#E6E6E6` → `#D2D2D2` → `#E0D2FA` → `#C8A5F0` → `#AF7DEB` → `#9150E1` → `#7823DC`

## Grep Patterns for Finding Violations

```bash
# Find potential color violations (hex codes not in KDS palette)
rg '#[0-9a-fA-F]{3,8}' --type html --type css --type tsx --type jsx

# Find gridlines (top KDS violation)
rg -i '(showgrid|grid.*true|axes\.grid|gridline)' --type py --type tsx --type jsx

# Find wrong font stacks
rg -i '(font-family|fontFamily)' --type css --type tsx --type jsx

# Find emoji/emoticon usage (forbidden)
rg '[\x{1F600}-\x{1F64F}\x{1F300}-\x{1F5FF}\x{1F680}-\x{1F6FF}]'
```
