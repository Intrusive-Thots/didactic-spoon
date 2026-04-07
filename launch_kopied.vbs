Set WshShell = CreateObject("WScript.Shell")
' Use the venv python if available, otherwise fallback to system python
python_cmd = """C:\Users\Administrator\Desktop\LeagueLoop\.venv\Scripts\python.exe"" ""C:\Users\Administrator\Desktop\LeagueLoop\src\tools\kopied.py"""
WshShell.Run python_cmd, 0, False
