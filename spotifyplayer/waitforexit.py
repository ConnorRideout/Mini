from threading import Thread

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pywinauto.application import Application
    from .player import GUI


class WaitExit(Thread):
    root: "GUI"
    app: "Application"

    def __init__(self, root: "GUI"):
        Thread.__init__(self, daemon=True)
        self.root = root
        self.app = self.root.spotify.app

    def run(self) -> None:
        self.app.wait_for_process_exit(timeout=7**7,
                                       retry_interval=0.1)
        self.root.closePlayer()
        self.root.destroy()
