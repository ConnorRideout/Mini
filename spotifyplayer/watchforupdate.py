from pywinauto.timings import wait_until as win_wait_until
from operator import ne as op_ne
from threading import Thread

from .lib.constants import *

if TYPE_CHECKING:
    from .player import GUI


class WatchUpdate(Thread):
    def __init__(self, root: "GUI"):
        Thread.__init__(self, daemon=True)
        self.running = True
        self.root = root
        win = root.spotify.win
        self.window_text = win.window_text

        sleep(2.5)
        # mute
        win.send_keystrokes('^{UP}')
        win.send_keystrokes('^+{DOWN}')
        sleep(0.5)
        # start playing
        win.send_keystrokes('{SPACE}')
        try:
            win_wait_until(timeout=2,
                           retry_interval=0.1,
                           func=win.window_text,
                           value=SPOTIFY_TITLE,
                           op=op_ne)
            sleep(0.1)
            self.startTitle = win.window_text()
        except Exception:
            self.startTitle = '  -  '
        # stop playing
        win.send_keystrokes('{SPACE}')
        sleep(0.1)
        # set volume to mid
        win.send_keystrokes('^{UP 8}')
        self.root.updateText(self.startTitle)

    def run(self) -> None:
        prevTitle = self.startTitle
        while self.running:
            sleep(0.5)
            # update player
            curTitle = self.window_text()
            if prevTitle == curTitle:  # NO CHANGE
                continue
            elif curTitle == SPOTIFY_TITLE:  # WAS JUST PAUSED
                if self.root.isPlaying:  # play status needs to be updated
                    self.root.chngToStopped()
                self.checkIfNew(prevTitle)
            elif prevTitle == SPOTIFY_TITLE:  # WAS JUST UNPAUSED
                if not self.root.isPlaying:  # play status needs to be updated
                    self.root.chngToPlaying()
                self.checkIfNew(curTitle)
            else:  # NEW TRACK
                self.root.updateText(curTitle)
            prevTitle = curTitle

    def checkIfNew(self, t: str) -> None:
        new = t.split(' - ', 1)[-1]
        old = self.root.track.get().split(' '*20)[-1]
        if new != old:
            self.root.updateText(t)
