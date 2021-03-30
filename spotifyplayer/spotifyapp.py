from win32gui import SetForegroundWindow, SetWindowPos, ShowWindow
from win32con import HWND_BOTTOM, HWND_TOP, SW_SHOWNOACTIVATE
from pywinauto.timings import wait_until as win_wait_until
from pywinauto.application import Application
from tkinter import messagebox as Mbox
from operator import ne as op_ne

from .lib.constants import *

if TYPE_CHECKING:
    from pywinauto.application import WindowSpecification
    from .player import GUI


class SpotifyApp:
    app: Application
    base: "WindowSpecification"
    win: "WindowSpecification"
    startTitle: str
    posY: int

    def __init__(self, root: "GUI"):
        self.closeOld()
        self.startApp()
        self.startTitle = self.getText()
        root.updateText(self.startTitle)
        self.showSpotify()
        ct = 0
        while True:
            try:
                if self.win.has_focus() or self.base.has_focus():
                    break
                self.win.minimize()
                sleep(0.1)
                self.win.restore()
                # SetWindowPos(self.base.handle, HWND_TOP,
                #              0, 0, 0, 0, TOP_FLAGS)
                SetWindowPos(self.win.handle, HWND_TOP,
                             0, 0, 0, 0, TOP_FLAGS)
            except Exception as ex:
                print(ex)
            ct += 1
            if ct == 10:
                self.showError()
                ct = 0
                self.showSpotify()

    @staticmethod
    def closeOld() -> None:
        try:
            Application().connect(title=SPOTIFY_TITLE).kill(soft=True)
        finally:
            return

    def startApp(self) -> None:
        self.win = None
        i = int()
        self.app = Application().start(SPOTIFY_EXE)
        while not self.win:
            try:
                self.base = self.app.top_window()
                self.win = self.base.top_level_parent()
                self.win.set_transparency(0)
                self.posY = self.base.rectangle().top
                self.win.move_window(y=-50)
                win_wait_until(timeout=3,
                               retry_interval=0.1,
                               func=self.win.window_text,
                               value=SPOTIFY_TITLE)
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

    def getText(self) -> str:
        sleep(2.5)
        # mute
        self.win.send_keystrokes('^{UP}')
        self.win.send_keystrokes('^+{DOWN}')
        sleep(0.5)
        # start playing
        self.win.send_keystrokes('{SPACE}')
        try:
            win_wait_until(timeout=2,
                           retry_interval=0.1,
                           func=self.win.window_text,
                           value=SPOTIFY_TITLE,
                           op=op_ne)
            sleep(0.1)
            nowPlaying = str(self.win.window_text())
        except TimeoutError:
            nowPlaying = str('  -  ')
        # stop playing
        self.win.send_keystrokes('{SPACE}')
        sleep(0.1)
        # set volume to mid
        self.win.send_keystrokes('^{UP 8}')
        return nowPlaying

    def hideSpotify(self) -> None:
        self.win.set_transparency(0)
        ShowWindow(self.win.handle, SW_SHOWNOACTIVATE)
        sleep(0.1)
        self.posY = self.base.rectangle().top
        SetWindowPos(self.win.handle, HWND_BOTTOM, 0, 0, 0, 0, BOTTOM_FLAGS)
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
        if Mbox.askyesno("Error", "Python can't seem to hook Spotify. Would you like to keep trying?\n(Note that Spotify can be open but not playing)"):
            return
        else:
            raise SystemExit
