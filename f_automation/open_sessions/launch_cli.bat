@echo off
REM ============================================================
REM  Launch sessions directly from CLI args.
REM  Usage:    launch_cli.bat name1 name2 [name3 ...]
REM  Or duplicate this file with hardcoded names for a preset.
REM ============================================================
wsl.exe -- bash -lic "cd /mnt/f/mypy && python -m f_automation.open_sessions.main %*"
