---
description: Build pipeline fixes and instructions for the LeagueLoop Installer
---

# LeagueLoop Installer Pipeline Fixes & Build Instructions

This workflow contains the historical context of issues encountered when first attempting to compile the LeagueLoop application into a standalone Windows installer, and the architectural solutions implemented to prevent them from recurring. 

**If you are updating the build pipeline, refer to these to avoid regressions.**

## Encountered Issues & Implemented Solutions

### 1. The `run.py` Entry Point Mismatch
- **The Problem:** The `run.py` file, used as the `PyInstaller` entry point, was importing `App` from `core.main` instead of the correctly renamed `LeagueLoopApp`. The code would compile successfully, but immediately crash with an `ImportError` on launch.
- **The Fix:** Updated the entry point to import `LeagueLoopApp` and instantiate it correctly.

### 2. The ONEFILE vs. ONEDIR Packaging Mismatch
- **The Problem:** `LeagueLoop.spec` was natively configured to output a `ONEFILE` monolithic executable wrapper. However, `installer.iss` (the Inno Setup script) was configured to package the entire `dist/LeagueLoop/` directory contents. This resulted in Inno Setup constantly failing to find the target files.
- **The Fix:** Modified `LeagueLoop.spec` to use the `COLLECT` pipeline, producing a standard `ONEDIR` distribution folder `dist/LeagueLoop/`. We then updated `build.bat` to correctly manage and clear this directory.

### 3. Missing `ISCC.exe` Build Dependency
- **The Problem:** The host machine lacked Inno Setup Compiler (`ISCC.exe`), leading to pipeline failures when attempting to compile the `.iss` installer script. We must ensure the build machine has Inno Setup.
- **The Fix:** Downloaded and installed Inno Setup silently via PowerShell `Invoke-WebRequest` to `C:\InnoSetup`, which is where `.agents` should probe in the future.

### 4. Logger `PermissionError` in Program Files
- **The Problem:** When running the packaged application installed in `C:\Program Files\LeagueLoop\`, the `logger.py` utility hardcoded `debug.log` and `error.log` to write to the Current Working Directory (`cwd`). This resulted in a fatal `[Errno 13] Permission denied` crash since the Windows `Program Files` directory is strictly Read-Only for standard users.
- **The Fix:** Redirected the FileHandlers in `utils/logger.py` to write logs specifically into the user's Local APPDATA folder: `%APPDATA%\LeagueLoop`. Added fallback contingencies to Write-Test the directory before hooking.

---

## Build Steps
When the user asks to "Build the Installer", run these commands sequentially:

```powershell
# 1. Clean previous artifacts and build the ONEDIR distribution
cd c:\Users\Administrator\Desktop\LeagueLoop
if (Test-Path build) { Remove-Item -Recurse -Force build }
if (Test-Path dist\LeagueLoop) { Remove-Item -Recurse -Force dist\LeagueLoop }

pyinstaller --clean LeagueLoop.spec 2>&1

# 2. Package the ONEDIR distribution into the Inno Setup installer
& "C:\InnoSetup\ISCC.exe" "c:\Users\Administrator\Desktop\LeagueLoop\installer.iss" 2>&1
```
