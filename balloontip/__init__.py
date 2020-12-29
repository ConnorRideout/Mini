# -- coding: utf-8 --

import win32gui as gui32
import win32con as con32
from sys import executable as py_exe
from os import path as os_path, system as os_sys
from time import sleep as t_sleep


class balloon_tip:
    def __init__(self, title, msg, timeout=7, iconPath=None):
        def showError(msg): return os_sys(
            """start "" powershell -command "write-host \\"{}\\"; pause""".format(
                os_path.basename(__file__) + "`n{}`n".format("="*25) + msg))
        message_map = {con32.WM_DESTROY: self.OnDestroy, }
        # Register the Window class
        wc = gui32.WNDCLASS()
        self.hinst = wc.hInstance = gui32.GetModuleHandle(None)
        wc.lpszClassName = 'PythonTaskbar'
        wc.lpfnWndProc = message_map  # could also specify a wndproc
        self.classAtom = gui32.RegisterClass(wc)
        # Create the Window
        style = con32.WS_OVERLAPPED | con32.WS_SYSMENU
        self.hwnd = gui32.CreateWindow(self.classAtom, 'Taskbar', style, 0,
                                       0, con32.CW_USEDEFAULT, con32.CW_USEDEFAULT, 0, 0, self.hinst, None)
        gui32.UpdateWindow(self.hwnd)

        icon_flags = con32.LR_LOADFROMFILE | con32.LR_DEFAULTSIZE
        def loadImg(i): return gui32.LoadImage(
            self.hinst, i, con32.IMAGE_ICON, 0, 0, icon_flags)
        tryImages = [lambda: loadImg(os_path.abspath(iconPath)),
                     lambda: gui32.LoadIcon(self.hinst, 1),
                     lambda: loadImg(
                         os_path.join(os_path.dirname(py_exe), "DLLs\\py.ico")),
                     lambda: gui32.LoadIcon(0, con32.IDI_APPLICATION)
                     ]
        for index, getImg in enumerate(tryImages):
            try:
                self.hicon = getImg()
                break
            except Exception as e:
                if 0 < index < 3:
                    continue
                elif iconPath or index == 3:
                    showError(e)

        flags = gui32.NIF_ICON | gui32.NIF_MESSAGE | gui32.NIF_TIP
        nid = (self.hwnd, 0, flags, con32.WM_USER+20, self.hicon, "tooltip")
        gui32.Shell_NotifyIcon(gui32.NIM_ADD, nid)
        gui32.Shell_NotifyIcon(gui32.NIM_MODIFY, (self.hwnd, 0, gui32.NIF_INFO,
                                                  con32.WM_USER + 20, self.hicon, "Balloon  tooltip", msg, 200, title))
        if timeout:
            t_sleep(timeout)
            gui32.DestroyWindow(self.hwnd)
            gui32.UnregisterClass(self.classAtom, self.hinst)

    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        gui32.Shell_NotifyIcon(gui32.NIM_DELETE, nid)
        gui32.PostQuitMessage(0)  # Terminate the app
