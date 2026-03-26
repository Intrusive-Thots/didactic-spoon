---
name: Build Installer
description: Compile the Inno Setup installer for LeagueLoop distribution
---

# Build Installer

## Prerequisites
- A successful PyInstaller build (see `build_executable` skill).
- Inno Setup 6 installed at `C:\Program Files (x86)\Inno Setup 6\ISCC.exe`.

## Steps

1. Ensure the `dist/LeagueLoop/` directory is up to date from a fresh PyInstaller build.

2. Compile the installer:
```powershell
& "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" "C:\Users\Administrator\Desktop\LeagueLoop\installer.iss"
```

3. The output `.exe` installer will be in the `Output/` directory.

## Notes
- The `installer.iss` script expects the PyInstaller output in `dist\LeagueLoop\`.
- Always rebuild the executable before recompiling the installer.
- Test the installer on a clean path to verify all files are bundled.
