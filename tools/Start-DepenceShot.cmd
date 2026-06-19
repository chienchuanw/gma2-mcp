@echo off
REM Double-click launcher for the Depence screenshot bridge.
REM Runs depence-shot-server.ps1 (which self-elevates, opens the firewall port,
REM and serves GET /shot.png on port 8099 from the interactive desktop session).
powershell -ExecutionPolicy Bypass -File "%~dp0depence-shot-server.ps1"
