def example():
    from . import ScrolledFrame
    from tkinter import Label, Button

    sframe = ScrolledFrame()
    (lbl := Label(sframe, text='Start', font='Calibri 12', justify='left')).grid()
    (rLbl := Label(sframe, text='HorzLabel0', font='Calibri 12')).grid(row=0, column=1)
    (bLbl := Label(sframe, text='VertLabel0', font='Calibri 12')).grid(row=1, column=0)

    Button(text='Fill With Text', command=lambda: lbl.config(text=__doc__)).pack(side='top')
    Button(text='Add Label Right', command=lambda: rLbl.config(text='{} HorzLabel{}'.format(t:=rLbl.cget('text'), int(t[-1])+1))).pack(side='right')
    Button(text='Add Label Bottom', command=lambda: bLbl.config(text='{}\nVertLabel{}'.format(t:=bLbl.cget('text'), int(t[-1])+1))).pack(side='bottom')

    sframe.pack(expand=True, fill='both', side='top')
    sframe.mainloop()

if __name__ == "__main__":
    example()