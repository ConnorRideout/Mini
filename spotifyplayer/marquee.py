from threading import Thread
from time import sleep

from .lib.constants import *

if TYPE_CHECKING:
    from tkinter import Label


class Marquee(Thread):
    running: bool
    lbl: "Label"
    lblWd: int
    curX: int

    def __init__(self, txtWd: int, lbl: "Label"):
        Thread.__init__(self, daemon=True)
        self.running = True
        self.lbl = lbl
        self.lblWd = (lbl.winfo_reqwidth() - txtWd)
        self.curX = int()

    def run(self) -> None:
        sleep(SCROLL_WAIT)
        while self.running:
            self.lbl.place(x=self.curX)
            self.curX += SCROLL_MOTION
            if abs(self.curX) == self.lblWd:
                self.curX = 0
                sleep(SCROLL_WAIT)
            else:
                sleep(SCROLL_TICK)
