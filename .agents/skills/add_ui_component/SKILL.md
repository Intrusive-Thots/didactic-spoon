---
name: Add UI Component
description: Create a new reusable customtkinter UI component following project conventions
---

# Add UI Component

## File Location
New components go in: `ui/components/<component_name>.py`

## Project Conventions

1. **Imports**: Always include:
```python
import customtkinter as ctk
from ui.components.factory import get_color, get_font, get_radius, TOKENS
from ui.ui_shared import CTkTooltip
from core.constants import SPACING_XS, SPACING_SM, SPACING_MD, SPACING_LG
```

2. **Class Structure**: Extend `ctk.CTkFrame`:
```python
class MyComponent(ctk.CTkFrame):
    def __init__(self, master, config, **kw):
        super().__init__(master, fg_color="transparent", corner_radius=8, **kw)
        self.config = config
        self._build_ui()
```

3. **Color Palette**:
   - Background: `get_color("colors.background.app")` → `#0A1428`
   - Card: `get_color("colors.background.card")` → `#0F1A24`
   - Gold Accent: `#C8AA6E`
   - Accent Primary: `get_color("colors.accent.primary")`
   - Text: `get_color("colors.text.primary")` / `.muted` / `.disabled`

4. **Register in __init__.py**: Add the import to `ui/components/__init__.py`.

5. **No unsupported kwargs**: Do NOT pass `cursor="xterm"` or similar to `CTkEntry`/`CTkLabel` — some customtkinter versions crash on these.

## Bolt Performance Rules
- Precompute `get_color()` and `get_font()` outside event handlers.
- Avoid `os.listdir()` inside UI callbacks — precompute to a dict.
