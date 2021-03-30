from subprocess import run, CREATE_NEW_CONSOLE
from sys import executable as py_exe
from typing import (Optional as O,
                    Union as U)
from pywintypes import HANDLE
from re import sub as re_sub
from pathlib import Path
import win32gui as gui32
import win32con as con32
from time import sleep

py_icon = Path(py_exe).parent.joinpath("DLLs", "py.ico")


class Balloontip:
    """Creates a popup balloontip on Windows 10

Methods
-------
onClick() -> None
    Called when the user clicks the balloontip. Override this method in subclasses
onDoubleClick() -> None
    Called when the user double-clicks the balloontip. Override this method in subclasses
onRightClick() -> None
    Called when the user right-clicks the balloontip. Override this method in subclasses
"""

    title: str
    msg: str
    timeout: U[int, float]
    icon: str
    _hinst: int
    _classAtom: int
    _hwnd: int
    _infoFlags: int
    _hicon: HANDLE

    def __init__(self, title: str, msg: str, timeout: U[int, float] = 6,
                 icon: O[str] = 'default', silent: bool = False):
        """\
        Parameters
        ----------
        title : str
            The text to display at the top of the balloontip
        msg : str
            The text to display as the body of the balloontip
        timeout : int | float, optional (default is 6)
            Seconds to keep the balloontip active. After ~4 seconds it is put into the action center
        icon : str, optional (default is "default")
            The balloontip's icon. One of "default", "info", "warning", "error", or an *.ico image file path
        silent : bool, optional (default is False)
            Whether to play a sound when the balloontip is displayed
        """
        self.title = title
        self.msg = msg
        self.timeout = timeout
        self.icon = icon
        self._run(silent)

    def _getIcon(self) -> bool:
        def getArgs(icon): return (self._hinst, icon, con32.IMAGE_ICON, 0, 0,
                                   con32.LR_LOADFROMFILE | con32.LR_DEFAULTSIZE)
        if Path(self.icon).exists():
            p = Path(self.icon).resolve()
            try:
                self._hicon = gui32.LoadImage(*getArgs(p))
                return True
            except Exception as e:
                self._showError(e, 'continue')

        imgFuncs = [
            lambda: gui32.LoadIcon(self._hinst, 1),
            lambda: gui32.LoadImage(*getArgs(py_icon)),
            lambda: gui32.LoadIcon(0, con32.IDI_APPLICATION)
        ]
        for i, getImg in enumerate(imgFuncs):
            try:
                self._hicon = getImg()
                break
            except Exception as e:
                if i < 2:
                    continue
                else:
                    self._showError(e, 'exit')
                    return False
        if self.icon:
            dwInfoFlags = dict(INFO=gui32.NIIF_INFO,
                               WARNING=gui32.NIIF_WARNING,
                               ERROR=gui32.NIIF_ERROR)
            self._infoFlags |= dwInfoFlags.get(str(self.icon).upper(), 0)
        return True

    @staticmethod
    def _showError(msg: str, txt: str) -> None:
        brk = f"`n{'=' * 25}`n"
        msg = re_sub(r'(\"|\')',
                     r'`\1',
                     str(msg))
        print(str(msg))
        run(['powershell', 'Read-Host',
             (f'''Error in {Path(__file__).parent}{brk}'''
              f'''{msg}{brk}Press 'Return' to {txt}''')],
            creationflags=CREATE_NEW_CONSOLE)

    def _onDestroy(self, *_):
        nid = (self._hwnd, 0)
        gui32.Shell_NotifyIcon(gui32.NIM_DELETE, nid)
        gui32.PostQuitMessage(0)

    def _onTaskbarNotify(self, *_, lparam):
        if lparam == con32.WM_LBUTTONUP:
            self.onClick()
        elif lparam == con32.WM_LBUTTONDBLCLK:
            self.onDoubleClick()
        elif lparam == con32.WM_RBUTTONUP:
            self.onRightClick()
        return 1

    def _run(self, quiet: bool = False):
        message_map = {con32.WM_DESTROY: self._onDestroy,
                       con32.WM_USER + 20: self._onTaskbarNotify, }
        # register the window class
        wc = gui32.WNDCLASS()
        self._hinst = wc.hInstance = gui32.GetModuleHandle(None)
        wc.lpszClassName = 'PythonBalloontip'
        wc.lpfnWndProc = message_map
        self._classAtom = gui32.RegisterClass(wc)
        # create the window
        style = con32.WS_OVERLAPPED | con32.WS_SYSMENU
        self._hwnd = gui32.CreateWindow(self._classAtom, 'Taskbar', style, 0, 0, con32.CW_USEDEFAULT,
                                        con32.CW_USEDEFAULT, 0, 0, self._hinst, None)
        gui32.UpdateWindow(self._hwnd)
        try:
            timeout = float(self.timeout)
            if timeout <= 0:
                raise ValueError(
                    "the 'timeout' parameter must be greater than 0")
        except Exception as e:
            self._showError(e, 'exit')
            return
        self._infoFlags = gui32.NIIF_NOSOUND if quiet else 0
        if not self._getIcon():
            return
        flags = gui32.NIF_ICON | gui32.NIF_MESSAGE | gui32.NIF_TIP | gui32.NIF_INFO
        nid = (self._hwnd, 0, flags, con32.WM_USER + 20, self._hicon,
               "Balloontip", self.msg, 200, self.title, self._infoFlags)
        gui32.Shell_NotifyIcon(gui32.NIM_ADD, nid)
        sleep(timeout)
        gui32.DestroyWindow(self._hwnd)
        gui32.UnregisterClass(self._classAtom, self._hinst)

    def onClick(self):
        """Override in subclassess"""
        pass

    def onDoubleClick(self):
        """Override in subclassess"""
        pass

    def onRightClick(self):
        """Override in subclasses"""
        pass
