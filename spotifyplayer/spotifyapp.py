from tkinter import Tk
from tkinter import messagebox as Mbox

from pywinauto.application import Application
from pywinauto.timings import wait_until as win_wait_until
from win32con import HWND_BOTTOM, SW_SHOWNOACTIVATE
from win32gui import SetForegroundWindow, SetWindowPos, ShowWindow

from .lib.constants import *


class SpotifyApp:
    def __init__(self):
        self.closeOld()
        self.startApp()

    @staticmethod
    def closeOld() -> None:
        try:
            Application().connect(title=SPOTIFY_TITLE).kill(soft=True)
        finally:
            return

    def startApp(self) -> None:
        self.win = None
        self.posY = 0
        i = 0
        self.app = Application().start(SPOTIFY_EXE)
        while not self.win:
            try:
                self.base = self.app.top_window()
                self.win = self.base.top_level_parent()
                self.win.minimize()
                self.hideSpotify()
                win_wait_until(3, 0.5, self.win.window_text, SPOTIFY_TITLE)
            except Exception:
                i += 1
                if i == 3:
                    self.showError()
                elif i == 4:
                    i = 2
                    try:
                        self.closeOld()
                        self.app = Application().start(SPOTIFY_EXE)
                    except Exception:
                        self.showError()

    def hideSpotify(self) -> None:
        self.win.set_transparency(0)
        ShowWindow(self.win.handle, SW_SHOWNOACTIVATE)
        sleep(0.1)
        self.posY = self.base.rectangle().top
        SetWindowPos(self.win.handle, HWND_BOTTOM, 0, 0, 0, 0, WINDOW_FLAGS)
        self.win.move_window(y=-50)
        if self.win.has_focus():
            try:
                SetForegroundWindow(DESKTOP_HWND)
            except Exception:
                self.hideSpotify()

    def showSpotify(self) -> None:
        self.win.move_window(y=max(self.posY, 0))
        self.win.set_transparency(255)

    @staticmethod
    def showError() -> None:
        Tk().withdraw()
        if Mbox.askyesno("Error", "Python can't seem to hook Spotify. Would you like to keep trying?\n(Note that Spotify can be open but not playing)"):
            return
        else:
            raise SystemExit
