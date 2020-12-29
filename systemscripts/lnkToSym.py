"""Convert a regular '.lnk' file or folder to a SymLink."""


from win32com.client import Dispatch
from os import path, symlink, remove


def main(lnkPath):
    """\
    lnkPath (type:string)
        The path to an existing .lnk file"""
    target = Dispatch("WScript.Shell").CreateShortcut(lnkPath).Targetpath
    symlink(target, path.splitext(lnkPath)[0])
    remove(lnkPath)
