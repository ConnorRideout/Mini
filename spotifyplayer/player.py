from win32gui import FindWindow, SetWindowLong, SetForegroundWindow
from tkinter.ttk import Style, Label, Frame
from tkinter import Tk, Canvas, StringVar
from time import sleep


from .watchforupdate import WatchUpdate
from .watchappmini import WatchMini
from .spotifyapp import SpotifyApp
from .playermenu import PlayerMenu
from .waitforexit import WaitExit
from .marquee import Marquee
from .lib.constants import *

if TYPE_CHECKING:
    from tkinter import Event


class GUI(Tk):
    artist: StringVar
    artistLbl: Label
    btns: dict[str, Canvas]
    isPlaying: bool
    marquees: list[Marquee]
    screen = Screen()
    spotify: SpotifyApp
    spotifyMini: bool
    threads: tuple[WatchMini, WatchUpdate]
    track: StringVar
    trackLbl: Label

    def __init__(self):
        # initialize tkinter
        Tk.__init__(self)
        self.configure(bg=CLR_BG)
        self.title("Spotify Taskbar Player")
        self.protocol(name="WM_DELETE_WINDOW",
                      func=self.closePlayer)
        self.attributes('-transparentcolor', CLR_BG,
                        '-topmost', True)
        self.overrideredirect(True)
        self.resizable(False, False)
        self.geometry(f'{self.screen.appW}'
                      f'x{self.screen.appH}'
                      f'+{self.screen.X}'
                      f'+{self.screen.Y}')
        # set default colors/fonts
        self.option_add('*background', CLR_BG)
        Style().configure('.', background=CLR_BG)
        Style().configure('TLabel',
                          font=FONT_DEF,
                          foreground=CLR_TEXT)
        self.buildPlayer()

    def buildPlayer(self) -> None:
        # initialize variables
        self.marquees = list()
        self.btns = dict()
        self.isPlaying = False
        self.spotifyMini = False
        self.track = StringVar()
        self.track.set(STARTUP_TEXT_L)
        self.artist = StringVar()
        self.artist.set(STARTUP_TEXT_R)
        # make GUI child of taskbar
        self.update_idletasks()
        hwnd = FindWindow(None, "Spotify Taskbar Player")
        trayhwnd = FindWindow('Shell_TrayWnd', None)
        SetWindowLong(hwnd, -8, trayhwnd)
        # build GUI elements
        self.createPlayer()
        self.updateLabels()
        pMenu = PlayerMenu(self)
        # start spotify
        self.spotify = SpotifyApp(self)
        # start threads
        WaitExit(self).start()
        self.threads = (WatchMini(self),
                        WatchUpdate(self, self.spotify.startTitle))
        for thread in self.threads:
            thread.start()
        # bind keys
        self.bind_all('<MouseWheel>', self.sendInput)
        self.bind_all('<ButtonRelease-3>', pMenu.show)

    def createPlayer(self) -> None:
        # create buttons
        for i, (btn, coords) in enumerate(BTN_POINTS.items()):
            self.btns[btn] = self.createButton(i, coords)
        self.btns['stop'].grid_remove()
        # create labels
        self.trackLbl = self.createLabel(1, self.track)
        self.artistLbl = self.createLabel(3, self.artist)

    def createButton(self, btn: int, coords: tuple[int]) -> Canvas:
        def hoverEvent(clr: str):
            cnv.itemconfigure(tagOrId=cir,
                              outline=clr)
            cnv.itemconfigure(tagOrId=poly,
                              outline=clr,
                              fill=clr)

        cnv = Canvas(master=self,
                     height=BTN_SIZE,
                     width=BTN_SIZE)
        # create outline
        cir: int = cnv.create_oval(0, 0, BTN_SIZE - 1, BTN_SIZE - 1,
                                   outline=CLR_BTNS)
        # create symbol
        poly: int = cnv.create_polygon(*coords,
                                       outline=CLR_BTNS,
                                       fill=CLR_BTNS)
        # bind hover/click
        cnv.bind(sequence='<Enter>',
                 func=lambda _: hoverEvent(CLR_BTN_HOVER))
        cnv.bind(sequence='<Leave>',
                 func=lambda _: hoverEvent(CLR_BTNS))
        cnv.bind(sequence='<ButtonRelease-1>',
                 func=lambda e, b=btn: self.sendInput(e, b))
        # place the canvas
        cnv.grid(column=[0, 2, 2, 4][btn],
                 row=0)
        return cnv

    def createLabel(self, col: int, svar: StringVar) -> Label:
        frm = Frame(master=self,
                    height=BTN_SIZE,
                    width=LBL_W)
        frm.grid(column=col,
                 row=0)
        lbl = Label(master=frm,
                    textvariable=svar)
        lbl.place(x=0,
                  rely=0.45,
                  anchor='w')
        return lbl

    def sendInput(self, event: "Event", btn: O[int] = None) -> None:
        if isinstance(btn, int):
            if (0 <= event.x <= BTN_SIZE) and (0 <= event.y <= BTN_SIZE) and (0 <= btn <= 3):
                if btn == 0:
                    self.spotify.win.send_keystrokes('^{LEFT}')
                elif 0 < btn < 3:
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

    def chngBtnState(self, state: str) -> None:
        self.isPlaying = (state == 'play')
        self.btns[state].grid_remove()
        self.btns['playstop'.replace(state, '')].grid()

    def chngToStopped(self): self.chngBtnState('stop')
    def chngToPlaying(self): self.chngBtnState('play')

    def stopMarquees(self) -> None:
        while self.marquees:
            thread = self.marquees.pop()
            try:
                thread.running = False
                if thread.is_alive():
                    thread.join(timeout=2)
            except Exception:
                pass

    def updateLabels(self) -> None:
        def setLbl(lbl: Label, svar: StringVar) -> None:
            lbl.place(x=0)
            lblW = lbl.winfo_reqwidth()
            if lblW >= LBL_W:
                txt = svar.get()
                svar.set(f'{txt}{SCROLL_BREAK}{txt}')
                self.marquees.append(Marquee(lblW, lbl))

        self.stopMarquees()
        # set labels
        setLbl(self.trackLbl, self.track)
        setLbl(self.artistLbl, self.artist)
        # start marquees
        for thread in self.marquees:
            thread.start()
        self.update_idletasks()

    def updateText(self, title: str) -> None:
        try:
            art, trk = title.split(' - ', 1)
        except ValueError:
            return
        self.artist.set(art)
        self.track.set(trk)
        self.updateLabels()

    def closePlayer(self) -> None:
        if self.winfo_viewable():
            self.track.set(SHUTDOWN_TXT_L)
            self.artist.set(SHUTDOWN_TXT_R)
            self.update_idletasks()
            self.updateLabels()
            sleep(2.5)
            self.stopMarquees()
            self.withdraw()
            for thread in self.threads:
                try:
                    thread.running = False
                    if thread.is_alive():
                        thread.join(timeout=2)
                except Exception:
                    continue
