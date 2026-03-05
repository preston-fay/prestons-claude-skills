#!/usr/bin/env python3
"""
Google Fonts lookup helper for font validation and suggestions.
Usage: python3 fonts.py <font-name>
       python3 fonts.py --suggest <category>

Maps font names to @remotion/google-fonts import paths.
"""

import sys
import re

# Curated list of high-quality Google Fonts organized by category.
# This is NOT exhaustive — it's the fonts most likely to be requested
# and that work well in video contexts (readable at scale, distinctive).

FONT_DATABASE = {
    # Sans-serif — Modern, clean
    "Inter": {"category": "sans-serif", "weights": [100,200,300,400,500,600,700,800,900], "import": "Inter"},
    "DM Sans": {"category": "sans-serif", "weights": [400,500,700], "import": "DMSans"},
    "Montserrat": {"category": "sans-serif", "weights": [100,200,300,400,500,600,700,800,900], "import": "Montserrat"},
    "Open Sans": {"category": "sans-serif", "weights": [300,400,500,600,700,800], "import": "OpenSans"},
    "Poppins": {"category": "sans-serif", "weights": [100,200,300,400,500,600,700,800,900], "import": "Poppins"},
    "Nunito": {"category": "sans-serif", "weights": [200,300,400,500,600,700,800,900], "import": "Nunito"},
    "Outfit": {"category": "sans-serif", "weights": [100,200,300,400,500,600,700,800,900], "import": "Outfit"},
    "Space Grotesk": {"category": "sans-serif", "weights": [300,400,500,600,700], "import": "SpaceGrotesk"},
    "Plus Jakarta Sans": {"category": "sans-serif", "weights": [200,300,400,500,600,700,800], "import": "PlusJakartaSans"},
    "IBM Plex Sans": {"category": "sans-serif", "weights": [100,200,300,400,500,600,700], "import": "IBMPlexSans"},
    "Manrope": {"category": "sans-serif", "weights": [200,300,400,500,600,700,800], "import": "Manrope"},
    "Sora": {"category": "sans-serif", "weights": [100,200,300,400,500,600,700,800], "import": "Sora"},
    "Albert Sans": {"category": "sans-serif", "weights": [100,200,300,400,500,600,700,800,900], "import": "AlbertSans"},
    "General Sans": {"category": "sans-serif", "weights": [200,300,400,500,600,700], "import": "GeneralSans"},
    "Figtree": {"category": "sans-serif", "weights": [300,400,500,600,700,800,900], "import": "Figtree"},
    "Geist": {"category": "sans-serif", "weights": [100,200,300,400,500,600,700,800,900], "import": "Geist"},

    # Serif — Elegant, editorial
    "Playfair Display": {"category": "serif", "weights": [400,500,600,700,800,900], "import": "PlayfairDisplay"},
    "Lora": {"category": "serif", "weights": [400,500,600,700], "import": "Lora"},
    "Merriweather": {"category": "serif", "weights": [300,400,700,900], "import": "Merriweather"},
    "Source Serif 4": {"category": "serif", "weights": [200,300,400,500,600,700,800,900], "import": "SourceSerif4"},
    "Fraunces": {"category": "serif", "weights": [100,200,300,400,500,600,700,800,900], "import": "Fraunces"},
    "DM Serif Display": {"category": "serif", "weights": [400], "import": "DMSerifDisplay"},
    "Newsreader": {"category": "serif", "weights": [200,300,400,500,600,700,800], "import": "Newsreader"},
    "Instrument Serif": {"category": "serif", "weights": [400], "import": "InstrumentSerif"},

    # Display — Headlines, large text
    "Bebas Neue": {"category": "display", "weights": [400], "import": "BebasNeue"},
    "Righteous": {"category": "display", "weights": [400], "import": "Righteous"},
    "Fredoka": {"category": "display", "weights": [300,400,500,600,700], "import": "Fredoka"},
    "Archivo Black": {"category": "display", "weights": [400], "import": "ArchivoBlack"},
    "Anton": {"category": "display", "weights": [400], "import": "Anton"},
    "Oswald": {"category": "display", "weights": [200,300,400,500,600,700], "import": "Oswald"},
    "Abril Fatface": {"category": "display", "weights": [400], "import": "AbrilFatface"},

    # Monospace — Code, data, counters
    "JetBrains Mono": {"category": "monospace", "weights": [100,200,300,400,500,600,700,800], "import": "JetBrainsMono"},
    "Fira Code": {"category": "monospace", "weights": [300,400,500,600,700], "import": "FiraCode"},
    "IBM Plex Mono": {"category": "monospace", "weights": [100,200,300,400,500,600,700], "import": "IBMPlexMono"},
    "Source Code Pro": {"category": "monospace", "weights": [200,300,400,500,600,700,800,900], "import": "SourceCodePro"},
    "Space Mono": {"category": "monospace", "weights": [400,700], "import": "SpaceMono"},
    "Geist Mono": {"category": "monospace", "weights": [100,200,300,400,500,600,700,800,900], "import": "GeistMono"},

    # Handwriting — Casual, personal
    "Caveat": {"category": "handwriting", "weights": [400,500,600,700], "import": "Caveat"},
    "Dancing Script": {"category": "handwriting", "weights": [400,500,600,700], "import": "DancingScript"},
    "Pacifico": {"category": "handwriting", "weights": [400], "import": "Pacifico"},
}


def lookup_font(name: str) -> dict | None:
    """Look up a font by name (case-insensitive)."""
    name_lower = name.lower().strip()
    for font_name, info in FONT_DATABASE.items():
        if font_name.lower() == name_lower:
            return {"name": font_name, **info}
    return None


def suggest_fonts(category: str, count: int = 5) -> list:
    """Suggest fonts in a given category."""
    results = []
    for font_name, info in FONT_DATABASE.items():
        if info["category"] == category:
            results.append({"name": font_name, **info})
    return results[:count]


def get_import_statement(font_name: str) -> str | None:
    """Get the @remotion/google-fonts import statement."""
    info = lookup_font(font_name)
    if not info:
        return None
    return f"import {{loadFont}} from '@remotion/google-fonts/{info['import']}';"


def find_similar(name: str, count: int = 3) -> list:
    """Find fonts with similar names (fuzzy match)."""
    name_lower = name.lower()
    scored = []
    for font_name in FONT_DATABASE:
        # Simple substring/prefix matching
        font_lower = font_name.lower()
        if name_lower in font_lower or font_lower in name_lower:
            scored.append((font_name, 2))
        elif any(word in font_lower for word in name_lower.split()):
            scored.append((font_name, 1))

    scored.sort(key=lambda x: -x[1])
    return [s[0] for s in scored[:count]]


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 fonts.py <font-name>          # Look up a font")
        print("  python3 fonts.py --suggest <category>  # sans-serif, serif, display, monospace, handwriting")
        print("  python3 fonts.py --import <font-name>  # Get import statement")
        sys.exit(0)

    if sys.argv[1] == "--suggest":
        category = sys.argv[2] if len(sys.argv) > 2 else "sans-serif"
        fonts = suggest_fonts(category)
        print(f"\nSuggested {category} fonts:")
        for f in fonts:
            weights = ", ".join(str(w) for w in f["weights"])
            print(f"  {f['name']} — weights: {weights}")
            print(f"    import: @remotion/google-fonts/{f['import']}")
        return

    if sys.argv[1] == "--import":
        name = " ".join(sys.argv[2:])
        stmt = get_import_statement(name)
        if stmt:
            print(stmt)
        else:
            print(f"Font not found: {name}")
            similar = find_similar(name)
            if similar:
                print(f"Did you mean: {', '.join(similar)}?")
        return

    # Default: look up font
    name = " ".join(sys.argv[1:])
    info = lookup_font(name)
    if info:
        weights = ", ".join(str(w) for w in info["weights"])
        print(f"\n{info['name']}")
        print(f"  Category: {info['category']}")
        print(f"  Weights: {weights}")
        print(f"  Import: @remotion/google-fonts/{info['import']}")
        print(f"  Statement: import {{loadFont}} from '@remotion/google-fonts/{info['import']}';")
    else:
        print(f"Font not found in database: {name}")
        similar = find_similar(name)
        if similar:
            print(f"Similar fonts: {', '.join(similar)}")
        print("\nThis doesn't mean it's not on Google Fonts — it just means it's not in our curated list.")
        print("Check https://fonts.google.com for the full catalog.")


if __name__ == "__main__":
    main()
