from threading import Thread

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .player import GUI


class WaitExit(Thread):
    def __init__(self, root: "GUI"):
        Thread.__init__(self, daemon=True)
        self.root = root
        self.app = self.root.spotify.app

    def run(self) -> None:
        self.app.wait_for_process_exit(timeout=7**7,
                                       retry_interval=1)
        self.root.closePlayer()
        self.root.destroy()
