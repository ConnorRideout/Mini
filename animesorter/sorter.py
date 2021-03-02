from tkinter import Tk, Frame, Label, Spinbox, LabelFrame as LFrame, messagebox as mbox
from os import listdir as os_listdir, rename as os_rename, path as os_path
from scrolledframe import ScrolledFrame as SFrame
from tkinter.ttk import Button, Separator, Style
from changecolor import lighten
from typing import Union as U

from .constants import *


class GUI(Tk):
    data: dict[str, dict[str, U[Frame, Spinbox, Label, str]]]
    defBg: str
    litBg: str
    checkValid: tuple[str, str]
    curRow: int
    scrFrm: SFrame
    maxNum: int

    def __init__(self):
        Tk.__init__(self)
        self.title('Change Order')
        self.geometry(f'{WIDTH}'
                      f'x{HEIGHT}'
                      f'+{(self.winfo_screenwidth() - WIDTH) // 2}'
                      f'+{(self.winfo_screenheight() - HEIGHT) // 2}')
        # init vars
        self.data = dict()
        self.defBg = self.cget('bg')
        self.litBg = lighten(color=self.winfo_rgb(self.defBg),
                             percent=5,
                             inputtype='RGB',
                             bitdepth=16)
        self.checkValid = (self.register(self.validateRange), '%P')
        self.curRow = int()
        # build window
        self.createFrame()
        self.insertData()

    def validateRange(self, val: str) -> bool:
        if not val or (val.isdigit() and 0 < int(val) <= self.maxNum):
            return True
        else:
            return False

    def createFrame(self) -> None:
        # create save button
        saveBtn = Button(master=self,
                         text="Save",
                         command=self.submit)
        saveBtn.place(anchor='s',
                      relx=0.5,
                      rely=1,
                      y=(-PAD))
        # create containing frame
        lfrm = LFrame(master=self,
                      text="Anime List")
        lfrm.place(anchor='n',
                   relx=0.5,
                   rely=0,
                   y=PAD,
                   relwidth=1,
                   width=(-PAD * 2),
                   relheight=1,
                   height=(-PAD * 3 - saveBtn.winfo_reqheight()))
        # create scrolling frame
        self.scrFrm = SFrame(master=lfrm,
                             scrollbars='e',
                             padding=PAD,
                             bd=0)
        self.scrFrm.place(anchor='nw',
                          relx=0,
                          relwidth=1,
                          rely=0,
                          relheight=1)
        self.scrFrm.columnconfigure(0, weight=1)

    def insertData(self) -> None:
        folders = [f for f in os_listdir() if os_path.isdir(f)]
        lastRow = int()
        new: list[str] = list()
        for fol in folders:
            n = fol[:2]
            if n.isdigit():
                lastRow = max(lastRow, (int(n) + 1))
                self.data[n] = dict(name=fol[2:].lstrip('. '),
                                    path=fol)
            else:
                new.append(fol)
        self.maxNum = max(len(folders), (lastRow - 1))
        Style().configure('TSeparator', background='red')
        for n in range(len(folders)):
            s = Separator(master=self.scrFrm,
                          orient='horizontal')
            s.grid(column=0,
                   row=(n + 1),
                   sticky='ew',
                   pady=3)
        for num, kwargs in self.data.items():
            self.fillInfo(num, **kwargs)
        for i, fol in enumerate(new):
            num = f'{(lastRow + i):02d}'
            self.fillInfo(num, fol, fol, False)

    def fillInfo(self, rowLbl: str, name: str, path: str, numbered: bool = True) -> None:
        curRow = int(rowLbl)
        bg = self.litBg if (curRow % 2) else self.defBg
        # create container
        frm = Frame(master=self.scrFrm,
                    bg=bg,
                    relief='sunken',
                    bd=1)
        frm.columnconfigure(1, weight=1)
        frm.grid(column=0,
                 row=curRow,
                 sticky='ew')
        # create spinbox
        sbox = Spinbox(master=frm,
                       width=3,
                       bg=bg,
                       font=FONT,
                       format='%02.0f',
                       takefocus=False,
                       from_=1,
                       to=self.maxNum,
                       validate='key',
                       validatecommand=self.checkValid)
        sbox.grid(column=0,
                  row=0)

        def commit(_=None, f=frm, s=sbox): self.updateList(f, s)
        def cancel(_=None, f=frm, s=sbox): self.cancelChange(f, s)
        sbox.config(command=commit)
        sbox.delete(0, 'end')
        if numbered:
            sbox.insert(0, rowLbl)
        sbox.bind('<Return>', commit)
        sbox.bind('<FocusOut>', cancel)
        sbox.bind('<Escape>', cancel)
        # create name label
        lbl = Label(master=frm,
                    text=name,
                    font=FONT,
                    bg=bg)
        lbl.grid(column=1,
                 row=0,
                 sticky='w')
        # save to data dict
        self.data[rowLbl] = dict(frm=frm,
                                 sbox=sbox,
                                 lbl=lbl,
                                 name=name,
                                 path=path)

    @staticmethod
    def cancelChange(frm: Frame, sbox: Spinbox) -> None:
        oldRow = f"{frm.grid_info()['row']:02d}"
        if oldRow != sbox.get():
            sbox.delete(0, 'end')
            sbox.insert(0, oldRow)

    def updateList(self, frm: Frame, sbox: Spinbox) -> None:
        # get spinbox value
        num = sbox.get()
        if not num:
            self.cancelChange(frm, sbox)
            return
        elif len(num) == 1:
            sbox.insert(0, '0')
        # get info
        moveTo = int(num)
        start = frm.grid_info()['row']
        oldInfo = self.data.pop(f'{start:02d}')
        # move
        curRow = f'{moveTo:02d}'
        if curRow in self.data:
            nmin = min(start, moveTo)
            nmax = max(start, moveTo)
            add = 1 if moveTo < start else -1
            change = {n: v for n, v in self.data.items()
                      if nmin <= int(n) <= nmax}
            while curRow in change:
                d = change[curRow]
                newRow = (int(curRow) + add)
                curRow = f'{newRow:02d}'
                bg = self.litBg if (newRow % 2) else self.defBg
                # update frame
                d['frm'].grid(row=newRow)
                d['frm'].config(bg=bg)
                # update spinbox
                d['sbox'].delete(0, 'end')
                d['sbox'].insert(0, curRow)
                d['sbox'].config(bg=bg)
                # update label
                d['lbl'].config(bg=bg)
                self.data[curRow] = d
        bg = self.litBg if (moveTo % 2) else self.defBg
        frm.grid(row=moveTo)
        frm.config(bg=bg)
        sbox.config(bg=bg)
        oldInfo['lbl'].config(bg=bg)
        self.data[f'{moveTo:02d}'] = oldInfo

    def submit(self):
        for row, info in self.data.items():
            oldPath: str = info['path']
            newPath = f"{info['sbox'].get()}. {info['name']}"
            if oldPath != newPath:
                os_rename(oldPath, newPath)
                self.data[row]['path'] = newPath
        mbox.showinfo("Complete", "Files have been successfully renamed")
