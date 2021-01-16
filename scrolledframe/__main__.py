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
the following immutable arguments:
-scrollbars (type:string; default='SE')
   Where to put the scrollbars (e/g 'SR'=South and Right)
   String must be 1 or 2 characters (NSEW and/or TBRL)
-padding (type:integer or list of integers; default=[3,3,0,0])
   Padding between the outer Frame/Scrollbars and the
   inner Frame. <all> or [EW, NS] or [left,top,right,bottom]
-dohide (type:boolean; default=True)
   Whether to hide the scrollbars when not needed
-doupdate (type:boolean; default=True)
   Whether to automatically redraw the Widget whenever it
   changes size. Setting to False may improve performance
-scrollspeed (type:integer; default=2)
   The number of lines to scroll by per mousewheel scroll.
   Setting to 0 disables mousewheel scrolling
"""


def example():
    try:
        from . import ScrolledFrame
    except ImportError:
        from __init__ import ScrolledFrame
    from tkinter import Label, Button

    sframe = ScrolledFrame()
    lbl = Label(sframe, text='Start', font='Calibri 12', justify='left')
    lbl.grid()
    curCol = 1
    curRow = 1
    rLbl = Label(sframe, text='HorzLabel1', font='Calibri 12')
    rLbl.grid(row=0, column=curCol)
    bLbl = Label(sframe, text='VertLabel1', font='Calibri 12')
    bLbl.grid(row=curRow, column=0)

    def b1cmd():
        lbl.config(text=__doc__)

    def b2cmd():
        nonlocal curCol
        curCol += 1
        txt = 'HorzLabel{}'.format(curCol)
        rLbl = Label(sframe, text=txt, font='Calibri 12')
        rLbl.grid(row=0, column=curCol)
        sframe.redraw()

    def b3cmd():
        nonlocal curRow
        curRow += 1
        txt = 'VertLabel{}'.format(curRow)
        bLbl = Label(sframe, text=txt, font='Calibri 12')
        bLbl.grid(row=curRow, column=0)
        sframe.redraw()

    b1 = Button(text='View readme', command=b1cmd)
    b1.pack(side='top')
    b2 = Button(text='Add Label Right', command=b2cmd)
    b2.pack(side='right')
    b3 = Button(text='Add Label Bottom', command=b3cmd)
    b3.pack(side='bottom')

    sframe.pack(expand=True, fill='both', side='top')
    sframe.update_idletasks()
    sframe.mainloop()


if __name__ == "__main__":
    example()
