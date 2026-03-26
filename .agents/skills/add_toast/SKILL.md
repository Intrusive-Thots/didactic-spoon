---
name: Add Toast Notification
description: Show a toast notification from anywhere in the application
---

# Add Toast Notification

## Usage

```python
from ui.components.toast import ToastManager

ToastManager.get_instance().show(
    "Your message here",
    icon="✅",           # emoji icon
    duration=3000,       # ms before auto-dismiss
    theme="success",     # "success", "error", "info"
    confetti=True        # optional celebration particles
)
```

## Available Themes
| Theme | Color | Use Case |
|-------|-------|----------|
| `success` | Green | Completed actions |
| `error` | Red | Failures, warnings |
| `info` | Blue | Neutral information |

## Thread Safety
Toasts must be called from the **main thread**. If calling from a background thread, wrap in `self.after(0, ...)`:
```python
self.after(0, lambda: ToastManager.get_instance().show("Done!", icon="🎉", theme="success"))
```

## Notes
- `ToastManager` is a singleton, initialized in `core/main.py` during app startup.
- Calling `get_instance()` before initialization will raise an error.
- The `confetti=True` option adds animated particles — use sparingly for special moments.
