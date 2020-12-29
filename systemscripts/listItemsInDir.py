"""Create a list of files and/or folders in a specified directory."""

from os import path as os_path, listdir as os_listdir
from textwrap import dedent


class main:
    """\
    mainDir (type:string)
        The path to the directory that is to be searched.
    outType (type:string)
        One of 'return', 'copy', or 'write'. 'return' simply returns the results.
        'copy' copies the results to the clipboard. 'write' writes the results to
        a file. If 'write', the following argument must be a path to a file.
    fileTypes (type:string OR list)
        One of 'folder', 'file', 'both', or a list of extensions to check."""

    def __init__(self, mainDir, outType, *args):
        if outType not in ['return', 'copy', 'write']:
            raise ValueError(dedent("""invalid value for argument in listFilesInDir: outType
                                    must be one of 'return', 'copy', or 'write'"""))
        if outType.lower() == 'write':
            outFile, *fileTypes = args
        else:
            outFile, *fileTypes = (None, *args) if args else (None, 'both')
        self.fileList = {os_path.join(mainDir, f) for f in os_listdir(mainDir)
                         if self.checkType(fileTypes, os_path.join(mainDir, f))}
        if outType.lower() == 'write':
            self.doWrite(outFile)
        elif outType == 'copy':
            from pyperclip import copy
            copy(str(self.fileList))
        else:
            print(self.fileList)

    def checkType(self, types, file):
        if len(types) == 1:
            t = types[0]
            return (os_path.exists(file) if 'both' in t else
                    os_path.isdir(file) if 'fol' in t else
                    os_path.isfile(file) if t in [os_path.splitext(file)[1][1:], 'file'] else
                    False)
        else:
            return (True if os_path.isfile(file) and
                    os_path.splitext(file)[1][1:] in types else False)

    def doWrite(self, outFile):
        if os_path.splitext(outFile)[1] == '.json':
            from json import dump as jsondump
            with open(outFile, 'w') as f:
                jsondump(self.fileList, f)
        else:
            with open(outFile, 'w') as f:
                f.write("\n".join(self.fileList))
