"""A collection of functions which take a color, alter it, and return the resulting color"""

from .constants import FORMATS
from .worker import lighten, darken, saturate, desaturate, invert

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Callable as C, Union as U


class _main:
    from argparse import ArgumentParser as ArgParser, RawTextHelpFormatter as TxtFormat
    from traceback import format_exc
    from os import path, system
    pKwargs = dict(add_help=False,
                   formatter_class=TxtFormat)
    hArgs = ['-h', '--help']
    hKwargs = dict(help="show this help message",
                   action='store_true')
    wArgs = ['-w', '--window']
    wKwargs = dict(help="redirect help and errors to a new window",
                   action='store_true')
    subPars: "dict[C, dict[str, U[str, ArgParser]]]" = dict()

    def __init__(self):
        def argHelp(full: bool = True) -> str:
            insert = ('percent: int = 25\n'
                      '    Percent by which to change the color. Number between 1 and 100,\n'
                      '    where 100 would change black to white or vice versa\n')
            info = ('color: str | list[int, int, int] | tuple[int, int, int]\n'
                    '    The initial color. If <inputtype> is "HEX", must be a string.\n'
                    '    Otherwise, must be a list or tuple of 3 integers\n'
                    f'{insert if full else ""}'
                    'inputtype: str = ""\n'
                    f'    The data type of the input. One of {FORMATS}.\n'
                    '    If not specified, it will be assumed to be "HEX" if <color> is\n'
                    '    a string, else "RGB8"\n'
                    'returnas: str = "HEX"\n'
                    f'    The data type to return. One of {FORMATS}\n')
            return info

        self.buildParser()
        funcInfo = {'lighten': [lighten, argHelp()],
                    'darken': [darken, argHelp()],
                    'saturate': [saturate, argHelp()],
                    'desaturate': [desaturate, argHelp()],
                    'invert': [invert, argHelp(False)]}
        for name, info in funcInfo.items():
            self.createHelp(name, *info)
        self.getArgs()

    def buildParser(self) -> None:
        progName = self.path.basename(self.path.dirname(__file__))
        self.parser = self.ArgParser(prog=progName,
                                     description=__doc__,
                                     **self.pKwargs)
        self.parser.add_argument(*self.hArgs, **self.hKwargs)
        self.parser.add_argument(*self.wArgs, **self.wKwargs)
        self.subparse = self.parser.add_subparsers(
            help="sub-command help")

    def createHelp(self, name: str, fn: "C", helpStr: str) -> None:
        subpar = self.subparse.add_parser(name=name,
                                          description=fn.__doc__,
                                          help=fn.__doc__,
                                          **self.pKwargs)
        subpar.add_argument(*self.hArgs, **self.hKwargs)
        subpar.add_argument(*self.wArgs, **self.wKwargs)
        subpar.add_argument('-a', '--args',
                            help=helpStr,
                            nargs='+')
        subpar.set_defaults(func=fn)
        self.subPars[fn] = dict(n=name, s=subpar)

    def getArgs(self) -> None:
        all_args = self.parser.parse_args()
        kw = dict(win=all_args.window)
        try:
            kw['fname'] = self.subPars[all_args.func]['n']
            if all_args.help:
                kw.update(dict(msgType="help",
                               msg=self.subPars[all_args.func]['s'].format_help()))
            else:
                try:
                    kw.update(dict(msgType="output",
                                   msg=all_args.func(*all_args.args)))
                except Exception:
                    kw.update(dict(msgType="error",
                                   msg=self.format_exc()))
        except Exception:
            kw.update(dict(fname="main",
                           msgType="help",
                           msg=self.parser.format_help()))
        self.show_info(**kw)
        raise SystemExit

    def show_info(self, win: bool, fname: str, msgType: str, msg: str) -> None:
        runinfo = f"{fname} {msgType}:"
        if win:
            output = (f">>> {runinfo}`n"
                      f"{msg}`n`n"
                      "Press <return> to close:")
            cmd = f'read-host \\"{output}\\"'.replace("\n", "`n")
            self.system(f'start "" powershell -command "{cmd}"')
        else:
            print(msg)


if __name__ == "__main__":
    _main()
