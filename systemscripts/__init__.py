"""Scripts for use with command line"""


def _show_info(script, output, win, msgType='error'):
	if win:
		os_sys("""start "" powershell -command "write-host \\"{}\\""; pause""".format(output.replace('\n', '`n')))
	else:
		print(output)

class createSym:
	"""\
	Create a SymLink in the current directory."""
	def argInfo(self):
		"""\
		initDir (type:string)
			The path where the SymLink should be placed"""
	from tkinter import Tk, filedialog
	from tkinter.ttk import Label, Button
	from os import symlink
	
	def __init__(self, initDir):
		self.root = self.Tk()
		wd, ht = 400, 100
		self.root.title("Create Symbolic Link")
		self.root.attributes('-topmost', 1)
		self.root.geometry('{}x{}+{:n}+{:n}'.format(wd, ht,
													self.root.winfo_screenwidth()/2-wd/2,
													self.root.winfo_screenheight()/2-ht/2))
		self.root.bind_all('<Escape>', lambda e: self.root.destroy())
		self.initDir = initDir

		self.Label(text="Would you like to make a Symlink for a folder or a file?",
				   font='Calibri 12').place(anchor='center', relx=0.5, rely=0.3)
		(btn:=self.Button(text="Folder", underline=0, command=lambda: self.createLink('folder'),
						  width=10)).place(anchor='center', relx=0.25, rely=0.66)
		btn.focus_set()
		btn.bind('<Return>', lambda e: btn.invoke())
		self.Button(text=" File ", command=lambda: self.createLink('file'),
					width=10).place(anchor='center', relx=0.5, rely=0.66)
		self.Button(text="Cancel", command=self.root.destroy,
					width=10).place(anchor='center', relx=0.75, rely=0.66)
		self.root.mainloop()

	def createLink(self, opt):
		try:
			if opt=='folder' and (target:=self.filedialog.askdirectory(initialdir=self.initDir,
													title='Select a folder to create a link to:')):
				name = os_path.join(self.initDir, os_path.basename(target))
			elif opt=='file' and (target:=self.filedialog.askopenfilename(initialdir=self.initDir,
													title='Select a file to create a link to:')):
				name = os_path.join(self.initDir, os_path.basename(target))
			else:
				return
			self.symlink(target, name)
			self.root.destroy()
		except Exception:
			self.root.destroy()
			_show_info('createSym', format_exc(), all_args.window)

class lnkToSym:
	"""\
	Convert a regular '.lnk' file or folder to a SymLink."""
	def argInfo(self):
		"""\
		lnkPath (type:string)
			The path to an existing .lnk file"""
	def __init__(self, lnkPath):
		from win32com.client import Dispatch
		from os import path, symlink, remove
		target = Dispatch("WScript.Shell").CreateShortcut(lnkPath).Targetpath
		symlink(target, path.splitext(lnkPath)[0])
		remove(lnkPath)

class createBorder:
	"""\
	Create a topmost window that acts as a border around the currently
	active window."""
	def argInfo(self):
		"""\
		args (type:list of 4 ints; optional)
			if provided, must be x position, y position, width, height of current window"""
	def __init__(self, *args):
		from tkinter import Tk, Frame
		from win32gui import GetForegroundWindow as GetForeWin, SetWindowLong
		from ahk import AHK

		x, y, w, h = args if len(args) == 4 else AHK().active_window.rect
		topWin, root = GetForeWin(), Tk()
		root.overrideredirect(True)
		root.title("-*Filter*-")
		root.config(bg='red')
		root.attributes('-transparentcolor', 'black', '-topmost', True, '-alpha', 0.5)
		root.geometry('{}x{}+{}+{}'.format(w, h, x, y))
		Frame(root, bg='black').place(anchor='center', relx=0.5, rely=0.5, width=-6, relwidth=1,
									  height=-6, relheight=1)
		root.update_idletasks()
		SetWindowLong(GetForeWin(), -8, topWin)
		root.mainloop()

class listItemsInDir:
	"""\
	Create a list of files and/or folders in a specified directory."""
	def argInfo(self):
		"""\
		mainDir (type:string)
			The path to the directory that is to be searched.
		outType (type:string)
			One of 'return', 'copy', or 'write'. 'return' simply returns the results.
			'copy' copies the results to the clipboard. 'write' writes the results to
			a file. If 'write', the following argument must be a path to a file.
		fileTypes (type:string OR list)
			One of 'folder', 'file', 'both', or a list of extensions to check."""
	from os import path, listdir
	def __init__(self, mainDir, outType, *args):
		if outType not in ['return','copy','write']:
			raise ValueError(dedent("""invalid value for argument in listFilesInDir: outType
									must be one of 'return', 'copy', or 'write'"""))
		if outType.lower() == 'write':
			outFile,*fileTypes = args
		else:
			outFile,*fileTypes = (None,*args) if args else (None,'both')
		self.fileList = {self.path.join(mainDir, f) for f in self.listdir(mainDir)
										if self.checkType(fileTypes, self.path.join(mainDir, f))}
		if outType.lower() == 'write':
			self.doWrite(outFile)
		elif outType == 'copy':
			from pyperclip import copy
			copy(str(self.fileList))
		else:
			return self.fileList

	def checkType(self, types, file):
		if len(types) == 1:
			t = types[0]
			return (self.path.exists(file) if 'both' in t else
					self.path.isdir(file) if 'fol' in t else
					self.path.isfile(file) if t in [self.path.splitext(file)[1][1:], 'file'] else
					False)
		else:
			return (True if self.path.isfile(file) and
					self.path.splitext(file)[1][1:] in types else False)

	def doWrite(self, outFile):
		if self.path.splitext(outFile)[1] == '.json':
			from json import dump as jsondump
			with open(outFile, 'w') as f:
				jsondump(self.fileList, f)
		else:
			with open(outFile, 'w') as f:
				f.write("\n".join(self.fileList))

class alterImages:
	"""\
	Resize all files in a directory to 2k and convert them to jpg."""
	def argInfo(self):
		"""\
		runFile (type:string)
			The path to the file that's running this script"""
	def __init__(self, runFile):
		from os import chdir, listdir
		chdir(os_path.dirname(runFile))
		files = ' '.join(['"{}"'.format(f) for f in listdir() if os_path.isfile(f) and
						 f != os_path.basename(runFile) and os_path.splitext(f)[1] != '.lnk'])
		args = [files, 't', '.jpg'] if os_sys(
			'nircmd qboxcomtop "Reformat files to jpg?" "Reformat" returnval 1') else [files, 'f', '']
		os_sys('magick convert {} -resize 2560x1440 -set filename:f "%{}" +adjoin "(2k) %[filename:f]{}"'
			   .format(*args))


class _main:
	def __init__(self, locs):
		self.parser = argparse.ArgumentParser(prog=os_path.basename(os_path.dirname(__file__)), description=__doc__, add_help=False,
											  formatter_class=argparse.RawTextHelpFormatter)
		self.parser.add_argument('-h', '--help', help="show this help message", action='store_true')
		self.parser.add_argument('-w', '--window', help="show help and errors in a window",
																				action='store_true')
		self.subpar, self.subs = self.parser.add_subparsers(help="sub-command help"), {}
		[self.createHelp(n,f) for n,f in locs.items()]
		self.getArgs()

	def createHelp(self, name, func):
		formatHelp = lambda t: dedent(t).replace('\t', '    ')
		s = self.subpar.add_parser(name, description=formatHelp(func.__doc__),
								   help=formatHelp(func.__doc__), add_help=False,
								   formatter_class=argparse.RawTextHelpFormatter)
		s.add_argument('-h', '--help', help="show this help message", action='store_true')
		s.add_argument('-w', '--window', help="show help and errors in a window",
																				action='store_true')
		s.add_argument('-a', '--args', help=formatHelp(func.argInfo.__doc__), nargs='+')
		s.set_defaults(func=func)
		self.subs.update({name: s})

	def getArgs(self):
		global all_args
		self.sIO = StringIO()
		with redirect_stdout(self.sIO):
			all_args = self.parser.parse_args()
			if all_args.help:
				try:
					self.subs[all_args.func.__name__].print_help()
				except AttributeError:
					self.parser.print_help()
		if (out:=self.sIO.getvalue()):
			try: f = all_args.func
			except AttributeError: f = None
			_show_info(f.__name__ if f else "Main", out, all_args.window, 'help')
			raise SystemExit
		else:
			try:
				all_args.func(*all_args.args)
			except Exception:
				_show_info(f.__name__ if (f:=all_args.func) else "Main",
							format_exc(), all_args.window)

locs = {na:fn for na,fn in locals().items() if na[0] != '_' and hasattr(fn, '__call__')}
from contextlib import redirect_stdout
from traceback import format_exc
from os import system as os_sys, path as os_path
from threading import Thread
from io import StringIO
from re import escape
from time import sleep
from textwrap import *
import argparse

def _run():
	_main(locs)
