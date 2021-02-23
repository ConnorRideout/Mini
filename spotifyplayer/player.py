from tkinter import Tk, Canvas, StringVar
from tkinter.ttk import Style, Label, Frame
from threading import Thread
from time import sleep

from win32gui import FindWindow, SetWindowLong, SetForegroundWindow

from .spotifyapp import SpotifyApp
from .playermenu import PlayerMenu
from .marquee import Marquee
from .waitforexit import WaitExit
from .watchappmini import WatchMini
from .watchforupdate import WatchUpdate
from .lib.constants import *

if TYPE_CHECKING:
    from typing import Optional as O
    from threading import Thread
    from tkinter import Event


class GUI(Tk):
    def __init__(self):
        # initialize tkinter
        self.screen = Screen()
        Tk.__init__(self)
        self.config(bg='black')
        self.title(APP_TITLE)
        self.protocol("WM_DELETE_WINDOW",
                      self.closePlayer)
        self.attributes('-transparentcolor', 'black',
                        '-topmost', True)
        self.overrideredirect(True)
        self.resizable(False, False)
        self.geometry(f'{self.screen.appW}'
                      f'x{self.screen.appH}'
                      f'+{self.screen.X}'
                      f'+{self.screen.Y}')
        # initialize variables
        self.spotifyMini = False
        self.isPlaying = False
        self.track = StringVar(self)
        self.track.set(STARTUP_TEXT_LEFT)
        self.artist = StringVar(self)
        self.artist.set(STARTUP_TEXT_RIGHT)
        self.marquees: "list[Thread]" = list()
        # set default styles
        self.option_add('*Canvas.background', 'black')
        Style().configure('TFrame', background='black')
        Style().configure('TLabel',
                          font=FONT_DEF,
                          background='black',
                          foreground='white')
        # make GUI child of taskbar
        self.setChild()
        # build GUI elements
        self.createPlayer()
        self.updateLabels()
        pMenu = PlayerMenu(self)
        # start spotify
        self.spotify = SpotifyApp()
        # start threads
        WaitExit(self).start()
        self.threads: "list[Thread]" = [WatchMini(self), WatchUpdate(self)]
        for thread in self.threads:
            thread.start()
        # re-enable the spotify window
        self.spotify.showSpotify()
        self.spotify.win.minimize()
        sleep(0.1)
        self.spotify.win.restore()
        # bind keys
        self.bind_all('<MouseWheel>', self.sendInput)
        self.bind_all('<ButtonRelease-3>', pMenu.show)

    def setChild(self) -> None:
        self.update_idletasks()
        self.hwnd = FindWindow(None, 'Spotify Taskbar Player')
        self.trayhwnd = FindWindow('Shell_TrayWnd', None)
        SetWindowLong(self.hwnd, -8, self.trayhwnd)

    def createPlayer(self) -> None:
        # create buttons
        self.btns: dict[str, Canvas] = dict()
        for i, (btn, coords) in enumerate(BTN_POINTS.items()):
            self.btns[btn] = self.createButton(i, coords)
        # create labels
        frmTrk = Frame(self,
                       height=BTN_SIZE,
                       width=LBL_W)
        self.trackLbl = Label(frmTrk,
                              textvariable=self.track)

        frmArt = Frame(self,
                       height=BTN_SIZE,
                       width=LBL_W)
        self.artistLbl = Label(frmArt,
                               textvariable=self.artist)
        # place everything
        self.btns['prev'].grid(column=0,
                               row=0)

        frmTrk.grid(column=1,
                    row=0)
        self.trackLbl.place(x=0,
                            rely=0.45,
                            anchor='w')

        self.btns['stop'].grid(column=2,
                               row=0)
        self.btns['stop'].grid_remove()
        self.btns['play'].grid(column=2,
                               row=0)

        frmArt.grid(column=3,
                    row=0)
        self.artistLbl.place(x=0,
                             rely=0.45,
                             anchor='w')

        self.btns['next'].grid(column=4,
                               row=0)

    def createButton(self, i: int, coords: list[int]) -> Canvas:
        def onEnter(thisCnv: Canvas, thisCir, thisPoly, clr: str = 'lightgray'):
            thisCnv.itemconfig(thisCir, outline=clr)
            thisCnv.itemconfig(thisPoly, outline=clr, fill=clr)

        def onExit(*args): onEnter(*args, 'white')

        cnv = Canvas(self,
                     height=BTN_SIZE,
                     width=BTN_SIZE)
        # create outline
        cir = cnv.create_oval(0, 0, BTN_SIZE - 1, BTN_SIZE - 1,
                              outline='white')
        # create symbol
        poly = cnv.create_polygon(*coords,
                                  outline='white',
                                  fill='white')
        # bind all
        cnv.bind('<Enter>',
                 lambda _, args=[cnv, cir, poly]: onEnter(*args))
        cnv.bind('<Leave>',
                 lambda _, args=[cnv, cir, poly]: onExit(*args))
        cnv.bind('<ButtonRelease-1>',
                 lambda e, n=i: self.sendInput(e, n))
        return cnv

    def sendInput(self, event: "Event", btn: "O[int]" = None) -> None:
        if isinstance(btn, int):
            if (0 <= event.x <= BTN_SIZE) and (0 <= event.y <= BTN_SIZE) and (0 <= btn <= 3):
                if btn == 0:
                    self.spotify.win.send_keystrokes('^{LEFT}')
                elif btn == 1 or btn == 2:
                    self.spotify.win.send_keystrokes('{SPACE}')
                    self.chngToStopped() if self.isPlaying else self.chngToPlaying()
                else:
                    self.spotify.win.send_keystrokes('^{RIGHT}')
        else:
            if event.delta > 0:
                self.spotify.win.send_keystrokes('^{UP}')
            elif event.delta < 0:
                self.spotify.win.send_keystrokes('^{DOWN}')
        if self.spotifyMini and self.spotify.win.has_focus():
            try:
                SetForegroundWindow(DESKTOP_HWND)
            except Exception:
                pass

    def chngToStopped(self) -> None:
        self.isPlaying = False
        self.btns['stop'].grid_remove()
        self.btns['play'].grid()

    def chngToPlaying(self) -> None:
        self.isPlaying = True
        self.btns['play'].grid_remove()
        self.btns['stop'].grid()

    def stopMarquees(self) -> None:
        while self.marquees:
            thread = self.marquees.pop()
            try:
                thread.running = False
                thread.join()
            except Exception:
                pass

    def updateLabels(self) -> None:
        self.stopMarquees()
        # set labels
        self.trackLbl.place(x=0)
        self.artistLbl.place(x=0)
        # track marquee
        trackW = self.trackLbl.winfo_reqwidth()
        if trackW >= LBL_W:
            txt = self.track.get()
            self.track.set(f'{txt}{" "*20}{txt}')
            self.marquees.append(Marquee(trackW, self.trackLbl))
        # artist marquee
        artistW = self.artistLbl.winfo_reqwidth()
        if artistW >= LBL_W:
            txt = self.artist.get()
            self.artist.set(f'{txt}{" "*20}{txt}')
            self.marquees.append(Marquee(artistW, self.artistLbl))
        for thread in self.marquees:
            thread.start()
        self.update_idletasks()

    def updateText(self, title: str) -> None:
        try:
            art, trk = title.split(' - ', 1)
        except Exception:
            return
        self.artist.set(art)
        self.track.set(trk)
        self.updateLabels()

    def closePlayer(self) -> None:
        if self.winfo_viewable():
            self.track.set(SHUTDOWN_TXT_LEFT)
            self.artist.set(SHUTDOWN_TXT_RIGHT)
            self.updateLabels()
            sleep(2)
            self.withdraw()
            self.stopMarquees()
            for thread in self.threads:
                try:
                    thread.running = False
                    thread.join()
                except Exception:
                    pass
