import os
from fileinput import input as fileinput
from operator import ne as NotEqual
from re import search as reSearch
from threading import Thread
from time import sleep
from tkinter import Tk, Toplevel, Menu, Canvas
from tkinter.ttk import Style, Label, Frame

from PIL import Image
from pywinauto import timings as winTimings
from pywinauto.application import Application
from trayicon import TrayIconBuilder as TrayIcon
from win32api import GetMonitorInfo, MonitorFromPoint
from win32com.client import Dispatch
from win32gui import FindWindow, SetWindowLong

# PATH VARIABLES
SPOTIFY_EXE = "C:\\Users\\Cryden\\AppData\\Roaming\\Spotify\\Spotify.exe"
SPOTIFY_AHK = "C:\\Admin Tools\\Python\\MyScripts\\spotifyplayer\\SpotifyAHK.exe"
SPOTIFY_LINK = "C:\\Users\\Cryden\\AppData\\Roaming\\Microsoft\\Internet Explorer\\Quick Launch\\User Pinned\\TaskBar\\Spotify.lnk"
TRAY_ICON_IMG = "C:\\Admin Tools\\Python\\MyScripts\\spotifyplayer\\SpotifyPlayer_icon.ico"

# TEXT VARIABLES
WIN_TITLE = "Spotify Premium"
STARTUP_TEXT1 = "    ~Welcome!~    "
STARTUP_TEXT2 = "   ~Starting up~   "
SHUTDOWN_TXT1 = "    ~Goodbye!~     "
SHUTDOWN_TXT2 = "~Shutting down~"
FONT_DEF = "Calibri 18"

# SIZE VARIABLES
LBL_W = 175
BTN_SIZE = 30
OFFSET_X = 275
OFFSET_X_STEP = 25
OFFSET_Y = 0
OFFSET_Y_STEP = 1


class SpotifyApp:
    def __init__(self):
        def closeOld(): return Application().connect(title=WIN_TITLE).kill(soft=True)
        try:
            closeOld()
        except Exception:
            pass

        self.app = Application().start(SPOTIFY_EXE)
        self.win, i = None, 0
        while not self.win:
            try:
                self.win = self.app.top_window().top_level_parent()
                winTimings.wait_until(5, 0.5, self.win.window_text, WIN_TITLE)
            except Exception:
                if (i := i+1) == 2:
                    try:
                        closeOld()
                        self.app = Application().start(SPOTIFY_EXE)
                    except Exception:
                        self.showError()
                elif i == 5:
                    self.showError()
                    i = 0

    def showError(self):
        if os.system('nircmd qboxcomtop "Python can\'t seem to hook Spotify. Would you like to keep trying?`n(Note that Spotify can be open but not playing)" "Error" returnval 1'):
            return
        else:
            raise SystemExit


class ScreenInfo:
    def __init__(self):
        monInfo = GetMonitorInfo(MonitorFromPoint((0, 0)))
        screen = {i: monInfo.get('Monitor')[n]
                  for n, i in enumerate(['x', 'y', 'w', 'h'])}
        self.taskbarH = screen['h']-monInfo.get('Work')[3]
        self.X = round(screen['w'] - LBL_W*2 - BTN_SIZE*3 - OFFSET_X)
        self.Y = round(screen['h'] - max(BTN_SIZE,
                                         (self.taskbarH+BTN_SIZE)/2) - OFFSET_Y)


class Marquee(Thread):
    def __init__(self, *args):
        Thread.__init__(self)
        self.running = True
        self.shortW, self.lbl = args
        self.longW, self.curX = [self.lbl.winfo_reqwidth(), 0]

    def run(self):
        try:
            while self.running:
                self.lbl.place(x=self.curX, rely=0.4, anchor='w')
                self.curX -= 1
                if abs(self.curX) == self.longW-self.shortW:
                    self.curX = 0
                    sleep(1.5)
                else:
                    sleep(0.025)
        finally:
            return


class PlayerMenu:
    def __init__(self, root):
        self.root = root
        self.mainmenu = Menu(root, tearoff=0)
        self.movemenu = Menu(self.mainmenu, tearoff=0)
        self.movemenu.add_command(
            label="Move (Horizontal)", command=lambda: self.movePlayer("X"))
        self.movemenu.add_command(
            label="Move (Vertical)", command=lambda: self.movePlayer("Y"))
        self.movemenu.add_separator()
        self.movemenu.add_command(
            label="Save Position", command=self.savePos, state='disabled')
        self.movemenu.add_command(
            label="Reset Position", command=self.resetPos, state='disabled')
        self.mainmenu.add_cascade(label="Move Player", menu=self.movemenu)
        self.mainmenu.add_separator()
        self.mainmenu.add_command(
            label="Exit Spotify", command=root.spotify.win.close)
        self.mainmenu.add_command(
            label="Close Player", command=root.closePlayer)
        self.mainmenu.add_separator()
        self.mainmenu.add_command(
            label="Minimize Player", command=root.trayicon.minimizePlayer)

    def movePlayer(self, axis):
        self.axis = axis
        [c.unbind('<ButtonRelease-1>') for c in self.root.mediaBtns]
        self.root.config(cursor="fleur")
        self.startX, self.startY = [
            round(self.root.winfo_rootx()), round(self.root.winfo_rooty())]
        self.root.bind('<Button-3>', self.stopMoving)
        self.root.bind('<Button-1>', self.on_click)
        self.root.bind('<B1-Motion>', self.on_move)
        self.root.bind('<ButtonRelease-1>', self.on_release)

    def on_click(self, event):
        self.xy = [event.x, event.y]
        self.tw = Toplevel(self.root, bg='white', bd=3, relief='groove')
        self.tw.attributes('-transparentcolor', 'white', '-topmost', 1)
        self.tw.overrideredirect(1)
        self.tw.geometry(self.root.geometry())

    def on_move(self, event):
        cX, cY = self.xy
        self.dX = OFFSET_X_STEP * \
            round((event.x-cX)/OFFSET_X_STEP) if self.axis == "X" else 0
        self.dY = 0 if self.axis == "X" else OFFSET_Y_STEP * \
            round((event.y-cY)/OFFSET_Y_STEP)
        self.tw.geometry('+{}+{}'.format(self.startX +
                                         self.dX, self.startY+self.dY))

    def on_release(self, event):
        global OFFSET_X, OFFSET_Y
        if self.tw.geometry() != self.root.geometry():
            self.root.geometry(self.tw.geometry())
            OFFSET_X -= self.dX
            OFFSET_Y -= self.dY
            self.movemenu.entryconfig(4, state='normal')
            self.movemenu.entryconfig(5, state='normal')
        self.tw.destroy()
        self.stopMoving()

    def stopMoving(self, event=None):
        self.root.unbind('<Button-3>')
        self.root.unbind('<Button-1>')
        self.root.unbind('<B1-Motion>')
        self.root.unbind('<ButtonRelease-1>')
        [c.bind('<ButtonRelease-1>', lambda e, n=n: self.root.sendInput(e, n))
         for n, c in enumerate(self.root.mediaBtns)]
        self.root.config(cursor="arrow")

    def savePos(self):
        self.movemenu.entryconfig(4, state='disabled')
        self.movemenu.entryconfig(5, state='disabled')
        change = {'OFFSET_X': OFFSET_X, 'OFFSET_Y': OFFSET_Y}
        for line in fileinput(__file__, inplace=True):
            line = line.rstrip('\r\n')
            out = '{} = {}'.format(s, r) if (r := change.get(
                s := line.split(' = ')[0])) != None else line
            print(out)

    def resetPos(self):
        self.movemenu.entryconfig(4, state='disabled')
        self.movemenu.entryconfig(5, state='disabled')
        self.root.focus_set()
        self.root.geometry(
            '+{}+{}'.format(self.root.screen.X, self.root.screen.Y))


class TrayMenu(TrayIcon):
    def __init__(self, root):
        self.root, self.is_mini = root, False
        TrayIcon.__init__(self, 'Spotify Player Icon', TRAY_ICON_IMG,
                          [("Exit Spotify", root.spotify.win.close),
                           ("Close Player", root.closePlayer),
                           'Separator',
                           ("Minimize Player", self.minimizePlayer,
                            {'checked': lambda i: self.is_mini}),
                           ("Set Topmost", root.setChild, {'default': True})])

    def minimizePlayer(self, i=None, mItem=None):
        if (mItem and mItem.checked) or (not mItem and self.is_mini):
            self.root.deiconify()
            self.is_mini = False
        else:
            self.root.withdraw()
            self.is_mini = True


class GUI(Tk):
    def __init__(self):
        # Initialize Variables
        self.spotify = SpotifyApp()
        self.screen = ScreenInfo()
        self.isPlaying = False
        self.showPlayer = True
        self.doClose = True
        # Initialize Tkinter
        Tk.__init__(self)
        self.trayicon = TrayMenu(self)
        self.trayicon.start()
        pMenu = PlayerMenu(self)
        # Set Tkinter options
        self.title('Spotify Taskbar Player')
        self.protocol("WM_DELETE_WINDOW", self.closePlayer)
        self.attributes('-transparentcolor', 'black', '-topmost', True)
        self.overrideredirect(True)
        self.config(bg='black')
        self.resizable(False, False)
        self.geometry('{}x{}+{}+{}'.format(BTN_SIZE*3 + LBL_W *
                                           2, BTN_SIZE, self.screen.X, self.screen.Y))
        self.option_add('*Canvas.background', 'black')
        Style().configure('TFrame', background='black')
        Style().configure('TLabel', font=FONT_DEF, background='black', foreground='white')
        # bind keys
        self.bind_all('<MouseWheel>', self.sendInput)
        self.bind_all('<ButtonRelease-3>',
                      lambda e: pMenu.mainmenu.post(e.x_root, self.winfo_rooty()))
        # Make GUI child of taskbar
        self.setChild()
        # Build GUI elements
        self.createPlayer()
        self.setLabels()
        # Start threads
        Thread(target=self.waitForExit, daemon=True).start()
        Thread(target=self.updateText, daemon=True).start()

    def setChild(self):
        self.update_idletasks()
        self.hwnd = FindWindow(None, 'Spotify Taskbar Player')
        SetWindowLong(self.hwnd, -8, FindWindow('Shell_TrayWnd', None))

    def createPlayer(self):
        # Create Buttons
        pvBtn = [23, 124, 142, 56, 142, 89, 199,
                 54, 199, 194, 142, 162, 142, 196]
        stBtn = [70, 70, 180, 70, 180, 180, 70, 180]
        plBtn = [83, 54, 204, 124, 83, 196]
        nxBtn = [225, 124, 106, 192, 106, 159,
                 49, 194, 49, 54, 106, 86, 106, 52]
        self.mediaBtns = [self.createButton(i, [round(
            BTN_SIZE*n/248) for n in lst]) for i, lst in enumerate([pvBtn, stBtn, plBtn, nxBtn])]
        self.prevBtn, self.stopBtn, self.playBtn, self.nextBtn = self.mediaBtns
        # Place everything
        self.prevBtn.grid(row=0, column=0)

        (frmTrk := Frame(self, height=BTN_SIZE, width=LBL_W)).grid(row=0, column=1)
        self.track = STARTUP_TEXT1
        self.trackLbl = Label(frmTrk)

        self.stopBtn.grid(row=0, column=2)
        self.stopBtn.grid_remove()
        self.playBtn.grid(row=0, column=2)

        (frmArt := Frame(self, height=BTN_SIZE, width=LBL_W)).grid(row=0, column=3)
        self.artist = STARTUP_TEXT2
        self.artistLbl = Label(frmArt)

        self.nextBtn.grid(row=0, column=4)

    def createButton(self, i, coords):
        cnv = Canvas(self, height=BTN_SIZE, width=BTN_SIZE)
        cir = cnv.create_oval(0, 0, BTN_SIZE-1, BTN_SIZE-1, outline='white')
        poly = cnv.create_polygon(*coords, outline='white', fill='white')
        cnv.bind('<Enter>', lambda e, c=cnv, o=cir, p=poly: [c.itemconfig(
            o, outline='lightgray'), c.itemconfig(p, outline='lightgray', fill='lightgray')])
        cnv.bind('<Leave>', lambda e, c=cnv, o=cir, p=poly: [c.itemconfig(
            o, outline='white'), c.itemconfig(p, outline='white', fill='white')])
        cnv.bind('<ButtonRelease-1>', lambda e, n=i: self.sendInput(e, n))
        return cnv

    def sendInput(self, event, btn=None):
        mini = False
        if self.spotify.win.is_minimized():
            self.spotify.win.restore()
            mini = True
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
                pass
        else:
            if event.delta > 0:
                self.spotify.win.send_keystrokes('^{UP}')
            else:
                self.spotify.win.send_keystrokes('^{DOWN}')
        if mini:
            self.spotify.win.minimize()

    def chngToStopped(self):
        self.stopBtn.grid_remove()
        self.playBtn.grid()
        self.isPlaying = False

    def chngToPlaying(self):
        self.playBtn.grid_remove()
        self.stopBtn.grid()
        self.isPlaying = True

    def stopMarquees(self):
        try:
            self.trackMarquee.running = False
            self.trackMarquee.join()
        except Exception:
            pass
        try:
            self.artistMarquee.running = False
            self.artistMarquee.join()
        except Exception:
            pass

    def setLabels(self):
        self.stopMarquees()
        # set labels
        self.trackLbl.config(text=self.track)
        self.trackLbl.place(x=0, rely=0.45, anchor='w')
        self.artistLbl.config(text=self.artist)
        self.artistLbl.place(x=0, rely=0.45, anchor='w')
        self.update_idletasks()
        # track marquee
        trackW = self.trackLbl.winfo_reqwidth()
        if trackW >= LBL_W:
            self.trackLbl.config(text=self.track+' '*20+self.track)
            self.trackMarquee = Marquee(trackW, self.trackLbl)
            self.trackMarquee.start()
        # artist marquee
        artistW = self.artistLbl.winfo_reqwidth()
        if artistW >= LBL_W:
            self.artistLbl.config(text=self.artist+' '*20+self.artist)
            self.artistMarquee = Marquee(artistW, self.artistLbl)
            self.artistMarquee.start()

    def updateText(self):
        def initText():
            try:
                winTimings.wait_until(
                    5, 0.5, self.spotify.win.window_text, WIN_TITLE)
                sleep(2)
                # make sure the volume isn't 0
                self.spotify.win.send_keystrokes('^{UP}')
                self.spotify.win.send_keystrokes('^+{DOWN}')  # mute
                sleep(0.5)
                self.spotify.win.send_keystrokes('{SPACE}')  # start playing
                try:
                    # timeout (sec), retry interval, func, value, operation
                    winTimings.wait_until(
                        5, 0.1, self.spotify.win.window_text, WIN_TITLE, op=NotEqual)
                    sleep(0.1)
                    title = self.spotify.win.window_text()
                except Exception:
                    title = '  -  '
                self.spotify.win.send_keystrokes('{SPACE}')  # stop playing
                sleep(0.1)
                self.spotify.win.send_keystrokes(
                    '^{UP 8}')  # set volume to mid
            except Exception:
                title = '  -  '
            return title

        def tryToUpdate(text):
            if (new := reSearch(r'^(.*?) \- (.*)$', text)):
                self.artist = new.group(1)
                self.track = new.group(2)
                self.setLabels()

        title = initText()
        # Loop for updates
        while True:
            sleep(0.5)
            # perform continuance checks
            if not self.showPlayer:
                break
            if (curTitle := self.spotify.win.window_text()) == title:
                continue
            # else update player
            if curTitle == WIN_TITLE:  # WAS JUST PAUSED
                if self.isPlaying:  # play status needs to be updated
                    self.chngToStopped()
                if self.track not in title:  # track needs to be updated
                    tryToUpdate(title)
            elif title == WIN_TITLE:  # WAS JUST UNPAUSED
                if not self.isPlaying:  # play status needs to be updated
                    self.chngToPlaying()
                if self.track not in curTitle:  # track needs to be updated
                    tryToUpdate(curTitle)
            else:  # NEW TRACK
                tryToUpdate(curTitle)
            title = curTitle

    def closePlayer(self):
        self.showPlayer = False
        self.track, self.artist = SHUTDOWN_TXT1, SHUTDOWN_TXT2
        self.setLabels()
        self.trayicon.stop()
        sleep(2)
        self.withdraw()

    def waitForExit(self):
        self.spotify.app.wait_for_process_exit(
            timeout=999*999, retry_interval=1)
        if self.showPlayer:
            self.closePlayer()
        changeShortcut(SPOTIFY_AHK)
        self.destroy()
        raise SystemExit


def changeShortcut(newPath):
    link = Dispatch("WScript.Shell").CreateShortcut(SPOTIFY_LINK)
    link.Targetpath = newPath
    link.save()


if __name__ == '__main__':
    try:
        changeShortcut(SPOTIFY_EXE)
        root = GUI()
        root.mainloop()
    except Exception:
        from traceback import format_exc
        os.system("""nircmd infobox "{}" "ERROR" """.format(
            format_exc().replace('\n', '~n')))
        # os.system("""start "" powershell -command "write-host \\"{}\\""; pause""".format(format_exc().replace('\n', '`n')))
