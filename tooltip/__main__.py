
def main():
	from . import CreateToolTip as tt
	from tkinter import Tk, Label

	root = Tk()
	root.geometry('300x300')
	lbl = Label(text='Hover for tooltip')
	lbl.place(anchor='center', relx=0.5, rely=0.5)
	
	tt(lbl, 'This is a tooltip', 'n')

	root.mainloop()



if __name__ == "__main__":
	main()