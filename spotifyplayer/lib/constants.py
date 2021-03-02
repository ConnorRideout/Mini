from win32con import SWP_ASYNCWINDOWPOS, SWP_NOACTIVATE, SWP_NOMOVE, SWP_NOSIZE, SWP_SHOWWINDOW
from win32api import GetMonitorInfo, MonitorFromPoint
from typing import TYPE_CHECKING, Optional as O
from collections import OrderedDict as oDict
from win32gui import FindWindow
from time import sleep


# PATH VARIABLES
SPOTIFY_EXE = "C:\\Users\\Cryden\\AppData\\Roaming\\Spotify\\Spotify.exe"
SPOTIFY_AHK = "C:\\Admin Tools\\Python\\MyScripts\\spotifyplayer\\lib\\SpotifyAHK.exe"
SPOTIFY_LINK = "C:\\Users\\Cryden\\AppData\\Roaming\\Microsoft\\Internet Explorer\\Quick Launch\\User Pinned\\TaskBar\\Spotify.lnk"

# TEXT VARIABLES
SPOTIFY_TITLE = "Spotify Premium"
STARTUP_TEXT_L = f'{"~Welcome!~":^15}'
STARTUP_TEXT_R = f'{"~Starting up~":^15}'
SHUTDOWN_TXT_L = f'{"~Goodbye!~":^15}'
SHUTDOWN_TXT_R = f'{"~Closing~":^15}'
FONT_DEF = "Ebrima 17"

# SCROLL VARIABLES
SCROLL_BREAK = f'{"":20}'
SCROLL_MOTION = -1
SCROLL_TICK = 0.025
SCROLL_WAIT = 1.5

# SIZE VARIABLES
LBL_W = 175
BTN_SIZE = 30
OFFSET_X = 275
OFFSET_X_STEP = 25
OFFSET_Y = 0
OFFSET_Y_STEP = 1

# COLOR VARIABLES
CLR_BG = 'black'
CLR_TEXT = 'white'
CLR_BTNS = 'white'
CLR_BTN_HOVER = 'lightgray'

# OTHER VARIABLES
BTN_POINTS: oDict[str, tuple[int]] = oDict(
    prev=(3, 15, 17, 7, 17, 11, 24, 7, 24, 23, 17, 20, 17, 24),
    stop=(8, 8, 22, 8, 22, 22, 8, 22),
    play=(10, 7, 25, 15, 10, 24),
    next=(27, 15, 13, 23, 13, 19, 6, 23, 6, 7, 13, 10, 13, 6)
)
BOTTOM_FLAGS = SWP_NOACTIVATE | SWP_NOMOVE | SWP_NOSIZE
TOP_FLAGS = SWP_NOMOVE | SWP_NOSIZE | SWP_SHOWWINDOW
DESKTOP_HWND = FindWindow('WorkerW', None)


class Screen:
    def __init__(self):
        monInfo: dict = GetMonitorInfo(MonitorFromPoint((0, 0)))
        monW, monH = monInfo.get('Monitor')[2:4]
        taskbarH = monH - monInfo.get('Work')[3]
        self.appW = LBL_W * 2 + BTN_SIZE * 3
        self.appH = max(BTN_SIZE, ((BTN_SIZE + taskbarH) // 2))
        self.X = round(monW - OFFSET_X - self.appW)
        self.Y = round(monH - OFFSET_Y - self.appH)
