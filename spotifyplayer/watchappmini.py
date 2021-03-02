from pywinauto.timings import wait_until as win_wait_until
from threading import Thread

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .player import GUI
    from pywinauto.application import WindowSpecification


class WatchMini(Thread):
    running: bool
    root: "GUI"
    win: "WindowSpecification"

    def __init__(self, root: "GUI"):
        Thread.__init__(self, daemon=True)
        self.running = True
        self.root = root
        self.win = self.root.spotify.win

    def run(self) -> None:
        while self.running:
            try:
                if self.root.spotifyMini:
                    self.root.spotify.hideSpotify()
                else:
                    self.root.spotify.showSpotify()
            except OSError:
                break
            win_wait_until(timeout=7**7,
                           retry_interval=0.1,
                           func=self.doCheck)

    def doCheck(self) -> bool:
        try:
            if self.root.spotifyMini:
                if self.win.has_focus():
                    self.root.spotifyMini = False
                    return True
                else:
                    return False
            else:
                if self.win.is_minimized():
                    self.root.spotifyMini = True
                    return True
                else:
                    return False
        except OSError:
            return True
