from threading import Thread, main_thread
from pystray import *
from time import sleep


class TrayIconBuilder(Thread):
	def __init__(self, title, icon, menu):
		Thread.__init__(self, daemon=True)
		if 'PIL.Image.Image' not in str(type(icon)):
			from PIL import Image
			try:
				icon = Image.open(icon)
			except Exception:
				raise ValueError("icon argument must be a valid image path or a PIL.Image.Image instance")
		if not isinstance(menu, (list, tuple)):
			raise ValueError("menu argument must be an array of arrays. Any non-array value will become a separator.")
		self.title, self.icon, self.menuItems = title, icon, []
		self.menu = Menu(*self.__createMenu(menu))

	def __createMenu(self, data, setvar=True):
		menuOut,subOut = [],[]
		for i in data:
			subData = []
			if isinstance(i, (list, tuple)):
				txt,act,opt,*n = *i,{}
				if isinstance(act, (list, tuple)):
					act,subData = Menu(*(m:=self.__createMenu(act,False))[0]), m[1]
				mItem = MenuItem(txt, act, **opt)
				if setvar:
					self.menuItems.append([mItem, subData])
				else:
					subOut.append([mItem, subData])
			else:
				mItem = Menu.SEPARATOR
			menuOut.append(mItem)
		return menuOut if setvar else [menuOut, subOut]

	def getMenuItem(self, *pointer):
		obj = self.menuItems[pointer.pop(0)]
		try:
			while pointer:
				obj = obj[1][pointer.pop(0)]
			return obj[0]
		except IndexError:
			return None

	def run(self):
		self.__tIcon = Icon(self.title, self.icon, self.title, self.menu)
		self.__tIcon.run()

	def show(self, show=True):
		self.__tIcon.visible = show

	def stop(self):
		self.show(False)
		self.__tIcon.stop()


class example:
	def __init__(self):
		from PIL import Image, ImageDraw
		from tkinter import Tk, Label
		# create a window
		self.root = Tk()
		self.root.protocol("WM_DELETE_WINDOW", self.onClose)
		Label(text='Hello').pack()

		# create trayicon image
		# tIcon_img = Image.new('RGB', (32, 32), 'white')
		# tIcon_img_draw = ImageDraw.Draw(tIcon_img)
		# tIcon_img_draw.rectangle((16, 0, 32, 16), fill='black')
		# tIcon_img_draw.rectangle((0, 16, 16, 32), fill='black')
		tIcon_img = "C:\\Users\\Cryden\\AppData\\Roaming\\Spotify\\SpotifyPlayer_icon.png"

		# create trayicon menu
		self.chk_state = False
		tIcon_submenu_submenu = [("Happy", lambda:print("Yay!")),
							  ("Sad", lambda:print("Aw..."))]
		tIcon_submenu = [("Hi", lambda:print("Hello")),
						  ("Bye", lambda:print("Goodbye")),
						  ("Emotions", tIcon_submenu_submenu)]
		tIcon_topmenu = [("Speak", tIcon_submenu),
					  'Separator',
					  ("Checkable", self.on_check, {'checked': lambda i: self.chk_state}),
					  ("Minimize", self.root.iconify, {'default':True}),
					  'Separator',
					  ("Close", self.onClose)]
	
		# create trayicon and show it
		self.tIcon = TrayIconBuilder('Test Icon', tIcon_img, tIcon_topmenu)
		self.tIcon.start()
		self.root.mainloop()

	def onClose(self):
		self.tIcon.stop()
		self.root.destroy()
	
	def on_check(self, icon, item):
		self.chk_state = not item.checked


