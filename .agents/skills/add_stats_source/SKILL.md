---
name: Add Stats Scraper Source
description: Add a new win rate data source to the stats scraper
---

# Add Stats Scraper Source

## Architecture
`services/stats_scraper.py` → `StatsScraper` fetches champion win rates from external data sources.

## Current Sources
- **op.gg** — Primary source for ARAM/ranked data
- **Meraki Analytics** — Role data and champion metadata
- **Offline fallback** — Returns baseline 50.0% when no data available

## Steps

1. Open `services/stats_scraper.py`.

2. Add a new fetch method:
```python
def _fetch_from_my_source(self):
    try:
        url = "https://api.example.com/champion-stats"
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            for champ in data:
                name = champ["name"]
                wr = float(champ["winRate"])
                self.cache[name.lower()] = wr
            self.log(f"Loaded {len(data)} champion stats from MySource")
    except Exception as e:
        Logger.error("Stats", f"MySource fetch error: {e}")
```

3. Call it from the initialization or refresh method.

4. Update `get_winrate()` to check your new cache.

## Notes
- Cache data in memory to minimize network calls.
- Respect rate limits — cache for at least 5 minutes.
- Set `self.is_offline = True` if all sources fail, so the UI can show "(Offline Mode)".
