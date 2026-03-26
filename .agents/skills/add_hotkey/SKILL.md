---
name: Add Hotkey Binding
description: Register a new global hotkey in LeagueLoop
---

# Add Hotkey Binding

## Architecture
Hotkeys use the `keyboard` library and are registered in `core/main.py` → `_bind_hotkeys()`.

## Steps

1. Add a config key for the hotkey in `config.json`:
```json
"hotkey_my_action": "ctrl+shift+x"
```

2. In `core/main.py`, add the handler method:
```python
def _hotkey_my_action(self):
    self.after(0, lambda: self._do_something())
```

3. Register in `_bind_hotkeys()`:
```python
self._my_action_hotkey = self.config.get("hotkey_my_action", "ctrl+shift+x")
keyboard.add_hotkey(self._my_action_hotkey, self._hotkey_my_action, suppress=False)
```

4. Optionally add it to the settings modal so users can customize the hotkey.

## Notes
- Always use `suppress=False` to avoid blocking other apps from receiving the key.
- Wrap callback logic in `self.after(0, ...)` to ensure it runs on the main thread.
- All hotkeys are unhooked and re-bound when settings are saved (`on_settings_saved()`).
- Available modifier keys: `ctrl`, `shift`, `alt`, `win`.
