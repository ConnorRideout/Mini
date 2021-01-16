from tkinter import Frame as _Frame, Canvas as _Canvas, Scrollbar as _Scrollbar, Grid as _Grid, Pack as _Pack, Place as _Place
from re import match as _re_match, sub as _re_sub


class ScrolledFrame(_Frame):
    def __init__(self, master=None, scrollbars='SE', padding=[3, 3, 0, 0],
                 dohide=True, doupdate=True, scrollspeed=2, **kwargs):
        padding = self.__expandPad(padding)
        self.__validateVars(padding, scrollbars)
        # set var defaults if not specified
        kwargs.update({'bd': kwargs.pop('borderwidth', kwargs.pop('bd', 2)),
                       'relief': kwargs.pop('relief', 'ridge'),
                       'width': kwargs.pop('width', 300),
                       'height': kwargs.pop('height', 200)})
        self.__BG = kwargs.get('background',
                               kwargs.get('bg', 'SystemButtonFace'))
        self.__CURSOR = kwargs.get('cursor', '')
        # set initial values
        self.__hideBars = dohide
        self.__scrollSpeed = scrollspeed
        self.hScrbar = False
        self.vScrbar = False
        self.__showVScroll = False
        self.__showHScroll = False
        self.__allChildren = dict()

        # create widget
        self.__createContainer(master, kwargs)
        self.__sfc = '{}_children'.format(self.container.winfo_id())
        self.__createScrollFrame(*padding)
        self.__retag()
        if doupdate:
            self.bind_class(self.__sfc, '<Configure>', self.redraw)

        # Pass geometry methods to container
        frame_methods = vars(_Frame).keys()
        all_geo_methods = vars(_Pack).keys() | vars(
            _Grid).keys() | vars(_Place).keys()
        geo_methods = all_geo_methods.difference(frame_methods)
        for method in geo_methods:
            if method[0] != '_' and 'config' not in method:
                setattr(self, method, getattr(self.container, method))

    def __expandPad(self, pad):
        # format the padding
        if isinstance(pad, (list, tuple)):
            l = len(pad)
            return pad if l == 4 else pad*2 if l == 2 else 'fail'
        else:
            return [pad]*4 if isinstance(pad, int) else 'fail'

    def __validateVars(self, pad, sbars):
        # check padding var
        if len([n for n in pad if isinstance(n, int)]) != 4:
            raise AttributeError(
                "<padding> argument must be a single integer (pad_edges) or a list of either 2 (pad_EW, pad_NS) or 4 ints (pad_left, pad_top, pad_right, pad_bottom)")
        # check scrollbars var
        repl = {'TBRL'[i]: 'NSEW'[i] for i in range(4)}
        s = _re_sub(r'T|B|R|L', lambda m: repl[m.group(0)], sbars.upper())
        if _re_match(r'[NS]($|[EW]$)|[EW]($|[NS]$)', s):
            self.__sbX = ''.join(set('NS') & set(s))
            self.__sbY = ''.join(set('EW') & set(s))
        else:
            raise AttributeError(
                "<scrollbars> argument must be 1 or 2 letters: 'N/T|S/B' and/or 'E/R|W/L")

    def __createContainer(self, master, kwargs):
        # create the container that holds everything
        self.container = _Frame(master, **kwargs)
        self.container.grid_propagate(0)
        self.container.rowconfigure(1 if self.__sbX == 'N' else 0,
                                    weight=1)
        self.container.columnconfigure(1 if self.__sbY == 'W' else 0,
                                       weight=1)

    def __createScrollFrame(self, pL, pT, pR, pB):
        # create the canvas that holds the scrolled window
        self.scrollCanvas = _Canvas(self.container,
                                    highlightthickness=0,
                                    bg=self.__BG,
                                    cursor=self.__CURSOR)
        self.scrollCanvas.grid(row=1 if self.__sbX == 'N' else 0,
                               column=1 if self.__sbY == 'W' else 0,
                               sticky='nsew',
                               padx=(pL, pR),
                               pady=(pT, pB))
        # create the scrolled window
        _Frame.__init__(self, self.scrollCanvas,
                        bg=self.__BG,
                        cursor=self.__CURSOR)
        # create scrollbars
        if self.__sbY:
            self.vScrbar = _Scrollbar(self.container,
                                      orient='vertical',
                                      command=self.scrollCanvas.yview)
            self.vScrbar.grid(row=1 if self.__sbX == 'N' else 0,
                              column=0 if self.__sbY == 'W' else 1,
                              sticky='ns')
            self.scrollCanvas.config(yscrollcommand=self.vScrbar.set)
            self.__showVScroll = True
        if self.__sbX:
            self.hScrbar = _Scrollbar(self.container,
                                      orient='horizontal',
                                      command=self.scrollCanvas.xview)
            self.hScrbar.grid(row=0 if self.__sbX == 'N' else 1,
                              column=1 if self.__sbY == 'W' else 0,
                              sticky='ew')
            self.scrollCanvas.config(xscrollcommand=self.hScrbar.set)
            self.__showHScroll = True
        # update vars then create the window
        self.__updateScrolling(['v', 'h'])
        self.__mainWin = self.scrollCanvas.create_window(0, 0,
                                                         anchor='nw',
                                                         window=self)

    def __bindScroll(self, func):
        def scrollView(e):
            val = -self.__scrollSpeed if e.delta > 0 else self.__scrollSpeed
            func(val, 'units')
        self.bind_class(self.__sfc, '<MouseWheel>', scrollView)

    def __updateScrolling(self, sbars):
        if self.vScrbar and 'v' in sbars:
            # there is a vert scrollbar and it needs to be updated
            if self.__showVScroll:
                # the vScroll is needed
                self.vScrbar.grid()
                if self.__scrollSpeed:
                    # bind the vScroll
                    self.__bindScroll(self.scrollCanvas.yview_scroll)
            else:
                # the vScroll isn't needed
                if self.__scrollSpeed and self.__showHScroll and 'h' not in sbars:
                    # there is a horz scrollbar and it won't be updated otherwise
                    self.__bindScroll(self.scrollCanvas.xview_scroll)
                if self.__hideBars:
                    # hide the vScroll
                    self.vScrbar.grid_remove()
        if self.hScrbar and 'h' in sbars:
            # there is a horz scrollbar and it needs to be updated
            if self.__showHScroll:
                # the hScroll is needed
                self.hScrbar.grid()
                if self.__scrollSpeed and not self.__showVScroll:
                    # there isn't a vert scrollbar, so bind the hScroll
                    self.__bindScroll(self.scrollCanvas.xview_scroll)
            elif self.__hideBars:
                # the hScroll isn't needed
                self.hScrbar.grid_remove()
        if self.__scrollSpeed and not self.__showVScroll and not self.__showHScroll:
            # neither scrollbar is needed
            self.unbind_class(self.__sfc, '<MouseWheel>')

    def __retag(self):
        # recurse through all children of widget and add the custom tag
        c = [self.container]
        [c.extend(w.winfo_children()) for w in c]
        curChildren = set(c)
        if (newWidgets := curChildren.difference(self.__allChildren)):
            [w.bindtags((self.__sfc,) + w.bindtags()) for w in newWidgets]
        self.__allChildren = curChildren

    def redraw(self, event=None):
        # update widget
        self.__retag()
        reqWd = self.winfo_reqwidth()
        scrCnvWd = self.scrollCanvas.winfo_width()
        reqHt = self.winfo_reqheight()
        scrCnvHt = self.scrollCanvas.winfo_height()
        rebind = list()
        # check if horz scroll exists and if so, if it's showing and shouldn't be or vice versa
        wide = reqWd <= scrCnvWd
        if self.hScrbar and ((wide and self.__showHScroll) or not (wide or self.__showHScroll)):
            self.__showHScroll = not self.__showHScroll
            rebind.append('h')
        # check if vert scroll exists and if so, if it's showing and shouldn't be or vice versa
        tall = reqHt <= scrCnvHt
        if self.vScrbar and ((tall and self.__showVScroll) or not (tall or self.__showVScroll)):
            self.__showVScroll = not self.__showVScroll
            rebind.append('v')
        # update the scrollbars if necessary
        if rebind:
            self.__updateScrolling(rebind)
        # update the window with the new sizes
        self.scrollCanvas.config(scrollregion=(0, 0, reqWd, reqHt))
        self.scrollCanvas.itemconfig(self.__mainWin,
                                     width=max(reqWd, scrCnvWd),
                                     height=max(reqHt, scrCnvHt))

    def configure(self, **kwargs):
        # intercept configure commands
        kw = dict()
        if (bg := kwargs.get('background', kwargs.get('bg'))):
            # get user requested background
            self.__BG = bg
            kw.update({'bg': self.__BG})
        if (cur := kwargs.get('cursor')):
            # get user requested cursor
            self.__CURSOR = cur
            kw.update({'cursor': self.__CURSOR})
        if kw:
            # update config for sub-widgets
            self.container.config(**kw)
            self.scrollCanvas.config(**kw)
        # update config for main widget
        _Frame.configure(self, **kwargs)

    config = configure
