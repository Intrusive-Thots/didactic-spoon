---
name: Test LCU Connection
description: Verify the League Client Update API connection and diagnose issues
---

# Test LCU Connection

## Steps

1. Launch LeagueLoop in dev mode (see `launch_dev` skill).

2. Check if the LCU lockfile exists:
```powershell
$lockfile = Get-ChildItem -Path "$env:LOCALAPPDATA\Riot Games\League of Legends" -Filter "lockfile" -Recurse -ErrorAction SilentlyContinue
if ($lockfile) { Get-Content $lockfile.FullName } else { Write-Host "Lockfile not found — League Client is not running." }
```

3. Parse the lockfile for port and auth token:
```
Format: processName:pid:port:password:protocol
```

4. Test a basic endpoint:
```powershell
$port = <port_from_lockfile>
$token = <password_from_lockfile>
$pair = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("riot:$token"))
Invoke-RestMethod -Uri "https://127.0.0.1:$port/lol-gameflow/v1/gameflow-phase" -Headers @{Authorization="Basic $pair"} -SkipCertificateCheck
```

## Common Issues
- **Lockfile not found**: League Client isn't running. Launch it first.
- **Connection refused**: Client may be starting up. Wait 10s and retry.
- **403 Forbidden**: Auth token is wrong. Re-read the lockfile.
