#NoEnv
#NoTrayIcon
#SingleInstance Force
SetWorkingDir %A_ScriptDir%

errlog := """""""$errlog"""""""
cmd := "($errlog='C:\Admin Tools\Python\MyScripts\spotifyplayer\lib\errorlog.txt'); "
cmd .= "Start-Process py -ArgumentList '-m spotifyplayer' -Verb runas -WindowStyle Hidden -Wait; "
cmd .= "if (Get-Content " errlog ") {[system.media.systemsounds]`:`:Hand.play(); Start-Process " errlog "}"

Run, % "powershell -command """ cmd """",, Hide

ExitApp