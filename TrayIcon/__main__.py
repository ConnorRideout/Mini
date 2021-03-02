try:
    from . import *
except ImportError:
    from __init__ import *
from tkinter import Tk, Label, Button


class example:
    def __init__(self):
        self.showNew = False
        self.tIcon = TrayIcon()
        rBtns = self.tIcon.Menu()
        rBtns.add_radiobutton('radio a1', lambda: print('a1'))
        rBtns.add_radiobutton('radio a2', lambda: print('a2'))
        rBtns.add_separator()
        rBtns.add_command('check A', lambda: print(rBtns.get_radiobutton('A')))
        rBtns.add_separator()
        rBtns.add_radiobutton('radio b1', lambda: print('b1'), 'B')
        rBtns.add_radiobutton('radio b2', lambda: print('b2'), 'B')
        rBtns.add_separator()
        rBtns.add_command('check B', lambda: print(rBtns.get_radiobutton('B')))
        cBtns = self.tIcon.Menu()
        cBtns.add_checkbutton('check button', lambda: print('check'))
        cBtns.add_separator()
        cBtns.add_command('check', lambda: print(
            cBtns.get_checkbutton('check button')))
        menu = self.tIcon.Menu(self.tIcon)
        menu.add_command('Print hi', lambda: print('hi'))
        menu.add_separator()
        menu.add_cascade('Radiobuttons', rBtns)
        menu.add_cascade('Checkbuttons', cBtns)
        menu.add_separator()
        menu.add_command('click to swap to "New"', self.swapNew,
                         visible=lambda _: not self.showNew)
        menu.add_command('click to change back to "Old"',
                         self.swapOld, visible=lambda _: self.showNew)
        self.tIcon.show()

        self.root = Tk()
        self.root.protocol('WM_DELETE_WINDOW', self.onClose)
        Label(text="This is the main window").pack()
        Button(text="Swap New", command=self.swapNew).pack()
        Button(text="Swap Old", command=self.swapOld).pack()
        self.root.mainloop()

    def swapNew(self):
        self.showNew = True
        self.tIcon.update()

    def swapOld(self):
        self.showNew = False
        self.tIcon.update()

    def onClose(self):
        self.tIcon.hide()
        self.root.destroy()


if __name__ == '__main__':
    example()
