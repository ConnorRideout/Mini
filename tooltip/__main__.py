from tkinter import Tk, Label


def main():
    try:
        from . import CreateTooltip as tt
    except ImportError:
        from pathlib import Path
        from subprocess import run
        pth = Path(__file__).parent
        run(['py', '-m', pth.name], cwd=pth.parent)
        raise SystemExit

    root = Tk()
    root.geometry('300x300')
    lbl = Label(text='Hover for tooltip',
                fg='black',
                bg='gray')
    lbl.place(anchor='center',
              relx=0.5,
              rely=0.5)

    tt(lbl, 'This is a tooltip', bg='lightyellow', fg='black')

    root.mainloop()


if __name__ == "__main__":
    main()
