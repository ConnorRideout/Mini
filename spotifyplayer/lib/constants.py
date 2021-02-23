from win32con import SWP_NOACTIVATE, SWP_NOMOVE, SWP_NOSIZE
from win32api import GetMonitorInfo, MonitorFromPoint
from typing import TYPE_CHECKING
from win32gui import FindWindow
from time import sleep


# PATH VARIABLES
SPOTIFY_EXE = "C:\\Users\\Cryden\\AppData\\Roaming\\Spotify\\Spotify.exe"
SPOTIFY_AHK = "C:\\Admin Tools\\Python\\MyScripts\\spotifyplayer\\lib\\SpotifyAHK.exe"
SPOTIFY_LINK = "C:\\Users\\Cryden\\AppData\\Roaming\\Microsoft\\Internet Explorer\\Quick Launch\\User Pinned\\TaskBar\\Spotify.lnk"

# TEXT VARIABLES
SPOTIFY_TITLE = "Spotify Premium"
APP_TITLE = "Spotify Taskbar Player"
STARTUP_TEXT_LEFT = "    ~Welcome!~    "
STARTUP_TEXT_RIGHT = "   ~Starting up~   "
SHUTDOWN_TXT_LEFT = "    ~Goodbye!~     "
SHUTDOWN_TXT_RIGHT = "~Shutting down~"

FONT_DEF = "Calibri 18"

# SIZE VARIABLES
LBL_W = 175
BTN_SIZE = 30
OFFSET_X = 275
OFFSET_X_STEP = 25
OFFSET_Y = 0
OFFSET_Y_STEP = 1

# OTHER VARIABLES
BTN_POINTS = dict(
    prev=[3, 15, 17, 7, 17, 11, 24, 7, 24, 23, 17, 20, 17, 24],
    stop=[8, 8, 22, 8, 22, 22, 8, 22],
    play=[10, 7, 25, 15, 10, 24],
    next=[27, 15, 13, 23, 13, 19, 6, 23, 6, 7, 13, 10, 13, 6]
)
WINDOW_FLAGS = SWP_NOACTIVATE | SWP_NOMOVE | SWP_NOSIZE
DESKTOP_HWND = FindWindow('WorkerW', None)


class Screen:
    def __init__(self):
        monInfo = GetMonitorInfo(MonitorFromPoint((0, 0)))
        monW = monInfo.get('Monitor')[2]
        monH = monInfo.get('Monitor')[3]
        taskbarH = monH - monInfo.get('Work')[3]
        self.appW = LBL_W * 2 + BTN_SIZE * 3
        self.appH = max(BTN_SIZE, round((BTN_SIZE + taskbarH) / 2))
        self.X = round(monW - OFFSET_X - self.appW)
        self.Y = round(monH - OFFSET_Y - self.appH)
