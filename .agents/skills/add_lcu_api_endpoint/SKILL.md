---
name: Add LCU API Endpoint
description: Make a new League Client API call from the automation engine
---

# Add LCU API Endpoint

## LCU Client Usage
The `LCUClient` is in `services/api_handler.py`. Use `self.lcu.request()`:

```python
# GET request
response = self.lcu.request("GET", "/lol-summoner/v1/current-summoner")
if response and response.status_code == 200:
    data = response.json()

# POST with data
response = self.lcu.request("POST", "/lol-lobby/v2/lobby", {"queueId": 450})

# PATCH
response = self.lcu.request("PATCH", "/lol-champ-select/v1/session/my-selection", {"selectedSkinId": 12345})

# DELETE
response = self.lcu.request("DELETE", "/lol-lobby/v2/lobby/matchmaking/search")
```

## Useful Endpoints
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/lol-gameflow/v1/gameflow-phase` | GET | Current game phase |
| `/lol-champ-select/v1/session` | GET | Champ select session data |
| `/lol-lobby/v2/lobby` | GET/POST | Lobby info / Create lobby |
| `/lol-lobby/v2/lobby/matchmaking/search` | POST/DELETE | Start/stop matchmaking |
| `/lol-matchmaking/v1/ready-check/accept` | POST | Accept ready check |
| `/lol-summoner/v1/current-summoner` | GET | Summoner info |
| `/lol-champ-select/v1/skin-carousel-skins` | GET | Available skins |
| `/lol-collections/v1/inventories/{summonerId}/champions` | GET | Owned champions |

## Notes
- The client auto-connects via lockfile discovery. Check `self.lcu.is_connected` before making calls.
- All requests are thread-safe — `LCUClient` handles SSL and auth internally.
- Failed requests return `None` or a non-200 status code. Always check both.
