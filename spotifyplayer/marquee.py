from threading import Thread
from time import sleep

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from tkinter import Label


class Marquee(Thread):
    def __init__(self, txtWd: int, lbl: "Label"):
        Thread.__init__(self, daemon=True)
        self.running = True
        self.lbl = lbl
        self.lblWd = lbl.winfo_reqwidth() - txtWd
        self.curX = 0

    def run(self) -> None:
        sleep(1.5)
        while self.running:
            self.lbl.place(x=self.curX)
            self.curX -= 1
            if abs(self.curX) == self.lblWd:
                self.curX = 0
                sleep(1.5)
            else:
                sleep(0.025)
