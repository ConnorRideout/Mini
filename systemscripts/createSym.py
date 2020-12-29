"""Create a SymLink in the current directory."""


from tkinter import Tk, filedialog as fdlg
from tkinter.ttk import Label, Button
from os import symlink, path as os_path
from traceback import format_exc


class main:
    """\
    initDir (type:string)
        The path where the SymLink should be placed"""

    def __init__(self, initDir):
        self.root = Tk()
        wd, ht = 400, 100
        self.root.title("Create Symbolic Link")
        self.root.attributes('-topmost', 1)
        x = self.root.winfo_screenwidth()/2-wd/2
        y = self.root.winfo_screenheight()/2-ht/2
        self.root.geometry('{}x{}+{:n}+{:n}'.format(wd, ht, x, y))
        self.root.bind_all('<Escape>', lambda e: self.root.destroy())
        self.initDir = initDir

        lbl1 = Label(
            text="Would you like to make a Symlink for a folder or a file?", font='Calibri 12')
        lbl1.place(anchor='center', relx=0.5, rely=0.3)
        folder_btn = Button(
            text="Folder", underline=0, command=lambda: self.createLink('folder'), width=10)
        folder_btn.place(anchor='center', relx=0.25, rely=0.66)
        folder_btn.focus_set()
        folder_btn.bind('<Return>', lambda e: folder_btn.invoke())
        file_btn = Button(
            text=" File ", command=lambda: self.createLink('file'), width=10)
        file_btn.place(anchor='center', relx=0.5, rely=0.66)
        cancel_btn = Button(
            text="Cancel", command=self.root.destroy, width=10)
        cancel_btn.place(anchor='center', relx=0.75, rely=0.66)
        self.root.mainloop()

    def createLink(self, opt):
        try:
            args = {'initialdir': self.initDir,
                    'title': 'Select a {} to create a link to:'.format(opt)}
            askitem = (lambda: fdlg.askdirectory(
                **args)) if opt == 'folder' else (lambda: fdlg.askopenfilename(**args))
            if opt in ['folder', 'file']:
                target = askitem()
                if target:
                    name = os_path.join(self.initDir, os_path.basename(target))
                else:
                    return
            else:
                return
            symlink(target, name)
            self.root.destroy()
        except Exception as ex:
            self.root.destroy()
            raise ex
