---
name: Git Sync
description: Commit all changes and sync with the remote repository
---

# Git Sync

## Steps

1. Stage all changes:
```powershell
git add -A
```

2. Commit with a descriptive message:
```powershell
git commit -m "chore: <description>"
```

3. Pull latest from remote (rebase to keep history clean):
```powershell
git pull --rebase origin master
```

4. If conflicts occur, resolve them, then:
```powershell
git add .
git rebase --continue
```

5. Push to remote:
```powershell
git push origin master
```

## Notes
- Always pull before push to avoid rejected pushes.
- Use `--rebase` to keep a linear commit history.
- For merge conflicts in auto-generated files like `.jules/bolt.md`, prefer keeping the incoming (remote) content.
- Working directory: `C:\Users\Administrator\Desktop\LeagueLoop`
