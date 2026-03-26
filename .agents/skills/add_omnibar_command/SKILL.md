---
name: Add Omnibar Command
description: Register a new command in the Ctrl+K omnibar command palette
---

# Add Omnibar Command

## Architecture
The omnibar is powered by `ui/components/omnibar.py`. Commands are provided by `core/main.py` → `_provide_commands()`.

## Steps

1. Open `core/main.py` and find the `_provide_commands()` method.

2. Add a new command dict to the `base_cmds` list:
```python
{
    "title": "My New Command",
    "subtitle": "Description shown below the title",
    "icon": "🔧",  # emoji prefix
    "action": self._my_command_handler
},
```

3. Implement the handler method on `LeagueLoopApp`:
```python
def _my_command_handler(self):
    # Your logic here
    if hasattr(self, "sidebar") and self.sidebar.winfo_exists():
        self.sidebar.update_action_log("Executed My Command")
```

## Notes
- Commands are fuzzy-matched by title and subtitle text.
- The omnibar opens with `Ctrl+K` (configurable via `hotkey_omnibar` in config).
- Actions run on the main thread — for heavy work, spawn a daemon thread.
- Dynamic commands (like queue modes) are injected via loop at the end of `_provide_commands()`.
