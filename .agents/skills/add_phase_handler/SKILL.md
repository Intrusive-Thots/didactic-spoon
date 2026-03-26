---
name: Add Automation Phase Handler
description: Add a new game phase handler to the automation engine
---

# Add Automation Phase Handler

## Architecture
`services/automation.py` → `AutomationEngine._tick()` polls the LCU for the current `gameflow-phase`, then dispatches to handlers.

## Current Phase Handlers
| Phase | Handler | Purpose |
|-------|---------|---------|
| `ReadyCheck` | `_handle_ready_check()` | Auto-accept match popup |
| `ChampSelect` | `_handle_champ_select()` | Priority sniper, skin equip |
| `EndOfGame` / `Lobby` | `_handle_auto_queue()` | Auto re-queue |

## Steps

1. Create the handler method:
```python
def _handle_my_phase(self, phase, session_data=None):
    if phase != "MyPhase":
        return
    if not self.config.get("my_feature_enabled"):
        return
    # Logic here
```

2. Register it in `_tick()` after the existing handler calls:
```python
self._handle_my_phase(phase)
```

3. Add a config toggle (see `add_toggle_setting` skill).

## Available LCU Phases
`None`, `Lobby`, `Matchmaking`, `ReadyCheck`, `ChampSelect`, `GameStart`, `InProgress`, `WaitingForStats`, `EndOfGame`, `Reconnect`

## Notes
- Handlers run on the automation thread, NOT the UI thread.
- To update UI from a handler, use `self.after(0, lambda: ...)` via a callback function.
- Respect `self.paused` — check it at the start of your handler.
