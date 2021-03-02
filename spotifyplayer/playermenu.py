from fileinput import input as fileinput
from tkinter import Toplevel, Menu
from os import path as os_path

from .lib.constants import *

if TYPE_CHECKING:
    from tkinter import Event
    from .player import GUI


class PlayerMenu(Menu):
    root: "GUI"
    movemenu: Menu
    axis: str
    startX: int
    startY: int
    cX: int
    cY: int
    tw: Toplevel

    def __init__(self, root: "GUI"):
        self.root = root
        Menu.__init__(self,
                      master=root,
                      tearoff=0)
        # create 'move' menu
        self.movemenu = Menu(master=self,
                             tearoff=0)
        self.movemenu.add_command(label="Move (Horizontal)",
                                  command=lambda: self.movePlayer("X"))
        self.movemenu.add_command(label="Move (Vertical)",
                                  command=lambda: self.movePlayer("Y"))
        self.movemenu.add_separator()
        self.movemenu.add_command(label="Save Position",
                                  command=self.savePos,
                                  state='disabled')
        self.movemenu.add_command(label="Reset Position",
                                  command=self.resetPos,
                                  state='disabled')
        # create 'main' menu
        self.add_cascade(label="Move Player",
                         menu=self.movemenu)
        self.add_separator()
        self.add_command(label="Exit Spotify",
                         command=lambda: root.spotify.win.close())
        self.add_command(label="Close Player",
                         command=root.closePlayer)

    def show(self, event: "Event") -> None:
        self.post(event.x_root, self.root.winfo_rooty())

    def movePlayer(self, axis: str) -> None:
        self.root.event_generate(sequence='<Motion>',
                                 warp=True,
                                 x=(self.root.screen.appW // 2),
                                 y=(self.root.screen.appH // 2))
        self.axis = axis
        cur = f"sb_{'h' if axis == 'X' else 'v'}_double_arrow"
        self.root.configure(cursor=cur)
        self.startX = self.root.winfo_rootx()
        self.startY = self.root.winfo_rooty()
        for btn in self.root.btns.values():
            btn.unbind(sequence='<ButtonRelease-1>')
        self.root.unbind_all(sequence='<ButtonRelease-3>')
        self.root.bind(sequence='<Escape>',
                       func=self.stopMoving)
        self.root.bind(sequence='<ButtonRelease-3>',
                       func=self.stopMoving)
        self.root.bind(sequence='<Button-1>',
                       func=self.on_click)
        self.root.bind(sequence='<B1-Motion>',
                       func=self.on_move)
        self.root.bind(sequence='<ButtonRelease-1>',
                       func=self.on_release)

    def on_click(self, event: "Event") -> None:
        self.cX = event.x
        self.cY = event.y
        self.tw = Toplevel(master=self.root,
                           bg='white',
                           bd=3,
                           relief='groove')
        self.tw.attributes('-transparentcolor', 'white',
                           '-topmost', 1)
        self.tw.overrideredirect(1)
        self.tw.geometry(self.root.geometry())

    def on_move(self, event: "Event") -> None:
        if self.axis == "X":
            pos = ((event.x - self.cX) // OFFSET_X_STEP)
            dX = OFFSET_X_STEP * pos
            dY = 0
        else:
            pos = ((event.y - self.cY) // OFFSET_Y_STEP)
            dX = 0
            dY = OFFSET_Y_STEP * pos
        self.tw.geometry(f'+{self.startX + dX}'
                         f'+{self.startY + dY}')

    def on_release(self, *_) -> None:
        if self.tw.geometry() != self.root.geometry():
            self.root.geometry(self.tw.geometry())
            self.movemenu.entryconfigure(3, state='normal')
            self.movemenu.entryconfigure(4, state='normal')
        self.tw.destroy()
        self.stopMoving()

    def stopMoving(self, *_) -> None:
        self.root.bind_all(sequence='<ButtonRelease-3>',
                           func=self.show)
        self.root.unbind(sequence='<Button-1>')
        self.root.unbind(sequence='<B1-Motion>')
        self.root.unbind(sequence='<ButtonRelease-1>')
        self.root.unbind(sequence='<Escape>')
        self.root.configure(cursor="")
        for id, btn in enumerate(self.root.btns.values()):
            btn.bind(sequence='<ButtonRelease-1>',
                     func=lambda e, n=id: self.root.sendInput(e, n))

    def savePos(self) -> None:
        global OFFSET_X, OFFSET_Y
        self.movemenu.entryconfigure(3, state='disabled')
        self.movemenu.entryconfigure(4, state='disabled')
        curX = self.root.winfo_rootx()
        curY = self.root.winfo_rooty()
        OFFSET_X += (self.root.screen.X - curX)
        OFFSET_Y += (self.root.screen.Y - curY)
        change = dict(OFFSET_X=OFFSET_X, OFFSET_Y=OFFSET_Y)
        line: str
        file = os_path.join(os_path.dirname(__file__), 'lib', 'constants.py')
        for line in fileinput(file, inplace=True):
            line = line.rstrip('\r\n')
            var = line.split(' = ')[0]
            if var in change:
                out = f'{var} = {change.get(var)}'
            else:
                out = line
            print(out)
        self.root.screen = Screen()

    def resetPos(self) -> None:
        self.movemenu.entryconfigure(3, state='disabled')
        self.movemenu.entryconfigure(4, state='disabled')
        self.root.focus_set()
        self.root.geometry(f'+{self.root.screen.X}'
                           f'+{self.root.screen.Y}')
