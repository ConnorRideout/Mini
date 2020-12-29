"""Create a topmost window that acts as a border around the currently
active window."""

from tkinter import Tk, Frame
from win32gui import GetForegroundWindow as GetForeWin, SetWindowLong
from ahk import AHK


def main(self, *args):
    """\
    args (type:list of 4 ints; optional)
        if provided, must be x position, y position, width, height of current window """

    x, y, w, h = args if len(args) == 4 else AHK().active_window.rect
    topWin, root = GetForeWin(), Tk()
    root.overrideredirect(True)
    root.title("-*Filter*-")
    root.config(bg='red')
    root.attributes('-transparentcolor', 'black',
                    '-topmost', True, '-alpha', 0.5)
    root.geometry('{}x{}+{}+{}'.format(w, h, x, y))
    f = Frame(root, bg='black')
    f.place(anchor='center', relx=0.5, rely=0.5,
            width=-6, relwidth=1, height=-6, relheight=1)
    root.update_idletasks()
    SetWindowLong(GetForeWin(), -8, topWin)
    root.mainloop()
