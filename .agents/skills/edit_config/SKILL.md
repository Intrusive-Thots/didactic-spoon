---
name: Edit Config
description: Safely modify config.json values with validation
---

# Edit Config

## File Location
`C:\Users\Administrator\Desktop\LeagueLoop\config.json`

## Steps

1. Read the current config:
```powershell
Get-Content "C:\Users\Administrator\Desktop\LeagueLoop\config.json" | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

2. To modify a value, edit `config.json` directly using the file edit tools.

3. Validate it parses cleanly:
```powershell
python -c "import json; json.load(open('config.json'))"
```

## Config Schema Reference
| Key | Type | Description |
|-----|------|-------------|
| `auto_accept` | bool | Auto-accept ready check |
| `auto_requeue` | bool | Auto re-queue after game |
| `accept_delay` | float | Seconds to wait before accepting |
| `aram_mode` | string | Game mode name (e.g. "ARAM") |
| `stealth_mode` | bool | Keep window hidden during games |
| `priority_picker.enabled` | bool | Enable priority sniper |
| `priority_picker.list` | string[] | Ordered champion names (DDragon keys) |

## Critical Rules
- Champion names in `priority_picker.list` must be **DDragon API keys** (e.g. `"MonkeyKing"` not `"Wukong"`, `"Khazix"` not `"Kha'Zix"`).
- Always validate JSON after editing to prevent runtime crashes.
- Back up before making major changes: `Copy-Item config.json config_backup.json`
