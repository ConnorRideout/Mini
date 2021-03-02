from threading import Thread

from .lib.constants import *

if TYPE_CHECKING:
    from .player import GUI
    from typing import Callable as C


class WatchUpdate(Thread):
    running: bool
    root: "GUI"
    startTitle: str
    window_text: "C[[], str]"

    def __init__(self, root: "GUI", title: str):
        Thread.__init__(self, daemon=True)
        self.running = True
        self.root = root
        self.startTitle = title
        win = root.spotify.win
        self.window_text = win.window_text

    def run(self) -> None:
        # the title last time it was checked
        prevTitle = self.startTitle
        while self.running:
            sleep(0.5)
            # the title right now
            curTitle = self.window_text()
        # ==NO CHANGE================================
            if prevTitle == curTitle:
                continue
        # ==WAS JUST PAUSED==========================
            elif curTitle == SPOTIFY_TITLE:
                if self.root.isPlaying:
                    # need to change play to stop
                    self.root.chngToStopped()
                self.checkIfNew(prevTitle)
        # ==WAS JUST UNPAUSED========================
            elif prevTitle == SPOTIFY_TITLE:
                if not self.root.isPlaying:
                    # need to change stop to play
                    self.root.chngToPlaying()
                self.checkIfNew(curTitle)
        # ==NEW TRACK================================
            else:
                self.root.updateText(curTitle)
            prevTitle = curTitle

    def checkIfNew(self, t: str) -> None:
        new = t.split(' - ', 1)[-1]
        old = self.root.track.get().split(SCROLL_BREAK)[-1]
        if new != old:
            self.root.updateText(t)
