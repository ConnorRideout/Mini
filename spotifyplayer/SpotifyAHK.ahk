#NoEnv
#NoTrayIcon
#SingleInstance Force
SetWorkingDir %A_ScriptDir%

Run, % "powershell -command ""Start-Process -FilePath python -ArgumentList 'SpotifyPlayer.py' -WindowStyle Hidden"""
ExitApp