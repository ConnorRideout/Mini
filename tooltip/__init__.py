from tkinter import Toplevel, Label

class CreateToolTip(object):
	def __init__(self, widget, text, side='s', bg='lightyellow'):
		# verify value
		if side.lower() not in ['s', 'n']:
			raise ValueError
		# create win
		self.widget = widget
		self.side = side.lower()
		self.tw = Toplevel(widget)
		self.tw.wm_attributes("-alpha", 0.7)
		self.tw.wm_overrideredirect(True)
		Label(self.tw, text=text, justify='left', bg=bg).pack(ipadx=1)
		self.tw.withdraw()
		widget.bind("<Enter>", self.enter)
		widget.bind("<Leave>", self.close)
	def enter(self, event=None):
		x = self.widget.winfo_rootx()
		y = self.widget.winfo_rooty() - self.tw.winfo_height() if self.side == 'n' else self.widget.winfo_rooty() + self.widget.winfo_height()
		self.tw.wm_geometry("+{}+{}".format(x, y))
		self.tw.deiconify()
	def close(self, event=None):
		self.tw.withdraw()