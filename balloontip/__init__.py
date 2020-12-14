# -- coding: utf-8 --

import win32gui as wGui
import win32con as wCon
from sys import executable as py_exe
from os import path as pth, system as os_sys
from time import sleep as t_sleep

class balloon_tip:
	def __init__(self, title, msg, timeout=7, iconPath=None):
		showError = lambda msg: os_sys('nircmd infobox "{}" "{} Error:"'
									   .format(msg,pth.split(__file__)[1]))
		message_map = {wCon.WM_DESTROY: self.OnDestroy,}
		# Register the Window class
		wc = wGui.WNDCLASS()
		self.hinst = wc.hInstance = wGui.GetModuleHandle(None)
		wc.lpszClassName = 'PythonTaskbar'
		wc.lpfnWndProc = message_map # could also specify a wndproc
		self.classAtom = wGui.RegisterClass(wc)
		# Create the Window
		style = wCon.WS_OVERLAPPED | wCon.WS_SYSMENU
		self.hwnd = wGui.CreateWindow(self.classAtom, 'Taskbar', style, 0, 0,
									  wCon.CW_USEDEFAULT, wCon.CW_USEDEFAULT,
									  0, 0, self.hinst, None)
		wGui.UpdateWindow(self.hwnd)
		
		icon_flags = wCon.LR_LOADFROMFILE | wCon.LR_DEFAULTSIZE
		loadImg = lambda i: wGui.LoadImage(self.hinst, i, wCon.IMAGE_ICON, 0, 0, icon_flags)
		tryImages = [lambda: loadImg(pth.abspath(iconPath)),
					 lambda: wGui.LoadIcon(self.hinst, 1),
					 lambda: loadImg(pth.join(pth.dirname(py_exe), "DLLs\\py.ico")),
					 lambda: wGui.LoadIcon(0, wCon.IDI_APPLICATION)
					]
		for index,getImg in enumerate(tryImages):
			try:
				self.hicon = getImg()
				break
			except Exception as e:
				if 0 < index < 3: continue
				elif iconPath or index == 3: showError(e)
		
		flags = wGui.NIF_ICON | wGui.NIF_MESSAGE | wGui.NIF_TIP
		nid = (self.hwnd, 0, flags, wCon.WM_USER+20, self.hicon, "tooltip")
		wGui.Shell_NotifyIcon(wGui.NIM_ADD, nid)
		wGui.Shell_NotifyIcon(wGui.NIM_MODIFY, (self.hwnd, 0, wGui.NIF_INFO,
												wCon.WM_USER + 20, self.hicon,
												"Balloon  tooltip", msg, 200, title))
		if timeout:
			t_sleep(timeout)
			wGui.DestroyWindow(self.hwnd)
			wGui.UnregisterClass(self.classAtom, self.hinst)

	def OnDestroy(self, hwnd, msg, wparam, lparam):
		nid = (self.hwnd, 0)
		wGui.Shell_NotifyIcon(wGui.NIM_DELETE, nid)
		wGui.PostQuitMessage(0) # Terminate the app