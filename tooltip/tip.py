from tkinter import Toplevel, Label, Widget


class CreateTooltip(Toplevel):
    """A Tooltip widget for tkinter"""
    _wgt: Widget
    _side: str
    _lbl: Label
    _tw: int
    _th: int

    def __init__(self, widget: Widget, text: str, side: str = 'n', **kwargs):
        """\
        Parameters
        ----------
        widget : Widget
            The parent widget
        text : str
            The tooltip text
        side : str, optional (default is "n")
            Which side of the parent widget to show the tooltip on
        **kwargs : dict, optional (default is justify="left", padx=1, pady=1)
            tkLabel Keyword Arguments for the tooltip
        """
        # verify value
        if side and side.lower() not in list('nsew'):
            raise ValueError('<side> parameter must be '
                             'one of "n", "s", "e", or "w"')
        # init vars
        self._wgt = widget
        self._side = side.lower()
        kwargs.update(justify=kwargs.pop('justify', 'left'),
                      padx=kwargs.pop('padx', 1),
                      pady=kwargs.pop('pady', 1))
        # create win
        Toplevel.__init__(self,
                          master=widget)
        self.attributes("-alpha", 0.75)
        self.overrideredirect(True)
        # create lbl
        self._lbl = Label(master=self,
                          text=text,
                          **kwargs)
        self._lbl.pack()
        self.update_idletasks()
        self._tw = self.winfo_reqwidth()
        self._th = self.winfo_reqheight()
        self.withdraw()
        widget.bind("<Enter>", self.enter)
        widget.bind("<Leave>", self.close)

    def configure(self, **kwargs):
        bg = kwargs.get('background', kwargs.get('bg'))
        if bg:
            Toplevel.configure(self, bg=bg)
        self._lbl.config(**kwargs)

    config = configure

    def enter(self, _) -> None:
        # get widget location
        wx = self._wgt.winfo_rootx()
        wy = self._wgt.winfo_rooty()
        ww = self._wgt.winfo_width()
        wh = self._wgt.winfo_height()
        # get screen width
        sw = self._wgt.winfo_screenwidth()
        # set tooltip location
        x = ((wx + ww) if self._side == 'e'
             else (wx - self._tw) if self._side == 'w'
             else max(0, min(wx, (sw - self._tw))))
        y = ((wy - self._th) if self._side == 'n'
             else (wy + wh) if self._side == 's'
             else (wy + (wh // 2) - (self._th // 2)))
        self.geometry(f"+{x}+{y}")
        self.deiconify()

    def close(self, _) -> None:
        self.withdraw()
