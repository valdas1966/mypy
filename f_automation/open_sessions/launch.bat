@echo off
REM ============================================================
REM  Launch the OpenSessions Tkinter GUI.
REM  Pin to taskbar / desktop for one-click access.
REM  Requires WSLg (Windows 11) for Tkinter to display.
REM ============================================================
start /min "" wsl.exe -- bash -lic "cd /mnt/f/mypy && python -m f_automation.open_sessions._gui"
