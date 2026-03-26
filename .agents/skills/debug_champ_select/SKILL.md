---
name: Debug Champ Select
description: Diagnose issues with champion select automation (priority sniper, skin equip)
---

# Debug Champ Select

## Architecture Overview
The champ select pipeline flows through:
1. `AutomationEngine._tick()` → detects `ChampSelect` phase
2. `_handle_champ_select()` → calls `_perform_priority_sniper()` and `_equip_random_skin()`
3. `stats_func` callback → updates sidebar lobby stats and priority grid's hovered champion

## Debugging Steps

1. Check if Priority Sniper is enabled:
```powershell
python -c "import json; c=json.load(open('config.json')); print(c.get('priority_picker', {}))"
```

2. Check if the current game mode has a bench (ARAM only):
- Priority Sniper only works when `session.benchChampions` is non-empty.
- Arena mode (queueId 1700) is explicitly excluded.

3. Monitor real-time automation logs:
```powershell
Select-String -Path "debug.log" -Pattern "\[Auto\]" | Select-Object -Last 30
```

4. Verify champion name resolution:
```powershell
python -c "
import json
data = json.load(open('cache/champion.json'))
for key, val in data['data'].items():
    print(f'{val[\"key\"]} -> {key}')
" | Select-String "<champion_name>"
```

## Common Issues
- **Priority Sniper not swapping**: Check `PRIORITY_SWAP_COOLDOWN` (1s default). The sniper won't swap faster than this.
- **Champion not found on bench**: Names must match DDragon keys exactly. Use `get_champ_name(id)` to verify.
- **Skin not equipping**: Only owned, non-base, non-disabled skins are eligible. Check `/lol-champ-select/v1/skin-carousel-skins`.
