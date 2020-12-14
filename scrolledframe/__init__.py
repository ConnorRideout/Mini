"""This ScrolledFrame Widget behaves like a Frame widget but also
has vertical and/or horizontal scroll bars. The bars can be on
either edge of the widget, and can be set to disappear
automatically when not needed.

The Class consists of an outer Frame (data member: container),
a Canvas (data member: scrollCanvas), up to two Scrollbars (data
member: vScrbar/hScrbar), and an inner Frame (class).
The outer Frame contains the Canvas and Scrollbar widgets. The
Canvas creates a window from the inner Frame widget.
Configuration options are passed to the inner Frame widget,
along with most method calls; however, geometry methods are
redirected to the outer Frame widget.

The Class also has a special function 'redraw' which will update
the Widget's scroll area and hide/unhide the scrollbars (if set).

The constructor accepts all Frame widget keyword arguments, plus
the following:
-scrollbars (type:string; default='SE')
   Where to put the scrollbars (e/g 'SR'=South and Right)
   String must be with 1 or 2 characters
-dohide (type:boolean; default=True)
   Whether to hide the scrollbars when not needed
-padding (type:list of integers; default=[3,3,0,0])
   Padding between the outer Frame/Scrollbars and the
   inner Frame. [left,top,right,bottom]
-doupdate (type:boolean; default=True)
   Whether to automatically redraw the Widget whenever it
   changes size. Setting to False may improve performance'
"""

from tkinter import Frame as _Frame, Canvas as _Canvas, Scrollbar as _Scrollbar, Grid as _Grid, Pack as _Pack, Place as _Place
from re import match as _re_match

class ScrolledFrame(_Frame):
	def __init__(self, master=None, scrollbars='SE', dohide=True,
				 padding=[3,3,0,0], doupdate=True, **kwargs):
		self.__validateVars(padding, scrollbars)
		# set var defaults if not specified
		kwargs.update({'bd': kwargs.pop('bd', kwargs.pop('borderwidth', 2)),
					   'relief': kwargs.pop('relief', 'ridge'),
					   'width': kwargs.pop('width', 300),
					   'height': kwargs.pop('height', 200)})
		self.__BG = kwargs.get('bg', kwargs.get('background', 'SystemButtonFace'))
		self.__CURSOR = kwargs.get('cursor', '')
		self.hScrbar = self.vScrbar = self.__showVScroll = self.__showHScroll = False
		self.__hideBars, self.__allChildren = dohide, {}

		# create widget
		self.__sfc = 'scrollframe_children'
		self.__createContainer(master, kwargs)
		self.__createScrollFrame(*padding)
		self.__retag()
		if doupdate:
			self.bind_class(self.__sfc, '<Configure>', self.redraw)

		# Pass geometry methods to container
		frame_methods = vars(_Frame).keys()
		all_geo_methods = vars(_Pack).keys() | vars(_Grid).keys() | vars(_Place).keys()
		geo_methods = all_geo_methods.difference(frame_methods)
		for method in geo_methods:
			if method[0] != '_' and 'config' not in method:
				setattr(self, method, getattr(self.container, method))

	def configure(self, **kwargs):
		bg, cur = kwargs.get('bg', kwargs.get('background')), kwargs.get('cursor')
		self.__BG = bg if bg else self.__BG
		self.__CURSOR = cur if cur else self.__CURSOR
		if bg or cur:
			self.container.config(bg=self.__BG, cursor=self.__CURSOR)
			self.scrollCanvas.config(bg=self.__BG, cursor=self.__CURSOR)
		_Frame.configure(self, **kwargs)

	config = configure

	def __validateVars(self, pad, sbars):
		if len([n for n in pad if isinstance(n, int)]) != 4:
			raise ValueError("<padding> argument must be a list of four integers: [pad_left, pad_top, pad_right, pad_bottom]")
		if _re_match(r'(?:([NTSB])|[ERWL])(?:$|(?:(?(1)[ERWL]|[NTSB])$))', s:=sbars.upper()):
			self.__sbX = 'N' if {'N','T'} & set(s) else 'S' if {'S','B'} & set(s) else None
			self.__sbY = 'E' if {'E','R'} & set(s) else 'W' if {'W','L'} & set(s) else None
		else:
			raise ValueError("<scrollbars> argument must be 1 or 2 letters: 'N/T|S/B' and/or 'E/R|W/L")

	def __createContainer(self, master, kwargs):
		self.container = _Frame(master, **kwargs)
		self.container.grid_propagate(0)
		self.container.rowconfigure((1 if self.__sbX == 'N' else 0), weight=1)
		self.container.columnconfigure((1 if self.__sbY == 'W' else 0), weight=1)

	def __createScrollFrame(self, pL, pT, pR, pB):
		self.scrollCanvas = _Canvas(self.container, highlightthickness=0, bg=self.__BG, cursor=self.__CURSOR)
		self.scrollCanvas.grid(row=(1 if self.__sbX == 'N' else 0),
							   column=(1 if self.__sbY == 'W' else 0),
							   sticky='nsew', padx=(pL, pR), pady=(pT, pB))
		_Frame.__init__(self, self.scrollCanvas, bg=self.__BG, cursor=self.__CURSOR)
		# create scroll bars
		if self.__sbY:
			self.vScrbar = _Scrollbar(self.container, orient='vertical', command=self.scrollCanvas.yview)
			self.vScrbar.grid(row=(1 if self.__sbX == 'N' else 0), column=(0 if self.__sbY == 'W' else 1), sticky='ns')
			self.scrollCanvas.config(yscrollcommand=self.vScrbar.set)
			self.__showVScroll = True
		if self.__sbX:
			self.hScrbar = _Scrollbar(self.container, orient='horizontal', command=self.scrollCanvas.xview)
			self.hScrbar.grid(row=(0 if self.__sbX == 'N' else 1), column=(1 if self.__sbY == 'W' else 0), sticky='ew')
			self.scrollCanvas.config(xscrollcommand=self.hScrbar.set)
			self.__showHScroll = True
		self.__rebindTags(['v','h'])
		self.__mainWin = self.scrollCanvas.create_window(0, 0, anchor='nw', window=self)

	def __rebindTags(self, sbars):
		if self.vScrbar and 'v' in sbars:
			if self.__showVScroll:
				self.vScrbar.grid()
				self.bind_class(self.__sfc, '<MouseWheel>', lambda e: self.scrollCanvas.yview_scroll((-2 if e.delta > 0 else 2), 'units'))
			else:
				if self.__showHScroll and 'h' not in sbars:
					self.bind_class(self.__sfc, '<MouseWheel>', lambda e: self.scrollCanvas.xview_scroll((-2 if e.delta > 0 else 2), 'units'))
				if self.__hideBars:
					self.vScrbar.grid_remove()
		if self.hScrbar and 'h' in sbars:
			if self.__showHScroll:
				self.hScrbar.grid()
				if not self.__showVScroll:
					self.bind_class(self.__sfc, '<MouseWheel>', lambda e: self.scrollCanvas.xview_scroll((-2 if e.delta > 0 else 2), 'units'))
			elif self.__hideBars:
				self.hScrbar.grid_remove()
		if not self.__showVScroll and not self.__showHScroll:
			self.unbind_class(self.__sfc, '<MouseWheel>')

	def __retag(self):
		c = [self.container]
		[c.extend(w.winfo_children()) for w in c]
		curChildren = set(c)
		if (newWidgets := curChildren.difference(self.__allChildren)):
			[w.bindtags((self.__sfc,) + w.bindtags()) for w in newWidgets]
		self.__allChildren = curChildren

	def redraw(self, event=None):
		self.__retag()
		rebind = []
		if self.vScrbar:
			if (tall := self.winfo_reqheight() <= self.scrollCanvas.winfo_height()) and self.__showVScroll:
				rebind.append('v')
				self.__showVScroll = False
			elif not tall and not self.__showVScroll:
				rebind.append('v')
				self.__showVScroll = True
		if self.hScrbar:
			if (wide := self.winfo_reqwidth() <= self.scrollCanvas.winfo_width()) and self.__showHScroll:
				rebind.append('h')
				self.__showHScroll = False
			elif not wide and not self.__showHScroll:
				rebind.append('h')
				self.__showHScroll = True
		if rebind:
			self.__rebindTags(rebind)
		self.scrollCanvas.config(scrollregion=(0, 0, self.winfo_reqwidth(), self.winfo_reqheight()))
		self.scrollCanvas.itemconfig(self.__mainWin, width=max(self.scrollCanvas.winfo_width(), self.winfo_reqwidth()),
													 height=max(self.scrollCanvas.winfo_height(), self.winfo_reqheight()))
