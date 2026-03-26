---
name: Update Design Tokens
description: Modify the UI design token system (colors, fonts, radii)
---

# Update Design Tokens

## Token Location
All design tokens are in `ui/components/factory.py` inside the `TOKENS` dictionary.

## Token Structure
```python
TOKENS = {
    "colors": {
        "background": {
            "app": "#0A1428",
            "card": "#0F1A24",
        },
        "text": {
            "primary": "#F0E6D2",
            "muted": "#6C757D",
            "disabled": "#3C4A5C",
        },
        "accent": {
            "primary": "#0ac8b9",
            "gold": "#C8AA6E",
        },
        "border": {
            "subtle": "#1E2328",
        },
        "state": {
            "hover": "#1a2733",
            "success": "#00C853",
        }
    },
    "font": { ... },
    "radius": { ... }
}
```

## Helper Functions
- `get_color("colors.text.primary")` → resolves dot-path to hex value
- `get_font("body", "bold")` → returns font tuple
- `get_radius("sm")` → returns corner radius int

## Bolt Performance Notes
- `get_color()` and `get_font()` use `@functools.lru_cache` for performance.
- After changing tokens, clear the cache or restart the app.
- Never call these helpers inside tight loops or event handlers — precompute to local variables.
